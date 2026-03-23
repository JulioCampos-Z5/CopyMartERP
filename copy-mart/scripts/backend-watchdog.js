/**
 * Vite Plugin — Backend Watchdog
 *
 * Se activa automáticamente al correr `npm run frontend` o `npm run dev`.
 * Arranca FastAPI si no está corriendo y lo monitorea durante el desarrollo.
 * Reintenta un máximo de MAX_REINTENTOS veces ante caídas.
 */

import { spawn }        from 'node:child_process'
import http             from 'node:http'
import path             from 'node:path'
import fs               from 'node:fs'
import { fileURLToPath } from 'node:url'

const __dirname   = path.dirname(fileURLToPath(import.meta.url))
const APP_DIR     = path.resolve(__dirname, '../../app')
const VENV_PYTHON = path.resolve(__dirname, '../../venv/Scripts/python.exe')
const ENV_FILE    = path.resolve(__dirname, '../../.env')

// ── Leer .env ────────────────────────────────────────────────────────────────

function cargarEnv(archivo) {
  const env = {}
  if (!fs.existsSync(archivo)) return env
  fs.readFileSync(archivo, 'utf-8')
    .split('\n')
    .forEach((linea) => {
      const limpia = linea.trim()
      if (!limpia || limpia.startsWith('#')) return
      const idx = limpia.indexOf('=')
      if (idx === -1) return
      const clave = limpia.slice(0, idx).trim()
      const valor = limpia.slice(idx + 1).trim()
      env[clave] = valor
    })
  return env
}

const env = cargarEnv(ENV_FILE)

const BACKEND_PORT = env.BACKEND_PORT ?? '8000'

// El health-check siempre va a localhost (misma máquina que corre el watchdog)
const BACKEND_URL  = `http://localhost:${BACKEND_PORT}/`
const MAX_REINTENTOS  = 3
const INTERVALO_MS    = 5_000
const TIMEOUT_HTTP_MS = 3_000
const ESPERA_ARRANQUE = 8_000

let reintentos  = 0
let proceso     = null
let verificando = false
let intervalId  = null

// ── Helpers ──────────────────────────────────────────────────────────────────

const ts    = () => new Date().toLocaleTimeString('es-MX')
const log   = (m) => console.log (`\x1b[36m[${ts()}] [watchdog]\x1b[0m ${m}`)
const warn  = (m) => console.warn(`\x1b[33m[${ts()}] [watchdog]\x1b[0m ⚠  ${m}`)
const error = (m) => console.error(`\x1b[31m[${ts()}] [watchdog]\x1b[0m ✗  ${m}`)

const esperar = (ms) => new Promise((r) => setTimeout(r, ms))

function chequearBackend() {
  return new Promise((resolve) => {
    const req = http.get(BACKEND_URL, { timeout: TIMEOUT_HTTP_MS }, (res) => {
      resolve(res.statusCode < 500)
    })
    req.on('error',   () => resolve(false))
    req.on('timeout', () => { req.destroy(); resolve(false) })
  })
}

// ── Gestión del proceso ──────────────────────────────────────────────────────

function iniciarBackend() {
  if (proceso) { proceso.kill(); proceso = null }

  proceso = spawn(VENV_PYTHON, ['main.py'], { cwd: APP_DIR, stdio: 'inherit' })

  proceso.on('error', (err) => {
    error(`No se pudo iniciar el proceso: ${err.message}`)
    proceso = null
  })

  proceso.on('exit', (codigo, señal) => {
    warn(`Backend terminó (código: ${codigo ?? '-'}, señal: ${señal ?? '-'})`)
    proceso = null
  })
}

async function monitorear() {
  if (verificando) return
  verificando = true

  const activo = await chequearBackend()

  if (activo) {
    if (reintentos > 0) {
      log('✓ Backend restaurado. Contador reiniciado.')
      reintentos = 0
    }
  } else if (!proceso) {
    if (reintentos >= MAX_REINTENTOS) {
      error(`Límite de ${MAX_REINTENTOS} reintentos alcanzado. Watchdog detenido.`)
      clearInterval(intervalId)
    } else {
      reintentos++
      warn(`Backend no responde. Reintento ${reintentos}/${MAX_REINTENTOS}...`)
      iniciarBackend()
      await esperar(ESPERA_ARRANQUE)
    }
  }

  verificando = false
}

function apagar() {
  clearInterval(intervalId)
  if (proceso) { proceso.kill(); proceso = null }
}

// ── Plugin de Vite ───────────────────────────────────────────────────────────

export default function backendWatchdog() {
  return {
    name: 'backend-watchdog',
    apply: 'serve',   // solo en modo dev, nunca en build

    async configureServer() {
      const yaActivo = await chequearBackend()

      if (yaActivo) {
        log('Backend ya está corriendo. Solo monitoreo activo.')
      } else {
        reintentos = 1
        log(`Arrancando backend (intento ${reintentos}/${MAX_REINTENTOS})...`)
        iniciarBackend()
        await esperar(ESPERA_ARRANQUE)
        log(`Iniciando monitoreo de ${BACKEND_URL}`)
      }

      intervalId = setInterval(monitorear, INTERVALO_MS)

      // Limpiar al cerrar Vite
      process.on('exit',    apagar)
      process.on('SIGINT',  apagar)
      process.on('SIGTERM', apagar)
    },
  }
}
