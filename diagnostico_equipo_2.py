import random
from datetime import datetime

# ==========================================================
# 1. ENCABEZADO
# ==========================================================

print("=================================================")
print("       DIAGNÓSTICO INTELIGENTE DE EQUIPO")
print("=================================================")

input("Bienvenido al sistema. Presiona ENTER para continuar: ")

nombre = input("Ingresa tu nombre completo: ")
direccion = input("Ingresa tu dirección: ")

numero_aleatorio = random.randint(1, 100000)

fecha_hora = datetime.now()
fecha = fecha_hora.strftime("%d/%m/%Y")
hora = fecha_hora.strftime("%H:%M:%S")


# ==========================================================
# 2. SELECCIÓN DEL DISPOSITIVO
# ==========================================================

dispositivo_opcion = ""

while dispositivo_opcion not in ["1", "2", "3", "4"]:

    print("\n===== SELECCIÓN DEL DISPOSITIVO =====")
    print("1. PC")
    print("2. Laptop")
    print("3. Servidor")
    print("4. Tablet")

    dispositivo_opcion = input("Selecciona tu dispositivo: ")

    if dispositivo_opcion not in ["1", "2", "3", "4"]:
        print("Opción no válida.")


if dispositivo_opcion == "1":
    dispositivo = "PC"

elif dispositivo_opcion == "2":
    dispositivo = "Laptop"

elif dispositivo_opcion == "3":
    dispositivo = "Servidor"

else:
    dispositivo = "Tablet"


# ==========================================================
# 3. DATOS GENERALES
# ==========================================================

modelo = input("\n¿Qué modelo es tu equipo?: ")
uso = int(input("¿Cuántos años de uso tiene?: "))

electricidad = input(
    "¿Tiene electricidad? (s/n): "
).lower() == "s"

enciende = input(
    "¿Enciende? (s/n): "
).lower() == "s"

imagen = input(
    "¿Muestra imagen? (s/n): "
).lower() == "s"


riesgo = 0
problemas = []
recomendaciones = []

diagnostico = "El equipo funciona correctamente."


# ==========================================================
# 4. REVISION GENERAL
# ==========================================================

print("\n==========================================")
print("          ANALIZANDO EQUIPO...")
print("==========================================")


# Proposición:
# NO tiene electricidad Y NO enciende

if not electricidad and not enciende:

    riesgo += 10

    problemas.append(
        "El equipo no tiene electricidad y no enciende."
    )

    recomendaciones.append(
        "Revisar cable, cargador, batería o fuente de alimentación."
    )


# Proposición:
# Tiene electricidad Y NO enciende

elif electricidad and not enciende:

    riesgo += 10

    problemas.append(
        "El equipo recibe electricidad pero no enciende."
    )

    recomendaciones.append(
        "Revisar botón de encendido, batería o fuente de alimentación."
    )


# Proposición:
# Enciende Y NO muestra imagen

elif enciende and not imagen:

    riesgo += 8

    problemas.append(
        "El equipo enciende pero no muestra imagen."
    )

    recomendaciones.append(
        "Revisar pantalla, monitor, cables o memoria RAM."
    )


# Proposición:
# Tiene electricidad Y enciende Y muestra imagen

elif electricidad and enciende and imagen:

    print("El equipo supera la revisión general.")


# ==========================================================
# 5. AÑOS DE USO
# ==========================================================

if uso >= 8:

    riesgo += 5

    problemas.append(
        "El equipo tiene muchos años de uso."
    )

    recomendaciones.append(
        "Realizar mantenimiento preventivo y revisar componentes."
    )

elif uso >= 5:

    riesgo += 3

    problemas.append(
        "El equipo tiene varios años de uso."
    )

    recomendaciones.append(
        "Revisar el estado general de los componentes."
    )


# ==========================================================
# 6. DIAGNÓSTICO DE PC
# ==========================================================

if dispositivo == "PC":

    print("\n===== DIAGNÓSTICO DE PC =====")

    procesador = input("¿Qué procesador tiene?: ")
    ram = int(input("¿Cuánta RAM tiene? (GB): "))

    if electricidad and enciende and imagen:

        tiempo = int(
            input("¿Cuántos segundos tarda en encender?: ")
        )

        monitor = input(
            "¿Dice 'Sin señal'? (s/n): "
        ).lower() == "s"

        internet = input(
            "¿Tiene problemas de Internet? (s/n): "
        ).lower() == "s"

        audio = input(
            "¿Tiene problemas de audio? (s/n): "
        ).lower() == "s"


        # RAM

        if ram < 4:

            riesgo += 5

            problemas.append(
                "Tiene poca memoria RAM."
            )

            recomendaciones.append(
                "Aumentar la memoria RAM."
            )

        elif ram < 8:

            riesgo += 2

            problemas.append(
                "La memoria RAM es limitada."
            )

            recomendaciones.append(
                "Considerar aumentar la memoria RAM."
            )


        # Tiempo de encendido

        if tiempo > 180:

            riesgo += 5

            problemas.append(
                "Tarda demasiado en encender."
            )

            recomendaciones.append(
                "Revisar el almacenamiento y los programas de inicio."
            )

        elif tiempo > 60:

            riesgo += 3

            problemas.append(
                "Tarda en encender."
            )

            recomendaciones.append(
                "Revisar los programas que se ejecutan al iniciar."
            )


        # ==================================================
        # PROPOSICIONES DE PC
        # ==================================================

        # RAM baja Y tarda mucho

        if ram < 4 and tiempo > 180:

            diagnostico = (
                "Posible problema de rendimiento."
            )


        # Problema de video

        elif monitor and not imagen:

            diagnostico = (
                "Posible problema de video."
            )


        # Internet Y audio

        elif internet and audio:

            diagnostico = (
                "Presenta problemas de Internet y audio."
            )


        # Internet O audio

        elif internet or audio:

            diagnostico = (
                "Presenta un problema de conexión o audio."
            )


        # RAM baja O tarda mucho

        elif ram < 4 or tiempo > 180:

            diagnostico = (
                "El equipo puede presentar lentitud."
            )


        # Tarda más de un minuto

        elif tiempo > 60:

            diagnostico = (
                "Posible lentitud al iniciar."
            )


        else:

            diagnostico = (
                "La PC funciona correctamente."
            )


# ==========================================================
# 7. DIAGNÓSTICO DE LAPTOP
# ==========================================================

elif dispositivo == "Laptop":

    print("\n===== DIAGNÓSTICO DE LAPTOP =====")

    procesador = input("¿Qué procesador tiene?: ")
    ram = int(input("¿Cuánta RAM tiene? (GB): "))


    if electricidad and enciende and imagen:

        bateria = input(
            "¿La batería dura poco? (s/n): "
        ).lower() == "s"

        calentamiento = input(
            "¿Se calienta demasiado? (s/n): "
        ).lower() == "s"

        lentitud = input(
            "¿Está lenta? (s/n): "
        ).lower() == "s"


        if bateria:

            riesgo += 4

            problemas.append(
                "La batería dura poco."
            )

            recomendaciones.append(
                "Revisar el estado de la batería."
            )


        if calentamiento:

            riesgo += 5

            problemas.append(
                "La laptop se calienta demasiado."
            )

            recomendaciones.append(
                "Limpiar ventiladores y sistema de refrigeración."
            )


        if lentitud:

            riesgo += 4

            problemas.append(
                "La laptop funciona lentamente."
            )

            recomendaciones.append(
                "Revisar memoria RAM y almacenamiento."
            )


        # ==================================================
        # PROPOSICIONES DE LAPTOP
        # ==================================================

        # Calentamiento Y batería

        if calentamiento and bateria:

            diagnostico = (
                "Posibles problemas de temperatura y batería."
            )


        # Calentamiento Y lentitud

        elif calentamiento and lentitud:

            diagnostico = (
                "Posibles problemas de temperatura y rendimiento."
            )


        # Batería O calentamiento

        elif bateria or calentamiento:

            diagnostico = (
                "Presenta un posible problema de energía o temperatura."
            )


        # Lentitud Y poca RAM

        elif lentitud and ram < 4:

            diagnostico = (
                "Posible problema de rendimiento."
            )


        # Poca RAM O lentitud

        elif ram < 4 or lentitud:

            diagnostico = (
                "La laptop puede presentar lentitud."
            )


        else:

            diagnostico = (
                "La laptop funciona correctamente."
            )


# ==========================================================
# 8. DIAGNÓSTICO DE SERVIDOR
# ==========================================================

elif dispositivo == "Servidor":

    print("\n===== DIAGNÓSTICO DE SERVIDOR =====")

    procesador = input("¿Qué procesador tiene?: ")
    ram = int(input("¿Cuánta RAM tiene? (GB): "))


    if electricidad and enciende and imagen:

        servicio = input(
            "¿Algún servicio no funciona? (s/n): "
        ).lower() == "s"

        red = input(
            "¿Tiene problemas de red? (s/n): "
        ).lower() == "s"

        almacenamiento = input(
            "¿Tiene poco espacio? (s/n): "
        ).lower() == "s"


        if servicio:

            riesgo += 6

            problemas.append(
                "Hay servicios que no funcionan."
            )

            recomendaciones.append(
                "Revisar los servicios del servidor."
            )


        if red:

            riesgo += 5

            problemas.append(
                "Tiene problemas de red."
            )

            recomendaciones.append(
                "Revisar la conexión y configuración de red."
            )


        if almacenamiento:

            riesgo += 5

            problemas.append(
                "Tiene poco espacio de almacenamiento."
            )

            recomendaciones.append(
                "Liberar espacio de almacenamiento."
            )


        # ==================================================
        # PROPOSICIONES DE SERVIDOR
        # ==================================================

        # Servicio Y red

        if servicio and red:

            diagnostico = (
                "Posible problema de servicios y red."
            )


        # Servicio Y almacenamiento

        elif servicio and almacenamiento:

            diagnostico = (
                "Posible problema de servicios y almacenamiento."
            )


        # Red Y almacenamiento

        elif red and almacenamiento:

            diagnostico = (
                "Posible problema de red y almacenamiento."
            )


        # Servicio O red

        elif servicio or red:

            diagnostico = (
                "Presenta un posible problema de servicio o red."
            )


        # Almacenamiento

        elif almacenamiento:

            diagnostico = (
                "Posible falta de espacio."
            )


        else:

            diagnostico = (
                "El servidor funciona correctamente."
            )


# ==========================================================
# 9. DIAGNÓSTICO DE TABLET
# ==========================================================

else:

    print("\n===== DIAGNÓSTICO DE TABLET =====")

    sistema = input("¿Qué sistema utiliza?: ")
    ram = int(input("¿Cuánta RAM tiene? (GB): "))


    if electricidad and enciende and imagen:

        tactil = input(
            "¿La pantalla táctil tiene problemas? (s/n): "
        ).lower() == "s"

        aplicaciones = input(
            "¿Las aplicaciones se cierran? (s/n): "
        ).lower() == "s"

        almacenamiento = input(
            "¿Tiene poco espacio? (s/n): "
        ).lower() == "s"


        if tactil:

            riesgo += 5

            problemas.append(
                "La pantalla táctil presenta problemas."
            )

            recomendaciones.append(
                "Revisar pantalla y digitalizador."
            )


        if aplicaciones:

            riesgo += 4

            problemas.append(
                "Las aplicaciones se cierran."
            )

            recomendaciones.append(
                "Revisar memoria RAM y sistema."
            )


        if almacenamiento:

            riesgo += 4

            problemas.append(
                "Tiene poco espacio."
            )

            recomendaciones.append(
                "Eliminar archivos innecesarios."
            )


        # ==================================================
        # PROPOSICIONES DE TABLET
        # ==================================================

        # Táctil Y aplicaciones

        if tactil and aplicaciones:

            diagnostico = (
                "Posibles problemas de pantalla y sistema."
            )


        # Aplicaciones Y almacenamiento

        elif aplicaciones and almacenamiento:

            diagnostico = (
                "Posible problema por falta de almacenamiento."
            )


        # Táctil O aplicaciones

        elif tactil or aplicaciones:

            diagnostico = (
                "Presenta un posible problema de pantalla o sistema."
            )


        # Almacenamiento O poca RAM

        elif almacenamiento or ram < 4:

            diagnostico = (
                "La tablet puede presentar problemas de rendimiento."
            )


        else:

            diagnostico = (
                "La tablet funciona correctamente."
            )


# ==========================================================
# 10. DIAGNÓSTICO GENERAL POR PROPOSICIONES
# ==========================================================

# NO electricidad Y NO enciende

if not electricidad and not enciende:

    diagnostico = (
        "Posible falla de alimentación eléctrica."
    )


# Electricidad Y NO enciende

elif electricidad and not enciende:

    diagnostico = (
        "Posible falla de encendido."
    )


# Electricidad Y enciende Y NO imagen

elif electricidad and enciende and not imagen:

    diagnostico = (
        "Posible falla de pantalla o video."
    )


# ==========================================================
# 11. NIVEL DE RIESGO
# ==========================================================

if riesgo >= 18:

    nivel = "CRÍTICO"

elif riesgo >= 11:

    nivel = "ALTO"

elif riesgo >= 6:

    nivel = "MEDIO"

else:

    nivel = "BAJO"


# ==========================================================
# 12. RESULTADO
# ==========================================================

print("\n=================================================")
print("             RESULTADO DEL ANÁLISIS")
print("=================================================")

print("Número de reporte:", numero_aleatorio)
print("Fecha:", fecha)
print("Hora:", hora)
print("Nombre:", nombre)
print("Dirección:", direccion)
print("Dispositivo:", dispositivo)
print("Modelo:", modelo)
print("Años de uso:", uso)


if dispositivo == "PC":

    print("Procesador:", procesador)
    print("RAM:", ram, "GB")

elif dispositivo == "Laptop":

    print("Procesador:", procesador)
    print("RAM:", ram, "GB")

elif dispositivo == "Servidor":

    print("Procesador:", procesador)
    print("RAM:", ram, "GB")

else:

    print("Sistema:", sistema)
    print("RAM:", ram, "GB")


# ==========================================================
# 13. DIAGNÓSTICO POR PROPOSICIONES
# ==========================================================

print("\n===== DIAGNÓSTICO POR PROPOSICIONES =====")
print(diagnostico)


# ==========================================================
# 14. NIVEL DE RIESGO
# ==========================================================

print("\nNivel de riesgo:", nivel)
print("Puntuación:", riesgo)


# ==========================================================
# 15. PROBLEMAS DETECTADOS
# ==========================================================

print("\n===== PROBLEMAS DETECTADOS =====")

if len(problemas) == 0:

    print("No se detectaron problemas.")

else:

    for problema in problemas:

        print("-", problema)


# ==========================================================
# 16. RECOMENDACIONES
# ==========================================================

print("\n===== RECOMENDACIONES =====")

if len(recomendaciones) == 0:

    print("El equipo funciona correctamente.")
    print("Se recomienda mantenimiento preventivo.")

else:

    for recomendacion in recomendaciones:

        print("-", recomendacion)


# ==========================================================
# 17. FIN
# ==========================================================

print("\n=================================================")
print("           FIN DEL DIAGNÓSTICO")
print("=================================================")

print("Reporte:", numero_aleatorio)
print("Fecha:", fecha)
print("Hora:", hora)