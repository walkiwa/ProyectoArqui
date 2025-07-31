from flask import Flask, render_template, request, redirect, session
import pyodbc
import os # Importar el módulo os para variables de entorno


app = Flask(__name__)
# Es mejor obtener la secret_key de una variable de entorno en producción
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'secreto_super_seguro_desarrollo') #

# Obtener las credenciales de la base de datos de variables de entorno
# Estas variables las configurarás en "Application settings" en el portal de Azure
server = os.environ.get('DB_SERVER') #
database = os.environ.get('DB_DATABASE') #
username = os.environ.get('DB_USERNAME') #
password = os.environ.get('DB_PASSWORD') #
driver = '{ODBC Driver 18 for SQL Server}' # Asegúrate de que este driver esté disponible en Azure Linux App Service

# Función para obtener una nueva conexión a la base de datos por cada petición o cuando se necesite
def get_db_connection():
    conn_str = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    return pyodbc.connect(conn_str) #

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def validar():
    usuario = request.form['usuario']
    clave = request.form['clave']
    try:
        with get_db_connection() as conn: # Usar 'with' para asegurar que la conexión se cierre
            cursor = conn.cursor()
            cursor.execute("SELECT Rol FROM Usuarios WHERE Usuario = ? AND Clave = ?", (usuario, clave))
            resultado = cursor.fetchone()
            if resultado:
                rol = resultado[0]
                session['usuario'] = usuario
                session['rol'] = rol
                return redirect('/crear_ticket') if rol == 'Usuario' else redirect('/ver_tickets')
    except Exception as e:
        # Esto imprimirá el error en los logs de la aplicación de Azure
        print(f"Error durante la validación de login: {e}")
        return "Error en la base de datos o credenciales incorrectas."

    return "Credenciales incorrectas"

@app.route('/crear_ticket')
def crear_ticket():
    # Asegúrate de que el usuario esté logueado y tenga el rol correcto para acceder aquí
    if 'usuario' not in session or session.get('rol') != 'Usuario':
        return redirect('/login')
    return render_template('crear_ticket.html')

@app.route('/ver_tickets')
def ver_tickets():
    # Asegúrate de que el usuario esté logueado
    if 'usuario' not in session:
        return redirect('/login')
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Tickets") # Considera filtrar tickets por usuario o rol si aplica
            tickets = cursor.fetchall()
            return render_template('ver_tickets.html', tickets=tickets)
    except Exception as e:
        print(f"Error al obtener tickets: {e}")
        return "Error al cargar los tickets."

# No se necesita app.run() aquí para el despliegue en Azure, Gunicorn lo manejará
# if __name__ == '__main__':
#    app.run()
