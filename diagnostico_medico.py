from datetime import datetime


print("====================================================")
print("          SISTEMA EXPERTO DE DIAGNÓSTICO MEDICO")
print("====================================================")


# ==========================================================
# 2. FECHA Y HORA DE LA CONSULTA
# ==========================================================

fecha_hora = datetime.now()

fecha = fecha_hora.strftime("%d/%m/%Y")
hora = fecha_hora.strftime("%H:%M:%S")


# ==========================================================
# 3. DATOS DEL PACIENTE
# ==========================================================

print("\n--- INGRESE SUS DATOS ---")

nombre = input("Nombre del paciente: ")
edad = int(input("Edad: "))
sexo = input("Sexo (M/F): ").upper()
peso = float(input("Peso en kg: "))
estatura = float(input("Estatura en metros: "))


# ==========================================================
# 4. CLASIFICACIÓN POR EDAD
# ==========================================================

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


# ==========================================================
# 5. INFORMACIÓN GENERAL DE LOS SÍNTOMAS
# ==========================================================

print("\n--- INFORMACIÓN DE LOS SÍNTOMAS ---")

tiempo_sintomas = int(
    input("¿Cuántos días lleva con los síntomas?: ")
)

intensidad = int(
    input("¿Qué tan fuertes son los síntomas? (1-10): ")
)

empeorando = input(
    "¿Los síntomas están empeorando? (s/n): "
).lower()


# ==========================================================
# 6. DETERMINAR GRAVEDAD
# ==========================================================

if intensidad <= 3:
    gravedad = "Leve"

elif intensidad <= 6:
    gravedad = "Moderada"

else:
    gravedad = "Severa"


# ==========================================================
# 7. EVOLUCIÓN DE LOS SÍNTOMAS
# ==========================================================

if tiempo_sintomas <= 2:
    evolucion = "Inicio de síntomas"

elif tiempo_sintomas <= 7:
    evolucion = "Síntomas en evolución"

else:
    evolucion = "Síntomas persistentes"


# ==========================================================
# 8. VARIABLES INICIALES
# ==========================================================

diagnostico = "Posible malestar general"

recomendacion = (
    "Mantener hidratación, descansar y observar la evolución "
    "de los síntomas."
)


# ==========================================================
# 9. NIÑOS
# ==========================================================

if edad <= 10:

    print("\n--- SÍNTOMAS PARA NIÑOS ---")

    dolor_garganta = input(
        "¿Tiene dolor de garganta? (s/n): "
    ).lower()

    dificultad_tragar = input(
        "¿Tiene dificultad para tragar? (s/n): "
    ).lower()

    fiebre = input(
        "¿Tiene fiebre? (s/n): "
    ).lower()

    dolor_oido = input(
        "¿Tiene dolor de oído? (s/n): "
    ).lower()

    irritabilidad = input(
        "¿Está más irritable de lo normal? (s/n): "
    ).lower()

    dolor_abdominal = input(
        "¿Tiene dolor abdominal? (s/n): "
    ).lower()

    nauseas = input(
        "¿Tiene náuseas? (s/n): "
    ).lower()

    vomito = input(
        "¿Ha presentado vómito? (s/n): "
    ).lower()

    cansancio = input(
        "¿Presenta mucho cansancio? (s/n): "
    ).lower()

    escalofrios = input(
        "¿Tiene escalofríos? (s/n): "
    ).lower()

    escurrimiento_nasal = input(
        "¿Tiene escurrimiento nasal? (s/n): "
    ).lower()

    estornudos = input(
        "¿Tiene estornudos frecuentes? (s/n): "
    ).lower()

    tos = input(
        "¿Tiene tos? (s/n): "
    ).lower()


    # ------------------------------------------------------
    # DIAGNÓSTICO INFANTIL
    # ------------------------------------------------------

    if (
        dolor_garganta == "s"
        and dificultad_tragar == "s"
        and fiebre == "s"
    ):

        diagnostico = "Posible infección de garganta"

        recomendacion = (
            "Mantener una adecuada hidratación, ofrecer líquidos "
            "y alimentos suaves. Evitar alimentos muy irritantes "
            "y vigilar la fiebre y la dificultad para tragar."
        )

    elif (
        dolor_oido == "s"
        and fiebre == "s"
        and irritabilidad == "s"
    ):

        diagnostico = "Posible infección de oído"

        recomendacion = (
            "Evitar introducir objetos o líquidos en el oído. "
            "Mantener reposo, vigilar la temperatura y observar "
            "si el dolor aumenta."
        )

    elif (
        dolor_abdominal == "s"
        and nauseas == "s"
        and vomito == "s"
    ):

        diagnostico = "Posible problema gastrointestinal"

        recomendacion = (
            "Mantener hidratación mediante pequeños sorbos de líquidos "
            "y ofrecer alimentos ligeros cuando sean tolerados. "
            "Vigilar la frecuencia del vómito y el dolor abdominal."
        )

    elif (
        fiebre == "s"
        and cansancio == "s"
        and escalofrios == "s"
    ):

        diagnostico = "Posible cuadro infeccioso con fiebre"

        recomendacion = (
            "Controlar periódicamente la temperatura, mantener hidratación "
            "y proporcionar reposo. Observar cambios en el estado general "
            "del niño."
        )

    elif (
        escurrimiento_nasal == "s"
        and estornudos == "s"
        and tos == "s"
    ):

        diagnostico = "Posible resfriado común"

        recomendacion = (
            "Mantener buena hidratación, permitir suficiente descanso "
            "y mantener limpio el ambiente. Vigilar la temperatura "
            "y la evolución de la tos."
        )

    elif (
        tos == "s"
        or escurrimiento_nasal == "s"
        or estornudos == "s"
    ):

        diagnostico = "Posible cuadro respiratorio"

        recomendacion = (
            "Mantener hidratación y reposo. Evitar humo, polvo y otros "
            "irritantes del ambiente. Vigilar la respiración y la aparición "
            "de fiebre."
        )

    elif (
        dolor_abdominal == "s"
        or nauseas == "s"
        or vomito == "s"
    ):

        diagnostico = "Posible malestar gastrointestinal"

        recomendacion = (
            "Ofrecer líquidos en pequeñas cantidades y evitar comidas "
            "muy pesadas o irritantes. Observar si aparecen vómitos "
            "frecuentes, fiebre o aumento del dolor."
        )

    elif dolor_oido == "s":

        diagnostico = "Posible afección del oído"

        recomendacion = (
            "Evitar manipular el oído y vigilar la intensidad del dolor. "
            "Mantener reposo y observar si aparece fiebre o secreción."
        )

    elif dolor_garganta == "s":

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


# ==========================================================
# 10. ADOLESCENTES
# ==========================================================

elif edad <= 17:

    print("\n--- SÍNTOMAS PARA ADOLESCENTES ---")

    granitos = input(
        "¿Tiene granitos o brotes en la piel? (s/n): "
    ).lower()

    piel_grasa = input(
        "¿Tiene la piel muy grasa? (s/n): "
    ).lower()

    dolor_cabeza = input(
        "¿Tiene dolor de cabeza? (s/n): "
    ).lower()

    sensibilidad_luz = input(
        "¿La luz le molesta? (s/n): "
    ).lower()

    dolor_estomago = input(
        "¿Tiene dolor de estómago? (s/n): "
    ).lower()

    ardor_estomago = input(
        "¿Tiene ardor en el estómago? (s/n): "
    ).lower()

    dolor_garganta = input(
        "¿Tiene dolor de garganta? (s/n): "
    ).lower()

    dificultad_tragar = input(
        "¿Tiene dificultad para tragar? (s/n): "
    ).lower()

    ojos_rojos = input(
        "¿Tiene los ojos rojos? (s/n): "
    ).lower()

    lagrimeo = input(
        "¿Tiene lagrimeo frecuente? (s/n): "
    ).lower()


    # ------------------------------------------------------
    # DIAGNÓSTICO ADOLESCENTE
    # ------------------------------------------------------

    if granitos == "s" and piel_grasa == "s":

        diagnostico = "Posible acné"

        recomendacion = (
            "Lavar la piel suavemente, evitar exprimir o manipular "
            "los granitos y mantener limpia la zona afectada. "
            "Observar la evolución de los brotes."
        )

    elif dolor_cabeza == "s" and sensibilidad_luz == "s":

        diagnostico = "Posible migraña"

        recomendacion = (
            "Descansar en un lugar tranquilo, con poca luz y poco ruido. "
            "Mantener hidratación y reducir temporalmente el uso de pantallas. "
            "Observar la intensidad y duración del dolor."
        )

    elif dolor_estomago == "s" and ardor_estomago == "s":

        diagnostico = "Posible gastritis o irritación estomacal"

        recomendacion = (
            "Preferir comidas ligeras, evitar alimentos muy irritantes, "
            "grasosos o picantes y mantener horarios regulares de comida. "
            "Observar si disminuye el ardor."
        )

    elif dolor_garganta == "s" and dificultad_tragar == "s":

        diagnostico = "Posible faringitis"

        recomendacion = (
            "Mantener hidratación, consumir líquidos y evitar alimentos "
            "que irriten la garganta. Vigilar la aparición de fiebre "
            "y el aumento de la dificultad para tragar."
        )

    elif ojos_rojos == "s" and lagrimeo == "s":

        diagnostico = "Posible irritación o conjuntivitis"

        recomendacion = (
            "Evitar frotarse los ojos, lavarse las manos con frecuencia "
            "y evitar compartir toallas. Vigilar la aparición de secreción "
            "o cambios en la visión."
        )

    elif granitos == "s" or piel_grasa == "s":

        diagnostico = "Posible problema dermatológico"

        recomendacion = (
            "Mantener una higiene suave de la piel, evitar manipular "
            "los brotes y observar si aumentan o cambian de apariencia."
        )

    elif dolor_cabeza == "s":

        diagnostico = "Posible cefalea"

        recomendacion = (
            "Descansar, mantener hidratación, reducir temporalmente "
            "el uso de pantallas y observar la intensidad y duración "
            "del dolor."
        )

    elif dolor_estomago == "s" or ardor_estomago == "s":

        diagnostico = "Posible malestar digestivo"

        recomendacion = (
            "Consumir alimentos ligeros, evitar irritantes y mantener "
            "una adecuada hidratación. Observar la evolución del malestar."
        )

    elif ojos_rojos == "s" or lagrimeo == "s":

        diagnostico = "Posible irritación ocular"

        recomendacion = (
            "Evitar frotarse los ojos, descansar la vista y reducir "
            "la exposición prolongada a pantallas. Vigilar la evolución."
        )

    elif dolor_garganta == "s":

        diagnostico = "Posible irritación de garganta"

        recomendacion = (
            "Mantener hidratación, consumir líquidos y evitar humo "
            "u otros irritantes. Vigilar la aparición de fiebre."
        )

    else:

        diagnostico = "Posible malestar general en adolescente"

        recomendacion = (
            "Mantener hidratación, descansar adecuadamente y observar "
            "la evolución de los síntomas."
        )


# ==========================================================
# 11. ADULTOS JÓVENES
# ==========================================================

elif edad <= 39:

    print("\n--- SÍNTOMAS PARA ADULTOS JÓVENES ---")

    estornudos = input(
        "¿Tiene estornudos frecuentes? (s/n): "
    ).lower()

    comezon_nariz = input(
        "¿Tiene comezón en la nariz? (s/n): "
    ).lower()

    dolor_cabeza = input(
        "¿Tiene dolor de cabeza? (s/n): "
    ).lower()

    cansancio = input(
        "¿Tiene cansancio? (s/n): "
    ).lower()

    diarrea = input(
        "¿Tiene diarrea? (s/n): "
    ).lower()

    dolor_abdominal = input(
        "¿Tiene dolor abdominal? (s/n): "
    ).lower()

    dificultad_dormir = input(
        "¿Tiene dificultad para dormir? (s/n): "
    ).lower()

    dolor_muscular = input(
        "¿Tiene dolor muscular? (s/n): "
    ).lower()

    rigidez = input(
        "¿Tiene rigidez muscular? (s/n): "
    ).lower()


    # ------------------------------------------------------
    # DIAGNÓSTICO ADULTO JOVEN
    # ------------------------------------------------------

    if estornudos == "s" and comezon_nariz == "s":

        diagnostico = "Posible alergia respiratoria"

        recomendacion = (
            "Identificar y evitar posibles desencadenantes como polvo, "
            "humo, perfumes o cambios ambientales. Mantener ventilado "
            "el espacio y observar cuándo aparecen los síntomas."
        )

    elif dolor_cabeza == "s" and cansancio == "s":

        diagnostico = "Posible cefalea asociada a cansancio"

        recomendacion = (
            "Priorizar el descanso, mantener hidratación y realizar pausas "
            "si se trabaja frente a pantallas. Observar si el dolor disminuye "
            "al descansar."
        )

    elif diarrea == "s" and dolor_abdominal == "s":

        diagnostico = "Posible problema gastrointestinal"

        recomendacion = (
            "Mantener una adecuada hidratación, consumir alimentos ligeros "
            "y evitar comidas muy grasosas o irritantes. Vigilar la frecuencia "
            "de la diarrea y la intensidad del dolor."
        )

    elif dificultad_dormir == "s" and cansancio == "s":

        diagnostico = "Posible alteración del sueño"

        recomendacion = (
            "Establecer horarios regulares para dormir, reducir pantallas "
            "antes de acostarse y evitar bebidas estimulantes por la noche. "
            "Observar la calidad del descanso."
        )

    elif dolor_muscular == "s" and rigidez == "s":

        diagnostico = "Posible problema muscular"

        recomendacion = (
            "Reducir temporalmente los esfuerzos físicos, permitir descanso "
            "a los músculos y realizar movimientos suaves sin forzar la zona. "
            "Observar si disminuye el dolor."
        )

    elif estornudos == "s" or comezon_nariz == "s":

        diagnostico = "Posible irritación o alergia respiratoria"

        recomendacion = (
            "Evitar polvo, humo y otros posibles desencadenantes. "
            "Mantener limpio y ventilado el espacio donde permanece "
            "la persona."
        )

    elif dolor_cabeza == "s":

        diagnostico = "Posible cefalea"

        recomendacion = (
            "Descansar, mantener hidratación y reducir temporalmente "
            "la exposición a pantallas o ambientes muy ruidosos. "
            "Observar la duración del dolor."
        )

    elif diarrea == "s" or dolor_abdominal == "s":

        diagnostico = "Posible malestar gastrointestinal"

        recomendacion = (
            "Mantener hidratación, preferir alimentos ligeros y evitar "
            "alimentos irritantes o muy grasosos mientras persistan "
            "los síntomas."
        )

    elif dificultad_dormir == "s":

        diagnostico = "Posible alteración del sueño"

        recomendacion = (
            "Mantener horarios regulares de descanso, disminuir el uso "
            "de pantallas antes de dormir y procurar un ambiente tranquilo."
        )

    elif dolor_muscular == "s" or rigidez == "s":

        diagnostico = "Posible molestia muscular"

        recomendacion = (
            "Evitar sobrecargas físicas, permitir descanso muscular "
            "y realizar movimientos suaves sin provocar dolor."
        )

    else:

        diagnostico = "Posible malestar general en adulto joven"

        recomendacion = (
            "Mantener hidratación, descansar adecuadamente y observar "
            "la evolución de los síntomas."
        )


# ==========================================================
# 12. ADULTOS
# ==========================================================

elif edad <= 59:

    print("\n--- SÍNTOMAS PARA ADULTOS ---")

    presion_sistolica = int(
        input("Ingrese el primer valor de la presión: ")
    )

    presion_diastolica = int(
        input("Ingrese el segundo valor de la presión: ")
    )

    dolor_cabeza = input(
        "¿Tiene dolor de cabeza? (s/n): "
    ).lower()

    mareo = input(
        "¿Tiene mareo? (s/n): "
    ).lower()

    mucha_sed = input(
        "¿Tiene mucha sed? (s/n): "
    ).lower()

    orinar_frecuente = input(
        "¿Orina con mucha frecuencia? (s/n): "
    ).lower()

    acidez = input(
        "¿Tiene acidez? (s/n): "
    ).lower()

    dolor_estomago = input(
        "¿Tiene dolor de estómago? (s/n): "
    ).lower()

    ardor_orinar = input(
        "¿Tiene ardor al orinar? (s/n): "
    ).lower()

    dolor_abdominal = input(
        "¿Tiene dolor abdominal? (s/n): "
    ).lower()

    cansancio = input(
        "¿Tiene cansancio? (s/n): "
    ).lower()


    # ------------------------------------------------------
    # DIAGNÓSTICO ADULTO
    # ------------------------------------------------------

    if (
        presion_sistolica >= 140
        or presion_diastolica >= 90
    ):

        if dolor_cabeza == "s" and mareo == "s":

            diagnostico = "Posible presión arterial elevada con síntomas"

            recomendacion = (
                "Permanecer en reposo unos minutos y repetir la medición "
                "de presión correctamente. Registrar el resultado y evitar "
                "actividad física intensa mientras persistan el dolor de cabeza "
                "y el mareo."
            )

        else:

            diagnostico = "Posible presión arterial elevada"

            recomendacion = (
                "Permanecer en reposo y repetir la medición después de unos "
                "minutos. Registrar los valores obtenidos y evitar esfuerzos "
                "físicos inmediatamente después de la medición."
            )

    elif mucha_sed == "s" and orinar_frecuente == "s":

        diagnostico = "Posible alteración de glucosa"

        recomendacion = (
            "Mantener una alimentación equilibrada, evitar un consumo excesivo "
            "de bebidas azucaradas y registrar la frecuencia de la sed y la "
            "orina. Considerar una medición de glucosa para conocer los valores."
        )

    elif acidez == "s" and dolor_estomago == "s":

        diagnostico = "Posible gastritis o reflujo"

        recomendacion = (
            "Realizar comidas ligeras, evitar alimentos muy picantes, grasosos "
            "o irritantes y evitar acostarse inmediatamente después de comer. "
            "Observar cuándo aparecen la acidez y el dolor."
        )

    elif ardor_orinar == "s" and dolor_abdominal == "s":

        diagnostico = "Posible infección urinaria"

        recomendacion = (
            "Mantener una adecuada hidratación y observar la frecuencia "
            "del ardor, el dolor abdominal y cualquier cambio al orinar."
        )

    elif cansancio == "s" and mareo == "s":

        diagnostico = "Posible cuadro de cansancio y mareo"

        recomendacion = (
            "Descansar, mantener hidratación y evitar levantarse rápidamente "
            "o realizar actividades que requieran mucho esfuerzo mientras "
            "continúe el mareo."
        )

    elif mucha_sed == "s" or orinar_frecuente == "s":

        diagnostico = "Posible alteración metabólica"

        recomendacion = (
            "Mantener hidratación, evitar el exceso de bebidas azucaradas "
            "y registrar la frecuencia de la sed o la necesidad de orinar "
            "para observar su evolución."
        )

    elif acidez == "s" or dolor_estomago == "s":

        diagnostico = "Posible problema digestivo"

        recomendacion = (
            "Preferir alimentos ligeros, reducir comidas muy grasosas, "
            "picantes o irritantes y evitar acostarse inmediatamente "
            "después de comer."
        )

    elif ardor_orinar == "s":

        diagnostico = "Posible problema urinario"

        recomendacion = (
            "Mantener una adecuada hidratación y observar la frecuencia "
            "del ardor y cualquier cambio en la orina."
        )

    elif dolor_cabeza == "s":

        diagnostico = "Posible cefalea"

        recomendacion = (
            "Descansar en un ambiente tranquilo, mantener hidratación "
            "y reducir temporalmente el uso de pantallas. Observar "
            "la duración e intensidad del dolor."
        )

    elif cansancio == "s":

        diagnostico = "Posible cuadro de fatiga"

        recomendacion = (
            "Priorizar el descanso, mantener horarios adecuados de sueño, "
            "hidratarse y observar si el cansancio disminuye con el reposo."
        )

    else:

        diagnostico = "Posible malestar general en adulto"

        recomendacion = (
            "Mantener hidratación, descansar adecuadamente y observar "
            "la evolución de cualquier síntoma."
        )


# ==========================================================
# 13. ADULTOS MAYORES
# ==========================================================

else:

    print("\n--- SÍNTOMAS PARA ADULTOS MAYORES ---")

    presion_sistolica = int(
        input("Ingrese el primer valor de la presión: ")
    )

    presion_diastolica = int(
        input("Ingrese el segundo valor de la presión: ")
    )

    dolor_cabeza = input(
        "¿Tiene dolor de cabeza? (s/n): "
    ).lower()

    mareo = input(
        "¿Tiene mareo? (s/n): "
    ).lower()

    mucha_sed = input(
        "¿Tiene mucha sed? (s/n): "
    ).lower()

    orinar_frecuente = input(
        "¿Orina con mucha frecuencia? (s/n): "
    ).lower()

    dolor_articulaciones = input(
        "¿Tiene dolor en las articulaciones? (s/n): "
    ).lower()

    rigidez = input(
        "¿Tiene rigidez en las articulaciones? (s/n): "
    ).lower()

    dolor_huesos = input(
        "¿Tiene dolor en los huesos? (s/n): "
    ).lower()

    debilidad = input(
        "¿Presenta debilidad? (s/n): "
    ).lower()

    fiebre = input(
        "¿Tiene fiebre? (s/n): "
    ).lower()

    tos = input(
        "¿Tiene tos? (s/n): "
    ).lower()


    # ------------------------------------------------------
    # DIAGNÓSTICO ADULTO MAYOR
    # ------------------------------------------------------

    if (
        presion_sistolica >= 140
        or presion_diastolica >= 90
    ):

        if dolor_cabeza == "s" and mareo == "s":

            diagnostico = "Posible presión arterial elevada con síntomas"

            recomendacion = (
                "Permanecer en reposo y repetir la medición después de unos "
                "minutos. Registrar los valores obtenidos y evitar esfuerzos "
                "físicos mientras continúen el mareo y el dolor de cabeza."
            )

        else:

            diagnostico = "Posible presión arterial elevada"

            recomendacion = (
                "Permanecer en reposo y repetir la medición correctamente. "
                "Registrar los valores para comparar posteriormente y mantener "
                "un control periódico de la presión."
            )

    elif mucha_sed == "s" and orinar_frecuente == "s":

        diagnostico = "Posible alteración de glucosa"

        recomendacion = (
            "Mantener hidratación, evitar el exceso de bebidas azucaradas "
            "y registrar la frecuencia de la sed y la orina. Considerar "
            "una medición de glucosa para conocer los valores."
        )

    elif (
        dolor_articulaciones == "s"
        and rigidez == "s"
    ):

        diagnostico = "Posible problema articular"

        recomendacion = (
            "Evitar sobrecargar las articulaciones, realizar movimientos "
            "suaves y mantener periodos adecuados de descanso. Observar "
            "si disminuyen el dolor y la rigidez."
        )

    elif dolor_huesos == "s" and debilidad == "s":

        diagnostico = "Posible problema musculoesquelético"

        recomendacion = (
            "Evitar esfuerzos físicos excesivos, mantener periodos de descanso "
            "y realizar movimientos suaves según la tolerancia. Vigilar "
            "la intensidad del dolor y la debilidad."
        )

    elif fiebre == "s" and tos == "s":

        diagnostico = "Posible infección respiratoria"

        recomendacion = (
            "Mantener hidratación, descansar y controlar periódicamente "
            "la temperatura. Evitar humo y otros irritantes respiratorios "
            "y vigilar cualquier dificultad para respirar."
        )

    elif dolor_articulaciones == "s" or rigidez == "s":

        diagnostico = "Posible problema articular"

        recomendacion = (
            "Evitar movimientos que aumenten el dolor, permitir descanso "
            "a las articulaciones y realizar movimientos suaves sin forzar."
        )

    elif dolor_huesos == "s" or debilidad == "s":

        diagnostico = "Posible problema musculoesquelético"

        recomendacion = (
            "Reducir los esfuerzos físicos, permitir descanso y observar "
            "si el dolor o la debilidad cambian durante el día."
        )

    elif fiebre == "s" or tos == "s":

        diagnostico = "Posible cuadro respiratorio"

        recomendacion = (
            "Mantener hidratación y reposo, controlar la temperatura "
            "y observar la evolución de la tos y la respiración."
        )

    elif mucha_sed == "s" or orinar_frecuente == "s":

        diagnostico = "Posible alteración metabólica"

        recomendacion = (
            "Mantener hidratación, reducir bebidas azucaradas y registrar "
            "la frecuencia de la sed y la necesidad de orinar."
        )

    elif dolor_cabeza == "s" or mareo == "s":

        diagnostico = "Posible cuadro de cefalea o mareo"

        recomendacion = (
            "Descansar, mantener hidratación y levantarse lentamente "
            "para evitar cambios bruscos de posición. Observar la intensidad "
            "y duración de los síntomas."
        )

    else:

        diagnostico = "Posible malestar general en adulto mayor"

        recomendacion = (
            "Mantener hidratación, descansar adecuadamente y observar "
            "cualquier cambio en el estado general o aparición de nuevos síntomas."
        )


# ==========================================================
# 14. RECOMENDACIONES SEGÚN LA GRAVEDAD
# ==========================================================

if gravedad == "Leve":

    recomendacion += (
        " La intensidad registrada es leve; continuar con las medidas "
        "anteriores y observar si los síntomas disminuyen."
    )

elif gravedad == "Moderada":

    recomendacion += (
        " La intensidad registrada es moderada; se recomienda reducir "
        "las actividades que puedan aumentar las molestias y vigilar "
        "la evolución durante las siguientes horas."
    )

else:

    recomendacion += (
        " La intensidad registrada es severa; se recomienda suspender "
        "actividades que puedan empeorar las molestias y buscar atención "
        "sanitaria si la intensidad continúa o aparecen señales de alarma."
    )


# ==========================================================
# 15. RECOMENDACIÓN SEGÚN LA EVOLUCIÓN
# ==========================================================

if evolucion == "Síntomas persistentes":

    recomendacion += (
        " Los síntomas llevan más de una semana, por lo que es importante "
        "dar seguimiento a su evolución y buscar atención sanitaria si "
        "no presentan mejoría."
    )


# ==========================================================
# 16. ALERTAS
# ==========================================================

alerta = (
    "No se detectaron señales de alerta según los datos ingresados."
)

if intensidad >= 9:

    alerta = (
        "ATENCIÓN: La intensidad de los síntomas es muy alta. "
        "Se recomienda buscar atención sanitaria de manera prioritaria."
    )

elif empeorando == "s":

    alerta = (
        "ATENCIÓN: Los síntomas están empeorando. "
        "Se recomienda suspender actividades que puedan agravarlos "
        "y buscar atención sanitaria si continúan aumentando."
    )


# ==========================================================
# 17. RESULTADO FINAL
# ==========================================================

print("\n")
print("====================================================")
print("                 RESULTADO")
print("====================================================")

print("\n--- DATOS DEL PACIENTE ---")

print("Nombre:", nombre)
print("Edad:", edad)
print("Sexo:", sexo)
print("Peso:", peso, "kg")
print("Estatura:", estatura, "m")
print("Rango de edad:", rango)

print("\n--- EVALUACIÓN ---")

print("Tiempo con síntomas:", tiempo_sintomas, "días")
print("Intensidad:", intensidad, "/10")
print("Gravedad:", gravedad)
print("Evolución:", evolucion)
print("¿Está empeorando?:", empeorando)

print("\n--- POSIBLE DIAGNÓSTICO ---")

print(diagnostico)

print("\n--- RECOMENDACIÓN ---")

print(recomendacion)

print("\n--- ALERTA ---")

print(alerta)

print("\n--- FECHA Y HORA DE LA CONSULTA ---")

print("Fecha:", fecha)
print("Hora:", hora)

