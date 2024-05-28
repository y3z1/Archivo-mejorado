import csv
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from colorama import init
import pyfiglet
import time

# Inicializar colorama
init(autoreset=True)

# Definir una clase para representar una transacción (ingreso o gasto)
class Transaccion:
    def __init__(self, descripcion, cantidad, tipo, fecha, moneda='EUR'):
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.tipo = tipo  # 'ingreso' o 'gasto'
        self.fecha = fecha  # fecha en formato 'DD-MM-YY'
        self.moneda = moneda  # Moneda, por defecto 'EUR'

# Definir una clase para representar el control de finanzas
class FinanzasPersonales:
    def __init__(self, archivo_csv):
        self.transacciones = []
        self.archivo_csv = archivo_csv
        self.cargar_desde_csv()

    def agregar_transaccion(self, transaccion):
        self.transacciones.append(transaccion)
        if transaccion.tipo == 'ingreso':
            messagebox.showinfo("Mensaje", "¡Así me gusta Chaval... sigue así!!!")
        else:
            messagebox.showwarning("Advertencia", "Chaval, controla el gasto!!!")
        self.guardar_en_csv()

    def mostrar_totales(self):
        total_ingresos = sum(t.cantidad for t in self.transacciones if t.tipo == 'ingreso')
        total_gastos = sum(t.cantidad for t in self.transacciones if t.tipo == 'gasto')
        balance = total_ingresos - total_gastos
        messagebox.showinfo("Totales", f"Total ingresos: {total_ingresos} EUR\nTotal gastos: {total_gastos} EUR\nBalance: {balance} EUR")

    def mostrar_transacciones(self):
        if not self.transacciones:
            messagebox.showinfo("Transacciones", "No hay transacciones registradas.")
            return
        transacciones_info = ""
        for t in self.transacciones:
            color = 'green' if t.tipo == 'ingreso' else 'red'
            transacciones_info += f"Fecha: {t.fecha}, Descripción: {t.descripcion}, Cantidad: {t.cantidad} {t.moneda}, Tipo: {t.tipo}\n"
        messagebox.showinfo("Transacciones", transacciones_info)

    def guardar_en_csv(self):
        with open(self.archivo_csv, mode='w', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow(['Fecha', 'Descripción', 'Cantidad', 'Tipo', 'Moneda'])
            for t in self.transacciones:
                escritor_csv.writerow([t.fecha, t.descripcion, int(t.cantidad), t.tipo, t.moneda])

    def cargar_desde_csv(self):
        try:
            with open(self.archivo_csv, mode='r') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Saltar la cabecera
                for fila in lector_csv:
                    if fila:
                        fecha, descripcion, cantidad, tipo, moneda = fila
                        transaccion = Transaccion(descripcion, float(cantidad), tipo, fecha, moneda)
                        self.transacciones.append(transaccion)
        except FileNotFoundError:
            print("El archivo CSV no existe, se creará uno nuevo al guardar las transacciones.")

def imprimir_titulo(titulo):
    ascii_art = pyfiglet.figlet_format(titulo)
    lines = ascii_art.split("\n")
    for line in lines:
        print(line)
        time.sleep(0.1)  # Pequeño retraso para el efecto de animación

def agregar_ingreso():
    descripcion = ingreso_var.get()
    cantidad = float(cantidad_var.get())
    fecha = fecha_var.get()
    try:
        datetime.strptime(fecha, '%d-%m-%y')
        transaccion = Transaccion(descripcion, cantidad, 'ingreso', fecha)
        finanzas.agregar_transaccion(transaccion)
        # Limpiar las entradas
        ingreso_var.set("")
        cantidad_var.set(0.0)
        fecha_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Fecha inválida. Por favor, ingrese la fecha en formato DD-MM-YY.")

def agregar_gasto():
    descripcion = gasto_var.get()
    cantidad = float(cantidad_gasto_var.get())
    fecha = fecha_gasto_var.get()
    try:
        datetime.strptime(fecha, '%d-%m-%y')
        transaccion = Transaccion(descripcion, cantidad, 'gasto', fecha)
        finanzas.agregar_transaccion(transaccion)
        # Limpiar las entradas
        gasto_var.set("")
        cantidad_gasto_var.set(0.0)
        fecha_gasto_var.set("")
    except ValueError:
        messagebox.showerror("Error", "Fecha inválida. Por favor, ingrese la fecha en formato DD-MM-YY.")

def mostrar_totales():
    finanzas.mostrar_totales()

def mostrar_transacciones():
    finanzas.mostrar_transacciones()

# Configuración de la ventana principal
root = Tk()
root.title("Patet Pecuniae")

# Crear variables para almacenar la entrada del usuario
ingreso_var = StringVar()
cantidad_var = DoubleVar()
fecha_var = StringVar()
gasto_var = StringVar()
cantidad_gasto_var = DoubleVar()
fecha_gasto_var = StringVar()

# Inicializar variables
ingreso_var.set("")
cantidad_var.set(0.0)
fecha_var.set("")
gasto_var.set("")
cantidad_gasto_var.set(0.0)
fecha_gasto_var.set("")

# Crear widgets
Label(root, text="Ingreso:").grid(row=0, column=0, padx=5, pady=5)
Entry(root, textvariable=ingreso_var).grid(row=0, column=1, padx=5, pady=5)
Label(root, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5)
Entry(root, textvariable=cantidad_var).grid(row=0, column=3, padx=5, pady=5)
Label(root, text="Fecha (DD-MM-YY):").grid(row=0, column=4, padx=5, pady=5)
Entry(root, textvariable=fecha_var).grid(row=0, column=5, padx=5, pady=5)
Button(root, text="Agregar Ingreso", command=agregar_ingreso).grid(row=0, column=6, padx=5, pady=5)

Label(root, text="Gasto:").grid(row=1, column=0, padx=5, pady=5)
Entry(root, textvariable=gasto_var).grid(row=1, column=1, padx=5, pady=5)
Label(root, text="Cantidad:").grid(row=1, column=2, padx=5, pady=5)
Entry(root, textvariable=cantidad_gasto_var).grid(row=1, column=3, padx=5, pady=5)
Label(root, text="Fecha (DD-MM-YY):").grid(row=1, column=4, padx=5, pady=5)
Entry(root, textvariable=fecha_gasto_var).grid(row=1, column=5, padx=5, pady=5)
Button(root, text="Agregar Gasto", command=agregar_gasto).grid(row=1, column=6, padx=5, pady=5)

Button(root, text="Mostrar Totales", command=mostrar_totales).grid(row=2, column=0, columnspan=3, padx=5, pady=5)
Button(root, text="Mostrar Transacciones", command=mostrar_transacciones).grid(row=2, column=3, columnspan=4, padx=5, pady=5)

# Crear instancia de FinanzasPersonales
archivo_csv = 'transacciones.csv'
finanzas = FinanzasPersonales(archivo_csv)

# Mostrar título animado y vistoso
imprimir_titulo("Patet Pecuniae")

# Iniciar el bucle de eventos
root.mainloop()
