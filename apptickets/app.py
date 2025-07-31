
from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'secreto123'

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:sqlserverjonnwalky.database.windows.net,1433;DATABASE=TicketsDB;UID=azureuser;PWD=Hazel123+'

@app.route('/')
def home():
    if 'usuario' in session:
        return 'Bienvenido ' + session['usuario']
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dbo.Usuarios WHERE Usuario = ? AND Clave = ?", (usuario, clave))
            row = cursor.fetchone()
            if row:
                session['usuario'] = usuario
                return redirect('/')
        except Exception as e:
            return 'Error en conexión: ' + str(e)
        return 'Credenciales incorrectas'
    return render_template('login.html')
