
# ==========================================
# TABLA DE VERDAD CON TKINTER
# ==========================================

import tkinter as tk
from tkinter import ttk


# ==========================================
# FUNCIÓN PARA GENERAR LA TABLA
# ==========================================

def generar_tabla():

    # Borrar los datos anteriores de la tabla
    for fila in tabla.get_children():
        tabla.delete(fila)

    # Valores posibles de P y Q
    valores = [True, False]

    # Recorrer todos los valores de P
    for P in valores:

        # Recorrer todos los valores de Q
        for Q in valores:

            # Operaciones lógicas
            negacion = not P
            conjuncion = P and Q
            disyuncion = P or Q
            condicional = (not P) or Q
            bicondicional = P == Q

            # Convertir True y False a V y F
            if P:
                resultado_P = "V"
            else:
                resultado_P = "F"

            if Q:
                resultado_Q = "V"
            else:
                resultado_Q = "F"

            if negacion:
                resultado_negacion = "V"
            else:
                resultado_negacion = "F"

            if conjuncion:
                resultado_conjuncion = "V"
            else:
                resultado_conjuncion = "F"

            if disyuncion:
                resultado_disyuncion = "V"
            else:
                resultado_disyuncion = "F"

            if condicional:
                resultado_condicional = "V"
            else:
                resultado_condicional = "F"

            if bicondicional:
                resultado_bicondicional = "V"
            else:
                resultado_bicondicional = "F"

            # Agregar los resultados a la tabla gráfica
            tabla.insert(
                "",
                tk.END,
                values=(
                    resultado_P,
                    resultado_Q,
                    resultado_negacion,
                    resultado_conjuncion,
                    resultado_disyuncion,
                    resultado_condicional,
                    resultado_bicondicional
                )
            )


# ==========================================
# CREAR LA VENTANA
# ==========================================

ventana = tk.Tk()

# Título de la ventana
ventana.title("Tabla de verdad")

# Tamaño de la ventana
ventana.geometry("500x500")


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    ventana,
    text="TABLA DE VERDAD",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=20)


# ==========================================
# BOTÓN
# ==========================================

boton = tk.Button(
    ventana,
    text="Generar tabla",
    command=generar_tabla
)

boton.pack(pady=10)


# ==========================================
# CREAR TABLA GRÁFICA
# ==========================================

tabla = ttk.Treeview(
    ventana,
    columns=(
        "P",
        "Q",
        "Negación",
        "Conjunción",
        "Disyunción",
        "Condicional",
        "Bicondicional"
    ),
    show="headings"
)


# ==========================================
# NOMBRES DE LAS COLUMNAS
# ==========================================

tabla.heading("P", text="P")
tabla.heading("Q", text="Q")
tabla.heading("Negación", text="¬P")
tabla.heading("Conjunción", text="P ∧ Q")
tabla.heading("Disyunción", text="P ∨ Q")
tabla.heading("Condicional", text="P → Q")
tabla.heading("Bicondicional", text="P ↔ Q")


# ==========================================
# ANCHO DE LAS COLUMNAS
# ==========================================

tabla.column("P", width=70, anchor="center")
tabla.column("Q", width=70, anchor="center")
tabla.column("Negación", width=90, anchor="center")
tabla.column("Conjunción", width=100, anchor="center")
tabla.column("Disyunción", width=100, anchor="center")
tabla.column("Condicional", width=100, anchor="center")
tabla.column("Bicondicional", width=110, anchor="center")


# Mostrar la tabla en la ventana
tabla.pack(pady=20)


# ==========================================
# MANTENER LA VENTANA ABIERTA
# ==========================================

ventana.mainloop()
