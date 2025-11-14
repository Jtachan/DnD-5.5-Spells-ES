# Regex para los sistemas de unidades:
_METRIC_UNITS_REGEX = r"[kmc]?m|kg|l"
_IMPERIAL_UNITS_REGEX = r"pies?|pulgadas?|millas?|galón|galones|libras?"

METRIC_SYSTEM_REGEX = rf"((\d+,)?\d+) ({_METRIC_UNITS_REGEX})[\s.,]"
IMPERIAL_SYSTEM_REGEX = rf"((\d+,)?\d+) ({_IMPERIAL_UNITS_REGEX})[\s.,]"

# Condiciones adicionales que aparecen en el campo de 'tiempo de lanzamiento'.
# Estas descripciones se mueven directamente al campo de 'descripcion'.
CONDITIONAL_ACTION_TEXT = {
    "que realizas de inmediato tras acertar a un objetivo con un arma cuerpo a cuerpo o un ataque sin armas": "El conjuro se realiza de inmediato tras acertar al objetivo con un arma cuerpo a cuerpo o un ataque sin armas.",
    "que realizas de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas": "El conjuro se realiza de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas.",
    "que realizas de inmediato tras acertar a una criatura con un arma a distancia": "El conjuro se realiza de inmediato tras acertar a una criatura con un arma a distancia.",
    "que llevas a cabo cuando tú o una criatura que puedes ver a 18 m o menos de ti caigáis": "El conjuro se lleva a cabo cuando tú o una criatura que puedes ver a 18 m o menos de ti caigáis.",
    "que llevas a cabo cuando una criatura que puedas ver a 18 m o menos de ti lance un conjuro usando componentes verbales, somáticos o materiales": "El conjuro se lleva a cabo cuando una criatura que puedas ver a 18 m o menos de ti lance un conjuro usando componentes verbales, somáticos o materiales.",
    "que llevas a cabo en respuesta a recibir daño de una criatura que puedas ver a 18 m o menos de ti": "El conjuro se lleva a cabo en respuesta a recibir daño de una criatura que puedas ver a 18 m o menos de ti.",
    "que llevas a cabo cuando te acierta una tirada de ataque o eres el objetivo del conjuro proyectil mágico": "El conjuro se lleva a cabo en respuesta al ser acertado por una tirada de ataque o ser objetivo del conjuro <i>proyectil mágico</i>.",
}

# Valores del campo de 'alcance' que no deberían estar en una lista:
NO_LIST_VALS_ALCANCE = ["Lanzador", "Toque", "Especial", "Vista", "Ilimitado"]

# Nombres de las carpetas conteniendo las distintas ediciones
FOLDER_EDITIONS = ("ed5_0", "ed5_5")
