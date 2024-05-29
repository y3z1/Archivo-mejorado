from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Base de datos simulada
transacciones = []
categorias_gasto = ['Alquiler', 'Compra', 'Agua', 'Luz', 'Gas', 'Internet', 'Samu Cole']

@app.route('/')
def index():
    return render_template('index.html', transacciones=transacciones, categorias_gasto=categorias_gasto)

@app.route('/agregar', methods=['POST'])
def agregar():
    descripcion = request.form['descripcion']
    cantidad = float(request.form['cantidad'])
    tipo = request.form['tipo']
    fecha = request.form['fecha']
    categoria = request.form.get('categoria', '')

    transaccion = {
        'descripcion': descripcion,
        'cantidad': cantidad,
        'tipo': tipo,
        'fecha': fecha,
        'categoria': categoria
    }
    transacciones.append(transaccion)
    flash('Transacción agregada con éxito!')
    return redirect(url_for('index'))

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    nueva_categoria = request.form['nueva_categoria']
    if nueva_categoria and nueva_categoria not in categorias_gasto:
        categorias_gasto.append(nueva_categoria)
        flash('Categoría agregada con éxito!')
    else:
        flash('La categoría ya existe o está vacía')
    return redirect(url_for('index'))

@app.route('/totales')
def totales():
    total_ingresos = sum(t['cantidad'] for t in transacciones if t['tipo'] == 'ingreso')
    total_gastos = sum(t['cantidad'] for t in transacciones if t['tipo'] == 'gasto')
    balance = total_ingresos - total_gastos
    return render_template('totales.html', total_ingresos=total_ingresos, total_gastos=total_gastos, balance=balance)

if __name__ == '__main__':
    app.run(debug=True)
