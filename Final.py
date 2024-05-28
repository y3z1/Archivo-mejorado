import csv
from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.font import Font

# Definir una clase para representar una tarea
class Tarea:
    def __init__(self, descripcion, completada=False):
        self.descripcion = descripcion
        self.completada = completada

# Definir una clase para manejar la lista de tareas
class ListaDeTareas:
    def __init__(self, archivo_csv):
        self.tareas = []
        self.archivo_csv = archivo_csv
        self.cargar_desde_csv()

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
        self.guardar_en_csv()

    def marcar_como_completada(self, indice):
        try:
            self.tareas[indice].completada = True
            self.guardar_en_csv()
        except IndexError:
            messagebox.showerror("Error", "Índice no válido. Por favor, seleccione un índice válido.")

    def eliminar_tarea(self, indice):
        try:
            self.tareas.pop(indice)
            self.guardar_en_csv()
        except IndexError:
            messagebox.showerror("Error", "Índice no válido. Por favor, seleccione un índice válido.")

    def guardar_en_csv(self):
        with open(self.archivo_csv, mode='w', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow(['Descripción', 'Completada'])
            for tarea in self.tareas:
                escritor_csv.writerow([tarea.descripcion, tarea.completada])

    def cargar_desde_csv(self):
        try:
            with open(self.archivo_csv, mode='r') as archivo:
                lector_csv = csv.reader(archivo)
                next(lector_csv)  # Saltar la cabecera
                for fila in lector_csv:
                    if fila:
                        descripcion, completada = fila
                        tarea = Tarea(descripcion, completada == 'True')
                        self.tareas.append(tarea)
        except FileNotFoundError:
            messagebox.showinfo("Información", "El archivo CSV no existe, se creará uno nuevo al guardar las tareas.")

# Definir la aplicación GUI
class AplicacionTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("YeziTask")
        self.lista_de_tareas = ListaDeTareas('tareas.csv')
        
        # Fuentes personalizadas
        self.fuente_titulo = Font(family="Times New Roman", size=16, weight="bold")
        self.fuente_lista = Font(family="Times New Roman", size=12)
        self.fuente_botones = Font(family="Times New Roman", size=10, weight="bold")

        # Colores
        self.color_fondo = "#bedcf7"
        self.color_texto = "#000000"
        self.color_botones = "#4CAF50"
        self.color_botones_texto = "#FFFFFF"
        self.color_tarea_agregada = "#FF7200"  # Naranja
        self.color_tarea_completada = "#46af15"  # Verde

        self.crear_widgets()

    def crear_widgets(self):
        self.root.configure(bg=self.color_fondo)
        
        self.frame_tareas = Frame(self.root, bg=self.color_fondo)
        self.frame_tareas.pack(pady=10)

        self.lista_tareas = Listbox(self.frame_tareas, width=50, height=10, selectmode=SINGLE, font=self.fuente_lista, bg=self.color_fondo, fg=self.color_texto)
        self.lista_tareas.pack(side=LEFT, padx=10)
        self.scrollbar = Scrollbar(self.frame_tareas)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.lista_tareas.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lista_tareas.yview)

        self.actualizar_lista_tareas()

        self.frame_botones = Frame(self.root, bg=self.color_fondo)
        self.frame_botones.pack(pady=10)

        self.boton_agregar = Button(self.frame_botones, text="Agregar Tarea", command=self.agregar_tarea, font=self.fuente_botones, bg=self.color_botones, fg=self.color_botones_texto)
        self.boton_agregar.pack(side=LEFT, padx=5)

        self.boton_completar = Button(self.frame_botones, text="Marcar como Completada", command=self.marcar_completada, font=self.fuente_botones, bg=self.color_botones, fg=self.color_botones_texto)
        self.boton_completar.pack(side=LEFT, padx=5)

        self.boton_eliminar = Button(self.frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea, font=self.fuente_botones, bg=self.color_botones, fg=self.color_botones_texto)
        self.boton_eliminar.pack(side=LEFT, padx=5)

    def actualizar_lista_tareas(self):
        self.lista_tareas.delete(0, END)
        for i, tarea in enumerate(self.lista_de_tareas.tareas):
            estado = "✓" if tarea.completada else "✗"
            self.lista_tareas.insert(END, f"{i + 1}. {tarea.descripcion} [{estado}]")
            if tarea.completada:
                self.lista_tareas.itemconfig(i, {'fg': self.color_tarea_completada})
            else:
                self.lista_tareas.itemconfig(i, {'fg': self.color_tarea_agregada})

    def agregar_tarea(self):
        descripcion = askstring("Agregar Tarea", "Descripción de la tarea:")
        if descripcion:
            nueva_tarea = Tarea(descripcion)
            self.lista_de_tareas.agregar_tarea(nueva_tarea)
            self.actualizar_lista_tareas()
        else:
            messagebox.showwarning("Advertencia", "La descripción de la tarea no puede estar vacía.")

    def marcar_completada(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lista_de_tareas.marcar_como_completada(indice)
            self.actualizar_lista_tareas()
        else:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")

    def eliminar_tarea(self):
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lista_de_tareas.eliminar_tarea(indice)
            self.actualizar_lista_tareas()
        else:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para eliminar.")

if __name__ == "__main__":
    root = Tk()
    app = AplicacionTareas(root)
    root.mainloop()
