import { reactive } from 'vue'

const modalState = reactive({
  visible: false,
  title: '',
  message: '',
  type: 'info', // info | success | error | warning | confirm
  autoCloseMs: 2500,
  confirmText: 'Aceptar',
  cancelText: 'Cancelar',
  resolver: null
})

function showModal({ title = '', message = '', type = 'info', autoCloseMs = 2500 } = {}) {
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

function success(message, title = 'Éxito', autoCloseMs = 2500) {
  showModal({ title, message, type: 'success', autoCloseMs })
}

function error(message, title = 'Error', autoCloseMs = 3000) {
  showModal({ title, message, type: 'error', autoCloseMs })
}

function info(message, title = 'Información', autoCloseMs = 2500) {
  showModal({ title, message, type: 'info', autoCloseMs })
}

function confirm(message, title = 'Confirmación', confirmText = 'Aceptar', cancelText = 'Cancelar') {
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

function onConfirm() {
  if (modalState.resolver) modalState.resolver(true)
  modalState.resolver = null
  hideModal()
}

function onCancel() {
  if (modalState.resolver) modalState.resolver(false)
  modalState.resolver = null
  hideModal()
}

export function useModalBus() {
  return { modalState, showModal, hideModal, success, error, info, confirm, onConfirm, onCancel }
}
