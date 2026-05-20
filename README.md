# KWL Fränkische Rohrwerke — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.3%2B-blue.svg)](https://www.home-assistant.io/)
[![Quality Scale](https://img.shields.io/badge/Quality%20Scale-Platinum-silver.svg)](https://developers.home-assistant.io/docs/core/integration-quality-scale/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Macht die **Fränkische Rohrwerke KWL** (Profi-Air) smart — ohne Cloud, ohne externen Dienst, ausschließlich über das lokale Netzwerk.

![Fränkische Rohrwerke](brand/logo.png)

---

## Funktionen

- **Lüftungsstufen 1–4** steuerbar als Fan-Entity mit Prozent-Schieberegler und Preset-Modi
- **Automatische Zeitsynchronisation** — beim Start und alle 24 Stunden, inkl. Sommer-/Winterzeit
- **Energie-Dashboard** — kumulativer kWh-Verbrauch pro Stufe basierend auf Betriebsstunden
- **Vollständiges Sensor-Mapping** — Temperaturen, Motor-RPM, Motorspannung
- **Bypass-Steuerung** — Manuell offen / Manuell zu / Automatisch
- **Temperaturkorrekturen** für alle vier Messfühler
- **HTTP Basic Auth** für den geschützten Installateur-Bereich
- **Optimistic Updates** — UI reagiert sofort ohne auf den nächsten Poll zu warten
- **Re-Auth Flow** — automatische Aufforderung bei abgelaufenen Zugangsdaten
- **Rekonfigurierung** — IP-Adresse und Zugangsdaten ohne Neueinrichtung änderbar
- **Repair Issue** — Filterwechsel-Alarm mit automatischer Quittierung am Gerät
- **Konfigurierbare Nennleistung** — Watt-Werte pro Stufe im Setup-Wizard einstellbar

---

## Unterstützte Geräte

Getestet mit der **Fränkische Rohrwerke Profi-Air** KWL-Anlage mit integriertem Webserver.

Das Gerät muss über HTTP erreichbar sein (Standard: `http://10.10.4.1`). Eine Internetverbindung ist nicht erforderlich.

---

## Installation

### Über HACS (empfohlen)

1. HACS öffnen → Integrationen → ⋮ → Benutzerdefinierte Repositories
2. URL eintragen: `https://github.com/johnnyh1975/ha-kwl-fraenkische`
3. Kategorie: Integration → Hinzufügen
4. Integration suchen und installieren
5. Home Assistant neu starten

### Manuell

1. Den Ordner `custom_components/kwl_fraenkische/` in dein HA-Konfigurationsverzeichnis kopieren
2. Home Assistant neu starten

---

## Einrichtung

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen**
2. Nach **KWL Fränkische Rohrwerke** suchen
3. **Schritt 1:** IP-Adresse der KWL eingeben (Standard: `10.10.4.1`)
4. **Schritt 2:** Installateur-Zugangsdaten eingeben
   - Benutzer: `install`
   - Passwort: `konfig12` *(Werkseinstellung — bitte ändern!)*
5. **Schritt 3:** Nennleistung pro Stufe bestätigen oder anpassen
   - Standardwerte gelten für die Profi-Air 400: 11 / 17.5 / 43.5 / 80 W
   - Eigene Werte können mit einer Strommesszange gemessen werden

> ⚠️ **Sicherheitshinweis:** Die Werkseinstellungen (`install` / `konfig12`) sind öffentlich bekannt. Bitte das Passwort direkt am Gerät unter `http://10.10.4.1/setup.htm` ändern.

### Neu konfigurieren

IP-Adresse oder Zugangsdaten können ohne Neueinrichtung geändert werden:
**Einstellungen → Geräte & Dienste → KWL → ⋮ → Neu konfigurieren**

---

## Entities

Alle Entities gehören zu einem einzigen Gerät **KWL** (identifiziert über die MAC-Adresse). Die Entity-IDs werden von HA aus dem Gerätenamen und dem Entitätsnamen generiert — typisch: `sensor.kwl_fraenkische_rohrwerke_abluft_temperatur`.

### Fan
| Entity | Beschreibung |
|--------|-------------|
| `fan.kwl_fraenkische_rohrwerke` | Lüftungssteuerung mit Stufe 1–4, Prozent und Preset-Modus |

**Preset-Modi** — exakte Namen für Automationen:
| Preset | Stufe | Prozent | Leistung (konfigurierbar) |
|--------|-------|---------|--------------------------|
| `Stufe 1 - Feuchteschutz` | 1 | 25% | Standard: 11 W |
| `Stufe 2 - Reduziert` | 2 | 50% | Standard: 17.5 W |
| `Stufe 3 - Nennlueeftung` | 3 | 75% | Standard: 43.5 W |
| `Stufe 4 - Intensivlueeftung` | 4 | 100% | Standard: 80 W |

> ⚠️ Die Preset-Namen enthalten keine Umlaute (`Nennlueeftung`, `Intensivlueeftung`). Automationen müssen exakt diese Schreibweise verwenden.

### Sensoren
| Entity (Suffix) | Beschreibung | Einheit |
|--------|-------------|---------|
| `_abluft_temperatur` | Ablufttemperatur (Innenluft) | °C |
| `_zuluft_temperatur` | Zulufttemperatur (nach Wärmetauscher) | °C |
| `_aussenluft_temperatur` | Außenlufttemperatur | °C |
| `_fortluft_temperatur` | Fortlufttemperatur (raus) | °C |
| `_zuluft_motor_u_min` | Zuluftmotor Drehzahl | rpm |
| `_abluft_motor_u_min` | Abluftmotor Drehzahl | rpm |
| `_zuluft_motor_spannung` | Zuluftmotor Spannung | V |
| `_abluft_motor_spannung` | Abluftmotor Spannung | V |
| `_aktuelle_leistung` | Aktuelle Leistungsaufnahme | W |
| `_energie_stufe_1` bis `_4` | Kumulativer Verbrauch pro Stufe | kWh |
| `_aktuelle_stufe` | Aktuelle Stufe als Text | — |
| `_bypass_status` | Bypass-Status | — |
| `_systemmeldung` | Aktuelle Systemmeldung | — |
| `_party_timer_restzeit` | Party-Timer Restzeit | min |

**Standardmäßig deaktiviert** (aktivierbar unter Einstellungen → Geräte):
| Entity (Suffix) | Beschreibung | Einheit |
|--------|-------------|---------|
| `_betriebsstunden_stufe_1` bis `_4` | Betriebsstunden pro Stufe | h |
| `_betriebsstunden_frostschutz` | Betriebsstunden Frostschutz | h |
| `_betriebsstunden_vorheizregister` | Betriebsstunden Vorheizregister | h |

### Binary Sensoren
| Entity (Suffix) | Beschreibung |
|--------|-------------|
| `_filter_ok` | Filterstatus (Problem = Filter wechseln) |
| `_safety_manager` | Safety Manager aktiv |
| `_passivhaus_modus` | Passivhaus-Modus aktiv |
| `_vorheizregister_aktiv` | Vorheizregister aktiv |

### Einstellungen (Number)
| Entity (Suffix) | Beschreibung | Bereich |
|--------|-------------|---------|
| `_party_timer_nachlauf` | Party-Timer Dauer | 10–240 min |
| `_bypass_schwelle_aussenluft` | Bypass-Auslösung Außenluft | 13–18 °C |
| `_bypass_schwelle_abluft` | Bypass-Auslösung Abluft | 18–25 °C |
| `_kalibrierung_abluft` | Temperaturkorrektur Abluft | ±4.9 °C |
| `_kalibrierung_zuluft` | Temperaturkorrektur Zuluft | ±4.9 °C |
| `_kalibrierung_fortluft` | Temperaturkorrektur Fortluft | ±4.9 °C |
| `_kalibrierung_aussenluft` | Temperaturkorrektur Außenluft | ±4.9 °C |

**Standardmäßig deaktiviert** (nur für Experten):

Luftmengen-Konfiguration pro Stufe (Zuluft + Abluft, 0–10 V)

### Auswahl (Select)
| Entity (Suffix) | Optionen |
|--------|---------|
| `_bypass_steuerung` | Manuell offen / Manuell zu / Automatisch |
| `_haustyp` | Eigenheim / Mietwohnung |
| `_vorheizregister_modus` | Aktiv / Passiv |
| `_safety_manager` | Mit / Ohne |
| `_ext_sensor_1_typ` bis `_4_typ` | Keiner / Feuchte (%H) / CO2 (ppm) |

### Buttons
| Entity (Suffix) | Beschreibung |
|--------|-------------|
| `_filterfehler_bestaetigen` | Filterwechsel-Alarm quittieren |
| `_externe_sensoren_umschalten` | Externe Sensoren ein-/ausschalten |

---

## Energie-Dashboard

Die vier Energie-Sensoren können direkt im HA Energie-Dashboard als **Individuelle Geräte** eingetragen werden:

**Einstellungen → Energie → Individuelle Geräte → Gerät hinzufügen**

Sensor-Namen: `sensor.kwl_fraenkische_rohrwerke_energie_stufe_1` bis `_4`

---

## Automatisierungsbeispiele

### Lüftung bei hoher CO2-Konzentration hochschalten
```yaml
automation:
  triggers:
    - trigger: numeric_state
      entity_id: sensor.co2_wohnzimmer
      above: 1000
  actions:
    - action: fan.set_preset_mode
      target:
        entity_id: fan.kwl_fraenkische_rohrwerke
      data:
        preset_mode: "Stufe 3 - Nennlueeftung"
```

### Sommer-Nacht-Vorkühlung (Bypass + Stufe 3)
```yaml
automation:
  alias: "KWL Bypass Sommer-Kühlung"
  triggers:
    - trigger: time
      at: "22:00:00"
  conditions:
    - condition: numeric_state
      entity_id: sensor.kwl_fraenkische_rohrwerke_abluft_temperatur
      above: 22
    - condition: template
      value_template: >
        {{ states('sensor.kwl_fraenkische_rohrwerke_aussenluft_temperatur') | float(0)
           < states('sensor.kwl_fraenkische_rohrwerke_abluft_temperatur') | float(0) - 2 }}
  actions:
    - action: select.select_option
      target:
        entity_id: select.kwl_fraenkische_rohrwerke_bypass_steuerung
      data:
        option: "Manuell offen"
    - action: fan.set_preset_mode
      target:
        entity_id: fan.kwl_fraenkische_rohrwerke
      data:
        preset_mode: "Stufe 3 - Nennlueeftung"
```

### Benachrichtigung bei Filterproblem
```yaml
automation:
  triggers:
    - trigger: state
      entity_id: binary_sensor.kwl_fraenkische_rohrwerke_filter_ok
      to: "on"
  actions:
    - action: notify.mobile_app
      data:
        message: "KWL: Filter muss gewechselt werden!"
```

---

## HTTP-Endpunkte

| Endpunkt | Methode | Auth | Beschreibung |
|----------|---------|------|-------------|
| `/status.xml` | GET | — | Alle Statuswerte (Poll alle 30 s) |
| `/stufe.cgi?stufe=N` | GET | — | Lüftungsstufe 1–4 setzen |
| `/setup.htm` | POST | — | Benutzereinstellungen |
| `/time.htm` | POST | — | Zeitsynchronisation |
| `/filter.cgi?filter=1` | GET | — | Filterfehler quittieren |
| `/sensor.cgi?sensor=1` | GET | — | Externe Sensoren umschalten |
| `/install/install.htm` | POST | Basic Auth | Installateureinstellungen |

---

## Fehlerbehebung

### Integration lädt nicht / Setup failed
Prüfe den HA-Log unter **Einstellungen → System → Protokolle**. Häufige Ursachen:
- Falsche Dateien kopiert → kompletten `kwl_fraenkische/` Ordner ersetzen und HA neu starten
- HA-Version zu alt → mindestens 2026.3 erforderlich

### Verbindungsfehler bei der Einrichtung
- KWL und HA müssen im gleichen Netzwerk sein
- Browser-Test: `http://10.10.4.1/status.xml` muss XML zurückgeben
- Bei Docker: Netzwerkmodus `host` prüfen

### Entity bleibt `unavailable`
```bash
curl -s http://10.10.4.1/status.xml | head -5
```
Gibt das XML zurück? Wenn nein, ist die KWL nicht erreichbar.

### Automation schlägt mit `not_valid_preset_mode` fehl
Die Preset-Namen müssen exakt stimmen — keine Umlaute:
```
Stufe 1 - Feuchteschutz
Stufe 2 - Reduziert
Stufe 3 - Nennlueeftung
Stufe 4 - Intensivlueeftung
```
Prüfen: **Entwicklerwerkzeuge → Zustände → `fan.kwl_fraenkische_rohrwerke`** → Attribut `preset_modes`

### Falsche Zugangsdaten (401)
HA zeigt automatisch einen Re-Auth Dialog. Alternativ:
**Einstellungen → Geräte & Dienste → KWL → ⋮ → Neu authentifizieren**

### Diagnose herunterladen
**Einstellungen → Geräte & Dienste → KWL → ⋮ → Diagnose herunterladen**
Sensitive Daten (Passwort, MAC) werden automatisch geschwärzt.

---

## Bekannte Einschränkungen

- Die KWL kann **nicht ausgeschaltet** werden — Stufe 1 ist der Mindestbetrieb
- Der Wochenplan des Geräts wird nicht in HA abgebildet — besser HA-Automationen nutzen
- Externe Sensoren (CO2, Feuchte) werden nur angezeigt wenn am Gerät angeschlossen und konfiguriert
- Auto-Discovery nicht möglich — die KWL hat kein mDNS/SSDP

---

## Changelog

### v1.0.0 (2026-05-20)
- Erstveröffentlichung
- Lüftungsstufen 1–4 als Fan-Entity mit Prozent und Preset-Modi
- Vollständiges Sensor-Mapping (Temperaturen, Motor, Energie)
- Bypass-Steuerung, Temperaturkorrekturen, Luftmengen-Einstellung
- Automatische Zeitsynchronisation mit DST
- HTTP Basic Auth für Installateur-Bereich
- Re-Auth Flow und Reconfigure Flow
- Konfigurierbare Nennleistung pro Stufe im Setup-Wizard
- Repair Issue für Filterwechsel mit automatischer Quittierung
- Diagnostics mit Redacting sensitiver Daten
- 117 Unit-Tests, Quality Scale: 🏆 Platinum

---

## Lizenz

MIT License — siehe [LICENSE](LICENSE)
