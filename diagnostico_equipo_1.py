print("===== DIAGNÓSTICO INTELIGENTE DE EQUIPO =====")

modelo = input("¿Qué modelo es tu equipo?: ")

uso = int(input("¿Cuántos años de uso tiene?: "))

ram = int(input("¿Cuánta RAM tiene? (GB): "))

tiempo = int(input("¿Cuántos segundos tarda en encender?: "))

procesador = input("¿Qué procesador tiene?: ")

electricidad = input("¿Tiene electricidad? (s/n): ").lower() == "s"

enciende = input("¿Enciende? (s/n): ").lower() == "s"

imagen = input("¿Muestra imagen? (s/n): ").lower() == "s"



# Variables para el diagnóstico
riesgo = 0
problemas = []
recomendaciones = []


print("\nAnalizando equipo...")


# Revisar electricidad
if not electricidad:
    riesgo += 5
    problemas.append("No recibe electricidad.")
    recomendaciones.append("Revisar el cable, enchufe o alimentación eléctrica.")


# Revisar encendido
elif not enciende:
    riesgo += 5
    problemas.append("El equipo no enciende.")
    recomendaciones.append("Revisar la fuente de poder o el cargador.")


# Revisar imagen
elif not imagen:
    riesgo += 4
    problemas.append("El equipo enciende pero no muestra imagen.")
    recomendaciones.append("Revisar monitor, RAM y cable de video.")


# Revisar RAM
if ram < 4:
    riesgo += 4
    problemas.append("RAM muy baja.")
    recomendaciones.append("Aumentar la RAM a 8 GB o más.")

elif ram < 8:
    riesgo += 2
    problemas.append("RAM limitada.")
    recomendaciones.append("Considerar aumentar la RAM.")


# Revisar tiempo de encendido
if tiempo > 120:
    riesgo += 4
    problemas.append("Tiempo de arranque muy alto.")
    recomendaciones.append("Revisar programas de inicio y almacenamiento.")

elif tiempo > 60:
    riesgo += 2
    problemas.append("Tiempo de arranque elevado.")
    recomendaciones.append("Realizar mantenimiento y revisar programas de inicio.")


# Revisar años de uso
if uso >= 8:
    riesgo += 4
    problemas.append("Equipo con muchos años de uso.")
    recomendaciones.append("Considerar actualizar o reemplazar algunos componentes.")

elif uso >= 5:
    riesgo += 2
    problemas.append("Equipo con varios años de uso.")
    recomendaciones.append("Realizar mantenimiento preventivo.")


# Determinar nivel de riesgo
if riesgo >= 10:
    nivel = "CRÍTICO"

elif riesgo >= 6:
    nivel = "ALTO"

elif riesgo >= 3:
    nivel = "MEDIO"

else:
    nivel = "BAJO"


# Mostrar resultados
print("\n===== RESULTADO DEL ANÁLISIS =====")

print("Modelo:", modelo)
print("Procesador:", procesador)
print("RAM:", ram, "GB")
print("Años de uso:", uso)
print("Tiempo de encendido:", tiempo, "segundos")

print("\nNivel de riesgo:", nivel)
print("Puntuación:", riesgo)


print("\n===== PROBLEMAS DETECTADOS =====")

if len(problemas) == 0:
    print("No se detectaron problemas importantes.")

else:
    for problema in problemas:
        print("-", problema)


print("\n===== RECOMENDACIONES =====")

if len(recomendaciones) == 0:
    print("El equipo tiene un funcionamiento adecuado.")

else:
    for recomendacion in recomendaciones:
        print("-", recomendacion)


print("\n===== DIAGNÓSTICO FINAL =====")

if nivel == "CRÍTICO":
    print("El equipo presenta varios problemas y necesita atención.")

elif nivel == "ALTO":
    print("El equipo presenta problemas importantes y se recomienda mantenimiento.")

elif nivel == "MEDIO":
    print("El equipo funciona, pero presenta algunos aspectos que pueden mejorarse.")

else:
    print("El equipo presenta un funcionamiento adecuado.")
