import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Cargar las variables desde el archivo .env
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

# Crear la URI de conexión a MongoDB Atlas
MONGO_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/"


# ==========================================
# LÓGICA DEL AGENTE REACTIVO
# ==========================================
class AgenteClimatizacion:
    """Agente Reactivo Simple que toma decisiones de climatización."""
    def __init__(self):
        self.temperatura = 0.0
        self.humedad = 0.0
        self.accion = ""

    def percibir(self, temperatura: float, humedad: float):
        self.temperatura = temperatura
        self.humedad = humedad

    def tomar_decision(self) -> str:
        if self.temperatura > 30 and self.humedad > 70:
            self.accion = "Encender aire acondicionado (Modo Deshumidificador)"
        elif self.temperatura > 30:
            self.accion = "Encender ventilador"
        elif self.temperatura < 18:
            self.accion = "Encender calefacción"
        else:
            self.accion = "Mantener sistema apagado"
            
        return self.accion


# ==========================================
# INTERFAZ GRÁFICA CON TKINTER + ATLAS
# ==========================================
class InterfazAgente:
    def __init__(self, root):
        self.root = root
        self.root.title("Agente de Climatización + MongoDB Atlas")
        self.root.geometry("480x420")
        self.root.resizable(False, False)
        
        self.agente = AgenteClimatizacion()
        self._crear_componentes()

    def _crear_componentes(self):
        # Título
        lbl_titulo = tk.Label(
            self.root, 
            text="Controlador de Climatización e Historial Atlas", 
            font=("Arial", 12, "bold")
        )
        lbl_titulo.pack(pady=15)

        # Contenedor de Entradas
        frame_entradas = ttk.LabelFrame(self.root, text=" Sensores del Entorno ", padding=15)
        frame_entradas.pack(fill="x", padx=20, pady=5)

        ttk.Label(frame_entradas, text="Temperatura actual (°C):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_temp = ttk.Entry(frame_entradas, width=15)
        self.entry_temp.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(frame_entradas, text="Humedad actual (%):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_humedad = ttk.Entry(frame_entradas, width=15)
        self.entry_humedad.grid(row=1, column=1, padx=10, pady=5)

        # Botón de Procesamiento y Guardado
        btn_evaluar = tk.Button(
            self.root, 
            text="Procesar y Guardar en Atlas", 
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 10, "bold"),
            command=self._procesar_y_guardar
        )
        btn_evaluar.pack(pady=15)

        # Contenedor de Salida
        frame_salida = ttk.LabelFrame(self.root, text=" Decisión del Agente ", padding=15)
        frame_salida.pack(fill="x", padx=20, pady=5)

        self.lbl_accion = tk.Label(
            frame_salida, 
            text="Esperando datos de sensores...", 
            font=("Arial", 10, "italic"),
            fg="#555555",
            wraplength=420
        )
        self.lbl_accion.pack()

    def _guardar_en_atlas(self, temp: float, hum: float, accion: str):
        """Conecta a Atlas y persiste el registro en la colección 'hola'."""
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = cliente[MONGO_DB]
        coleccion = db[MONGO_COLLECTION]

        documento = {
            "temperatura_c": temp,
            "humedad_porcentaje": hum,
            "accion_ejecutada": accion,
            "fecha_registro": datetime.datetime.now(datetime.timezone.utc)
        }

        coleccion.insert_one(documento)
        cliente.close()

    def _procesar_y_guardar(self):
        # Validar entradas
        try:
            temp = float(self.entry_temp.get().strip())
            hum = float(self.entry_humedad.get().strip())
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor ingresa valores numéricos válidos.")
            return

        if not (0 <= hum <= 100):
            messagebox.showwarning("Dato Inválido", "La humedad debe estar entre 0% y 100%.")
            return

        # 1. Ejecutar Agente Reactivo
        self.agente.percibir(temp, hum)
        accion = self.agente.tomar_decision()

        # 2. Guardar en MongoDB Atlas
        try:
            self._guardar_en_atlas(temp, hum, accion)
            mensaje_db = "\n[✓ Guardado exitosamente en MongoDB Atlas]"
        except PyMongoError as e:
            mensaje_db = f"\n[✕ Error de conexión a Atlas: {e}]"

        # 3. Determinar color dinámico según la acción
        color = "#2E7D32"  # Verde (apagado)
        if "calefacción" in accion:
            color = "#C62828"  # Rojo
        elif "ventilador" in accion or "aire acondicionado" in accion:
            color = "#1565C0"  # Azul

        # 4. Actualizar Interfaz
        self.lbl_accion.config(
            text=f"Acción: {accion}{mensaje_db}", 
            font=("Arial", 10, "bold"),
            fg=color
        )


# ==========================================
# EJECUCIÓN
# ==========================================
if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazAgente(ventana)
    ventana.mainloop()