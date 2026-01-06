#!/usr/bin/env python
"""
Script de inicio para CopyMart ERP
Configura las variables de entorno y inicia el servidor FastAPI
"""
import sys
import os

# Agregar la carpeta app al path de Python
app_path = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_path)

# Ahora importar uvicorn e iniciar
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'app.main:app',
        host='0.0.0.0',
        port=8000,
        reload=True
    )
