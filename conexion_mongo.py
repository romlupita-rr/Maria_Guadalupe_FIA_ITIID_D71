import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Reemplaza con tus datos reales de MongoDB Atlas
# Ejemplo: "mongodb+srv://mi_usuario:mi_password@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority"
MONGO_URI = "mongodb+srv://<usuario>:<password>@<cluster-url>/?retryWrites=true&w=majority"

def guardar_datos():
    nombre = entry_nombre.get().strip()
    edad_texto = entry_edad.get().strip()

    # Validaciones básicas
    if not nombre or not edad_texto:
        messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")
        return

    if not edad_texto.isdigit():
        messagebox.showwarning("Advertencia", "La edad debe ser un número entero válido.")
        return

    try:
        # Conexión a MongoDB Atlas
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = cliente["tabla_verdad"]
        coleccion = db["tabla"]

        # Estructura del documento
        dato = {
            "nombre": nombre,
            "edad": int(edad_texto)
        }

        # Guardar en Atlas
        coleccion.insert_one(dato)
        
        messagebox.showinfo("Éxito", "¡Conexión exitosa!\nDato guardado correctamente en Atlas.")
        
        # Limpiar campos tras guardar
        entry_nombre.delete(0, tk.END)
        entry_edad.delete(0, tk.END)

        cliente.close()

    except PyMongoError as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a MongoDB Atlas:\n{e}")

# Configuración de la ventana Tkinter
ventana = tk.Tk()
ventana.title("Registro MongoDB Atlas")
ventana.geometry("350x220")
ventana.resizable(False, False)

# Formulario
label_nombre = tk.Label(ventana, text="Nombre:", font=("Arial", 10))
label_nombre.pack(pady=(15, 2))
entry_nombre = tk.Entry(ventana, width=30)
entry_nombre.pack(pady=2)

label_edad = tk.Label(ventana, text="Edad:", font=("Arial", 10))
label_edad.pack(pady=(10, 2))
entry_edad = tk.Entry(ventana, width=30)
entry_edad.pack(pady=2)

# Botón para guardar
btn_guardar = tk.Button(
    ventana, 
    text="Guardar en MongoDB Atlas", 
    bg="#4CAF50", 
    fg="white", 
    font=("Arial", 10, "bold"),
    command=guardar_datos
)
btn_guardar.pack(pady=20)

ventana.mainloop()