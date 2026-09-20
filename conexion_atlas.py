from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener variables
usuario = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
base_datos = os.getenv("MONGO_DB")
coleccion_nombre = os.getenv("MONGO_COLLECTION")

# Crear URL de conexión
mongo_url = f"mongodb+srv://{usuario}:{password}@{cluster}/"

# Conectar a MongoDB Atlas
cliente = MongoClient(mongo_url)

# Seleccionar base de datos
db = cliente[base_datos]

# Seleccionar colección
coleccion = db[coleccion_nombre]

# Insertar un dato
dato = {
    "nombre": "Guadalupe",
    "edad": 22
}

coleccion.insert_one(dato)

print("Conexión exitosa a MongoDB Atlas")
print("Dato guardado correctamente")

# Cerrar conexión
cliente.close()