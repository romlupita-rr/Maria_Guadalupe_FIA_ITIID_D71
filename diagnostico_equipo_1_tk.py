
import tkinter as tk
from tkinter import messagebox


# ==========================================
# FUNCIÓN PARA BORRAR
# ==========================================

def borrar_diagnostico():

    # Borrar datos de los campos
    entrada_modelo.delete(0, tk.END)
    entrada_uso.delete(0, tk.END)
    entrada_ram.delete(0, tk.END)
    entrada_tiempo.delete(0, tk.END)
    entrada_procesador.delete(0, tk.END)

    # Regresar opciones a Sí
    electricidad_var.set("s")
    enciende_var.set("s")
    imagen_var.set("s")

    # Borrar resultado
    resultado.delete("1.0", tk.END)


# ==========================================
# FUNCIÓN PARA DIAGNOSTICAR
# ==========================================

def diagnosticar():

    modelo = entrada_modelo.get()

    try:
        uso = int(entrada_uso.get())
        ram = int(entrada_ram.get())
        tiempo = int(entrada_tiempo.get())

    except ValueError:
        messagebox.showerror(
            "Error",
            "Años de uso, RAM y tiempo de encendido deben ser números."
        )
        return

    procesador = entrada_procesador.get()

    electricidad = electricidad_var.get() == "s"
    enciende = enciende_var.get() == "s"
    imagen = imagen_var.get() == "s"

    # Variables para el diagnóstico
    riesgo = 0
    problemas = []
    recomendaciones = []

    # ==========================================
    # REVISAR ELECTRICIDAD
    # ==========================================

    if not electricidad:

        riesgo += 5

        problemas.append("No recibe electricidad.")

        recomendaciones.append(
            "Revisar el cable, enchufe o alimentación eléctrica."
        )

    elif not enciende:

        riesgo += 5

        problemas.append("El equipo no enciende.")

        recomendaciones.append(
            "Revisar la fuente de poder o el cargador."
        )

    elif not imagen:

        riesgo += 4

        problemas.append(
            "El equipo enciende pero no muestra imagen."
        )

        recomendaciones.append(
            "Revisar monitor, RAM y cable de video."
        )

    # ==========================================
    # REVISAR RAM
    # ==========================================

    if ram < 4:

        riesgo += 4

        problemas.append("RAM muy baja.")

        recomendaciones.append(
            "Aumentar la RAM a 8 GB o más."
        )

    elif ram < 8:

        riesgo += 2

        problemas.append("RAM limitada.")

        recomendaciones.append(
            "Considerar aumentar la RAM."
        )

    # ==========================================
    # REVISAR TIEMPO DE ENCENDIDO
    # ==========================================

    if tiempo > 120:

        riesgo += 4

        problemas.append("Tiempo de arranque muy alto.")

        recomendaciones.append(
            "Revisar programas de inicio y almacenamiento."
        )

    elif tiempo > 60:

        riesgo += 2

        problemas.append("Tiempo de arranque elevado.")

        recomendaciones.append(
            "Realizar mantenimiento y revisar programas de inicio."
        )

    # ==========================================
    # REVISAR AÑOS DE USO
    # ==========================================

    if uso >= 8:

        riesgo += 4

        problemas.append("Equipo con muchos años de uso.")

        recomendaciones.append(
            "Considerar actualizar o reemplazar algunos componentes."
        )

    elif uso >= 5:

        riesgo += 2

        problemas.append("Equipo con varios años de uso.")

        recomendaciones.append(
            "Realizar mantenimiento preventivo."
        )

    # ==========================================
    # NIVEL DE RIESGO
    # ==========================================

    if riesgo >= 10:

        nivel = "CRÍTICO"

    elif riesgo >= 6:

        nivel = "ALTO"

    elif riesgo >= 3:

        nivel = "MEDIO"

    else:

        nivel = "BAJO"

    # ==========================================
    # RESULTADO
    # ==========================================

    texto = ""

    texto += "===== RESULTADO DEL ANÁLISIS =====\n"

    texto += "Modelo: " + modelo + "\n"

    texto += "Procesador: " + procesador + "\n"

    texto += "RAM: " + str(ram) + " GB\n"

    texto += "Años de uso: " + str(uso) + "\n"

    texto += "Tiempo de encendido: " + str(tiempo) + " segundos\n"

    texto += "\nNivel de riesgo: " + nivel + "\n"

    texto += "Puntuación: " + str(riesgo) + "\n"

    texto += "\n===== PROBLEMAS DETECTADOS =====\n"

    if len(problemas) == 0:

        texto += "No se detectaron problemas importantes.\n"

    else:

        for problema in problemas:

            texto += "- " + problema + "\n"

    texto += "\n===== RECOMENDACIONES =====\n"

    if len(recomendaciones) == 0:

        texto += "El equipo tiene un funcionamiento adecuado.\n"

    else:

        for recomendacion in recomendaciones:

            texto += "- " + recomendacion + "\n"

    texto += "\n===== DIAGNÓSTICO FINAL =====\n"

    if nivel == "CRÍTICO":

        texto += "El equipo presenta varios problemas y necesita atención."

    elif nivel == "ALTO":

        texto += "El equipo presenta problemas importantes y se recomienda mantenimiento."

    elif nivel == "MEDIO":

        texto += "El equipo funciona, pero presenta algunos aspectos que pueden mejorarse."

    else:

        texto += "El equipo presenta un funcionamiento adecuado."

    # Mostrar resultado
    resultado.delete("1.0", tk.END)

    resultado.insert(tk.END, texto)


# ==========================================
# VENTANA
# ==========================================

ventana = tk.Tk()

ventana.title("Diagnóstico inteligente de equipo")

ventana.geometry("650x800")


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    ventana,
    text="DIAGNÓSTICO INTELIGENTE DE EQUIPO",
    font=("Arial", 15, "bold")
)

titulo.pack(pady=8)


# ==========================================
# MODELO
# ==========================================

tk.Label(
    ventana,
    text="Modelo del equipo:"
).pack()

entrada_modelo = tk.Entry(
    ventana,
    width=35
)

entrada_modelo.pack(pady=2)


# ==========================================
# AÑOS
# ==========================================

tk.Label(
    ventana,
    text="Años de uso:"
).pack()

entrada_uso = tk.Entry(
    ventana,
    width=15
)

entrada_uso.pack(pady=2)


# ==========================================
# RAM
# ==========================================

tk.Label(
    ventana,
    text="RAM (GB):"
).pack()

entrada_ram = tk.Entry(
    ventana,
    width=15
)

entrada_ram.pack(pady=2)


# ==========================================
# TIEMPO
# ==========================================

tk.Label(
    ventana,
    text="Tiempo de encendido (segundos):"
).pack()

entrada_tiempo = tk.Entry(
    ventana,
    width=15
)

entrada_tiempo.pack(pady=2)


# ==========================================
# PROCESADOR
# ==========================================

tk.Label(
    ventana,
    text="Procesador:"
).pack()

entrada_procesador = tk.Entry(
    ventana,
    width=35
)

entrada_procesador.pack(pady=2)


# ==========================================
# ELECTRICIDAD
# ==========================================

tk.Label(
    ventana,
    text="¿Tiene electricidad?"
).pack(pady=(5, 0))

electricidad_var = tk.StringVar(
    value="s"
)

marco_electricidad = tk.Frame(ventana)

marco_electricidad.pack()

tk.Radiobutton(
    marco_electricidad,
    text="Sí",
    variable=electricidad_var,
    value="s"
).pack(side="left")

tk.Radiobutton(
    marco_electricidad,
    text="No",
    variable=electricidad_var,
    value="n"
).pack(side="left")


# ==========================================
# ENCIENDE
# ==========================================

tk.Label(
    ventana,
    text="¿Enciende?"
).pack(pady=(5, 0))

enciende_var = tk.StringVar(
    value="s"
)

marco_enciende = tk.Frame(ventana)

marco_enciende.pack()

tk.Radiobutton(
    marco_enciende,
    text="Sí",
    variable=enciende_var,
    value="s"
).pack(side="left")

tk.Radiobutton(
    marco_enciende,
    text="No",
    variable=enciende_var,
    value="n"
).pack(side="left")


# ==========================================
# IMAGEN
# ==========================================

tk.Label(
    ventana,
    text="¿Muestra imagen?"
).pack(pady=(5, 0))

imagen_var = tk.StringVar(
    value="s"
)

marco_imagen = tk.Frame(ventana)

marco_imagen.pack()

tk.Radiobutton(
    marco_imagen,
    text="Sí",
    variable=imagen_var,
    value="s"
).pack(side="left")

tk.Radiobutton(
    marco_imagen,
    text="No",
    variable=imagen_var,
    value="n"
).pack(side="left")


# ==========================================
# BOTÓN DIAGNOSTICAR
# ==========================================

boton = tk.Button(
    ventana,
    text="DIAGNOSTICAR",
    command=diagnosticar,
    width=20
)

boton.pack(pady=8)


# ==========================================
# BOTÓN BORRAR
# ==========================================

boton_borrar = tk.Button(
    ventana,
    text="BORRAR / NUEVO DIAGNÓSTICO",
    command=borrar_diagnostico,
    width=25
)

boton_borrar.pack(pady=5)


# ==========================================
# RESULTADO
# ==========================================

resultado = tk.Text(
    ventana,
    width=70,
    height=12
)

resultado.pack(pady=5)


# ==========================================
# INICIAR VENTANA
# ==========================================

ventana.mainloop()
