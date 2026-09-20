import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime




ventana = tk.Tk()
ventana.title("Sistema Experto de Diagnóstico Médico")

ventana.geometry("900x600")
ventana.minsize(800, 550)

ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)



nombre_var = tk.StringVar()
edad_var = tk.StringVar()
sexo_var = tk.StringVar()
peso_var = tk.StringVar()
estatura_var = tk.StringVar()

tiempo_var = tk.StringVar()
intensidad_var = tk.StringVar()
empeorando_var = tk.StringVar(value="No")

variables_sintomas = {}




titulo = tk.Label(
    ventana,
    text="SISTEMA EXPERTO DE DIAGNÓSTICO MÉDICO",
    font=("Arial", 15, "bold")
)

titulo.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(10, 5)
)



contenedor = ttk.Frame(ventana)

contenedor.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=12,
    pady=5
)

contenedor.columnconfigure(0, weight=1)
contenedor.columnconfigure(1, weight=1)
contenedor.rowconfigure(0, weight=1)




panel_izquierdo = ttk.Frame(
    contenedor,
    relief="solid",
    borderwidth=1
)

panel_izquierdo.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 6)
)


#Datos del paciente 

frame_datos = ttk.LabelFrame(
    panel_izquierdo,
    text="Datos del paciente"
)

frame_datos.pack(
    fill="x",
    padx=10,
    pady=8
)


ttk.Label(
    frame_datos,
    text="Nombre:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    frame_datos,
    textvariable=nombre_var,
    width=30
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    frame_datos,
    text="Edad:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    frame_datos,
    textvariable=edad_var,
    width=30
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    frame_datos,
    text="Sexo:"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

sexo_combo = ttk.Combobox(
    frame_datos,
    textvariable=sexo_var,
    values=["M", "F"],
    state="readonly",
    width=27
)

sexo_combo.grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    frame_datos,
    text="Peso (kg):"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    frame_datos,
    textvariable=peso_var,
    width=30
).grid(
    row=3,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    frame_datos,
    text="Estatura (m):"
).grid(
    row=4,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    frame_datos,
    textvariable=estatura_var,
    width=30
).grid(
    row=4,
    column=1,
    padx=5,
    pady=5
)


# Informacion general 

frame_general = ttk.LabelFrame(
    panel_izquierdo,
    text="Información de los síntomas"
)

frame_general.pack(
    fill="x",
    padx=10,
    pady=8
)


ttk.Label(
    frame_general,
    text="Días con síntomas:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Entry(
    frame_general,
    textvariable=tiempo_var,
    width=30
).grid(
    row=0,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    frame_general,
    text="Intensidad (1-10):"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Spinbox(
    frame_general,
    from_=1,
    to=10,
    textvariable=intensidad_var,
    width=28
).grid(
    row=1,
    column=1,
    padx=5,
    pady=5
)


ttk.Label(
    frame_general,
    text="¿Los síntomas empeoran?"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

ttk.Combobox(
    frame_general,
    textvariable=empeorando_var,
    values=["Sí", "No"],
    state="readonly",
    width=27
).grid(
    row=2,
    column=1,
    padx=5,
    pady=5
)


#Boton para cargar sintomas 

boton_sintomas = ttk.Button(
    panel_izquierdo,
    text="Cargar síntomas según edad",
    command=lambda: cargar_sintomas()
)

boton_sintomas.pack(
    padx=10,
    pady=8,
    fill="x"
)




panel_derecho = ttk.Frame(
    contenedor,
    relief="solid",
    borderwidth=1
)

panel_derecho.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(6, 0)
)

panel_derecho.columnconfigure(0, weight=1)
panel_derecho.rowconfigure(1, weight=1)



ttk.Label(
    panel_derecho,
    text="Síntomas",
    font=("Arial", 14, "bold")
).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=8
)




canvas = tk.Canvas(
    panel_derecho,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    panel_derecho,
    orient="vertical",
    command=canvas.yview
)

frame_sintomas = ttk.Frame(canvas)

ventana_canvas = canvas.create_window(
    (0, 0),
    window=frame_sintomas,
    anchor="nw"
)


def actualizar_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


frame_sintomas.bind(
    "<Configure>",
    actualizar_scroll
)


def ajustar_ancho(event):

    canvas.itemconfig(
        ventana_canvas,
        width=event.width
    )


canvas.bind(
    "<Configure>",
    ajustar_ancho
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.grid(
    row=1,
    column=0,
    sticky="nsew"
)

scrollbar.grid(
    row=1,
    column=1,
    sticky="ns"
)




def scroll_mouse(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind(
    "<MouseWheel>",
    scroll_mouse
)




def crear_sintoma(nombre, texto):

    variable = tk.StringVar(value="No")

    variables_sintomas[nombre] = variable

    frame = ttk.Frame(frame_sintomas)

    frame.pack(
        fill="x",
        padx=10,
        pady=5
    )

    ttk.Label(
        frame,
        text=texto,
        wraplength=280
    ).pack(
        side="left",
        fill="x",
        expand=True
    )

    ttk.Radiobutton(
        frame,
        text="Sí",
        value="Sí",
        variable=variable
    ).pack(
        side="left",
        padx=5
    )

    ttk.Radiobutton(
        frame,
        text="No",
        value="No",
        variable=variable
    ).pack(
        side="left",
        padx=5
    )



def limpiar_sintomas():

    for widget in frame_sintomas.winfo_children():
        widget.destroy()

    variables_sintomas.clear()

    canvas.yview_moveto(0)


# Cargar sintomas segun la edad 

def cargar_sintomas():

    limpiar_sintomas()

    try:

        edad = int(edad_var.get())

        if edad < 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Error",
            "Ingrese una edad válida."
        )

        return


    # ======================================================
    # NIÑOS
    # ======================================================

    if edad <= 10:

        sintomas = [

            ("dolor_garganta", "¿Tiene dolor de garganta?"),
            ("dificultad_tragar", "¿Tiene dificultad para tragar?"),
            ("fiebre", "¿Tiene fiebre?"),
            ("dolor_oido", "¿Tiene dolor de oído?"),
            ("irritabilidad", "¿Está más irritable de lo normal?"),
            ("dolor_abdominal", "¿Tiene dolor abdominal?"),
            ("nauseas", "¿Tiene náuseas?"),
            ("vomito", "¿Ha presentado vómito?"),
            ("cansancio", "¿Presenta mucho cansancio?"),
            ("escalofrios", "¿Tiene escalofríos?"),
            ("escurrimiento_nasal", "¿Tiene escurrimiento nasal?"),
            ("estornudos", "¿Tiene estornudos frecuentes?"),
            ("tos", "¿Tiene tos?")
        ]


    # ======================================================
    # ADOLESCENTES
    # ======================================================

    elif edad <= 17:

        sintomas = [

            ("granitos", "¿Tiene granitos o brotes en la piel?"),
            ("piel_grasa", "¿Tiene la piel muy grasa?"),
            ("dolor_cabeza", "¿Tiene dolor de cabeza?"),
            ("sensibilidad_luz", "¿La luz le molesta?"),
            ("dolor_estomago", "¿Tiene dolor de estómago?"),
            ("ardor_estomago", "¿Tiene ardor en el estómago?"),
            ("dolor_garganta", "¿Tiene dolor de garganta?"),
            ("dificultad_tragar", "¿Tiene dificultad para tragar?"),
            ("ojos_rojos", "¿Tiene los ojos rojos?"),
            ("lagrimeo", "¿Tiene lagrimeo frecuente?")
        ]


    # ======================================================
    # ADULTOS JÓVENES
    # ======================================================

    elif edad <= 39:

        sintomas = [

            ("estornudos", "¿Tiene estornudos frecuentes?"),
            ("comezon_nariz", "¿Tiene comezón en la nariz?"),
            ("dolor_cabeza", "¿Tiene dolor de cabeza?"),
            ("cansancio", "¿Tiene cansancio?"),
            ("diarrea", "¿Tiene diarrea?"),
            ("dolor_abdominal", "¿Tiene dolor abdominal?"),
            ("dificultad_dormir", "¿Tiene dificultad para dormir?"),
            ("dolor_muscular", "¿Tiene dolor muscular?"),
            ("rigidez", "¿Tiene rigidez muscular?")
        ]


    # ======================================================
    # ADULTOS
    # ======================================================

    elif edad <= 59:

        sintomas = [

            ("dolor_cabeza", "¿Tiene dolor de cabeza?"),
            ("mareo", "¿Tiene mareo?"),
            ("mucha_sed", "¿Tiene mucha sed?"),
            ("orinar_frecuente", "¿Orina con mucha frecuencia?"),
            ("acidez", "¿Tiene acidez?"),
            ("dolor_estomago", "¿Tiene dolor de estómago?"),
            ("ardor_orinar", "¿Tiene ardor al orinar?"),
            ("dolor_abdominal", "¿Tiene dolor abdominal?"),
            ("cansancio", "¿Tiene cansancio?")
        ]


    # ======================================================
    # ADULTOS MAYORES
    # ======================================================

    else:

        sintomas = [

            ("dolor_cabeza", "¿Tiene dolor de cabeza?"),
            ("mareo", "¿Tiene mareo?"),
            ("mucha_sed", "¿Tiene mucha sed?"),
            ("orinar_frecuente", "¿Orina con mucha frecuencia?"),
            ("dolor_articulaciones", "¿Tiene dolor en las articulaciones?"),
            ("rigidez", "¿Tiene rigidez en las articulaciones?"),
            ("dolor_huesos", "¿Tiene dolor en los huesos?"),
            ("debilidad", "¿Presenta debilidad?"),
            ("fiebre", "¿Tiene fiebre?"),
            ("tos", "¿Tiene tos?")
        ]


    for nombre, texto in sintomas:

        crear_sintoma(
            nombre,
            texto
        )


# ==========================================================
# OBTENER VALOR DE SÍNTOMA
# ==========================================================

def sintoma(nombre):

    if nombre in variables_sintomas:
        return variables_sintomas[nombre].get() == "Sí"

    return False


# ==========================================================
# PEDIR PRESIÓN
# ==========================================================

def pedir_numero(titulo, mensaje):

    ventana_presion = tk.Toplevel(ventana)

    ventana_presion.title(titulo)
    ventana_presion.geometry("350x170")
    ventana_presion.resizable(False, False)

    ventana_presion.transient(ventana)
    ventana_presion.grab_set()

    valor = tk.StringVar()

    ttk.Label(
        ventana_presion,
        text=mensaje,
        font=("Arial", 11)
    ).pack(
        pady=15
    )

    entrada = ttk.Entry(
        ventana_presion,
        textvariable=valor,
        width=20
    )

    entrada.pack()

    entrada.focus()

    resultado = [None]


    def aceptar():

        try:

            numero = int(valor.get())

            if numero <= 0:
                raise ValueError

            resultado[0] = numero

            ventana_presion.destroy()

        except ValueError:

            messagebox.showerror(
                "Error",
                "Ingrese un valor numérico válido.",
                parent=ventana_presion
            )


    ttk.Button(
        ventana_presion,
        text="Aceptar",
        command=aceptar
    ).pack(
        pady=15
    )

    ventana.wait_window(
        ventana_presion
    )

    return resultado[0]


# ==========================================================
# MOSTRAR RESULTADO
# ==========================================================

def mostrar_resultado(texto):

    ventana_resultado = tk.Toplevel(ventana)

    ventana_resultado.title(
        "Resultado del diagnóstico"
    )

    # VENTANA MÁS PEQUEÑA
    ventana_resultado.geometry(
        "650x500"
    )

    ventana_resultado.minsize(
        550,
        400
    )

    ventana_resultado.resizable(
        True,
        True
    )


    # ------------------------------------------------------
    # MARCO DEL RESULTADO
    # ------------------------------------------------------

    marco_resultado = ttk.Frame(
        ventana_resultado
    )

    marco_resultado.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )


    # ------------------------------------------------------
    # CAJA DE TEXTO
    # ------------------------------------------------------

    texto_resultado = tk.Text(
        marco_resultado,
        wrap="word",
        font=("Arial", 10),
        padx=10,
        pady=10
    )


    # ------------------------------------------------------
    # BARRA DE DESPLAZAMIENTO
    # ------------------------------------------------------

    scrollbar_resultado = ttk.Scrollbar(
        marco_resultado,
        orient="vertical",
        command=texto_resultado.yview
    )


    texto_resultado.configure(
        yscrollcommand=scrollbar_resultado.set
    )


    texto_resultado.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar_resultado.pack(
        side="right",
        fill="y"
    )


    # ------------------------------------------------------
    # INSERTAR RESULTADO
    # ------------------------------------------------------

    texto_resultado.insert(
        "1.0",
        texto
    )


    texto_resultado.configure(
        state="disabled"
    )


    # ------------------------------------------------------
    # BOTÓN CERRAR
    # ------------------------------------------------------

    ttk.Button(
        ventana_resultado,
        text="Cerrar",
        command=ventana_resultado.destroy
    ).pack(
        pady=(0, 12)
    )


# ==========================================================
# DIAGNÓSTICO
# ==========================================================

def diagnosticar():

    # ------------------------------------------------------
    # VALIDAR DATOS
    # ------------------------------------------------------

    nombre = nombre_var.get().strip()

    if not nombre:

        messagebox.showerror(
            "Error",
            "Ingrese el nombre del paciente."
        )

        return


    try:

        edad = int(edad_var.get())
        peso = float(peso_var.get())
        estatura = float(estatura_var.get())
        tiempo_sintomas = int(tiempo_var.get())
        intensidad = int(intensidad_var.get())

        if edad < 0:
            raise ValueError

        if peso <= 0:
            raise ValueError

        if estatura <= 0:
            raise ValueError

        if tiempo_sintomas < 0:
            raise ValueError

        if intensidad < 1 or intensidad > 10:
            raise ValueError


    except ValueError:

        messagebox.showerror(
            "Error",
            "Verifique que todos los datos numéricos sean válidos."
        )

        return


    sexo = sexo_var.get()


    if not sexo:

        messagebox.showerror(
            "Error",
            "Seleccione el sexo."
        )

        return


    if not variables_sintomas:

        messagebox.showwarning(
            "Síntomas",
            "Primero presione 'Cargar síntomas según edad'."
        )

        return


    # ------------------------------------------------------
    # FECHA Y HORA
    # ------------------------------------------------------

    fecha_hora = datetime.now()

    fecha = fecha_hora.strftime("%d/%m/%Y")
    hora = fecha_hora.strftime("%H:%M:%S")


    # ------------------------------------------------------
    # RANGO DE EDAD
    # ------------------------------------------------------

    if edad <= 10:

        rango = "Niño"

    elif edad <= 17:

        rango = "Adolescente"

    elif edad <= 39:

        rango = "Adulto joven"

    elif edad <= 59:

        rango = "Adulto"

    else:

        rango = "Adulto mayor"


    # ------------------------------------------------------
    # GRAVEDAD
    # ------------------------------------------------------

    if intensidad <= 3:

        gravedad = "Leve"

    elif intensidad <= 6:

        gravedad = "Moderada"

    else:

        gravedad = "Severa"


    # ------------------------------------------------------
    # EVOLUCIÓN
    # ------------------------------------------------------

    if tiempo_sintomas <= 2:

        evolucion = "Inicio de síntomas"

    elif tiempo_sintomas <= 7:

        evolucion = "Síntomas en evolución"

    else:

        evolucion = "Síntomas persistentes"


    # ------------------------------------------------------
    # VARIABLES INICIALES
    # ------------------------------------------------------

    diagnostico = "Posible malestar general"

    recomendacion = (
        "Mantener hidratación, descansar y observar la evolución "
        "de los síntomas."
    )


    # ======================================================
    # NIÑOS
    # ======================================================

    if edad <= 10:

        dolor_garganta = sintoma("dolor_garganta")
        dificultad_tragar = sintoma("dificultad_tragar")
        fiebre = sintoma("fiebre")
        dolor_oido = sintoma("dolor_oido")
        irritabilidad = sintoma("irritabilidad")
        dolor_abdominal = sintoma("dolor_abdominal")
        nauseas = sintoma("nauseas")
        vomito = sintoma("vomito")
        cansancio = sintoma("cansancio")
        escalofrios = sintoma("escalofrios")
        escurrimiento_nasal = sintoma("escurrimiento_nasal")
        estornudos = sintoma("estornudos")
        tos = sintoma("tos")


        if dolor_garganta and dificultad_tragar and fiebre:

            diagnostico = "Posible infección de garganta"

            recomendacion = (
                "Mantener una adecuada hidratación, ofrecer líquidos "
                "y alimentos suaves. Evitar alimentos muy irritantes "
                "y vigilar la fiebre y la dificultad para tragar."
            )


        elif dolor_oido and fiebre and irritabilidad:

            diagnostico = "Posible infección de oído"

            recomendacion = (
                "Evitar introducir objetos o líquidos en el oído. "
                "Mantener reposo, vigilar la temperatura y observar "
                "si el dolor aumenta."
            )


        elif dolor_abdominal and nauseas and vomito:

            diagnostico = "Posible problema gastrointestinal"

            recomendacion = (
                "Mantener hidratación mediante pequeños sorbos de líquidos "
                "y ofrecer alimentos ligeros cuando sean tolerados. "
                "Vigilar la frecuencia del vómito y el dolor abdominal."
            )


        elif fiebre and cansancio and escalofrios:

            diagnostico = "Posible cuadro infeccioso con fiebre"

            recomendacion = (
                "Controlar periódicamente la temperatura, mantener hidratación "
                "y proporcionar reposo. Observar cambios en el estado general "
                "del niño."
            )


        elif escurrimiento_nasal and estornudos and tos:

            diagnostico = "Posible resfriado común"

            recomendacion = (
                "Mantener buena hidratación, permitir suficiente descanso "
                "y mantener limpio el ambiente. Vigilar la temperatura "
                "y la evolución de la tos."
            )


        elif tos or escurrimiento_nasal or estornudos:

            diagnostico = "Posible cuadro respiratorio"

            recomendacion = (
                "Mantener hidratación y reposo. Evitar humo, polvo y otros "
                "irritantes del ambiente. Vigilar la respiración y la aparición "
                "de fiebre."
            )


        elif dolor_abdominal or nauseas or vomito:

            diagnostico = "Posible malestar gastrointestinal"

            recomendacion = (
                "Ofrecer líquidos en pequeñas cantidades y evitar comidas "
                "muy pesadas o irritantes. Observar si aparecen vómitos "
                "frecuentes, fiebre o aumento del dolor."
            )


        elif dolor_oido:

            diagnostico = "Posible afección del oído"

            recomendacion = (
                "Evitar manipular el oído y vigilar la intensidad del dolor. "
                "Mantener reposo y observar si aparece fiebre o secreción."
            )


        elif dolor_garganta:

            diagnostico = "Posible irritación o infección de garganta"

            recomendacion = (
                "Mantener hidratación, ofrecer líquidos y evitar alimentos "
                "muy irritantes. Vigilar la aparición de fiebre o dificultad "
                "para tragar."
            )


        else:

            diagnostico = "Posible malestar general infantil"

            recomendacion = (
                "Mantener una adecuada hidratación, permitir suficiente descanso "
                "y observar cualquier cambio en los síntomas."
            )


    # ======================================================
    # ADOLESCENTES
    # ======================================================

    elif edad <= 17:

        granitos = sintoma("granitos")
        piel_grasa = sintoma("piel_grasa")
        dolor_cabeza = sintoma("dolor_cabeza")
        sensibilidad_luz = sintoma("sensibilidad_luz")
        dolor_estomago = sintoma("dolor_estomago")
        ardor_estomago = sintoma("ardor_estomago")
        dolor_garganta = sintoma("dolor_garganta")
        dificultad_tragar = sintoma("dificultad_tragar")
        ojos_rojos = sintoma("ojos_rojos")
        lagrimeo = sintoma("lagrimeo")


        if granitos and piel_grasa:

            diagnostico = "Posible acné"

            recomendacion = (
                "Lavar la piel suavemente, evitar exprimir o manipular "
                "los granitos y mantener limpia la zona afectada."
            )


        elif dolor_cabeza and sensibilidad_luz:

            diagnostico = "Posible migraña"

            recomendacion = (
                "Descansar en un lugar tranquilo, con poca luz y poco ruido. "
                "Mantener hidratación y reducir temporalmente el uso de pantallas."
            )


        elif dolor_estomago and ardor_estomago:

            diagnostico = "Posible gastritis o irritación estomacal"

            recomendacion = (
                "Preferir comidas ligeras, evitar alimentos muy irritantes, "
                "grasosos o picantes y mantener horarios regulares de comida."
            )


        elif dolor_garganta and dificultad_tragar:

            diagnostico = "Posible faringitis"

            recomendacion = (
                "Mantener hidratación, consumir líquidos y evitar alimentos "
                "que irriten la garganta. Vigilar la aparición de fiebre."
            )


        elif ojos_rojos and lagrimeo:

            diagnostico = "Posible irritación o conjuntivitis"

            recomendacion = (
                "Evitar frotarse los ojos, lavarse las manos con frecuencia "
                "y evitar compartir toallas."
            )


        elif granitos or piel_grasa:

            diagnostico = "Posible problema dermatológico"

            recomendacion = (
                "Mantener una higiene suave de la piel, evitar manipular "
                "los brotes y observar su evolución."
            )


        elif dolor_cabeza:

            diagnostico = "Posible cefalea"

            recomendacion = (
                "Descansar, mantener hidratación y reducir temporalmente "
                "el uso de pantallas."
            )


        elif dolor_estomago or ardor_estomago:

            diagnostico = "Posible malestar digestivo"

            recomendacion = (
                "Consumir alimentos ligeros, evitar irritantes y mantener "
                "una adecuada hidratación."
            )


        elif ojos_rojos or lagrimeo:

            diagnostico = "Posible irritación ocular"

            recomendacion = (
                "Evitar frotarse los ojos, descansar la vista y reducir "
                "la exposición prolongada a pantallas."
            )


        elif dolor_garganta:

            diagnostico = "Posible irritación de garganta"

            recomendacion = (
                "Mantener hidratación, consumir líquidos y evitar humo "
                "u otros irritantes."
            )


        else:

            diagnostico = "Posible malestar general en adolescente"

            recomendacion = (
                "Mantener hidratación, descansar adecuadamente y observar "
                "la evolución de los síntomas."
            )


    # ======================================================
    # ADULTOS JÓVENES
    # ======================================================

    elif edad <= 39:

        estornudos = sintoma("estornudos")
        comezon_nariz = sintoma("comezon_nariz")
        dolor_cabeza = sintoma("dolor_cabeza")
        cansancio = sintoma("cansancio")
        diarrea = sintoma("diarrea")
        dolor_abdominal = sintoma("dolor_abdominal")
        dificultad_dormir = sintoma("dificultad_dormir")
        dolor_muscular = sintoma("dolor_muscular")
        rigidez = sintoma("rigidez")


        if estornudos and comezon_nariz:

            diagnostico = "Posible alergia respiratoria"

            recomendacion = (
                "Identificar y evitar posibles desencadenantes como polvo, "
                "humo, perfumes o cambios ambientales."
            )


        elif dolor_cabeza and cansancio:

            diagnostico = "Posible cefalea asociada a cansancio"

            recomendacion = (
                "Priorizar el descanso, mantener hidratación y realizar pausas "
                "si se trabaja frente a pantallas."
            )


        elif diarrea and dolor_abdominal:

            diagnostico = "Posible problema gastrointestinal"

            recomendacion = (
                "Mantener una adecuada hidratación, consumir alimentos ligeros "
                "y evitar comidas muy grasosas o irritantes."
            )


        elif dificultad_dormir and cansancio:

            diagnostico = "Posible alteración del sueño"

            recomendacion = (
                "Establecer horarios regulares para dormir, reducir pantallas "
                "antes de acostarse y evitar bebidas estimulantes por la noche."
            )


        elif dolor_muscular and rigidez:

            diagnostico = "Posible problema muscular"

            recomendacion = (
                "Reducir temporalmente los esfuerzos físicos, permitir descanso "
                "a los músculos y realizar movimientos suaves."
            )


        elif estornudos or comezon_nariz:

            diagnostico = "Posible irritación o alergia respiratoria"

            recomendacion = (
                "Evitar polvo, humo y otros posibles desencadenantes."
            )


        elif dolor_cabeza:

            diagnostico = "Posible cefalea"

            recomendacion = (
                "Descansar, mantener hidratación y reducir temporalmente "
                "la exposición a pantallas."
            )


        elif diarrea or dolor_abdominal:

            diagnostico = "Posible malestar gastrointestinal"

            recomendacion = (
                "Mantener hidratación, preferir alimentos ligeros y evitar "
                "alimentos irritantes o muy grasosos."
            )


        elif dificultad_dormir:

            diagnostico = "Posible alteración del sueño"

            recomendacion = (
                "Mantener horarios regulares de descanso y disminuir el uso "
                "de pantallas antes de dormir."
            )


        elif dolor_muscular or rigidez:

            diagnostico = "Posible molestia muscular"

            recomendacion = (
                "Evitar sobrecargas físicas y permitir descanso muscular."
            )


        else:

            diagnostico = "Posible malestar general en adulto joven"

            recomendacion = (
                "Mantener hidratación, descansar adecuadamente y observar "
                "la evolución de los síntomas."
            )


    # ======================================================
    # ADULTOS
    # ======================================================

    elif edad <= 59:

        presion_sistolica = pedir_numero(
            "Presión arterial",
            "Ingrese el primer valor de la presión:"
        )

        if presion_sistolica is None:
            return


        presion_diastolica = pedir_numero(
            "Presión arterial",
            "Ingrese el segundo valor de la presión:"
        )

        if presion_diastolica is None:
            return


        dolor_cabeza = sintoma("dolor_cabeza")
        mareo = sintoma("mareo")
        mucha_sed = sintoma("mucha_sed")
        orinar_frecuente = sintoma("orinar_frecuente")
        acidez = sintoma("acidez")
        dolor_estomago = sintoma("dolor_estomago")
        ardor_orinar = sintoma("ardor_orinar")
        dolor_abdominal = sintoma("dolor_abdominal")
        cansancio = sintoma("cansancio")


        if presion_sistolica >= 140 or presion_diastolica >= 90:

            if dolor_cabeza and mareo:

                diagnostico = "Posible presión arterial elevada con síntomas"

                recomendacion = (
                    "Permanecer en reposo y repetir la medición de presión "
                    "correctamente. Registrar el resultado y evitar actividad "
                    "física intensa mientras persistan los síntomas."
                )

            else:

                diagnostico = "Posible presión arterial elevada"

                recomendacion = (
                    "Permanecer en reposo y repetir la medición después de "
                    "unos minutos. Registrar los valores obtenidos."
                )


        elif mucha_sed and orinar_frecuente:

            diagnostico = "Posible alteración de glucosa"

            recomendacion = (
                "Mantener una alimentación equilibrada, evitar un consumo "
                "excesivo de bebidas azucaradas y considerar una medición "
                "de glucosa."
            )


        elif acidez and dolor_estomago:

            diagnostico = "Posible gastritis o reflujo"

            recomendacion = (
                "Realizar comidas ligeras, evitar alimentos muy picantes, "
                "grasosos o irritantes y evitar acostarse inmediatamente "
                "después de comer."
            )


        elif ardor_orinar and dolor_abdominal:

            diagnostico = "Posible infección urinaria"

            recomendacion = (
                "Mantener una adecuada hidratación y observar la frecuencia "
                "del ardor y el dolor abdominal."
            )


        elif cansancio and mareo:

            diagnostico = "Posible cuadro de cansancio y mareo"

            recomendacion = (
                "Descansar, mantener hidratación y evitar levantarse "
                "rápidamente mientras continúe el mareo."
            )


        elif mucha_sed or orinar_frecuente:

            diagnostico = "Posible alteración metabólica"

            recomendacion = (
                "Mantener hidratación, evitar el exceso de bebidas azucaradas "
                "y registrar la frecuencia de la sed o la necesidad de orinar."
            )


        elif acidez or dolor_estomago:

            diagnostico = "Posible problema digestivo"

            recomendacion = (
                "Preferir alimentos ligeros, reducir comidas muy grasosas, "
                "picantes o irritantes."
            )


        elif ardor_orinar:

            diagnostico = "Posible problema urinario"

            recomendacion = (
                "Mantener una adecuada hidratación y observar cualquier "
                "cambio en la orina."
            )


        elif dolor_cabeza:

            diagnostico = "Posible cefalea"

            recomendacion = (
                "Descansar en un ambiente tranquilo, mantener hidratación "
                "y observar la duración e intensidad del dolor."
            )


        elif cansancio:

            diagnostico = "Posible cuadro de fatiga"

            recomendacion = (
                "Priorizar el descanso, mantener horarios adecuados de sueño "
                "e hidratarse."
            )


        else:

            diagnostico = "Posible malestar general en adulto"

            recomendacion = (
                "Mantener hidratación, descansar adecuadamente y observar "
                "la evolución de cualquier síntoma."
            )


    # ======================================================
    # ADULTOS MAYORES
    # ======================================================

    else:

        presion_sistolica = pedir_numero(
            "Presión arterial",
            "Ingrese el primer valor de la presión:"
        )

        if presion_sistolica is None:
            return


        presion_diastolica = pedir_numero(
            "Presión arterial",
            "Ingrese el segundo valor de la presión:"
        )

        if presion_diastolica is None:
            return


        dolor_cabeza = sintoma("dolor_cabeza")
        mareo = sintoma("mareo")
        mucha_sed = sintoma("mucha_sed")
        orinar_frecuente = sintoma("orinar_frecuente")
        dolor_articulaciones = sintoma("dolor_articulaciones")
        rigidez = sintoma("rigidez")
        dolor_huesos = sintoma("dolor_huesos")
        debilidad = sintoma("debilidad")
        fiebre = sintoma("fiebre")
        tos = sintoma("tos")


        if presion_sistolica >= 140 or presion_diastolica >= 90:

            if dolor_cabeza and mareo:

                diagnostico = "Posible presión arterial elevada con síntomas"

                recomendacion = (
                    "Permanecer en reposo y repetir la medición después de "
                    "unos minutos. Registrar los valores obtenidos."
                )

            else:

                diagnostico = "Posible presión arterial elevada"

                recomendacion = (
                    "Permanecer en reposo y repetir la medición correctamente. "
                    "Registrar los valores para comparar posteriormente."
                )


        elif mucha_sed and orinar_frecuente:

            diagnostico = "Posible alteración de glucosa"

            recomendacion = (
                "Mantener hidratación, evitar el exceso de bebidas azucaradas "
                "y considerar una medición de glucosa."
            )


        elif dolor_articulaciones and rigidez:

            diagnostico = "Posible problema articular"

            recomendacion = (
                "Evitar sobrecargar las articulaciones, realizar movimientos "
                "suaves y mantener periodos adecuados de descanso."
            )


        elif dolor_huesos and debilidad:

            diagnostico = "Posible problema musculoesquelético"

            recomendacion = (
                "Evitar esfuerzos físicos excesivos, mantener periodos de "
                "descanso y realizar movimientos suaves."
            )


        elif fiebre and tos:

            diagnostico = "Posible infección respiratoria"

            recomendacion = (
                "Mantener hidratación, descansar y controlar periódicamente "
                "la temperatura. Vigilar cualquier dificultad para respirar."
            )


        elif dolor_articulaciones or rigidez:

            diagnostico = "Posible problema articular"

            recomendacion = (
                "Evitar movimientos que aumenten el dolor y permitir descanso "
                "a las articulaciones."
            )


        elif dolor_huesos or debilidad:

            diagnostico = "Posible problema musculoesquelético"

            recomendacion = (
                "Reducir los esfuerzos físicos y permitir descanso."
            )


        elif fiebre or tos:

            diagnostico = "Posible cuadro respiratorio"

            recomendacion = (
                "Mantener hidratación y reposo, controlar la temperatura "
                "y observar la evolución de la tos."
            )


        elif mucha_sed or orinar_frecuente:

            diagnostico = "Posible alteración metabólica"

            recomendacion = (
                "Mantener hidratación, reducir bebidas azucaradas y registrar "
                "la frecuencia de la sed y la necesidad de orinar."
            )


        elif dolor_cabeza or mareo:

            diagnostico = "Posible cuadro de cefalea o mareo"

            recomendacion = (
                "Descansar, mantener hidratación y levantarse lentamente "
                "para evitar cambios bruscos de posición."
            )


        else:

            diagnostico = "Posible malestar general en adulto mayor"

            recomendacion = (
                "Mantener hidratación, descansar adecuadamente y observar "
                "cualquier cambio en el estado general."
            )


    #Recomendaciones
    if gravedad == "Leve":

        recomendacion += (
            " La intensidad registrada es leve; continuar con las medidas "
            "anteriores y observar si los síntomas disminuyen."
        )


    elif gravedad == "Moderada":

        recomendacion += (
            " La intensidad registrada es moderada; se recomienda reducir "
            "las actividades que puedan aumentar las molestias y vigilar "
            "la evolución."
        )


    else:

        recomendacion += (
            " La intensidad registrada es severa; se recomienda suspender "
            "actividades que puedan empeorar las molestias y buscar atención "
            "sanitaria si la intensidad continúa."
        )


    #Evolucion

    if evolucion == "Síntomas persistentes":

        recomendacion += (
            " Los síntomas llevan más de una semana, por lo que es importante "
            "dar seguimiento a su evolución y buscar atención sanitaria si "
            "no presentan mejoría."
        )


    #Alertas

    alerta = (
        "No se detectaron señales de alerta según los datos ingresados."
    )


    if intensidad >= 9:

        alerta = (
            "ATENCIÓN: La intensidad de los síntomas es muy alta. "
            "Se recomienda buscar atención sanitaria de manera prioritaria."
        )


    elif empeorando_var.get() == "Sí":

        alerta = (
            "ATENCIÓN: Los síntomas están empeorando. "
            "Se recomienda buscar atención sanitaria si continúan aumentando."
        )


    #Resultado final 

    resultado = ""

    resultado += "====================================================\n"
    resultado += "                 RESULTADO\n"
    resultado += "====================================================\n\n"

    resultado += "--- DATOS DEL PACIENTE ---\n\n"

    resultado += f"Nombre: {nombre}\n"
    resultado += f"Edad: {edad}\n"
    resultado += f"Sexo: {sexo}\n"
    resultado += f"Peso: {peso} kg\n"
    resultado += f"Estatura: {estatura} m\n"
    resultado += f"Rango de edad: {rango}\n\n"

    resultado += "--- EVALUACIÓN ---\n\n"

    resultado += f"Tiempo con síntomas: {tiempo_sintomas} días\n"
    resultado += f"Intensidad: {intensidad}/10\n"
    resultado += f"Gravedad: {gravedad}\n"
    resultado += f"Evolución: {evolucion}\n"
    resultado += f"¿Está empeorando?: {empeorando_var.get()}\n\n"

    resultado += "--- POSIBLE DIAGNÓSTICO ---\n\n"

    resultado += diagnostico + "\n\n"

    resultado += "--- RECOMENDACIÓN ---\n\n"

    resultado += recomendacion + "\n\n"

    resultado += "--- ALERTA ---\n\n"

    resultado += alerta + "\n\n"

    resultado += "--- FECHA Y HORA DE LA CONSULTA ---\n\n"

    resultado += f"Fecha: {fecha}\n"
    resultado += f"Hora: {hora}\n\n"

    


    mostrar_resultado(resultado)


#Borrar todos los datos ingresados 

def borrar_datos():

    nombre_var.set("")
    edad_var.set("")
    sexo_var.set("")
    peso_var.set("")
    estatura_var.set("")

    tiempo_var.set("")
    intensidad_var.set("")
    empeorando_var.set("No")

    limpiar_sintomas()




frame_botones = ttk.Frame(ventana)

frame_botones.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=15,
    pady=(5, 10)
)

frame_botones.columnconfigure(0, weight=1)
frame_botones.columnconfigure(1, weight=1)
frame_botones.columnconfigure(2, weight=1)


# Boton para diagnosticar 

boton_diagnosticar = ttk.Button(
    frame_botones,
    text="DIAGNOSTICAR",
    command=diagnosticar
)

boton_diagnosticar.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=5
)


#Boton para borrar datos

boton_borrar = ttk.Button(
    frame_botones,
    text="BORRAR DATOS",
    command=borrar_datos
)

boton_borrar.grid(
    row=0,
    column=1,
    sticky="ew",
    padx=5
)


#Boton salir

boton_salir = ttk.Button(
    frame_botones,
    text="SALIR",
    command=ventana.destroy
)

boton_salir.grid(
    row=0,
    column=2,
    sticky="ew",
    padx=5
)



ventana.mainloop()