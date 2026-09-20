# =====================================
# TABLA DE VERDAD
# =====================================

valores = [True, False]

print("P   Q   ¬P   P∧Q   P∨Q   P→Q   P↔Q")
print("------------------------------------")

for P in valores:
    for Q in valores:

        negacion = not P
        conjuncion = P and Q
        disyuncion = P or Q
        condicional = (not P) or Q
        bicondicional = P == Q

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

        print(
            resultado_P,
            resultado_Q,
            resultado_negacion,
            resultado_conjuncion,
            resultado_disyuncion,
            resultado_condicional,
            resultado_bicondicional
        )