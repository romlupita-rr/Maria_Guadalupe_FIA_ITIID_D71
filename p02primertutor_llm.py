import tkinter as tk
from tkinter import messagebox
import threading
import ollama


# =================================
# CONFIGURACIÓN
# =================================

MODELO = "llama3.2:1b"

mensaje_sistema = """
Eres Music IA, un tutor de música para estudiantes.

Explicas de forma sencilla temas como:
- Géneros musicales
- Instrumentos
- Notas
- Acordes
- Ritmo
- Melodía
- Teoría musical
- Historia de la música

Reglas:
1. Explica de forma sencilla.
2. Da ejemplos cuando sea necesario.
3. Sé breve pero útil.
4. No inventes información.
5. Puedes hacer preguntas para comprobar si el estudiante entendió.
"""


# Historial de la conversación
mensajes = [
    {
        "role": "system",
        "content": mensaje_sistema
    }
]


# =================================
# MOSTRAR MENSAJE
# =================================

def mostrar_mensaje(nombre, texto):

    historial.config(state="normal")

    historial.insert(
        tk.END,
        nombre + "\n",
        "titulo"
    )

    historial.insert(
        tk.END,
        texto + "\n\n"
    )

    historial.config(state="disabled")

    historial.see(tk.END)


# =================================
# ENVIAR PREGUNTA
# =================================

def enviar():

    pregunta = entrada.get("1.0", tk.END).strip()

    if not pregunta:
        messagebox.showwarning(
            "Aviso",
            "Escribe una pregunta."
        )
        return

    entrada.delete("1.0", tk.END)

    mostrar_mensaje(
        "TÚ",
        pregunta
    )

    mensajes.append({
        "role": "user",
        "content": pregunta
    })

    # Desactivar botones mientras se procesa
    boton_enviar.config(
        state="disabled",
        text="PENSANDO..."
    )

    boton_resumen.config(
        state="disabled"
    )

    # Ejecutar Ollama en segundo plano
    threading.Thread(
        target=consultar_ollama,
        daemon=True
    ).start()


# =================================
# CONSULTAR OLLAMA
# =================================

def consultar_ollama():

    try:

        respuesta = ollama.chat(
            model=MODELO,
            messages=mensajes
        )

        texto = respuesta["message"]["content"]

        mensajes.append({
            "role": "assistant",
            "content": texto
        })

        # Actualizar Tkinter desde el hilo principal
        ventana.after(
            0,
            lambda: terminar_respuesta(texto)
        )

    except Exception as error:

        # Quitar la última pregunta si hubo error
        if mensajes and mensajes[-1]["role"] == "user":
            mensajes.pop()

        ventana.after(
            0,
            lambda: mostrar_error(error)
        )


# =================================
# TERMINAR RESPUESTA
# =================================

def terminar_respuesta(texto):

    mostrar_mensaje(
        "♫ MUSIC IA",
        texto
    )

    boton_enviar.config(
        state="normal",
        text="ENVIAR"
    )

    boton_resumen.config(
        state="normal"
    )

    entrada.focus()


# =================================
# MOSTRAR ERROR
# =================================

def mostrar_error(error):

    boton_enviar.config(
        state="normal",
        text="ENVIAR"
    )

    boton_resumen.config(
        state="normal"
    )

    messagebox.showerror(
        "Error",
        "No se pudo conectar con Ollama.\n\n"
        + str(error)
    )


# =================================
# RESUMEN
# =================================

def mostrar_resumen():

    if len(mensajes) <= 1:

        messagebox.showinfo(
            "Resumen",
            "Todavía no existe una conversación."
        )

        return

    conversacion = ""

    for mensaje in mensajes[1:]:

        conversacion += (
            mensaje["role"]
            + ": "
            + mensaje["content"]
            + "\n"
        )

    prompt = f"""
Haz un resumen breve de esta conversación de aprendizaje musical.

Indica:

- Los temas de música que preguntó el estudiante.
- Los conceptos que se explicaron.
- Qué debería repasar el estudiante.

No inventes información que no aparezca en la conversación.

Conversación:

{conversacion}
"""

    boton_resumen.config(
        state="disabled",
        text="GENERANDO..."
    )

    boton_enviar.config(
        state="disabled"
    )

    # Ejecutar el resumen en segundo plano
    threading.Thread(
        target=generar_resumen,
        args=(prompt,),
        daemon=True
    ).start()


# =================================
# GENERAR RESUMEN CON OLLAMA
# =================================

def generar_resumen(prompt):

    try:

        respuesta = ollama.chat(
            model=MODELO,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        resumen = respuesta["message"]["content"]

        ventana.after(
            0,
            lambda: mostrar_resumen_final(resumen)
        )

    except Exception as error:

        ventana.after(
            0,
            lambda: mostrar_error_resumen(error)
        )


# =================================
# MOSTRAR RESUMEN
# =================================

def mostrar_resumen_final(resumen):

    boton_resumen.config(
        state="normal",
        text="RESUMEN"
    )

    boton_enviar.config(
        state="normal"
    )

    messagebox.showinfo(
        "Resumen de aprendizaje",
        resumen
    )

    entrada.focus()


# =================================
# ERROR DEL RESUMEN
# =================================

def mostrar_error_resumen(error):

    boton_resumen.config(
        state="normal",
        text="RESUMEN"
    )

    boton_enviar.config(
        state="normal"
    )

    messagebox.showerror(
        "Error",
        "No se pudo generar el resumen.\n\n"
        + str(error)
    )


# =================================
# NUEVA CONVERSACIÓN
# =================================

def nueva_conversacion():

    global mensajes

    mensajes = [
        {
            "role": "system",
            "content": mensaje_sistema
        }
    ]

    historial.config(
        state="normal"
    )

    historial.delete(
        "1.0",
        tk.END
    )

    historial.config(
        state="disabled"
    )

    mostrar_mensaje(
        "♫ MUSIC IA",
        "¡Hola! Soy tu tutor de música.\n"
        "¿Qué quieres aprender hoy?"
    )

    entrada.focus()


# =================================
# VENTANA
# =================================

ventana = tk.Tk()

ventana.title(
    "♫ Music IA - Tutor de Música"
)

ventana.geometry(
    "750x500"
)

ventana.minsize(
    700,
    450
)

ventana.configure(
    bg="#181824"
)


# =================================
# ENCABEZADO
# =================================

encabezado = tk.Frame(
    ventana,
    bg="#292943",
    height=65
)

encabezado.pack(
    fill="x"
)

encabezado.pack_propagate(False)


tk.Label(
    encabezado,
    text="♫",
    font=("Arial", 24, "bold"),
    bg="#292943",
    fg="#c084fc"
).pack(
    side="left",
    padx=(20, 8)
)


tk.Label(
    encabezado,
    text="MUSIC IA",
    font=("Arial", 18, "bold"),
    bg="#292943",
    fg="white"
).pack(
    side="left"
)


tk.Label(
    encabezado,
    text="Tutor de música",
    font=("Arial", 10),
    bg="#292943",
    fg="#bbbbcc"
).pack(
    side="left",
    padx=10
)


# =================================
# HISTORIAL
# =================================

historial = tk.Text(
    ventana,
    bg="#222233",
    fg="white",
    font=("Arial", 10),
    wrap="word",
    state="disabled",
    relief="flat"
)

historial.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=12
)


historial.tag_config(
    "titulo",
    foreground="#c084fc",
    font=("Arial", 10, "bold")
)


# =================================
# ENTRADA
# =================================

entrada = tk.Text(
    ventana,
    height=2,
    bg="#292943",
    fg="white",
    insertbackground="white",
    font=("Arial", 10),
    wrap="word",
    relief="flat"
)

entrada.pack(
    fill="x",
    padx=15,
    pady=(0, 8)
)


# =================================
# BOTONES
# =================================

botones = tk.Frame(
    ventana,
    bg="#181824"
)

botones.pack(
    pady=(0, 12)
)


# BOTÓN ENVIAR

boton_enviar = tk.Button(
    botones,
    text="ENVIAR",
    command=enviar,
    width=13,
    height=1,
    bg="#8b5cf6",
    fg="white",
    relief="flat",
    font=("Arial", 9, "bold")
)

boton_enviar.pack(
    side="left",
    padx=4
)


# BOTÓN RESUMEN

boton_resumen = tk.Button(
    botones,
    text="RESUMEN",
    command=mostrar_resumen,
    width=13,
    height=1,
    bg="#3b3b58",
    fg="white",
    relief="flat",
    font=("Arial", 9, "bold")
)

boton_resumen.pack(
    side="left",
    padx=4
)


# BOTÓN NUEVA

boton_nueva = tk.Button(
    botones,
    text="NUEVA",
    command=nueva_conversacion,
    width=13,
    height=1,
    bg="#3b3b58",
    fg="white",
    relief="flat",
    font=("Arial", 9, "bold")
)

boton_nueva.pack(
    side="left",
    padx=4
)


# =================================
# MENSAJE INICIAL
# =================================

mostrar_mensaje(
    "♫ MUSIC IA",
    "¡Hola! Soy tu tutor de música.\n"
    "¿Qué quieres aprender hoy?"
)


entrada.focus()


# =================================
# INICIAR PROGRAMA
# =================================

ventana.mainloop()