import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId


# ==========================================
# CONFIGURACIÓN DE MONGODB ATLAS
# ==========================================

load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}"
    f"@{MONGO_CLUSTER}/"
)


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
        """El agente recibe las percepciones del entorno."""
        self.temperatura = temperatura
        self.humedad = humedad

    def tomar_decision(self) -> str:
        """El agente decide qué acción realizar."""

        if self.temperatura > 30 and self.humedad > 70:
            self.accion = (
                "Encender aire acondicionado "
                "(Modo Deshumidificador)"
            )

        elif self.temperatura > 30:
            self.accion = "Encender ventilador"

        elif self.temperatura < 18:
            self.accion = "Encender calefacción"

        else:
            self.accion = "Mantener sistema apagado"

        return self.accion


# ==========================================
# CONEXIÓN Y CRUD DE MONGODB
# ==========================================

class MongoDB:
    """Clase encargada de las operaciones CRUD en MongoDB Atlas."""

    def conectar(self):
        """Conecta con MongoDB Atlas."""

        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        # Verificar conexión
        cliente.admin.command("ping")

        db = cliente[MONGO_DB]
        coleccion = db[MONGO_COLLECTION]

        return cliente, coleccion

    # ======================================
    # CREATE - GUARDAR
    # ======================================

    def guardar_registro(
        self,
        temperatura,
        humedad,
        accion
    ):
        """Guarda un nuevo registro."""

        cliente, coleccion = self.conectar()

        try:

            documento = {
                "temperatura_c": temperatura,
                "humedad_porcentaje": humedad,
                "accion_ejecutada": accion,
                "fecha_registro": datetime.datetime.now(
                    datetime.timezone.utc
                )
            }

            resultado = coleccion.insert_one(documento)

            return str(resultado.inserted_id)

        finally:
            cliente.close()

    # ======================================
    # READ - LEER TODOS
    # ======================================

    def obtener_registros(self):
        """Obtiene los registros de MongoDB."""

        cliente, coleccion = self.conectar()

        try:

            registros = list(
                coleccion.find()
                .sort("_id", -1)
            )

            return registros

        finally:
            cliente.close()

    # ======================================
    # READ - LEER UNO
    # ======================================

    def obtener_registro(self, id_registro):
        """Obtiene un registro específico."""

        cliente, coleccion = self.conectar()

        try:

            registro = coleccion.find_one(
                {
                    "_id": ObjectId(id_registro)
                }
            )

            return registro

        finally:
            cliente.close()

    # ======================================
    # UPDATE - ACTUALIZAR
    # ======================================

    def actualizar_registro(
        self,
        id_registro,
        temperatura,
        humedad,
        accion
    ):
        """Actualiza un registro existente."""

        cliente, coleccion = self.conectar()

        try:

            resultado = coleccion.update_one(
                {
                    "_id": ObjectId(id_registro)
                },
                {
                    "$set": {
                        "temperatura_c": temperatura,
                        "humedad_porcentaje": humedad,
                        "accion_ejecutada": accion,
                        "fecha_registro": datetime.datetime.now(
                            datetime.timezone.utc
                        )
                    }
                }
            )

            return resultado.modified_count

        finally:
            cliente.close()

    # ======================================
    # DELETE - ELIMINAR
    # ======================================

    def eliminar_registro(self, id_registro):
        """Elimina un registro."""

        cliente, coleccion = self.conectar()

        try:

            resultado = coleccion.delete_one(
                {
                    "_id": ObjectId(id_registro)
                }
            )

            return resultado.deleted_count

        finally:
            cliente.close()


# ==========================================
# INTERFAZ GRÁFICA
# ==========================================

class InterfazAgente:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Agente de Climatización + MongoDB Atlas"
        )

        self.root.geometry("900x650")
        self.root.resizable(False, False)

        self.agente = AgenteClimatizacion()
        self.mongodb = MongoDB()

        # ID seleccionado actualmente
        self.id_seleccionado = None

        self._crear_componentes()

        self._cargar_historial()


    # ======================================
    # CREAR INTERFAZ
    # ======================================

    def _crear_componentes(self):

        # ----------------------------------
        # TÍTULO
        # ----------------------------------

        lbl_titulo = tk.Label(
            self.root,
            text="Agente de Climatización",
            font=("Arial", 18, "bold")
        )

        lbl_titulo.pack(pady=15)


        # ----------------------------------
        # ENTRADAS
        # ----------------------------------

        frame_entradas = ttk.LabelFrame(
            self.root,
            text=" Sensores del Entorno ",
            padding=15
        )

        frame_entradas.pack(
            fill="x",
            padx=20,
            pady=5
        )


        ttk.Label(
            frame_entradas,
            text="Temperatura actual (°C):"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )


        self.entry_temp = ttk.Entry(
            frame_entradas,
            width=15
        )

        self.entry_temp.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )


        ttk.Label(
            frame_entradas,
            text="Humedad actual (%):"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )


        self.entry_humedad = ttk.Entry(
            frame_entradas,
            width=15
        )

        self.entry_humedad.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )


        # ----------------------------------
        # BOTONES
        # ----------------------------------

        frame_botones = ttk.Frame(
            frame_entradas
        )

        frame_botones.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=20
        )


        self.btn_guardar = tk.Button(
            frame_botones,
            text="Guardar",
            bg="green",
            fg="white",
            command=self._crear_registro
        )

        self.btn_guardar.grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )


        self.btn_actualizar = tk.Button(
            frame_botones,
            text="Actualizar",
            bg="orange",
            command=self._actualizar_registro
        )

        self.btn_actualizar.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )


        self.btn_eliminar = tk.Button(
            frame_botones,
            text="Eliminar",
            bg="red",
            fg="white",
            command=self._eliminar_registro
        )

        self.btn_eliminar.grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )


        self.btn_limpiar = tk.Button(
            frame_botones,
            text="Limpiar",
            bg="blue",
            fg="white",
            command=self._limpiar_campos
        )

        self.btn_limpiar.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )


        # ----------------------------------
        # DECISIÓN DEL AGENTE
        # ----------------------------------

        frame_salida = ttk.LabelFrame(
            self.root,
            text=" Decisión del Agente ",
            padding=15
        )

        frame_salida.pack(
            fill="x",
            padx=20,
            pady=10
        )


        self.lbl_accion = tk.Label(
            frame_salida,
            text="Esperando datos de sensores...",
            font=("Arial", 10, "bold"),
            fg="#555555",
            wraplength=800
        )

        self.lbl_accion.pack()


        # ----------------------------------
        # TABLA
        # ----------------------------------

        frame_tabla = ttk.LabelFrame(
            self.root,
            text=" Historial en MongoDB Atlas ",
            padding=10
        )

        frame_tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


        columnas = (
            "Fecha",
            "Temperatura",
            "Humedad",
            "Acción",
            "ID"
        )


        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=13
        )


        self.tabla.heading(
            "Fecha",
            text="Fecha"
        )

        self.tabla.heading(
            "Temperatura",
            text="Temperatura"
        )

        self.tabla.heading(
            "Humedad",
            text="Humedad"
        )

        self.tabla.heading(
            "Acción",
            text="Acción"
        )

        self.tabla.heading(
            "ID",
            text="ID MongoDB"
        )


        self.tabla.column(
            "Fecha",
            width=150
        )

        self.tabla.column(
            "Temperatura",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "Humedad",
            width=100,
            anchor="center"
        )

        self.tabla.column(
            "Acción",
            width=300
        )

        self.tabla.column(
            "ID",
            width=220
        )


        scrollbar = ttk.Scrollbar(
            frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar.set
        )


        self.tabla.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )


        # ----------------------------------
        # SELECCIÓN
        # ----------------------------------

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self._seleccionar_registro
        )


    # ======================================
    # CREATE
    # ======================================

    def _crear_registro(self):

        try:

            temp = float(
                self.entry_temp.get().strip()
            )

            hum = float(
                self.entry_humedad.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Ingresa valores numéricos válidos."
            )

            return


        if not -100 <= temp <= 100:

            messagebox.showwarning(
                "Dato inválido",
                "La temperatura debe estar entre -100 y 100 °C."
            )

            return


        if not 0 <= hum <= 100:

            messagebox.showwarning(
                "Dato inválido",
                "La humedad debe estar entre 0% y 100%."
            )

            return


        # El agente percibe los datos

        self.agente.percibir(
            temp,
            hum
        )


        # El agente toma una decisión

        accion = self.agente.tomar_decision()


        try:

            id_registro = self.mongodb.guardar_registro(
                temp,
                hum,
                accion
            )


            messagebox.showinfo(
                "Registro guardado",
                "El registro fue guardado correctamente."
            )


            self.lbl_accion.config(
                text=f"Acción: {accion}"
            )


            self._limpiar_campos()

            self._recargar_tabla()


        except PyMongoError as e:

            messagebox.showerror(
                "Error de MongoDB",
                f"No fue posible guardar el registro:\n\n{e}"
            )


    # ======================================
    # READ
    # ======================================

    def _cargar_historial(self):

        try:

            registros = self.mongodb.obtener_registros()

            for registro in registros:

                self.tabla.insert(
                    "",
                    tk.END,
                    values=(
                        self._formatear_fecha(
                            registro.get("fecha_registro")
                        ),
                        f"{registro.get('temperatura_c', 0)} °C",
                        f"{registro.get('humedad_porcentaje', 0)} %",
                        registro.get(
                            "accion_ejecutada",
                            "N/A"
                        ),
                        str(
                            registro.get("_id", "")
                        )
                    )
                )

        except PyMongoError as e:

            messagebox.showwarning(
                "Advertencia",
                f"No fue posible cargar los registros:\n\n{e}"
            )


    # ======================================
    # SELECCIONAR REGISTRO
    # ======================================

    def _seleccionar_registro(
        self,
        event=None
    ):

        seleccion = self.tabla.selection()

        if not seleccion:
            return


        item = self.tabla.item(
            seleccion[0]
        )

        valores = item["values"]


        if not valores:
            return


        self.id_seleccionado = str(
            valores[4]
        )


        temperatura = str(
            valores[1]
        ).replace(" °C", "")


        humedad = str(
            valores[2]
        ).replace(" %", "")


        self.entry_temp.delete(
            0,
            tk.END
        )

        self.entry_temp.insert(
            0,
            temperatura
        )


        self.entry_humedad.delete(
            0,
            tk.END
        )

        self.entry_humedad.insert(
            0,
            humedad
        )


        self.lbl_accion.config(
            text=f"Registro seleccionado: {self.id_seleccionado}"
        )


    # ======================================
    # UPDATE
    # ======================================

    def _actualizar_registro(self):

        if not self.id_seleccionado:

            messagebox.showwarning(
                "Selecciona un registro",
                "Selecciona primero un registro de la tabla."
            )

            return


        try:

            temp = float(
                self.entry_temp.get().strip()
            )

            hum = float(
                self.entry_humedad.get().strip()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Ingresa valores numéricos válidos."
            )

            return


        if not -100 <= temp <= 100:

            messagebox.showwarning(
                "Dato inválido",
                "La temperatura debe estar entre -100 y 100 °C."
            )

            return


        if not 0 <= hum <= 100:

            messagebox.showwarning(
                "Dato inválido",
                "La humedad debe estar entre 0% y 100%."
            )

            return


        # Volver a calcular la decisión

        self.agente.percibir(
            temp,
            hum
        )

        accion = self.agente.tomar_decision()


        try:

            modificados = self.mongodb.actualizar_registro(
                self.id_seleccionado,
                temp,
                hum,
                accion
            )


            if modificados == 0:

                messagebox.showwarning(
                    "Sin cambios",
                    "No se encontró el registro o no hubo cambios."
                )

                return


            messagebox.showinfo(
                "Actualizado",
                "El registro fue actualizado correctamente."
            )


            self.lbl_accion.config(
                text=f"Acción: {accion}"
            )


            self._limpiar_campos()

            self._recargar_tabla()


        except PyMongoError as e:

            messagebox.showerror(
                "Error",
                f"No fue posible actualizar:\n\n{e}"
            )


    # ======================================
    # DELETE
    # ======================================

    def _eliminar_registro(self):

        if not self.id_seleccionado:

            messagebox.showwarning(
                "Selecciona un registro",
                "Selecciona primero un registro."
            )

            return


        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Seguro que deseas eliminar este registro?"
        )


        if not confirmar:
            return


        try:

            eliminados = self.mongodb.eliminar_registro(
                self.id_seleccionado
            )


            if eliminados == 0:

                messagebox.showwarning(
                    "No encontrado",
                    "El registro no existe en MongoDB."
                )

                return


            messagebox.showinfo(
                "Eliminado",
                "El registro fue eliminado correctamente."
            )


            self._limpiar_campos()

            self._recargar_tabla()


        except PyMongoError as e:

            messagebox.showerror(
                "Error",
                f"No fue posible eliminar:\n\n{e}"
            )


    # ======================================
    # LIMPIAR
    # ======================================

    def _limpiar_campos(self):

        self.entry_temp.delete(
            0,
            tk.END
        )

        self.entry_humedad.delete(
            0,
            tk.END
        )

        self.id_seleccionado = None

        self.lbl_accion.config(
            text="Esperando datos de sensores...",
            fg="#555555"
        )


        for item in self.tabla.selection():

            self.tabla.selection_remove(
                item
            )


    # ======================================
    # RECARGAR TABLA
    # ======================================

    def _recargar_tabla(self):

        for item in self.tabla.get_children():

            self.tabla.delete(item)


        self._cargar_historial()


    # ======================================
    # FORMATEAR FECHA
    # ======================================

    def _formatear_fecha(self, fecha):

        if fecha is None:
            return "N/A"


        if isinstance(
            fecha,
            datetime.datetime
        ):

            return fecha.astimezone().strftime(
                "%Y-%m-%d %H:%M:%S"
            )


        return str(fecha)


# ==========================================
# EJECUCIÓN
# ==========================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = InterfazAgente(
        ventana
    )

    ventana.mainloop()