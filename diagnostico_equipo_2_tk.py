import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

ventana = tk.Tk()
ventana.title("Sistema Experto de Diagnóstico Médico")
ventana.geometry("1200x800")
ventana.minsize(900, 650)


# ============================================================
# VARIABLES
# ============================================================

nombre = tk.StringVar()
edad = tk.StringVar()
sexo = tk.StringVar(value="M")
peso = tk.StringVar()
estatura = tk.StringVar()

dias = tk.StringVar()
intensidad = tk.IntVar(value=5)
empeoran = tk.StringVar(value="Sí")


# ============================================================
# VARIABLES DE SÍNTOMAS
# ============================================================

sintomas = {}


# ============================================================
# LISTAS DE SÍNTOMAS SEGÚN EDAD
# ============================================================

sintomas_nino = [
    "¿Tiene fiebre?",
    "¿Tiene tos?",
    "¿Tiene dolor de garganta?",
    "¿Tiene escurrimiento nasal?",
    "¿Tiene estornudos frecuentes?",
    "¿Tiene diarrea?",
    "¿Tiene vómito?",
    "¿Tiene dolor abdominal?",
    "¿Tiene dolor de cabeza?",
    "¿Está cansado o débil?"
]

sintomas_adolescente = [
    "¿Tiene fiebre?",
    "¿Tiene tos?",
    "¿Tiene dolor de garganta?",
    "¿Tiene escurrimiento nasal?",
    "¿Tiene estornudos frecuentes?",
    "¿Tiene comezón en la nariz?",
    "¿Tiene dolor de cabeza?",
    "¿Tiene cansancio?",
    "¿Tiene diarrea?",
    "¿Tiene dolor abdominal?",
    "¿Tiene dificultad para dormir?",
    "¿Tiene dolor muscular?"
]

sintomas_joven = [
    "¿Tiene estornudos frecuentes?",
    "¿Tiene comezón en la nariz?",
    "¿Tiene dolor de cabeza?",
    "¿Tiene cansancio?",
    "¿Tiene diarrea?",
    "¿Tiene dolor abdominal?",
    "¿Tiene dificultad para dormir?",
    "¿Tiene dolor muscular?",
    "¿Tiene rigidez muscular?",
    "¿Tiene fiebre?",
    "¿Tiene tos?",
    "¿Tiene dolor de garganta?"
]

sintomas_adulto = [
    "¿Tiene dolor de cabeza?",
    "¿Tiene cansancio?",
    "¿Tiene diarrea?",
    "¿Tiene dolor abdominal?",
    "¿Tiene dificultad para dormir?",
    "¿Tiene dolor muscular?",
    "¿Tiene rigidez muscular?",
    "¿Tiene fiebre?",
    "¿Tiene tos?",
    "¿Tiene dificultad para respirar?",
    "¿Tiene mareos?",
    "¿Tiene dolor en el pecho?"
]

sintomas_mayor = [
    "¿Tiene dolor de cabeza?",
    "¿Tiene cansancio?",
    "¿Tiene diarrea?",
    "¿Tiene dolor abdominal?",
    "¿Tiene dificultad para dormir?",
    "¿Tiene dolor muscular?",
    "¿Tiene rigidez muscular?",
    "¿Tiene fiebre?",
    "¿Tiene dificultad para respirar?",
    "¿Tiene mareos?",
    "¿Tiene dolor en el pecho?",
    "¿Tiene confusión?",
    "¿Tiene debilidad?"
]


# ============================================================
# OBTENER RANGO DE EDAD
# ============================================================

def obtener_rango_edad(valor):
    if valor <= 12:
        return "Niño"
    elif valor <= 17:
        return "Adolescente"
    elif valor <= 29:
        return "Joven adulto"
    elif valor <= 59:
        return "Adulto"
    else:
        return "Adulto mayor"


# ============================================================
# CARGAR SÍNTOMAS AUTOMÁTICAMENTE
# ============================================================

def cargar_sintomas(event=None):

    # Borrar síntomas anteriores
    for widget in marco_sintomas.winfo_children():
        widget.destroy()

    sintomas.clear()

    edad_texto = edad.get().strip()

    if edad_texto == "":
        etiqueta_edad_info.config(
            text="Ingresa la edad para mostrar los síntomas."
        )
        actualizar_scroll()
        return

    try:
        edad_numero = int(edad_texto)

        if edad_numero < 0 or edad_numero > 120:
            etiqueta_edad_info.config(
                text="La edad debe estar entre 0 y 120 años."
            )
            actualizar_scroll()
            return

    except ValueError:
        etiqueta_edad_info.config(
            text="La edad debe ser un número entero."
        )
        actualizar_scroll()
        return

    rango = obtener_rango_edad(edad_numero)

    etiqueta_edad_info.config(
        text=f"Rango de edad: {rango}"
    )

    if rango == "Niño":
        lista = sintomas_nino

    elif rango == "Adolescente":
        lista = sintomas_adolescente

    elif rango == "Joven adulto":
        lista = sintomas_joven

    elif rango == "Adulto":
        lista = sintomas_adulto

    else:
        lista = sintomas_mayor

    for i, pregunta in enumerate(lista):

        variable = tk.StringVar(value="No")

        sintomas[pregunta] = variable

        tk.Label(
            marco_sintomas,
            text=pregunta,
            font=("Arial", 11)
        ).grid(
            row=i,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        tk.Radiobutton(
            marco_sintomas,
            text="Sí",
            variable=variable,
            value="Sí",
            font=("Arial", 10)
        ).grid(
            row=i,
            column=1,
            padx=5
        )

        tk.Radiobutton(
            marco_sintomas,
            text="No",
            variable=variable,
            value="No",
            font=("Arial", 10)
        ).grid(
            row=i,
            column=2,
            padx=5
        )

    actualizar_scroll()


# ============================================================
# SABER SI UN SÍNTOMA ESTÁ PRESENTE
# ============================================================

def tiene_sintoma(texto):

    for pregunta, variable in sintomas.items():

        if texto.lower() in pregunta.lower():

            return variable.get() == "Sí"

    return False


# ============================================================
# DIAGNÓSTICO
# ============================================================

def diagnosticar():

    # --------------------------------------------------------
    # DATOS DEL PACIENTE
    # --------------------------------------------------------

    nombre_paciente = nombre.get().strip()
    edad_texto = edad.get().strip()
    sexo_paciente = sexo.get()
    peso_texto = peso.get().strip()
    estatura_texto = estatura.get().strip()

    dias_texto = dias.get().strip()
    intensidad_numero = intensidad.get()
    empeoran_respuesta = empeoran.get()

    # --------------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------------

    if nombre_paciente == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa el nombre del paciente."
        )
        return

    if edad_texto == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa la edad del paciente."
        )
        return

    try:
        edad_numero = int(edad_texto)

        if edad_numero < 0 or edad_numero > 120:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "La edad debe ser un número entero entre 0 y 120."
        )
        return

    if peso_texto == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa el peso."
        )
        return

    try:
        peso_numero = float(peso_texto)

        if peso_numero <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "El peso debe ser un número positivo."
        )
        return

    if estatura_texto == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa la estatura."
        )
        return

    try:
        estatura_numero = float(estatura_texto)

        if estatura_numero <= 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "La estatura debe ser un número positivo."
        )
        return

    if dias_texto == "":
        messagebox.showwarning(
            "Dato faltante",
            "Ingresa los días con síntomas."
        )
        return

    try:
        dias_numero = int(dias_texto)

        if dias_numero < 0:
            raise ValueError

    except ValueError:
        messagebox.showerror(
            "Error",
            "Los días deben ser un número entero positivo."
        )
        return

    # --------------------------------------------------------
    # CARGAR SÍNTOMAS SI TODAVÍA NO APARECEN
    # --------------------------------------------------------

    if not sintomas:
        cargar_sintomas()

    if not sintomas:
        messagebox.showwarning(
            "Síntomas",
            "Primero ingresa una edad válida para cargar los síntomas."
        )
        return

    # --------------------------------------------------------
    # RANGO DE EDAD
    # --------------------------------------------------------

    rango = obtener_rango_edad(edad_numero)

    # --------------------------------------------------------
    # CONTADORES
    # --------------------------------------------------------

    positivos = 0

    problemas = []

    recomendaciones = []

    # --------------------------------------------------------
    # CONTAR SÍNTOMAS
    # --------------------------------------------------------

    for pregunta, variable in sintomas.items():

        if variable.get() == "Sí":

            positivos += 1

            texto = pregunta.replace("¿", "")
            texto = texto.replace("?", "")

            problemas.append(texto)

    # --------------------------------------------------------
    # DIAGNÓSTICO INICIAL
    # --------------------------------------------------------

    diagnostico = "No se identifican suficientes síntomas para establecer una condición específica."

    # --------------------------------------------------------
    # REGLAS PARA ESTORNUDOS / ALERGIA
    # --------------------------------------------------------

    estornudos = tiene_sintoma("estornudos")
    comezon = tiene_sintoma("comezón")
    escurrimiento = tiene_sintoma("escurrimiento nasal")

    if estornudos and comezon:
        diagnostico = "Posible cuadro alérgico o rinitis."
        recomendaciones.append(
            "Evitar posibles factores que provoquen alergia y consultar a un profesional de salud."
        )

    elif estornudos and escurrimiento:
        diagnostico = "Posible infección respiratoria o cuadro alérgico."
        recomendaciones.append(
            "Mantener hidratación y vigilar la evolución de los síntomas."
        )

    # --------------------------------------------------------
    # REGLAS RESPIRATORIAS
    # --------------------------------------------------------

    tos = tiene_sintoma("tos")
    garganta = tiene_sintoma("dolor de garganta")
    fiebre = tiene_sintoma("fiebre")

    if tos and garganta and fiebre:
        diagnostico = "Posible infección respiratoria."
        recomendaciones.append(
            "Descansar, mantenerse hidratado y buscar valoración médica."
        )

    elif tos and garganta:
        diagnostico = "Posible irritación o infección de vías respiratorias."
        recomendaciones.append(
            "Mantener hidratación y vigilar si aparecen fiebre o dificultad respiratoria."
        )

    # --------------------------------------------------------
    # REGLAS DIGESTIVAS
    # --------------------------------------------------------

    diarrea = tiene_sintoma("diarrea")
    abdominal = tiene_sintoma("dolor abdominal")
    vomito = tiene_sintoma("vómito")

    if diarrea and abdominal and vomito:
        diagnostico = "Posible cuadro gastrointestinal."
        recomendaciones.append(
            "Mantener una adecuada hidratación y buscar valoración médica si los síntomas son intensos."
        )

    elif diarrea and abdominal:
        diagnostico = "Posible problema gastrointestinal."
        recomendaciones.append(
            "Mantener hidratación y observar la evolución."
        )

    elif diarrea:
        diagnostico = "Posible alteración gastrointestinal."
        recomendaciones.append(
            "Tomar suficientes líquidos y vigilar signos de deshidratación."
        )

    # --------------------------------------------------------
    # DOLOR MUSCULAR
    # --------------------------------------------------------

    muscular = tiene_sintoma("dolor muscular")
    rigidez = tiene_sintoma("rigidez muscular")

    if muscular and rigidez and fiebre:
        diagnostico = "Posible cuadro infeccioso que requiere valoración médica."
        recomendaciones.append(
            "Buscar valoración médica, especialmente si los síntomas aumentan."
        )

    elif muscular and rigidez:
        diagnostico = "Posible tensión o alteración muscular."
        recomendaciones.append(
            "Descansar y vigilar la evolución del dolor."
        )

    elif muscular:
        diagnostico = "Posible malestar o dolor muscular."
        recomendaciones.append(
            "Descansar y vigilar la evolución de los síntomas."
        )

    # --------------------------------------------------------
    # DOLOR DE CABEZA
    # --------------------------------------------------------

    cabeza = tiene_sintoma("dolor de cabeza")

    if cabeza and fiebre:
        diagnostico = "Dolor de cabeza asociado a un posible cuadro infeccioso."
        recomendaciones.append(
            "Vigilar la fiebre y consultar a un profesional de salud si persiste."
        )

    # --------------------------------------------------------
    # DIFICULTAD RESPIRATORIA
    # --------------------------------------------------------

    respiracion = tiene_sintoma("dificultad para respirar")

    if respiracion:
        diagnostico = "Se presenta dificultad para respirar."
        recomendaciones.append(
            "Buscar atención médica, especialmente si la dificultad respiratoria es intensa."
        )

    # --------------------------------------------------------
    # DOLOR EN EL PECHO
    # --------------------------------------------------------

    pecho = tiene_sintoma("dolor en el pecho")

    if pecho:
        diagnostico = "Se presenta dolor en el pecho."
        recomendaciones.append(
            "Buscar atención médica inmediata si el dolor es intenso, repentino o se acompaña de dificultad para respirar."
        )

    # --------------------------------------------------------
    # MAREOS / CONFUSIÓN / DEBILIDAD
    # --------------------------------------------------------

    mareos = tiene_sintoma("mareos")
    confusion = tiene_sintoma("confusión")
    debilidad = tiene_sintoma("debilidad")

    if confusion:
        recomendaciones.append(
            "La confusión requiere valoración médica."
        )

    if mareos:
        recomendaciones.append(
            "Evitar actividades de riesgo y vigilar la evolución de los mareos."
        )

    if debilidad:
        recomendaciones.append(
            "Descansar y consultar si la debilidad es intensa o persiste."
        )

    # --------------------------------------------------------
    # DIFICULTAD PARA DORMIR
    # --------------------------------------------------------

    dormir = tiene_sintoma("dificultad para dormir")

    if dormir:
        recomendaciones.append(
            "Mantener horarios regulares de sueño y evitar estimulantes antes de dormir."
        )

    # --------------------------------------------------------
    # NIVEL DE RIESGO
    # --------------------------------------------------------

    riesgo = 0

    riesgo += positivos * 2

    if fiebre:
        riesgo += 2

    if respiracion:
        riesgo += 6

    if pecho:
        riesgo += 7

    if confusion:
        riesgo += 6

    if dias_numero >= 7:
        riesgo += 2

    if intensidad_numero >= 8:
        riesgo += 3

    if empeoran_respuesta == "Sí":
        riesgo += 3

    # --------------------------------------------------------
    # NIVEL
    # --------------------------------------------------------

    if riesgo >= 18:
        nivel = "CRÍTICO"

    elif riesgo >= 11:
        nivel = "ALTO"

    elif riesgo >= 6:
        nivel = "MEDIO"

    else:
        nivel = "BAJO"

    # --------------------------------------------------------
    # RECOMENDACIÓN GENERAL
    # --------------------------------------------------------

    if not recomendaciones:

        recomendaciones.append(
            "Mantener una alimentación equilibrada, hidratación adecuada y observar la evolución."
        )

    if nivel in ["CRÍTICO", "ALTO"]:

        recomendaciones.append(
            "Se recomienda buscar valoración médica."
        )

    elif nivel == "MEDIO":

        recomendaciones.append(
            "Si los síntomas persisten o empeoran, consultar a un profesional de salud."
        )

    else:

        recomendaciones.append(
            "Continuar observando los síntomas y consultar si empeoran."
        )

    # --------------------------------------------------------
    # IMC
    # --------------------------------------------------------

    imc = peso_numero / (estatura_numero ** 2)

    if imc < 18.5:
        categoria_imc = "Bajo peso"

    elif imc < 25:
        categoria_imc = "Peso normal"

    elif imc < 30:
        categoria_imc = "Sobrepeso"

    else:
        categoria_imc = "Obesidad"

    # --------------------------------------------------------
    # REPORTE
    # --------------------------------------------------------

    numero_reporte = random.randint(10000, 99999)

    ahora = datetime.now()

    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M:%S")

    # --------------------------------------------------------
    # MOSTRAR RESULTADO
    # --------------------------------------------------------

    resultado.delete("1.0", tk.END)

    resultado.insert(
        tk.END,
        "============================================================\n"
    )

    resultado.insert(
        tk.END,
        "             SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO\n"
    )

    resultado.insert(
        tk.END,
        "============================================================\n\n"
    )

    resultado.insert(
        tk.END,
        f"Número de reporte: {numero_reporte}\n"
    )

    resultado.insert(
        tk.END,
        f"Fecha: {fecha}\n"
    )

    resultado.insert(
        tk.END,
        f"Hora: {hora}\n\n"
    )

    resultado.insert(
        tk.END,
        "---------------- DATOS DEL PACIENTE ----------------\n"
    )

    resultado.insert(
        tk.END,
        f"Nombre: {nombre_paciente}\n"
    )

    resultado.insert(
        tk.END,
        f"Edad: {edad_numero} años\n"
    )

    resultado.insert(
        tk.END,
        f"Rango de edad: {rango}\n"
    )

    resultado.insert(
        tk.END,
        f"Sexo: {sexo_paciente}\n"
    )

    resultado.insert(
        tk.END,
        f"Peso: {peso_numero:.2f} kg\n"
    )

    resultado.insert(
        tk.END,
        f"Estatura: {estatura_numero:.2f} m\n"
    )

    resultado.insert(
        tk.END,
        f"IMC: {imc:.2f} - {categoria_imc}\n\n"
    )

    resultado.insert(
        tk.END,
        "---------------- INFORMACIÓN DE SÍNTOMAS ----------------\n"
    )

    resultado.insert(
        tk.END,
        f"Días con síntomas: {dias_numero}\n"
    )

    resultado.insert(
        tk.END,
        f"Intensidad: {intensidad_numero}/10\n"
    )

    resultado.insert(
        tk.END,
        f"¿Los síntomas empeoran?: {empeoran_respuesta}\n"
    )

    resultado.insert(
        tk.END,
        f"Cantidad de síntomas positivos: {positivos}\n\n"
    )

    resultado.insert(
        tk.END,
        "---------------- DIAGNÓSTICO ----------------\n"
    )

    resultado.insert(
        tk.END,
        f"{diagnostico}\n\n"
    )

    resultado.insert(
        tk.END,
        f"Nivel de riesgo: {nivel}\n"
    )

    resultado.insert(
        tk.END,
        f"Puntuación de riesgo: {riesgo}\n\n"
    )

    resultado.insert(
        tk.END,
        "---------------- SÍNTOMAS PRESENTES ----------------\n"
    )

    if problemas:

        for problema in problemas:

            resultado.insert(
                tk.END,
                f"- {problema}\n"
            )

    else:

        resultado.insert(
            tk.END,
            "- No se registraron síntomas.\n"
        )

    resultado.insert(
        tk.END,
        "\n---------------- RECOMENDACIONES ----------------\n"
    )

    for recomendacion in recomendaciones:

        resultado.insert(
            tk.END,
            f"- {recomendacion}\n"
        )

    resultado.insert(
        tk.END,
        "\n============================================================\n"
    )

    resultado.insert(
        tk.END,
        "                     FIN DEL REPORTE\n"
    )

    resultado.insert(
        tk.END,
        "============================================================\n"
    )

    # Llevar al resultado
    marco_resultado.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=5
    )

    ventana.update_idletasks()

    resultado.see("1.0")


# ============================================================
# BORRAR TODOS LOS DATOS
# ============================================================

def borrar_datos():

    respuesta = messagebox.askyesno(
        "Borrar datos",
        "¿Quieres borrar todos los datos y comenzar un nuevo diagnóstico?"
    )

    if not respuesta:
        return

    nombre.set("")
    edad.set("")
    sexo.set("M")
    peso.set("")
    estatura.set("")

    dias.set("")
    intensidad.set(5)
    empeoran.set("Sí")

    sintomas.clear()

    for widget in marco_sintomas.winfo_children():
        widget.destroy()

    etiqueta_edad_info.config(
        text="Ingresa la edad para mostrar los síntomas."
    )

    resultado.delete(
        "1.0",
        tk.END
    )

    contenedor_canvas.yview_moveto(0)


# ============================================================
# SALIR
# ============================================================

def salir():

    respuesta = messagebox.askyesno(
        "Salir",
        "¿Deseas salir del sistema?"
    )

    if respuesta:
        ventana.destroy()


# ============================================================
# SCROLL
# ============================================================

def actualizar_scroll(event=None):

    contenedor_canvas.configure(
        scrollregion=contenedor_canvas.bbox("all")
    )


def ajustar_ancho(event):

    contenedor_canvas.itemconfig(
        ventana_canvas,
        width=event.width
    )


def scroll_mouse(event):

    contenedor_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


# ============================================================
# TÍTULO
# ============================================================

titulo = tk.Label(
    ventana,
    text="SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO",
    font=("Arial", 22, "bold")
)

titulo.pack(
    pady=15
)


# ============================================================
# CONTENEDOR DE LA PARTE CENTRAL
# ============================================================

marco_contenido = tk.Frame(ventana)

marco_contenido.pack(
    fill="both",
    expand=True,
    padx=10
)


# ============================================================
# CANVAS
# ============================================================

contenedor_canvas = tk.Canvas(
    marco_contenido,
    highlightthickness=0
)

barra_vertical = ttk.Scrollbar(
    marco_contenido,
    orient="vertical",
    command=contenedor_canvas.yview
)

marco_principal = tk.Frame(
    contenedor_canvas
)

ventana_canvas = contenedor_canvas.create_window(
    (0, 0),
    window=marco_principal,
    anchor="nw"
)

marco_principal.bind(
    "<Configure>",
    actualizar_scroll
)

contenedor_canvas.bind(
    "<Configure>",
    ajustar_ancho
)

contenedor_canvas.configure(
    yscrollcommand=barra_vertical.set
)

contenedor_canvas.pack(
    side="left",
    fill="both",
    expand=True
)

barra_vertical.pack(
    side="right",
    fill="y"
)

ventana.bind_all(
    "<MouseWheel>",
    scroll_mouse
)


# ============================================================
# DOS COLUMNAS
# ============================================================

marco_izquierdo = tk.LabelFrame(
    marco_principal,
    text="Datos del paciente",
    padx=15,
    pady=15,
    font=("Arial", 12, "bold")
)

marco_izquierdo.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=10,
    pady=10
)


marco_derecho = tk.LabelFrame(
    marco_principal,
    text="Síntomas",
    padx=15,
    pady=15,
    font=("Arial", 12, "bold")
)

marco_derecho.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=10,
    pady=10
)

marco_principal.columnconfigure(
    0,
    weight=1
)

marco_principal.columnconfigure(
    1,
    weight=1
)


# ============================================================
# DATOS DEL PACIENTE
# ============================================================

tk.Label(
    marco_izquierdo,
    text="Nombre:"
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)

entrada_nombre = tk.Entry(
    marco_izquierdo,
    textvariable=nombre,
    width=35
)

entrada_nombre.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    marco_izquierdo,
    text="Edad:"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)

entrada_edad = tk.Entry(
    marco_izquierdo,
    textvariable=edad,
    width=35
)

entrada_edad.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)

# Al cambiar la edad, cargar síntomas
entrada_edad.bind(
    "<KeyRelease>",
    cargar_sintomas
)


tk.Label(
    marco_izquierdo,
    text="Sexo:"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=8
)

combo_sexo = ttk.Combobox(
    marco_izquierdo,
    textvariable=sexo,
    values=["M", "F"],
    state="readonly",
    width=32
)

combo_sexo.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    marco_izquierdo,
    text="Peso (kg):"
).grid(
    row=3,
    column=0,
    sticky="w",
    pady=8
)

entrada_peso = tk.Entry(
    marco_izquierdo,
    textvariable=peso,
    width=35
)

entrada_peso.grid(
    row=3,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    marco_izquierdo,
    text="Estatura (m):"
).grid(
    row=4,
    column=0,
    sticky="w",
    pady=8
)

entrada_estatura = tk.Entry(
    marco_izquierdo,
    textvariable=estatura,
    width=35
)

entrada_estatura.grid(
    row=4,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# INFORMACIÓN DE SÍNTOMAS
# ============================================================

marco_info = tk.LabelFrame(
    marco_izquierdo,
    text="Información de los síntomas",
    padx=10,
    pady=10
)

marco_info.grid(
    row=5,
    column=0,
    columnspan=2,
    sticky="ew",
    pady=15
)


tk.Label(
    marco_info,
    text="Días con síntomas:"
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)

entrada_dias = tk.Entry(
    marco_info,
    textvariable=dias,
    width=15
)

entrada_dias.grid(
    row=0,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    marco_info,
    text="Intensidad (1-10):"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)

entrada_intensidad = tk.Spinbox(
    marco_info,
    from_=1,
    to=10,
    textvariable=intensidad,
    width=13
)

entrada_intensidad.grid(
    row=1,
    column=1,
    padx=10,
    pady=8
)


tk.Label(
    marco_info,
    text="¿Los síntomas empeoran?"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=8
)

combo_empeoran = ttk.Combobox(
    marco_info,
    textvariable=empeoran,
    values=["Sí", "No"],
    state="readonly",
    width=13
)

combo_empeoran.grid(
    row=2,
    column=1,
    padx=10,
    pady=8
)


# ============================================================
# INFORMACIÓN DE EDAD
# ============================================================

etiqueta_edad_info = tk.Label(
    marco_izquierdo,
    text="Ingresa la edad para mostrar los síntomas.",
    font=("Arial", 10, "italic")
)

etiqueta_edad_info.grid(
    row=6,
    column=0,
    columnspan=2,
    pady=10
)


# ============================================================
# SÍNTOMAS
# ============================================================

marco_sintomas = tk.Frame(
    marco_derecho
)

marco_sintomas.pack(
    fill="both",
    expand=True
)


# ============================================================
# RESULTADO
# ============================================================

marco_resultado = tk.LabelFrame(
    marco_principal,
    text="Resultado del diagnóstico",
    padx=10,
    pady=10,
    font=("Arial", 12, "bold")
)

marco_resultado.grid(
    row=1,
    column=0,
    columnspan=2,
    sticky="nsew",
    padx=10,
    pady=10
)


barra_resultado = ttk.Scrollbar(
    marco_resultado,
    orient="vertical"
)

barra_resultado.pack(
    side="right",
    fill="y"
)


resultado = tk.Text(
    marco_resultado,
    height=15,
    wrap="word",
    font=("Consolas", 10),
    yscrollcommand=barra_resultado.set
)

resultado.pack(
    fill="both",
    expand=True
)

barra_resultado.config(
    command=resultado.yview
)


# ============================================================
# BOTONES FIJOS
# ============================================================
#
# IMPORTANTE:
# Estos botones están FUERA del Canvas.
# Por eso siempre estarán visibles.
# ============================================================

marco_botones = tk.Frame(
    ventana,
    relief="raised",
    borderwidth=1
)

marco_botones.pack(
    fill="x",
    side="bottom",
    padx=10,
    pady=10
)


boton_diagnosticar = tk.Button(
    marco_botones,
    text="DIAGNOSTICAR",
    command=diagnosticar,
    font=("Arial", 12, "bold"),
    width=20,
    height=2,
    cursor="hand2"
)

boton_diagnosticar.pack(
    side="left",
    padx=15,
    pady=8
)


boton_borrar = tk.Button(
    marco_botones,
    text="BORRAR DATOS",
    command=borrar_datos,
    font=("Arial", 12, "bold"),
    width=20,
    height=2,
    cursor="hand2"
)

boton_borrar.pack(
    side="left",
    padx=15,
    pady=8
)


boton_salir = tk.Button(
    marco_botones,
    text="SALIR",
    command=salir,
    font=("Arial", 12, "bold"),
    width=15,
    height=2,
    cursor="hand2"
)

boton_salir.pack(
    side="right",
    padx=15,
    pady=8
)


# ============================================================
# ACTUALIZAR SCROLL
# ============================================================

ventana.update_idletasks()

actualizar_scroll()


# ============================================================
# INICIAR
# ============================================================

ventana.mainloop()