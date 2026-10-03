import os
import re
import json
import csv
import time
import threading
from datetime import datetime, timezone
from collections import Counter, defaultdict

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING
from pydantic import BaseModel, ValidationError
import ollama

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    REPORTLAB_OK = True
except Exception:
    REPORTLAB_OK = False


load_dotenv()

MONGO_CLUSTER = os.getenv("MONGO_CLUSTER", "")
MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")
MONGO_DB = os.getenv("MONGO_DB", "logismart")
MONGO_URI = os.getenv("MONGO_URI", "")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


CATEGORIAS = {
    "materiales_peligrosos": [
        "peligroso", "derrame", "fuga", "quimico",
        "inflamable", "toxico", "corrosivo"
    ],
    "sobrepeso": [
        "sobrepeso", "excede", "bascula",
        "exceso de peso", "sobrecarga"
    ],
    "acceso_no_autorizado": [
        "sin autorizacion", "no autorizado",
        "acceso denegado", "barrera", "intruso"
    ],
    "falla_hardware": [
        "camara", "sensor", "lector", "rfid",
        "no enciende", "apagado", "danado", "falla electrica"
    ],
    "falla_software": [
        "sistema", "error", "pantalla", "caido",
        "no carga", "lento", "software", "aplicacion"
    ],
    "somnolencia_conductor": [
        "somnolencia", "dormido", "cansancio",
        "fatiga", "sueno"
    ]
}

PALABRAS_URGENTES = [
    "urgente", "emergencia", "accidente",
    "incendio", "herido", "critico", "inmediato"
]

PRIORIDAD_BASE = {
    "materiales_peligrosos": "critica",
    "somnolencia_conductor": "alta",
    "acceso_no_autorizado": "alta",
    "sobrepeso": "media",
    "falla_hardware": "media",
    "falla_software": "baja",
    "otro": "baja"
}

ORDEN_PRIORIDAD = ["baja", "media", "alta", "critica"]

ESTADOS_INCIDENTE = [
    "nuevo",
    "en_atencion",
    "cerrado"
]

COLECCIONES = [
    "camiones",
    "accesos",
    "incidentes",
    "riesgos_eticos",
    "evaluaciones_llm"
]


def normalizar(texto):
    texto = str(texto or "").lower()
    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n"
    }

    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)

    return texto


def nivel_riesgo(probabilidad, impacto):
    try:
        valor = int(probabilidad) * int(impacto)
    except Exception:
        return "bajo", 0

    if valor >= 17:
        nivel = "critico"
    elif valor >= 10:
        nivel = "alto"
    elif valor >= 5:
        nivel = "medio"
    else:
        nivel = "bajo"

    return nivel, valor


def evaluar_reglas(P, Q, R, S, C=True, H=False):
    A = P and S and not Q
    E = P and (R or Q)

    I = P and C
    J = R and H

    return {
        "A": A,
        "E": E,
        "I": I,
        "J": J
    }


def explicar_reglas(P, Q, R, S, C=True, H=False):
    resultados = evaluar_reglas(P, Q, R, S, C, H)

    explicacion = []

    explicacion.append(
        f"A = P AND S AND NOT Q -> "
        f"{P} AND {S} AND NOT {Q} = {resultados['A']}"
    )

    explicacion.append(
        f"E = P AND (R OR Q) -> "
        f"{P} AND ({R} OR {Q}) = {resultados['E']}"
    )

    explicacion.append(
        f"I = P AND C -> "
        f"{P} AND {C} = {resultados['I']}"
    )

    explicacion.append(
        f"J = R AND H -> "
        f"{R} AND {H} = {resultados['J']}"
    )

    return "\n".join(explicacion)


def extraer_datos(texto):
    texto_normalizado = normalizar(texto)

    placas = re.findall(
        r"\b[A-Z0-9]{2,3}-\d{2,3}-[A-Z0-9]{1,2}\b",
        texto.upper()
    )

    camiones = re.findall(
        r"\bCAM-\d+\b",
        texto.upper()
    )

    pesos = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:kg|kgs|kilogramos|ton|toneladas)\b",
        texto_normalizado
    )

    ubicaciones = re.findall(
        r"\b(?:anden|puerta|muelle|caseta|dock)\s*[A-Za-z0-9-]*\b",
        texto_normalizado
    )

    return {
        "placas": placas,
        "camiones": camiones,
        "pesos": pesos,
        "ubicaciones": ubicaciones
    }


def clasificar_reglas(texto):
    texto_n = normalizar(texto)

    encontrados = {}

    for categoria, palabras in CATEGORIAS.items():
        coincidencias = []

        for palabra in palabras:
            if palabra in texto_n:
                coincidencias.append(palabra)

        if coincidencias:
            encontrados[categoria] = coincidencias

    if not encontrados:
        categoria = "otro"
    else:
        categoria = max(
            encontrados,
            key=lambda x: len(encontrados[x])
        )

    prioridad = PRIORIDAD_BASE.get(categoria, "baja")

    if any(palabra in texto_n for palabra in PALABRAS_URGENTES):
        if prioridad == "baja":
            prioridad = "media"
        elif prioridad == "media":
            prioridad = "alta"
        elif prioridad == "alta":
            prioridad = "critica"

    datos = extraer_datos(texto)

    return {
        "categoria": categoria,
        "prioridad": prioridad,
        "entidades": datos,
        "resumen": (
            f"Clasificación realizada mediante reglas. "
            f"Categoría detectada: {categoria}."
        )
    }


class ResultadoLLM(BaseModel):
    categoria: str
    prioridad: str
    entidades: dict
    resumen: str


def conectar_mongo():
    try:
        if MONGO_URI:
            cliente = MongoClient(
                MONGO_URI,
                serverSelectionTimeoutMS=5000
            )
        elif MONGO_CLUSTER and MONGO_USER and MONGO_PASSWORD:
            uri = (
                f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
                f"@{MONGO_CLUSTER}/"
                f"?retryWrites=true&w=majority"
            )

            cliente = MongoClient(
                uri,
                serverSelectionTimeoutMS=5000
            )
        else:
            cliente = MongoClient(
                "mongodb://localhost:27017/",
                serverSelectionTimeoutMS=3000
            )

        cliente.admin.command("ping")

        return cliente, cliente[MONGO_DB], None

    except Exception as e:
        return None, None, str(e)


class DB:
    def __init__(self):
        self.cliente = None
        self.db = None
        self.error = None
        self.conectar()

    def conectar(self):
        self.cliente, self.db, self.error = conectar_mongo()

    def disponible(self):
        return self.db is not None

    def coleccion(self, nombre):
        if not self.disponible():
            return None

        return self.db[nombre]

    def insertar(self, coleccion, documento):
        if not self.disponible():
            raise RuntimeError(
                "No hay conexión con MongoDB."
            )

        resultado = self.db[coleccion].insert_one(documento)
        return resultado.inserted_id

    def actualizar(self, coleccion, filtro, cambios):
        if not self.disponible():
            raise RuntimeError(
                "No hay conexión con MongoDB."
            )

        return self.db[coleccion].update_one(
            filtro,
            {"$set": cambios}
        )

    def eliminar(self, coleccion, filtro):
        if not self.disponible():
            raise RuntimeError(
                "No hay conexión con MongoDB."
            )

        return self.db[coleccion].delete_one(filtro)

    def buscar(self, coleccion, filtro=None, limite=100):
        if not self.disponible():
            return []

        filtro = filtro or {}

        return list(
            self.db[coleccion]
            .find(filtro)
            .sort("_id", DESCENDING)
            .limit(limite)
        )

    def contar(self, coleccion, filtro=None):
        if not self.disponible():
            return 0

        return self.db[coleccion].count_documents(
            filtro or {}
        )


def limpiar_mongo(documento):
    if isinstance(documento, dict):
        resultado = {}

        for clave, valor in documento.items():
            if clave == "_id":
                resultado[clave] = str(valor)
            else:
                resultado[clave] = limpiar_mongo(valor)

        return resultado

    if isinstance(documento, list):
        return [
            limpiar_mongo(x)
            for x in documento
        ]

    if isinstance(documento, datetime):
        return documento.isoformat()

    return documento


def validar_llm(respuesta):
    try:
        if isinstance(respuesta, dict):
            datos = respuesta
        else:
            datos = json.loads(respuesta)

        resultado = ResultadoLLM(**datos)

        if resultado.categoria not in list(CATEGORIAS.keys()) + ["otro"]:
            raise ValueError("Categoría no válida.")

        if resultado.prioridad not in ORDEN_PRIORIDAD:
            raise ValueError("Prioridad no válida.")

        return resultado.model_dump()

    except (
        json.JSONDecodeError,
        ValidationError,
        ValueError,
        TypeError
    ):
        return None


def llamar_llm(texto, modelo=None):
    modelo = modelo or OLLAMA_MODEL

    prompt = f"""
Clasifica el siguiente correo de LogiSmart.

Debes responder únicamente con JSON válido.

El JSON debe tener exactamente estos campos:

{{
  "categoria": "materiales_peligrosos | sobrepeso | acceso_no_autorizado | falla_hardware | falla_software | somnolencia_conductor | otro",
  "prioridad": "baja | media | alta | critica",
  "entidades": {{}},
  "resumen": "resumen breve"
}}

No agregues markdown.
No agregues explicaciones fuera del JSON.

Correo:
{texto}
"""

    inicio = time.perf_counter()

    for intento in range(2):
        try:
            respuesta = ollama.chat(
                model=modelo,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un clasificador de incidentes. "
                            "Responde solamente JSON válido."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                format="json"
            )

            contenido = respuesta["message"]["content"]

            resultado = validar_llm(contenido)

            if resultado:
                latencia = time.perf_counter() - inicio

                return {
                    "resultado": resultado,
                    "latencia": latencia,
                    "valido": True,
                    "intentos": intento + 1
                }

        except Exception:
            pass

    latencia = time.perf_counter() - inicio

    return {
        "resultado": None,
        "latencia": latencia,
        "valido": False,
        "intentos": 2
    }


def prioridad_mayor(p1, p2):
    if p1 not in ORDEN_PRIORIDAD:
        p1 = "baja"

    if p2 not in ORDEN_PRIORIDAD:
        p2 = "baja"

    if ORDEN_PRIORIDAD.index(p1) >= ORDEN_PRIORIDAD.index(p2):
        return p1

    return p2


def fusionar(reglas, llm):
    if not llm:
        return {
            **reglas,
            "fuente": "reglas",
            "requiere_revision_humana": False
        }

    categoria_reglas = reglas["categoria"]
    categoria_llm = llm["categoria"]

    prioridad = prioridad_mayor(
        reglas["prioridad"],
        llm["prioridad"]
    )

    desacuerdo = categoria_reglas != categoria_llm

    if desacuerdo:
        if ORDEN_PRIORIDAD.index(
            llm["prioridad"]
        ) > ORDEN_PRIORIDAD.index(
            reglas["prioridad"]
        ):
            categoria = categoria_llm
        else:
            categoria = categoria_reglas
    else:
        categoria = categoria_llm

    return {
        "categoria": categoria,
        "prioridad": prioridad,
        "entidades": llm.get(
            "entidades",
            reglas.get("entidades", {})
        ),
        "resumen": llm.get(
            "resumen",
            reglas.get("resumen", "")
        ),
        "fuente": "hibrido",
        "requiere_revision_humana": desacuerdo
    }


def clasificar(texto, modelo=None):
    inicio = time.perf_counter()

    reglas = clasificar_reglas(texto)

    llm_info = llamar_llm(
        texto,
        modelo
    )

    llm = llm_info["resultado"]

    resultado = fusionar(
        reglas,
        llm
    )

    resultado["latencia_reglas"] = 0
    resultado["latencia_llm"] = llm_info["latencia"]
    resultado["latencia_total"] = (
        time.perf_counter() - inicio
    )

    resultado["llm_valido"] = llm_info["valido"]

    return resultado


CORREOS = [
    ("Hay una fuga de químico inflamable en el camión CAM-101.", "materiales_peligrosos"),
    ("El camión presenta sobrepeso según la báscula.", "sobrepeso"),
    ("Se detectó acceso no autorizado en la puerta principal.", "acceso_no_autorizado"),
    ("La cámara del acceso no funciona.", "falla_hardware"),
    ("El sistema de registro no carga.", "falla_software"),
    ("El conductor presenta signos de somnolencia.", "somnolencia_conductor"),
    ("Existe un derrame de material tóxico.", "materiales_peligrosos"),
    ("El peso del camión excede el permitido.", "sobrepeso"),
    ("Una persona intentó entrar sin autorización.", "acceso_no_autorizado"),
    ("El lector RFID dejó de funcionar.", "falla_hardware"),
    ("La aplicación muestra un error.", "falla_software"),
    ("El conductor está muy cansado.", "somnolencia_conductor"),
    ("Se reporta una sustancia corrosiva.", "materiales_peligrosos"),
    ("La carga presenta exceso de peso.", "sobrepeso"),
    ("La barrera fue abierta por una persona no autorizada.", "acceso_no_autorizado"),
    ("El sensor dejó de responder.", "falla_hardware"),
    ("El sistema está caído.", "falla_software"),
    ("El operador reporta fatiga.", "somnolencia_conductor"),
    ("Hay material peligroso derramado.", "materiales_peligrosos"),
    ("La báscula registra una sobrecarga.", "sobrepeso"),
    ("Se detectó un intruso en el área.", "acceso_no_autorizado"),
    ("La cámara está apagada.", "falla_hardware"),
    ("La pantalla del sistema presenta error.", "falla_software"),
    ("El conductor tiene sueño.", "somnolencia_conductor"),
    ("Se reporta una fuga de material químico.", "materiales_peligrosos"),
    ("El camión excede el límite de peso.", "sobrepeso"),
    ("El acceso fue denegado a una persona.", "acceso_no_autorizado"),
    ("El lector no enciende.", "falla_hardware"),
    ("La aplicación está lenta.", "falla_software"),
    ("El conductor se encuentra dormido.", "somnolencia_conductor")
]


def evaluar_30(modelo=None):
    resultados = []

    for texto, esperado in CORREOS:
        inicio = time.perf_counter()

        reglas = clasificar_reglas(texto)

        regla_latencia = (
            time.perf_counter() - inicio
        )

        llm_info = llamar_llm(
            texto,
            modelo
        )

        llm = llm_info["resultado"]

        if llm:
            categoria_llm = llm["categoria"]
        else:
            categoria_llm = "otro"

        fusion = fusionar(
            reglas,
            llm
        )

        resultados.append({
            "esperado": esperado,
            "reglas": reglas["categoria"],
            "llm": categoria_llm,
            "hibrido": fusion["categoria"],
            "latencia_reglas": regla_latencia,
            "latencia_llm": llm_info["latencia"],
            "latencia_hibrido": (
                regla_latencia +
                llm_info["latencia"]
            )
        })

    return resultados


def exactitud(datos, campo):
    if not datos:
        return 0

    correctos = sum(
        1 for x in datos
        if x["esperado"] == x[campo]
    )

    return correctos / len(datos)


def matriz_confusion(datos, campo):
    matriz = defaultdict(Counter)

    for dato in datos:
        matriz[dato["esperado"]][dato[campo]] += 1

    return dict(matriz)


def truth_rows():
    filas = []

    for P in [False, True]:
        for Q in [False, True]:
            for R in [False, True]:
                for S in [False, True]:
                    for C in [False, True]:
                        for H in [False, True]:

                            resultados = evaluar_reglas(
                                P, Q, R, S, C, H
                            )

                            filas.append({
                                "P": P,
                                "Q": Q,
                                "R": R,
                                "S": S,
                                "C": C,
                                "H": H,
                                "A": resultados["A"],
                                "E": resultados["E"],
                                "I": resultados["I"],
                                "J": resultados["J"]
                            })

    return filas


class App:
    def __init__(self, root):
        self.root = root

        self.root.title(
            "LogiSmart - Sistema de Gestión"
        )

        self.root.geometry(
            "1250x780"
        )

        self.root.minsize(
            1050,
            650
        )

        self.db = DB()

        self.modelo = OLLAMA_MODEL

        self.historial_chat = []

        self.crear_interfaz()

        self.actualizar_dashboard()

    def crear_interfaz(self):
        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.tab_dashboard()
        self.tab_camiones()
        self.tab_accesos()
        self.tab_verdad()
        self.tab_incidentes()
        self.tab_asistente()
        self.tab_riesgos()
        self.tab_crud()
        self.tab_reportes()
        self.tab_configuracion()

    def crear_tab(self, titulo):
        frame = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            frame,
            text=titulo
        )

        return frame

    def tab_dashboard(self):
        self.dashboard = self.crear_tab(
            "Dashboard"
        )

        arriba = ttk.Frame(
            self.dashboard
        )

        arriba.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.lbl_camiones = ttk.Label(
            arriba,
            text="Camiones atendidos: 0",
            font=("Arial", 14)
        )

        self.lbl_camiones.grid(
            row=0,
            column=0,
            padx=20
        )

        self.lbl_incidentes = ttk.Label(
            arriba,
            text="Incidentes abiertos: 0",
            font=("Arial", 14)
        )

        self.lbl_incidentes.grid(
            row=0,
            column=1,
            padx=20
        )

        self.lbl_riesgos = ttk.Label(
            arriba,
            text="Riesgos críticos: 0",
            font=("Arial", 14)
        )

        self.lbl_riesgos.grid(
            row=0,
            column=2,
            padx=20
        )

        ttk.Button(
            arriba,
            text="Actualizar",
            command=self.actualizar_dashboard
        ).grid(
            row=0,
            column=3,
            padx=20
        )

        self.dashboard_tree = ttk.Treeview(
            self.dashboard,
            columns=(
                "categoria",
                "semana",
                "cantidad"
            ),
            show="headings"
        )

        for columna in (
            "categoria",
            "semana",
            "cantidad"
        ):
            self.dashboard_tree.heading(
                columna,
                text=columna.capitalize()
            )

        self.dashboard_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

    def actualizar_dashboard(self):
        if not hasattr(self, "dashboard_tree"):
            return

        if not self.db.disponible():
            self.lbl_camiones.config(
                text="MongoDB: sin conexión"
            )
            return

        accesos = self.db.contar(
            "accesos"
        )

        abiertos = self.db.contar(
            "incidentes",
            {
                "status": {
                    "$ne": "cerrado"
                }
            }
        )

        criticos = self.db.contar(
            "riesgos_eticos",
            {
                "$or": [
                    {"nivel": "critico"},
                    {"nivel_residual": "critico"}
                ]
            }
        )

        self.lbl_camiones.config(
            text=f"Registros de acceso: {accesos}"
        )

        self.lbl_incidentes.config(
            text=f"Incidentes abiertos: {abiertos}"
        )

        self.lbl_riesgos.config(
            text=f"Riesgos críticos: {criticos}"
        )

        for item in self.dashboard_tree.get_children():
            self.dashboard_tree.delete(item)

        incidentes = self.db.buscar(
            "incidentes",
            {},
            1000
        )

        grupos = Counter()

        for incidente in incidentes:
            categoria = incidente.get(
                "classification",
                incidente.get(
                    "categoria",
                    "otro"
                )
            )

            fecha = incidente.get(
                "created_at"
            )

            if isinstance(fecha, datetime):
                semana = fecha.isocalendar().week
            else:
                semana = "N/D"

            grupos[
                (categoria, semana)
            ] += 1

        for (categoria, semana), cantidad in grupos.items():
            self.dashboard_tree.insert(
                "",
                "end",
                values=(
                    categoria,
                    semana,
                    cantidad
                )
            )

    def tab_camiones(self):
        tab = self.crear_tab(
            "Camiones"
        )

        formulario = ttk.Frame(tab)
        formulario.pack(
            fill="x",
            padx=15,
            pady=15
        )

        campos = [
            "placa",
            "camion_id",
            "empresa",
            "autorizacion",
            "certificacion_conductor"
        ]

        self.camion_vars = {}

        for fila, campo in enumerate(campos):
            ttk.Label(
                formulario,
                text=campo
            ).grid(
                row=fila,
                column=0,
                padx=5,
                pady=5,
                sticky="w"
            )

            var = tk.StringVar()

            self.camion_vars[campo] = var

            ttk.Entry(
                formulario,
                textvariable=var,
                width=45
            ).grid(
                row=fila,
                column=1,
                padx=5,
                pady=5
            )

        ttk.Button(
            formulario,
            text="Guardar camión",
            command=self.guardar_camion
        ).grid(
            row=0,
            column=2,
            rowspan=2,
            padx=15
        )

        self.camiones_tree = ttk.Treeview(
            tab,
            columns=(
                "placa",
                "camion_id",
                "empresa",
                "autorizacion",
                "certificacion_conductor"
            ),
            show="headings"
        )

        for columna in self.camiones_tree["columns"]:
            self.camiones_tree.heading(
                columna,
                text=columna
            )

        self.camiones_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        ttk.Button(
            tab,
            text="Actualizar lista",
            command=self.cargar_camiones
        ).pack(
            pady=5
        )

        self.cargar_camiones()

    def guardar_camion(self):
        documento = {
            campo: var.get().strip()
            for campo, var in self.camion_vars.items()
        }

        documento["created_at"] = datetime.now(
            timezone.utc
        )

        try:
            self.db.insertar(
                "camiones",
                documento
            )

            messagebox.showinfo(
                "Correcto",
                "Camión guardado."
            )

            self.cargar_camiones()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def cargar_camiones(self):
        if not hasattr(self, "camiones_tree"):
            return

        for item in self.camiones_tree.get_children():
            self.camiones_tree.delete(item)

        try:
            datos = self.db.buscar(
                "camiones",
                {},
                200
            )

            for dato in datos:
                self.camiones_tree.insert(
                    "",
                    "end",
                    values=(
                        dato.get("placa", ""),
                        dato.get("camion_id", ""),
                        dato.get("empresa", ""),
                        dato.get("autorizacion", ""),
                        dato.get(
                            "certificacion_conductor",
                            ""
                        )
                    )
                )

        except Exception:
            pass

    def tab_accesos(self):
        tab = self.crear_tab(
            "Accesos"
        )

        izquierda = ttk.Frame(tab)
        izquierda.pack(
            side="left",
            fill="y",
            padx=20,
            pady=20
        )

        derecha = ttk.Frame(tab)
        derecha.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.acceso_vars = {}

        variables = [
            "P",
            "Q",
            "R",
            "S",
            "C",
            "H"
        ]

        for fila, variable in enumerate(variables):
            var = tk.BooleanVar(
                value=False
            )

            self.acceso_vars[variable] = var

            ttk.Checkbutton(
                izquierda,
                text=variable,
                variable=var,
                command=self.actualizar_reglas
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=5
            )

        ttk.Label(
            izquierda,
            text="Placa"
        ).grid(
            row=7,
            column=0,
            sticky="w",
            pady=5
        )

        self.placa_acceso = tk.StringVar()

        ttk.Entry(
            izquierda,
            textvariable=self.placa_acceso
        ).grid(
            row=8,
            column=0,
            pady=5
        )

        ttk.Label(
            izquierda,
            text="Camión ID"
        ).grid(
            row=9,
            column=0,
            sticky="w",
            pady=5
        )

        self.camion_acceso = tk.StringVar()

        ttk.Entry(
            izquierda,
            textvariable=self.camion_acceso
        ).grid(
            row=10,
            column=0,
            pady=5
        )

        ttk.Label(
            izquierda,
            text="Operador"
        ).grid(
            row=11,
            column=0,
            sticky="w",
            pady=5
        )

        self.operador_acceso = tk.StringVar()

        ttk.Entry(
            izquierda,
            textvariable=self.operador_acceso
        ).grid(
            row=12,
            column=0,
            pady=5
        )

        ttk.Button(
            izquierda,
            text="Guardar acceso",
            command=self.guardar_acceso
        ).grid(
            row=13,
            column=0,
            pady=15
        )

        self.resultados_reglas = {}

        for fila, nombre in enumerate(
            ["A", "E", "I", "J"]
        ):
            ttk.Label(
                derecha,
                text=f"{nombre}:"
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=8
            )

            label = ttk.Label(
                derecha,
                text="FALSO",
                font=("Arial", 14)
            )

            label.grid(
                row=fila,
                column=1,
                sticky="w",
                padx=10
            )

            self.resultados_reglas[nombre] = label

        self.semaforo_canvas = tk.Canvas(
            derecha,
            width=130,
            height=320
        )

        self.semaforo_canvas.grid(
            row=0,
            column=2,
            rowspan=5,
            padx=40
        )

        self.actualizar_reglas()

    def actualizar_reglas(self):
        valores = {
            nombre: var.get()
            for nombre, var in self.acceso_vars.items()
        }

        resultados = evaluar_reglas(
            valores["P"],
            valores["Q"],
            valores["R"],
            valores["S"],
            valores["C"],
            valores["H"]
        )

        for nombre, valor in resultados.items():
            self.resultados_reglas[
                nombre
            ].config(
                text="VERDADERO" if valor else "FALSO"
            )

        self.actualizar_semaforo(
            resultados
        )

    def actualizar_semaforo(self, resultados):
        canvas = self.semaforo_canvas

        canvas.delete("all")

        canvas.create_oval(
            30,
            20,
            100,
            90,
            fill="red" if resultados["E"] else "white"
        )

        canvas.create_oval(
            30,
            120,
            100,
            190,
            fill="yellow" if resultados["I"] else "white"
        )

        canvas.create_oval(
            30,
            220,
            100,
            290,
            fill="green" if resultados["A"] else "white"
        )

    def guardar_acceso(self):
        valores = {
            nombre: var.get()
            for nombre, var in self.acceso_vars.items()
        }

        resultados = evaluar_reglas(
            valores["P"],
            valores["Q"],
            valores["R"],
            valores["S"],
            valores["C"],
            valores["H"]
        )

        documento = {
            "placa": self.placa_acceso.get().strip(),
            "camion_id": self.camion_acceso.get().strip(),
            "P": valores["P"],
            "Q": valores["Q"],
            "R": valores["R"],
            "S": valores["S"],
            "C": valores["C"],
            "H": valores["H"],
            "A": resultados["A"],
            "E": resultados["E"],
            "I": resultados["I"],
            "J": resultados["J"],
            "operator": self.operador_acceso.get().strip(),
            "timestamp": datetime.now(
                timezone.utc
            ),
            "explicacion": explicar_reglas(
                valores["P"],
                valores["Q"],
                valores["R"],
                valores["S"],
                valores["C"],
                valores["H"]
            )
        }

        try:
            self.db.insertar(
                "accesos",
                documento
            )

            messagebox.showinfo(
                "Correcto",
                "Acceso guardado."
            )

            self.actualizar_dashboard()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def tab_verdad(self):
        tab = self.crear_tab(
            "Verdad"
        )

        controles = ttk.Frame(tab)
        controles.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.verdad_vars = {}

        for columna in [
            "P",
            "Q",
            "R",
            "S",
            "C",
            "H"
        ]:
            var = tk.BooleanVar()

            self.verdad_vars[columna] = var

            ttk.Checkbutton(
                controles,
                text=columna,
                variable=var,
                command=self.actualizar_verdad
            ).pack(
                side="left",
                padx=5
            )

        self.verdad_resultado = ttk.Label(
            controles,
            text=""
        )

        self.verdad_resultado.pack(
            side="left",
            padx=20
        )

        self.verdad_tree = ttk.Treeview(
            tab,
            columns=(
                "P",
                "Q",
                "R",
                "S",
                "C",
                "H",
                "A",
                "E",
                "I",
                "J"
            ),
            show="headings"
        )

        for columna in self.verdad_tree["columns"]:
            self.verdad_tree.heading(
                columna,
                text=columna
            )

        self.verdad_tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        for fila in truth_rows():
            self.verdad_tree.insert(
                "",
                "end",
                values=tuple(
                    "1" if fila[columna] else "0"
                    for columna in self.verdad_tree["columns"]
                )
            )

    def actualizar_verdad(self):
        valores = {
            nombre: var.get()
            for nombre, var in self.verdad_vars.items()
        }

        resultados = evaluar_reglas(
            valores["P"],
            valores["Q"],
            valores["R"],
            valores["S"],
            valores["C"],
            valores["H"]
        )

        self.verdad_resultado.config(
            text=str(resultados)
        )

    def tab_incidentes(self):
        tab = self.crear_tab(
            "Incidentes"
        )

        izquierda = ttk.Frame(tab)
        izquierda.pack(
            side="left",
            fill="y",
            padx=15,
            pady=15
        )

        derecha = ttk.Frame(tab)
        derecha.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        ttk.Label(
            izquierda,
            text="Correo o incidente"
        ).pack(
            anchor="w"
        )

        self.email_text = tk.Text(
            izquierda,
            width=48,
            height=15
        )

        self.email_text.pack(
            pady=8
        )

        ttk.Button(
            izquierda,
            text="Clasificar con Ollama",
            command=self.clasificar_incidente
        ).pack(
            pady=5
        )

        ttk.Button(
            izquierda,
            text="Guardar incidente",
            command=self.guardar_incidente
        ).pack(
            pady=5
        )

        ttk.Label(
            derecha,
            text="Resultado"
        ).pack(
            anchor="w"
        )

        self.incidente_resultado = tk.Text(
            derecha,
            height=15
        )

        self.incidente_resultado.pack(
            fill="x",
            pady=8
        )

        self.incidentes_tree = ttk.Treeview(
            derecha,
            columns=(
                "categoria",
                "prioridad",
                "status"
            ),
            show="headings"
        )

        for columna in self.incidentes_tree["columns"]:
            self.incidentes_tree.heading(
                columna,
                text=columna.capitalize()
            )

        self.incidentes_tree.pack(
            fill="both",
            expand=True
        )

        self.cargar_incidentes()

    def clasificar_incidente(self):
        texto = self.email_text.get(
            "1.0",
            "end"
        ).strip()

        if not texto:
            messagebox.showwarning(
                "Aviso",
                "Escribe un correo."
            )
            return

        self.incidente_resultado.delete(
            "1.0",
            "end"
        )

        self.incidente_resultado.insert(
            "end",
            "Clasificando con Ollama...\n"
        )

        def trabajo():
            resultado = clasificar(
                texto,
                self.modelo
            )

            self.root.after(
                0,
                lambda: self.mostrar_resultado_incidente(
                    resultado
                )
            )

        threading.Thread(
            target=trabajo,
            daemon=True
        ).start()

    def mostrar_resultado_incidente(self, resultado):
        self.ultimo_resultado_incidente = resultado

        self.incidente_resultado.delete(
            "1.0",
            "end"
        )

        self.incidente_resultado.insert(
            "end",
            json.dumps(
                resultado,
                indent=4,
                ensure_ascii=False
            )
        )

    def guardar_incidente(self):
        texto = self.email_text.get(
            "1.0",
            "end"
        ).strip()

        if not texto:
            messagebox.showwarning(
                "Aviso",
                "Escribe el incidente."
            )
            return

        if not hasattr(
            self,
            "ultimo_resultado_incidente"
        ):
            resultado = clasificar(
                texto,
                self.modelo
            )
        else:
            resultado = (
                self.ultimo_resultado_incidente
            )

        documento = {
            "original_email": texto,
            "classification": resultado[
                "categoria"
            ],
            "categoria": resultado[
                "categoria"
            ],
            "prioridad": resultado[
                "prioridad"
            ],
            "extracted_data": resultado[
                "entidades"
            ],
            "status": "nuevo",
            "resultado": resultado,
            "created_at": datetime.now(
                timezone.utc
            ),
            "history": [
                {
                    "status": "nuevo",
                    "timestamp": datetime.now(
                        timezone.utc
                    )
                }
            ]
        }

        try:
            self.db.insertar(
                "incidentes",
                documento
            )

            self.db.insertar(
                "evaluaciones_llm",
                {
                    "prompt": texto,
                    "response": resultado,
                    "model": self.modelo,
                    "latency": resultado[
                        "latencia_llm"
                    ],
                    "matched_rules": resultado[
                        "fuente"
                    ],
                    "created_at": datetime.now(
                        timezone.utc
                    )
                }
            )

            messagebox.showinfo(
                "Correcto",
                "Incidente guardado."
            )

            self.cargar_incidentes()
            self.actualizar_dashboard()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def cargar_incidentes(self):
        if not hasattr(
            self,
            "incidentes_tree"
        ):
            return

        for item in self.incidentes_tree.get_children():
            self.incidentes_tree.delete(item)

        try:
            datos = self.db.buscar(
                "incidentes",
                {},
                200
            )

            for dato in datos:
                self.incidentes_tree.insert(
                    "",
                    "end",
                    values=(
                        dato.get(
                            "classification",
                            dato.get(
                                "categoria",
                                "otro"
                            )
                        ),
                        dato.get(
                            "prioridad",
                            ""
                        ),
                        dato.get(
                            "status",
                            ""
                        )
                    )
                )

        except Exception:
            pass

    def tab_asistente(self):
        tab = self.crear_tab(
            "Asistente LLM"
        )

        superior = ttk.Frame(tab)
        superior.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.chat = tk.Text(
            superior,
            state="disabled",
            wrap="word",
            font=("Arial", 11)
        )

        self.chat.pack(
            fill="both",
            expand=True
        )

        entrada = ttk.Frame(tab)
        entrada.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        self.pregunta = tk.StringVar()

        self.entrada_chat = ttk.Entry(
            entrada,
            textvariable=self.pregunta,
            font=("Arial", 11)
        )

        self.entrada_chat.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )

        self.entrada_chat.bind(
            "<Return>",
            self.enviar_pregunta
        )

        ttk.Button(
            entrada,
            text="Enviar",
            command=self.enviar_pregunta
        ).pack(
            side="right"
        )

        self.agregar_chat(
            "Sistema",
            "Escribe una pregunta sobre los datos "
            "registrados en MongoDB."
        )

    def agregar_chat(self, usuario, texto):
        self.chat.config(
            state="normal"
        )

        self.chat.insert(
            "end",
            f"{usuario}:\n{texto}\n\n"
        )

        self.chat.see(
            "end"
        )

        self.chat.config(
            state="disabled"
        )

    def enviar_pregunta(self, event=None):
        pregunta = self.pregunta.get().strip()

        if not pregunta:
            return "break"

        self.pregunta.set("")

        self.agregar_chat(
            "Tú",
            pregunta
        )

        self.agregar_chat(
            "Asistente",
            "Buscando información en MongoDB..."
        )

        threading.Thread(
            target=self.procesar_pregunta,
            args=(pregunta,),
            daemon=True
        ).start()

        return "break"

    def extraer_consultas(self, pregunta):
        pregunta_n = normalizar(
            pregunta
        )

        camiones = re.findall(
            r"\bCAM-\d+\b",
            pregunta.upper()
        )

        placas = re.findall(
            r"\b[A-Z0-9]{2,3}-\d{2,3}-[A-Z0-9]{1,2}\b",
            pregunta.upper()
        )

        categorias = []

        for categoria, palabras in CATEGORIAS.items():
            if (
                categoria in pregunta_n or
                any(
                    palabra in pregunta_n
                    for palabra in palabras
                )
            ):
                categorias.append(
                    categoria
                )

        return {
            "camiones": list(
                dict.fromkeys(camiones)
            ),
            "placas": list(
                dict.fromkeys(placas)
            ),
            "categorias": list(
                dict.fromkeys(categorias)
            )
        }

    def buscar_contexto_asistente(self, pregunta):
        if not self.db.disponible():
            return {
                "contexto": [],
                "fuentes": [],
                "encontro": False
            }

        consultas = self.extraer_consultas(
            pregunta
        )

        registros = []
        fuentes = []

        camiones = consultas["camiones"]
        placas = consultas["placas"]
        categorias = consultas["categorias"]

        filtros_camion = []

        if camiones:
            filtros_camion.extend([
                {"camion_id": {"$in": camiones}},
                {"camion_id": {
                    "$in": [
                        x.upper()
                        for x in camiones
                    ]
                }}
            ])

        if placas:
            filtros_camion.append(
                {"placa": {"$in": placas}}
            )

        if filtros_camion:
            filtro = {
                "$or": filtros_camion
            }

            encontrados = self.db.buscar(
                "camiones",
                filtro,
                30
            )

            for dato in encontrados:
                dato["_coleccion"] = "camiones"
                registros.append(dato)

                fuentes.append(
                    f"camiones/{dato.get('_id')}"
                )

            encontrados = self.db.buscar(
                "accesos",
                filtro,
                50
            )

            for dato in encontrados:
                dato["_coleccion"] = "accesos"
                registros.append(dato)

                fuentes.append(
                    f"accesos/{dato.get('_id')}"
                )

            encontrados = self.db.buscar(
                "incidentes",
                {
                    "$or": [
                        {
                            "extracted_data.camiones": {
                                "$in": camiones
                            }
                        },
                        {
                            "resultado.entidades.camiones": {
                                "$in": camiones
                            }
                        },
                        {
                            "original_email": {
                                "$regex": "|".join(
                                    camiones
                                ),
                                "$options": "i"
                            }
                        }
                    ]
                },
                50
            )

            for dato in encontrados:
                dato["_coleccion"] = "incidentes"
                registros.append(dato)

                fuentes.append(
                    f"incidentes/{dato.get('_id')}"
                )

        if categorias:
            encontrados = self.db.buscar(
                "incidentes",
                {
                    "$or": [
                        {
                            "classification": {
                                "$in": categorias
                            }
                        },
                        {
                            "categoria": {
                                "$in": categorias
                            }
                        }
                    ]
                },
                50
            )

            for dato in encontrados:
                dato["_coleccion"] = "incidentes"
                registros.append(dato)

                fuentes.append(
                    f"incidentes/{dato.get('_id')}"
                )

        if not registros:
            palabras = [
                palabra
                for palabra in normalizar(
                    pregunta
                ).split()
                if len(palabra) >= 5
            ]

            if palabras:
                expresion = "|".join(
                    re.escape(x)
                    for x in palabras[:8]
                )

                encontrados = self.db.buscar(
                    "incidentes",
                    {
                        "$or": [
                            {
                                "original_email": {
                                    "$regex": expresion,
                                    "$options": "i"
                                }
                            },
                            {
                                "classification": {
                                    "$regex": expresion,
                                    "$options": "i"
                                }
                            }
                        ]
                    },
                    30
                )

                for dato in encontrados:
                    dato["_coleccion"] = "incidentes"
                    registros.append(dato)

                    fuentes.append(
                        f"incidentes/{dato.get('_id')}"
                    )

        unicos = {}

        for registro in registros:
            identificador = str(
                registro.get("_id")
            )

            unicos[
                identificador
            ] = registro

        registros = list(
            unicos.values()
        )

        fuentes = list(
            dict.fromkeys(fuentes)
        )

        return {
            "contexto": [
                limpiar_mongo(x)
                for x in registros[:100]
            ],
            "fuentes": fuentes[:100],
            "encontro": bool(registros)
        }

    def construir_prompt_asistente(
        self,
        pregunta,
        contexto,
        fuentes
    ):
        contexto_json = json.dumps(
            contexto,
            indent=2,
            ensure_ascii=False
        )

        fuentes_texto = "\n".join(
            f"- {fuente}"
            for fuente in fuentes
        )

        return f"""
Eres el asistente de LogiSmart.

Responde la pregunta del usuario utilizando
SOLAMENTE la información que aparece en
los registros de MongoDB proporcionados.

No inventes información.

Si la información permite responder parcialmente,
explica qué datos sí se encontraron y qué dato
no aparece.

Relaciona los registros cuando sea necesario.

Por ejemplo, si preguntan por qué un camión
fue enviado a inspección, revisa sus accesos,
las reglas A, E, I y J, incidentes y prioridades.

Menciona los datos que justifican la respuesta.

Al final indica las fuentes utilizadas.

Pregunta del usuario:
{pregunta}

Información recuperada de MongoDB:
{contexto_json}

Fuentes:
{fuentes_texto}
"""

    def procesar_pregunta(self, pregunta):
        datos = self.buscar_contexto_asistente(
            pregunta
        )

        if not datos["encontro"]:
            respuesta = (
                "No encontré información relacionada "
                "con esa pregunta en MongoDB. "
                "No voy a inventar una respuesta."
            )

            self.root.after(
                0,
                lambda: self.agregar_chat(
                    "Asistente",
                    respuesta
                )
            )

            return

        prompt = self.construir_prompt_asistente(
            pregunta,
            datos["contexto"],
            datos["fuentes"]
        )

        try:
            respuesta = ollama.chat(
                model=self.modelo,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Responde de forma clara, "
                            "breve y basada únicamente "
                            "en los datos proporcionados."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            texto = respuesta["message"]["content"]

            texto += (
                "\n\nFuentes consultadas:\n" +
                "\n".join(
                    f"- {x}"
                    for x in datos["fuentes"]
                )
            )

        except Exception as e:
           texto = (
    "Se encontró información en MongoDB, "
    "pero no fue posible consultar Ollama.\n\n"
    "Datos encontrados:\n"
    + json.dumps(
        datos["contexto"],
        indent=2,
        ensure_ascii=False
    )
    + f"\n\nError de Ollama: {e}"
)

        self.historial_chat.append({
            "pregunta": pregunta,
            "respuessta": texto,
            "fuentes": datos["fuentes"],
            "timestamp": datetime.now(
                timezone.utc
            )
        })

        self.root.after(
            0,
            lambda: self.agregar_chat(
                "Asistente",
                texto
            )
        )

    def tab_riesgos(self):
        tab = self.crear_tab(
            "Riesgos"
        )

        formulario = ttk.Frame(tab)
        formulario.pack(
            fill="x",
            padx=15,
            pady=15
        )

        campos = [
            "modulo",
            "descripcion",
            "categoria",
            "probabilidad",
            "impacto",
            "mitigacion",
            "probabilidad_residual",
            "impacto_residual"
        ]

        self.riesgo_vars = {}

        for fila, campo in enumerate(campos):
            ttk.Label(
                formulario,
                text=campo
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=3
            )

            var = tk.StringVar()

            self.riesgo_vars[campo] = var

            ttk.Entry(
                formulario,
                textvariable=var,
                width=55
            ).grid(
                row=fila,
                column=1,
                pady=3,
                padx=5
            )

        ttk.Button(
            formulario,
            text="Guardar riesgo",
            command=self.guardar_riesgo
        ).grid(
            row=0,
            column=2,
            padx=15
        )

        ttk.Button(
            formulario,
            text="Ver gráfica",
            command=self.grafica_riesgos
        ).grid(
            row=1,
            column=2,
            padx=15
        )

        self.riesgos_tree = ttk.Treeview(
            tab,
            columns=(
                "modulo",
                "categoria",
                "riesgo",
                "residual"
            ),
            show="headings"
        )

        for columna in self.riesgos_tree["columns"]:
            self.riesgos_tree.heading(
                columna,
                text=columna.capitalize()
            )

        self.riesgos_tree.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.cargar_riesgos()

    def guardar_riesgo(self):
        try:
            probabilidad = int(
                self.riesgo_vars[
                    "probabilidad"
                ].get()
            )

            impacto = int(
                self.riesgo_vars[
                    "impacto"
                ].get()
            )

            probabilidad_residual = int(
                self.riesgo_vars[
                    "probabilidad_residual"
                ].get()
            )

            impacto_residual = int(
                self.riesgo_vars[
                    "impacto_residual"
                ].get()
            )

            nivel, valor = nivel_riesgo(
                probabilidad,
                impacto
            )

            nivel_residual, valor_residual = (
                nivel_riesgo(
                    probabilidad_residual,
                    impacto_residual
                )
            )

            documento = {
                "modulo": self.riesgo_vars[
                    "modulo"
                ].get(),
                "descripcion": self.riesgo_vars[
                    "descripcion"
                ].get(),
                "categoria": self.riesgo_vars[
                    "categoria"
                ].get(),
                "probabilidad": probabilidad,
                "impacto": impacto,
                "mitigacion": self.riesgo_vars[
                    "mitigacion"
                ].get(),
                "probabilidad_residual":
                    probabilidad_residual,
                "impacto_residual":
                    impacto_residual,
                "nivel": nivel,
                "valor": valor,
                "nivel_residual":
                    nivel_residual,
                "valor_residual":
                    valor_residual,
                "historico": [],
                "created_at": datetime.now(
                    timezone.utc
                )
            }

            self.db.insertar(
                "riesgos_eticos",
                documento
            )

            messagebox.showinfo(
                "Correcto",
                "Riesgo guardado."
            )

            self.cargar_riesgos()
            self.actualizar_dashboard()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def cargar_riesgos(self):
        if not hasattr(
            self,
            "riesgos_tree"
        ):
            return

        for item in self.riesgos_tree.get_children():
            self.riesgos_tree.delete(item)

        datos = self.db.buscar(
            "riesgos_eticos",
            {},
            200
        )

        for dato in datos:
            self.riesgos_tree.insert(
                "",
                "end",
                values=(
                    dato.get(
                        "modulo",
                        ""
                    ),
                    dato.get(
                        "categoria",
                        ""
                    ),
                    f"{dato.get('nivel', '')} "
                    f"({dato.get('valor', '')})",
                    f"{dato.get('nivel_residual', '')} "
                    f"({dato.get('valor_residual', '')})"
                )
            )

    def grafica_riesgos(self):
        datos = self.db.buscar(
            "riesgos_eticos",
            {},
            200
        )

        if not datos:
            messagebox.showinfo(
                "Riesgos",
                "No hay datos para mostrar."
            )
            return

        niveles = [
            "bajo",
            "medio",
            "alto",
            "critico"
        ]

        cantidades = []

        for nivel in niveles:
            cantidad = sum(
                1
                for dato in datos
                if dato.get(
                    "nivel_residual"
                ) == nivel
            )

            cantidades.append(
                cantidad
            )

        ventana = tk.Toplevel(
            self.root
        )

        ventana.title(
            "Riesgo residual"
        )

        ventana.geometry(
            "700x500"
        )

        figura = plt.Figure(
            figsize=(7, 4),
            dpi=100
        )

        eje = figura.add_subplot(
            111
        )

        eje.bar(
            niveles,
            cantidades
        )

        eje.set_title(
            "Riesgo residual"
        )

        eje.set_xlabel(
            "Nivel"
        )

        eje.set_ylabel(
            "Cantidad"
        )

        figura.tight_layout()

        canvas = FigureCanvasTkAgg(
            figura,
            master=ventana
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    def tab_crud(self):
        tab = self.crear_tab(
            "CRUD"
        )

        izquierda = ttk.Frame(tab)
        izquierda.pack(
            side="left",
            fill="y",
            padx=15,
            pady=15
        )

        derecha = ttk.Frame(tab)
        derecha.pack(
            side="left",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        ttk.Label(
            izquierda,
            text="Colección"
        ).pack(
            anchor="w"
        )

        self.crud_coleccion = tk.StringVar(
            value="camiones"
        )

        ttk.Combobox(
            izquierda,
            textvariable=self.crud_coleccion,
            values=COLECCIONES,
            state="readonly"
        ).pack(
            pady=5
        )

        ttk.Label(
            izquierda,
            text="Documento JSON"
        ).pack(
            anchor="w"
        )

        self.crud_json = tk.Text(
            izquierda,
            width=45,
            height=20
        )

        self.crud_json.pack(
            pady=5
        )

        ttk.Button(
            izquierda,
            text="Crear",
            command=self.crud_crear
        ).pack(
            pady=3
        )

        ttk.Button(
            izquierda,
            text="Actualizar",
            command=self.crud_actualizar
        ).pack(
            pady=3
        )

        ttk.Button(
            izquierda,
            text="Eliminar",
            command=self.crud_eliminar
        ).pack(
            pady=3
        )

        ttk.Button(
            izquierda,
            text="Consultar",
            command=self.crud_consultar
        ).pack(
            pady=3
        )

        self.crud_resultado = tk.Text(
            derecha
        )

        self.crud_resultado.pack(
            fill="both",
            expand=True
        )

    def obtener_json_crud(self):
        texto = self.crud_json.get(
            "1.0",
            "end"
        ).strip()

        if not texto:
            return {}

        return json.loads(
            texto
        )

    def crud_crear(self):
        try:
            documento = self.obtener_json_crud()

            self.db.insertar(
                self.crud_coleccion.get(),
                documento
            )

            messagebox.showinfo(
                "Correcto",
                "Documento creado."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def crud_consultar(self):
        try:
            datos = self.db.buscar(
                self.crud_coleccion.get(),
                {},
                100
            )

            self.crud_resultado.delete(
                "1.0",
                "end"
            )

            self.crud_resultado.insert(
                "end",
                json.dumps(
                    [
                        limpiar_mongo(x)
                        for x in datos
                    ],
                    indent=4,
                    ensure_ascii=False
                )
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def crud_actualizar(self):
        try:
            documento = self.obtener_json_crud()

            if "_id" not in documento:
                raise ValueError(
                    "El documento necesita _id."
                )

            from bson import ObjectId

            identificador = ObjectId(
                documento["_id"]
            )

            cambios = {
                clave: valor
                for clave, valor in documento.items()
                if clave != "_id"
            }

            self.db.actualizar(
                self.crud_coleccion.get(),
                {"_id": identificador},
                cambios
            )

            messagebox.showinfo(
                "Correcto",
                "Documento actualizado."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def crud_eliminar(self):
        try:
            documento = self.obtener_json_crud()

            if "_id" not in documento:
                raise ValueError(
                    "El documento necesita _id."
                )

            from bson import ObjectId

            self.db.eliminar(
                self.crud_coleccion.get(),
                {
                    "_id": ObjectId(
                        documento["_id"]
                    )
                }
            )

            messagebox.showinfo(
                "Correcto",
                "Documento eliminado."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def tab_reportes(self):
        tab = self.crear_tab(
            "Reportes"
        )

        ttk.Button(
            tab,
            text="Exportar camiones CSV",
            command=self.exportar_camiones
        ).pack(
            pady=10
        )

        ttk.Button(
            tab,
            text="Exportar incidentes CSV",
            command=self.exportar_incidentes
        ).pack(
            pady=10
        )

        ttk.Button(
            tab,
            text="Exportar riesgos JSON",
            command=self.exportar_riesgos
        ).pack(
            pady=10
        )

        ttk.Button(
            tab,
            text="Generar PDF",
            command=self.generar_pdf
        ).pack(
            pady=10
        )

        ttk.Button(
            tab,
            text="Evaluar 30 correos",
            command=self.evaluar_30_gui
        ).pack(
            pady=10
        )

        self.reporte_resultado = tk.Text(
            tab,
            height=20
        )

        self.reporte_resultado.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def guardar_csv(self, archivo, datos):
        if not datos:
            return

        claves = set()

        for dato in datos:
            claves.update(
                dato.keys()
            )

        claves = list(claves)

        with open(
            archivo,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as salida:

            escritor = csv.DictWriter(
                salida,
                fieldnames=claves
            )

            escritor.writeheader()

            for dato in datos:
                escritor.writerow({
                    clave: str(
                        dato.get(clave, "")
                    )
                    for clave in claves
                })

    def exportar_camiones(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV", "*.csv")
            ]
        )

        if not archivo:
            return

        datos = self.db.buscar(
            "camiones",
            {},
            10000
        )

        self.guardar_csv(
            archivo,
            [
                limpiar_mongo(x)
                for x in datos
            ]
        )

        messagebox.showinfo(
            "Correcto",
            "Archivo exportado."
        )

    def exportar_incidentes(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[
                ("CSV", "*.csv")
            ]
        )

        if not archivo:
            return

        datos = self.db.buscar(
            "incidentes",
            {},
            10000
        )

        self.guardar_csv(
            archivo,
            [
                limpiar_mongo(x)
                for x in datos
            ]
        )

        messagebox.showinfo(
            "Correcto",
            "Archivo exportado."
        )

    def exportar_riesgos(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON", "*.json")
            ]
        )

        if not archivo:
            return

        datos = self.db.buscar(
            "riesgos_eticos",
            {},
            10000
        )

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as salida:

            json.dump(
                [
                    limpiar_mongo(x)
                    for x in datos
                ],
                salida,
                indent=4,
                ensure_ascii=False
            )

        messagebox.showinfo(
            "Correcto",
            "Archivo exportado."
        )

    def generar_pdf(self):
        if not REPORTLAB_OK:
            messagebox.showerror(
                "Error",
                "Instala reportlab."
            )
            return

        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF", "*.pdf")
            ]
        )

        if not archivo:
            return

        datos = self.db.buscar(
            "incidentes",
            {},
            100
        )

        documento = canvas.Canvas(
            archivo,
            pagesize=letter
        )

        documento.setFont(
            "Helvetica-Bold",
            16
        )

        documento.drawString(
            50,
            750,
            "Reporte LogiSmart"
        )

        y = 720

        documento.setFont(
            "Helvetica",
            10
        )

        for dato in datos[:35]:
            texto = (
                f"{dato.get('classification', 'otro')} "
                f"- {dato.get('prioridad', '')} "
                f"- {dato.get('status', '')}"
            )

            documento.drawString(
                50,
                y,
                texto[:110]
            )

            y -= 18

            if y < 50:
                documento.showPage()
                y = 750

        documento.save()

        messagebox.showinfo(
            "Correcto",
            "PDF generado."
        )

    def evaluar_30_gui(self):
        self.reporte_resultado.delete(
            "1.0",
            "end"
        )

        self.reporte_resultado.insert(
            "end",
            "Evaluando 30 correos con Ollama...\n"
        )

        def trabajo():
            datos = evaluar_30(
                self.modelo
            )

            resultados = {
                "accuracy_reglas": exactitud(
                    datos,
                    "reglas"
                ),
                "accuracy_llm": exactitud(
                    datos,
                    "llm"
                ),
                "accuracy_hibrido": exactitud(
                    datos,
                    "hibrido"
                ),
                "latencia_reglas_promedio":
                    sum(
                        x["latencia_reglas"]
                        for x in datos
                    ) / len(datos),
                "latencia_llm_promedio":
                    sum(
                        x["latencia_llm"]
                        for x in datos
                    ) / len(datos),
                "latencia_hibrido_promedio":
                    sum(
                        x["latencia_hibrido"]
                        for x in datos
                    ) / len(datos),
                "matriz_reglas":
                    matriz_confusion(
                        datos,
                        "reglas"
                    ),
                "matriz_llm":
                    matriz_confusion(
                        datos,
                        "llm"
                    ),
                "matriz_hibrido":
                    matriz_confusion(
                        datos,
                        "hibrido"
                    )
            }

            self.root.after(
                0,
                lambda: self.mostrar_evaluacion(
                    resultados
                )
            )

        threading.Thread(
            target=trabajo,
            daemon=True
        ).start()

    def mostrar_evaluacion(self, resultados):
        self.reporte_resultado.delete(
            "1.0",
            "end"
        )

        self.reporte_resultado.insert(
            "end",
            json.dumps(
                resultados,
                indent=4,
                ensure_ascii=False
            )
        )

    def tab_configuracion(self):
        tab = self.crear_tab(
            "Configuración"
        )

        ttk.Label(
            tab,
            text="Modelo de Ollama"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        self.modelo_var = tk.StringVar(
            value=self.modelo
        )

        ttk.Entry(
            tab,
            textvariable=self.modelo_var,
            width=50
        ).pack(
            padx=20,
            pady=5
        )

        ttk.Button(
            tab,
            text="Guardar configuración",
            command=self.guardar_configuracion
        ).pack(
            padx=20,
            pady=10
        )

        ttk.Button(
            tab,
            text="Probar MongoDB",
            command=self.probar_mongo
        ).pack(
            padx=20,
            pady=10
        )

        ttk.Button(
            tab,
            text="Probar Ollama",
            command=self.probar_ollama
        ).pack(
            padx=20,
            pady=10
        )

        ttk.Button(
            tab,
            text="Cargar datos de demostración",
            command=self.cargar_demo
        ).pack(
            padx=20,
            pady=10
        )

    def guardar_configuracion(self):
        self.modelo = (
            self.modelo_var.get().strip()
        )

        messagebox.showinfo(
            "Configuración",
            f"Modelo configurado: {self.modelo}"
        )

    def probar_mongo(self):
        self.db.conectar()

        if self.db.disponible():
            messagebox.showinfo(
                "MongoDB",
                "Conexión correcta."
            )
        else:
            messagebox.showerror(
                "MongoDB",
                f"No se pudo conectar.\n\n"
                f"{self.db.error}"
            )

    def probar_ollama(self):
        try:
            respuesta = ollama.chat(
                model=self.modelo,
                messages=[
                    {
                        "role": "user",
                        "content": "Responde solamente: OK"
                    }
                ]
            )

            texto = respuesta[
                "message"
            ]["content"]

            messagebox.showinfo(
                "Ollama",
                texto
            )

        except Exception as e:
            messagebox.showerror(
                "Ollama",
                str(e)
            )

    def cargar_demo(self):
        try:
            ahora = datetime.now(
                timezone.utc
            )

            self.db.insertar(
                "camiones",
                {
                    "placa": "ABC-123-X",
                    "camion_id": "CAM-102",
                    "empresa": "LogiSmart Demo",
                    "autorizacion": "vigente",
                    "certificacion_conductor":
                        "vigente",
                    "created_at": ahora
                }
            )

            reglas = evaluar_reglas(
                True,
                False,
                True,
                True,
                True,
                False
            )

            self.db.insertar(
                "accesos",
                {
                    "placa": "ABC-123-X",
                    "camion_id": "CAM-102",
                    "P": True,
                    "Q": False,
                    "R": True,
                    "S": True,
                    "C": True,
                    "H": False,
                    "A": reglas["A"],
                    "E": reglas["E"],
                    "I": reglas["I"],
                    "J": reglas["J"],
                    "operator": "demo",
                    "timestamp": ahora,
                    "explicacion":
                        explicar_reglas(
                            True,
                            False,
                            True,
                            True,
                            True,
                            False
                        )
                }
            )

            self.db.insertar(
                "incidentes",
                {
                    "original_email":
                        "El CAM-102 requiere inspección "
                        "porque se detectó una condición "
                        "de acceso que debe verificarse.",
                    "classification":
                        "acceso_no_autorizado",
                    "categoria":
                        "acceso_no_autorizado",
                    "prioridad": "alta",
                    "extracted_data": {
                        "camiones": ["CAM-102"],
                        "placas": ["ABC-123-X"]
                    },
                    "status": "en_atencion",
                    "created_at": ahora,
                    "history": [
                        {
                            "status": "nuevo",
                            "timestamp": ahora
                        },
                        {
                            "status": "en_atencion",
                            "timestamp": ahora
                        }
                    ]
                }
            )

            messagebox.showinfo(
                "Demo",
                "Datos de demostración cargados."
            )

            self.cargar_camiones()
            self.cargar_incidentes()
            self.actualizar_dashboard()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )


def main():
    root = tk.Tk()

    app = App(root)

    root.mainloop()


if __name__ == "__main__":
    main()