#!/bin/bash
# Navegar al directorio donde Azure despliega tu código
cd /home/site/wwwroot

# Ejecutar Gunicorn. 'app:app' significa que buscará una instancia 'app' en el archivo 'app.py'.
# --timeout 600 es útil para conexiones de DB que puedan tomar más tiempo.
gunicorn --bind=0.0.0.0 --timeout 600 app:app
