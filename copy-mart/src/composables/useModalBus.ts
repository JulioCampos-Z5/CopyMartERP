/**
 * Composable: Modal Bus (TypeScript)
 * ===================================
 * Sistema de notificaciones y confirmaciones con modales
 */

import { reactive } from 'vue'

type ModalType = 'info' | 'success' | 'error' | 'warning' | 'confirm'

interface ModalState {
  visible: boolean
  title: string
  message: string
  type: ModalType
  autoCloseMs: number
  confirmText: string
  cancelText: string
  resolver: ((value: boolean) => void) | null
}

const modalState = reactive<ModalState>({
  visible: false,
  title: '',
  message: '',
  type: 'info',
  autoCloseMs: 2500,
  confirmText: 'Aceptar',
  cancelText: 'Cancelar',
  resolver: null
})

interface ShowModalOptions {
  title?: string
  message?: string
  type?: ModalType
  autoCloseMs?: number
}

function showModal({ title = '', message = '', type = 'info', autoCloseMs = 2500 }: ShowModalOptions = {}) {
  modalState.title = title
  modalState.message = message
  modalState.type = type
  modalState.autoCloseMs = autoCloseMs
  modalState.visible = true
  if (type !== 'confirm' && autoCloseMs && autoCloseMs > 0) {
    setTimeout(() => hideModal(), autoCloseMs)
  }
}

function hideModal() {
  modalState.visible = false
}

function success(message: string, title: string = 'Éxito', autoCloseMs: number = 2500) {
  showModal({ title, message, type: 'success', autoCloseMs })
}

function error(message: string, title: string = 'Error', autoCloseMs: number = 3000) {
  showModal({ title, message, type: 'error', autoCloseMs })
}

function info(message: string, title: string = 'Información', autoCloseMs: number = 2500) {
  showModal({ title, message, type: 'info', autoCloseMs })
}

function confirm(
  message: string, 
  title: string = 'Confirmación', 
  confirmText: string = 'Aceptar', 
  cancelText: string = 'Cancelar'
): Promise<boolean> {
  modalState.title = title
  modalState.message = message
  modalState.type = 'confirm'
  modalState.confirmText = confirmText
  modalState.cancelText = cancelText
  modalState.autoCloseMs = 0
  modalState.visible = true
  return new Promise((resolve) => {
    modalState.resolver = resolve
  })
}

function handleConfirm() {
  if (modalState.resolver) {
    modalState.resolver(true)
    modalState.resolver = null
  }
  hideModal()
}

function handleCancel() {
  if (modalState.resolver) {
    modalState.resolver(false)
    modalState.resolver = null
  }
  hideModal()
}

export function useModalBus() {
  return {
    modalState,
    showModal,
    hideModal,
    success,
    error,
    info,
    confirm,
    handleConfirm,
    handleCancel
  }
}
