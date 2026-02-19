/**
 * Configuracion de Logging para Frontend (Vite)
 */

const isBrowser = typeof window !== 'undefined';
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://192.168.100.58:8000';
const LOG_ENDPOINT = '/api/logs/frontend';
const SEND_LEVELS = new Set(['debug', 'info', 'warn', 'error', 'success']);

function safeStringify(data) {
  try {
    return JSON.stringify(data);
  } catch (err) {
    return String(data);
  }
}

function writeLog(level, message, data = '') {
  const timestamp = new Date().toLocaleString('es-MX');
  let logEntry = `[${timestamp}] [${level.toUpperCase()}] ${message}`;

  if (data) {
    if (typeof data === 'object') {
      logEntry += ` | ${safeStringify(data)}`;
    } else {
      logEntry += ` | ${data}`;
    }
  }

  if (isBrowser) {
    console.debug(logEntry);
    if (SEND_LEVELS.has(level)) {
      sendToServer({ level, message, data, timestamp });
    }
  }
}

async function sendToServer(payload) {
  try {
    await fetch(`${API_BASE_URL}${LOG_ENDPOINT}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...payload,
        url: window?.location?.href || undefined
      }),
      keepalive: true
    });
  } catch (_) {
    // Evitar bucles de error si el backend no esta disponible
  }
}

// Interceptar errores no capturados
if (isBrowser) {
  // Error handler global
  window.addEventListener('error', (event) => {
    const msg = `${event.filename}:${event.lineno}:${event.colno} - ${event.message}`;
    console.error(`❌ [ERROR] ${msg}`);
    writeLog('error', 'Unhandled Error', { 
      message: event.message,
      filename: event.filename,
      line: event.lineno,
      column: event.colno
    });
  });

  // Promesas rechazadas
  window.addEventListener('unhandledrejection', (event) => {
    const msg = event.reason?.message || String(event.reason);
    console.error(`❌ [UNHANDLED REJECTION] ${msg}`);
    writeLog('error', 'Unhandled Promise Rejection', { 
      reason: msg,
      promise: event.reason
    });
  });
}

// Exportar funciones de logging
const logger = {
  info: (message, data) => {
    console.log(`ℹ️ [INFO] ${message}`, data || '');
    writeLog('info', message, data || '');
  },
  
  debug: (message, data) => {
    console.debug(`🔍 [DEBUG] ${message}`, data || '');
    writeLog('debug', message, data || '');
  },
  
  warn: (message, data) => {
    console.warn(`⚠️ [WARN] ${message}`, data || '');
    writeLog('warn', message, data || '');
  },
  
  error: (message, data) => {
    console.error(`❌ [ERROR] ${message}`, data || '');
    writeLog('error', message, data || '');
  },
  
  success: (message, data) => {
    console.log(`✅ [SUCCESS] ${message}`, data || '');
    writeLog('success', message, data || '');
  },
  
  corsError: (endpoint, origin, status) => {
    const msg = `CORS Error: ${endpoint} from ${origin} (${status})`;
    console.error(`🚫 ${msg}`);
    writeLog('error', 'CORS Error', { endpoint, origin, status });
  },
  
  apiError: (method, endpoint, status, message) => {
    const msg = `API ${method} ${endpoint} - ${status}: ${message}`;
    console.error(`❌ ${msg}`);
    writeLog('error', 'API Error', { method, endpoint, status, message });
  },
  
  // Nueva función para registrar peticiones HTTP con métricas
  httpRequest: (method, endpoint, status, responseTimeMs, size = null) => {
    const sizeInfo = size ? ` | Size: ${(size / 1024).toFixed(2)}KB` : '';
    const msg = `HTTP ${method} ${endpoint} | Status: ${status} | Time: ${responseTimeMs.toFixed(2)}ms${sizeInfo}`;
    
    // Colorear según status code
    if (status >= 200 && status < 300) {
      console.log(`✅ ${msg}`);
      writeLog('info', `HTTP Request Success`, { method, endpoint, status, responseTimeMs, size });
    } else if (status >= 400 && status < 500) {
      console.warn(`⚠️ ${msg}`);
      writeLog('warn', `HTTP Request Client Error`, { method, endpoint, status, responseTimeMs, size });
    } else if (status >= 500) {
      console.error(`❌ ${msg}`);
      writeLog('error', `HTTP Request Server Error`, { method, endpoint, status, responseTimeMs, size });
    }
  }
};

export default logger;
