
import tkinter as tk
from tkinter import messagebox
import json


class LogiSmart:

    def __init__(self):
        self.riesgos = []

    # seccion 2 
    def camion(self, P, Q, R, S):

        A = P and S and not Q
        E = P and (R or Q)

        return A, E

    # seccion 3 
    def incidente(self, texto):

        texto = texto.lower()

        if "login" in texto or "iniciar sesión" in texto:
            categoria = "Autenticacion"
            prioridad = "Alta"

        elif "permiso" in texto or "autorizacion" in texto:
            categoria = "Autorizacion"
            prioridad = "Alta"

        elif "camara" in texto or "cámara" in texto:
            categoria = "Camara"
            prioridad = "Media"

        else:
            categoria = "General"
            prioridad = "Baja"

        datos = {
            "incidente": texto,
            "categoria": categoria,
            "prioridad": prioridad,
            "correo": "soporte@logismart.com"
        }

        return json.dumps(datos, indent=4)

    # seccion 4
    def agregar_riesgo(self, modulo, riesgo, impacto, probabilidad):

        nivel = impacto * probabilidad

        if nivel >= 7:
            tipo = "Alto"
        elif nivel >= 4:
            tipo = "Medio"
        else:
            tipo = "Bajo"

        datos = {
            "modulo": modulo,
            "riesgo": riesgo,
            "impacto": impacto,
            "probabilidad": probabilidad,
            "nivel": nivel,
            "clasificacion": tipo
        }

        self.riesgos.append(datos)



agente = LogiSmart()



ventana = tk.Tk()
ventana.title("LogiSmart")
ventana.geometry("650x550")


titulo = tk.Label(
    ventana,
    text="LogiSmart - Centro de Control",
    font=("Arial", 18)
)
titulo.pack(pady=10)


#PEAS
peas = tk.Label(
    ventana,
    text="""
PEAS

Desempeño:
Decidir si un camion puede entrar
y si necesita inspeccion.

Entorno:
Centro de control y entrada de camiones.

Actuadores:
Permitir acceso, inspeccionar y enviar alertas.

Sensores:
Autorizacion, peso, carga y certificacion.

COMUNICACION DEL AGENTE:
El ambiente proporciona datos al agente.
El agente procesa los datos y genera una accion.
""",
    justify="left"
)

peas.pack(pady=10)




def probar_camion():

    A, E = agente.camion(
        P.get(),
        Q.get(),
        R.get(),
        S.get()
    )

    resultado = ""

    if A:
        resultado += "Acceso estandar: PERMITIDO\n"
    else:
        resultado += "Acceso estandar: NO PERMITIDO\n"

    if E:
        resultado += "Inspeccion especial: SI"
    else:
        resultado += "Inspeccion especial: NO"

    resultado_camion.config(text=resultado)


P = tk.BooleanVar()
Q = tk.BooleanVar()
R = tk.BooleanVar()
S = tk.BooleanVar()

tk.Checkbutton(
    ventana,
    text="P - Tiene autorizacion",
    variable=P
).pack()

tk.Checkbutton(
    ventana,
    text="Q - Excede el peso",
    variable=Q
).pack()

tk.Checkbutton(
    ventana,
    text="R - Tiene carga peligrosa",
    variable=R
).pack()

tk.Checkbutton(
    ventana,
    text="S - Conductor certificado",
    variable=S
).pack()

tk.Button(
    ventana,
    text="Evaluar camion",
    command=probar_camion
).pack(pady=5)

resultado_camion = tk.Label(
    ventana,
    text=""
)

resultado_camion.pack()




tk.Label(
    ventana,
    text="Incidente:"
).pack(pady=5)

entrada = tk.Entry(
    ventana,
    width=50
)

entrada.pack()


def probar_incidente():

    texto = entrada.get()

    if texto == "":
        messagebox.showwarning(
            "Aviso",
            "Escribe un incidente"
        )
        return

    resultado = agente.incidente(texto)

    salida.delete("1.0", tk.END)
    salida.insert(tk.END, resultado)


tk.Button(
    ventana,
    text="Clasificar incidente",
    command=probar_incidente
).pack(pady=5)


salida = tk.Text(
    ventana,
    height=8,
    width=65
)

salida.pack()



def mostrar_riesgos():

    agente.riesgos = []

    agente.agregar_riesgo(
        "Camara",
        "Sesgo en vision nocturna",
        3,
        3
    )

    agente.agregar_riesgo(
        "Identificacion",
        "Violacion de privacidad",
        3,
        2
    )

    texto = json.dumps(
        agente.riesgos,
        indent=4
    )

    riesgos.delete("1.0", tk.END)
    riesgos.insert(tk.END, texto)


tk.Button(
    ventana,
    text="Mostrar riesgos",
    command=mostrar_riesgos
).pack(pady=5)


riesgos = tk.Text(
    ventana,
    height=8,
    width=65
)

riesgos.pack()


ventana.mainloop()