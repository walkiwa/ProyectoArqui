from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'secreto_super_seguro'

# Conexión a Azure SQL Database
server = 'sqlserverjonnwalky.database.windows.net'
database = 'TicketsDB'
username = 'Adminjw'
password = 'Abc123++'
driver = '{ODBC Driver 18 for SQL Server}'

conn = pyodbc.connect(
    f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
)

cursor = conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def validar():
    usuario = request.form['usuario']
    clave = request.form['clave']
    cursor.execute("SELECT Rol FROM Usuarios WHERE Usuario = ? AND Clave = ?", (usuario, clave))
    resultado = cursor.fetchone()
    if resultado:
        rol = resultado[0]
        session['usuario'] = usuario
        session['rol'] = rol
        return redirect('/crear_ticket') if rol == 'Usuario' else redirect('/ver_tickets')
    return "Credenciales incorrectas"

@app.route('/crear_ticket')
def crear_ticket():
    return render_template('crear_ticket.html')

@app.route('/ver_tickets')
def ver_tickets():
    cursor.execute("SELECT * FROM Tickets")
    tickets = cursor.fetchall()
    return render_template('ver_tickets.html', tickets=tickets)

if __name__ == '__main__':
    app.run()
