"""Konstanten für die KWL Fränkische Rohrwerke Integration."""
DOMAIN = "kwl_fraenkische"

# Nennleistung pro Lueeftungsstufe in Watt (gemessen)
LEVEL_TO_WATT: dict[int, float] = {
    1: 11.0,
    2: 17.5,
    3: 43.5,
    4: 80.0,
}

# Config Entry Keys fuer Watt-Werte
CONF_WATT_LEVEL_1 = "watt_level_1"
CONF_WATT_LEVEL_2 = "watt_level_2"
CONF_WATT_LEVEL_3 = "watt_level_3"
CONF_WATT_LEVEL_4 = "watt_level_4"

# Standardwerte (gemessen an Profi-Air 400)
DEFAULT_WATT = {1: 11.0, 2: 17.5, 3: 43.5, 4: 80.0}

# Alle bekannten XML-Tags aus status.xml
# Wird fuer unknown_tags Discovery genutzt
ALL_KNOWN_TAGS: frozenset[str] = frozenset({
    # Temperaturen
    "abl0", "zul0", "aul0", "fol0",
    # Motor RPM
    "MoStZlUm", "MoStAlUm",
    # Motor Spannung
    "MoStZlVo", "MoStAlVo",
    # Airflow Volt pro Stufe
    "st1z", "st1a", "st2z", "st2a",
    "st3z", "st3a", "st4z", "st4a",
    # Betriebsstunden
    "BsSt1", "BsSt2", "BsSt3", "BsSt4",
    "BsFs", "BsVhr",
    # Temperaturkorrekturen
    "kor1", "kor2", "kor3", "kor4",
    # Status / Steuerung
    "safety", "passiv", "vorheiz", "installtyp",
    "filter0", "filtertime", "rest_time",
    "sensortyp1", "sensortyp2", "sensortyp3", "sensortyp4",
    "S1amb0", "S2amb0", "S3amb0", "S4amb0",
    "meldung", "grundst", "nachlauf",
    "config_mac", "config_ip",
    "bypass", "partytime", "aktuell0", "control0",
    "BipaAutAUL", "BipaAutABL",
    "stufe1", "stufe2", "stufe3", "stufe4",
    "SprachWahl",
})

# Bekannte Endpunkte
ENDPOINT_INSTALL = "/install/install.htm"
ENDPOINT_TIME    = "/time.htm"
ENDPOINT_WOPLA   = "/wopla.htm"
ENDPOINT_SETUP   = "/setup.htm"
ENDPOINT_STATUS  = "/status.xml"
