import logging
import logging.handlers
from pathlib import Path
import time
from datetime import datetime

# Crear directorio de logs si no existe
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Formato detallado con más información
class DetailedFormatter(logging.Formatter):
    """Formatter personalizado con información detallada"""
    
    def format(self, record):
        # Generar timestamp
        if not hasattr(record, 'asctime'):
            record.asctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if hasattr(record, 'request_time'):
            # Para logs de peticiones HTTP
            return (
                f"[{record.asctime}] {record.levelname:8s} | "
                f"{record.method:6s} {record.path} | "
                f"Status: {record.status} | "
                f"Tiempo: {record.request_time:.2f}ms | "
                f"IP: {record.ip}"
            )
        elif hasattr(record, 'error_type'):
            # Para logs de errores
            return (
                f"[{record.asctime}] {record.levelname:8s} | "
                f"Error: {record.error_type} | "
                f"{record.getMessage()}"
            )
        else:
            # Logs normales
            return (
                f"[{record.asctime}] {record.levelname:8s} | "
                f"{record.name:20s} | {record.getMessage()}"
            )

# Configurar logging para el backend
def setup_logging():
    """Configura el sistema de logging para FastAPI"""
    
    # Logger raíz
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Limpiar handlers existentes
    logger.handlers = []
    
    # Formato detallado
    formatter = DetailedFormatter(
        '%(asctime)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo (Python.log)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "python.log",
        maxBytes=10485760,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Logger específico para FastAPI/Uvicorn
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    
    return logger

# Inicializar logging
logger = setup_logging()
logger.info("=" * 80)
logger.info("CopyMart ERP - Backend iniciado")
logger.info("=" * 80)

# Función para registrar peticiones HTTP
def log_request(method: str, path: str, status: int, response_time_ms: float, ip: str = "unknown"):
    """Registra detalles de una petición HTTP"""
    record = logging.LogRecord(
        name="http.request",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="HTTP Request",
        args=(),
        exc_info=None
    )
    record.method = method
    record.path = path
    record.status = status
    record.request_time = response_time_ms
    record.ip = ip
    logger.handle(record)

# Función para registrar errores de API
def log_api_error(error_type: str, message: str, details: dict = None):
    """Registra errores de API"""
    msg = f"{message}"
    if details:
        msg += f" | Detalles: {details}"
    
    record = logging.LogRecord(
        name="api.error",
        level=logging.ERROR,
        pathname="",
        lineno=0,
        msg=msg,
        args=(),
        exc_info=None
    )
    record.error_type = error_type
    logger.handle(record)

