## Crear entorno virtual

python -m venv venv

## Activar entorno virtual

venv\Scripts\activate

## Instalar dependencias

pip install -r requirements.txt

## Ejecutar servidor

uvicorn app.main:app --reload

## Documentacion

http://127.0.0.1:8000/docs
