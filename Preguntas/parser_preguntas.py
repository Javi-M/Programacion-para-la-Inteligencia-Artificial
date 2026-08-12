# Un script para recorrer todas las preguntas y guardarlas en un CSV.
# Es importante mantener la forma de escribir las preguntas-respuestas.
# (En este código se entiende por qué).

# GENERADO CON CHATGPT:
import re

def parser_preguntas(archivo_entrada) -> list[dict[str, str]]:
    """ 
    Parsea las preguntas de un archivo y devuelve una lista de diccionarios.
    
    Cada diccionario está asociado a una pregunta-respuesta-aclaración.

    Está pensado para construir una tabla, por lo que las claves del diccionario
    son nombradas como "columnas". Diccionario con las keys:
    
    - archivo
    - actual_h1
    - actual_h2
    - actual_h3
    - preguntas
    - respuesta
    - aclaracion

    """
    columnas = [
        "archivo",
        "actual_h1",
        "actual_h2",
        "actual_h3",
        "pregunta",
        "respuesta",
        "aclaracion",
    ]

    resultados = []

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    h1 = h2 = h3 = ""
    en_comentario = False
    en_note = False
    en_tip = False

    pregunta = []
    respuesta = []
    aclaracion = []

    for linea in lineas:

        # ---------------------------------------------------------------
        # Ignorar comentarios HTML <!-- ... -->
        # ---------------------------------------------------------------
        if en_comentario:
            if "-->" in linea:
                en_comentario = False
                linea = linea.split("-->", 1)[1]
            else:
                continue

        while "<!--" in linea:
            antes, resto = linea.split("<!--", 1)

            if "-->" in resto:
                linea = antes + resto.split("-->", 1)[1]
            else:
                linea = antes
                en_comentario = True
                break

        if en_comentario and not linea.strip():
            continue

        # ---------------------------------------------------------------
        # Ignorar separadores
        # ---------------------------------------------------------------
        if linea.strip() == "---":
            continue

        # ---------------------------------------------------------------
        # Headings
        # ---------------------------------------------------------------
        if not en_note:
            m = re.match(r"^(#{1,3})\s+(.+?)\s*$", linea)

            if m:
                nivel = len(m.group(1))
                texto = m.group(2)

                if nivel == 1:
                    h1, h2, h3 = texto, "", ""
                elif nivel == 2:
                    h2, h3 = texto, ""
                elif nivel == 3:
                    h3 = texto

                continue

        # ---------------------------------------------------------------
        # Apertura de callout-note
        # ---------------------------------------------------------------
        if re.match(r"^\s*:::\s*\{[^}]*\bcallout-note\b", linea):
            en_note = True
            en_tip = False
            pregunta = []
            respuesta = []
            aclaracion = []
            continue

        # ---------------------------------------------------------------
        # Dentro de callout-note
        # ---------------------------------------------------------------
        if en_note:

            # Apertura de callout-tip
            if re.match(r"^\s*:::\s*\{[^}]*\bcallout-tip\b", linea):
                en_tip = True
                continue

            # Cierre del tip
            if linea.strip() == ":::" and en_tip:
                en_tip = False
                continue

            # Cierre del note
            if linea.strip() == ":::" and not en_tip:
                resultados.append({
                    "archivo": archivo_entrada,
                    "actual_h1": h1,
                    "actual_h2": h2,
                    "actual_h3": h3,
                    "pregunta": "".join(pregunta).strip(),
                    "respuesta": "".join(respuesta).strip(),
                    "aclaracion": "".join(aclaracion).strip(),
                })

                en_note = False
                continue

            # Contenido
            if en_tip:
                respuesta.append(linea)
            elif respuesta:
                aclaracion.append(linea)
            else:
                pregunta.append(linea)

    return resultados

# Ejemplo:
# preguntas_2 = parser_preguntas("preguntas_2.qmd")
# preguntas_2[0] contiene el primer diccionario.
# preguntas_2[0]["pregunta"] contiene... la primera pregunta.
# (La ruta depende de donde esté situado el wd, directorio de trabajo actual).