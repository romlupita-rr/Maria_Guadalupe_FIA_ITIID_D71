import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# 1. Cargar las variables del archivo .env
load_dotenv()

# Obtener variables de entorno
usuario = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
base_datos = os.getenv("MONGO_DB")
coleccion_nombre = os.getenv("MONGO_COLLECTION")

# Crear URL de conexión a MongoDB Atlas
mongo_url = f"mongodb+srv://{usuario}:{password}@{cluster}/"


# 2. Función para guardar los datos ingresados en la interfaz
def guardar_dato():
    # Obtener el texto ingresado en los campos de Tkinter
    nombre = entry_nombre.get().strip()
    edad_texto = entry_edad.get().strip()

    # Validación: Campos vacíos
    if not nombre or not edad_texto:
        messagebox.showwarning("Atención", "Por favor ingresa nombre y edad.")
        return

    # Validación: Edad debe ser entero
    if not edad_texto.isdigit():
        messagebox.showwarning("Atención", "La edad debe ser un número entero.")
        return

    try:
        # Conectar a MongoDB Atlas
        cliente = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        db = cliente[base_datos]
        coleccion = db[coleccion_nombre]

        # Estructura del documento a guardar
        dato = {
            "nombre": nombre,
            "edad": int(edad_texto)
        }

        # Guardar en la colección de Atlas
        coleccion.insert_one(dato)

        # Mensaje de confirmación
        messagebox.showinfo("Éxito", "Conexión exitosa a MongoDB Atlas\nDato guardado correctamente.")

        # Limpiar las entradas de texto
        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)

        # Cerrar conexión
        cliente.close()

    except PyMongoError as e:
        messagebox.showerror("Error de Conexión", f"No se pudo guardar en MongoDB Atlas:\n{e}")


# 3. Construcción de la Interfaz Gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Registro MongoDB Atlas")
ventana.geometry("340x230")
ventana.resizable(False, False)

# Componentes de la interfaz
label_nombre = tk.Label(ventana, text="Nombre:", font=("Arial", 10))
label_nombre.pack(pady=(15, 2))
entry_nombre = tk.Entry(ventana, width=30)
entry_nombre.pack(pady=2)

label_edad = tk.Label(ventana, text="Edad:", font=("Arial", 10))
label_edad.pack(pady=(10, 2))
entry_edad = tk.Entry(ventana, width=30)
entry_edad.pack(pady=2)

# Botón vinculado a la función guardar_dato mediante el parámetro 'command'
btn_guardar = tk.Button(
    ventana,
    text="Guardar en Atlas",
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    command=guardar_dato
)
btn_guardar.pack(pady=20)

# Iniciar la interfaz gráfica
ventana.mainloop()