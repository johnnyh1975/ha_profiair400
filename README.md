# KWL Fränkische Rohrwerke — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![HA Version](https://img.shields.io/badge/Home%20Assistant-2026.3%2B-blue.svg)](https://www.home-assistant.io/)
[![Quality Scale](https://img.shields.io/badge/Quality%20Scale-Platinum-silver.svg)](https://developers.home-assistant.io/docs/core/integration-quality-scale/)
[![Tests](https://img.shields.io/badge/Tests-161%20passing-brightgreen.svg)](.github/workflows/validate.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.1.0-blue.svg)](CHANGELOG.md)

Local-only Home Assistant integration for **Fränkische Rohrwerke Profi-Air** ventilation units. No cloud, no external services — talks directly to your KWL over HTTP, the same way the built-in web interface does.

![Fränkische Rohrwerke](brand/logo.png)

---

## Table of Contents

- [Why this integration?](#why-this-integration)
- [Supported devices](#supported-devices)
- [How Capability Discovery works](#how-capability-discovery-works)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Entities](#entities)
- [Energy Dashboard](#energy-dashboard)
- [Automation examples](#automation-examples)
- [Feature comparison](#feature-comparison)
- [Troubleshooting](#troubleshooting)
- [HTTP endpoints](#http-endpoints-reference)
- [Known limitations](#known-limitations)
- [Changelog](#changelog)

---

## Why this integration?

Most smart home integrations for ventilation systems depend on cloud services or proprietary apps. This integration uses your KWL's built-in HTTP interface — **your data never leaves your home network**.

Beyond basic control, this integration brings genuinely intelligent ventilation:

- **Weather-aware cooling** — open bypass only when tomorrow's forecast exceeds your threshold
- **Presence-aware scheduling** — drop to minimum level when everyone leaves
- **CO2-responsive ventilation** — boost automatically when sensors trigger
- **Energy tracking** — cumulative kWh per level in the HA Energy Dashboard

The built-in weekly schedule on the device cannot do any of this. HA automations can.

---

## Supported devices

This integration works with **all Fränkische Rohrwerke Profi-Air models** that expose an HTTP interface on your local network. It automatically detects what your firmware supports and creates only the relevant entities.

| Model | Interface | Entities |
|-------|-----------|----------|
| Profi-Air 400 (classic firmware) | `/status.xml` + installer area | Full — motor, corrections, ext. sensors, installer |
| Profi-Air 250 Touch | `/status.xml` | Core — temperatures, bypass, filter, energy |
| Profi-Air 400 Touch | `/status.xml` | Core — temperatures, bypass, filter, energy |
| Other Profi-Air models with HTTP | `/status.xml` | Auto-detected — open an issue if something is missing |

> **Profi-Air 250 Touch** and **Profi-Air 400 Touch** users: this integration works with your device. Capability Discovery automatically detects what your firmware supports and skips entities that are not available.

> Not sure which model you have? If `http://YOUR_KWL_IP/status.xml` returns XML data, this integration will work.

---

## How Capability Discovery works

Since v1.1.0, the integration **automatically discovers** what your device supports on first startup — no manual configuration required.

```
First startup
      ↓
Poll /status.xml → inventory all XML tags
      ↓
Probe 3 endpoints in parallel (3 s timeout each):
    /install/install.htm  →  installer area available?
    /time.htm             →  time sync supported?
    /wopla.htm            →  program control available?
      ↓
Build KWLCapabilities — frozen snapshot of device features
      ↓
Each platform filters its entity list:
    required_tag missing    → entity not created
    required_endpoint down  → entity not created
      ↓
Only working entities appear in HA — zero unavailable clutter
```

**What this means in practice:**

- A full-featured firmware gets all entities (motor RPM, installer settings, corrections, external sensors…)
- A minimal firmware (newer Touch) gets only the entities that actually work
- If a firmware update adds new XML tags, a restart picks them up automatically
- Unknown tags are logged and shown in Diagnostics — please open a GitHub issue so we can add support

---

## Features

### Control
- **Ventilation levels 1–4** — fan entity with percentage slider, preset modes and optimistic UI updates
- **Bypass control** — Manual open / Manual closed / Automatic
- **Control mode** — switch between Weekly Program and Manual *(if `/wopla.htm` reachable)*
- **Party timer** — configurable duration 10–240 min
- **Language selection** — DE / EN / FR / IT / NL
- **Temperature corrections** — calibrate all four sensors ±4.9 °C *(if firmware supports)*
- **Airflow calibration** — per-level supply and exhaust tuning *(if firmware supports, disabled by default)*
- **Installer settings** — bypass thresholds, house type, pre-heater, safety manager, external sensors via HTTP Basic Auth *(if installer area reachable)*

### Monitoring
- **All four temperatures** — outdoor, supply (after heat exchanger), exhaust (indoor), extract (outgoing)
- **Motor RPM and voltage** — supply and exhaust motors *(if firmware supports)*
- **Current power** — real-time watts based on active level (configurable per device)
- **Cumulative energy** — kWh per level, ready for HA Energy Dashboard
- **Filter status** — OK / needs replacement (binary sensor + automatic repair issue)
- **Filter lifetime** — total and remaining days *(if firmware supports)*
- **Operating hours** — per level, frost protection, pre-heater *(disabled by default)*
- **Safety manager, passive mode, pre-heater** — binary sensors *(if firmware supports)*
- **External sensor values** — up to 4 CO2 or humidity sensors *(if firmware supports)*
- **System message, bypass status, party timer, current level text**

### Smart home integration
- **Automatic time sync** — on startup and every 24 hours, DST-aware *(if firmware supports)*
- **Energy dashboard** — four kWh sensors compatible with HA Energy panel
- **Re-auth flow** — HA prompts for new credentials automatically on 401
- **Reconfigure flow** — change IP or credentials without reinstalling
- **Repair issue** — filter alert with one-click acknowledgement in HA UI
- **Download diagnostics** — full capability report, sensitive data auto-redacted

### Quality
- 🏆 **HA Integration Quality Scale: Platinum**
- **161 automated tests** — unit, config flow, capability discovery
- **Full translations** — 🇩🇪 German and 🇬🇧 English
- **GitHub Actions CI** — HACS validation + Hassfest + pytest on Python 3.12/3.13

---

## Requirements

- Home Assistant **2026.3** or newer
- KWL reachable via HTTP on your local network (typically `http://10.10.4.1`)
- No internet connection required

---

## Installation

### Via HACS (recommended)

1. Open HACS → Integrations → ⋮ → Custom repositories
2. Add URL: `https://github.com/johnnyh1975/ha-kwl-fraenkische`
3. Category: Integration → Add
4. Search for **KWL Fränkische Rohrwerke** and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/kwl_fraenkische/` folder into your HA config directory
2. Restart Home Assistant

---

## Setup

1. **Settings → Devices & Services → Add Integration**
2. Search for **KWL Fränkische Rohrwerke**
3. **Step 1 — IP address:** Enter the IP of your KWL (default: `10.10.4.1`)
4. **Step 2 — Credentials:** Enter installer credentials *(only shown if installer area detected)*
   - Factory default: Username `install` / Password `konfig12`
5. **Step 3 — Power values:** Confirm or adjust watt per level
   - Defaults for Profi-Air 400: **11 / 17.5 / 43.5 / 80 W**
   - Measure with a clamp meter for accurate energy tracking

> ⚠️ **Security:** Factory credentials `install` / `konfig12` are publicly known. Change the password at `http://YOUR_KWL_IP/setup.htm` before or immediately after setup.

### Upgrade from v1.1.0 to v1.2.0

Install the new version via HACS and restart HA. The three new DiIn binary sensors appear automatically if your firmware exposes them — no reconfiguration needed.

### Upgrade from v1.0.0 to v1.1.0

Simply install the new version via HACS and restart HA. Capability Discovery runs automatically on the first poll — no reconfiguration needed. All existing entities are preserved; new capability-dependent entities are added if your firmware supports them.

### Reconfigure

Change IP or credentials without reinstalling:
**Settings → Devices & Services → KWL → ⋮ → Reconfigure**

---

## Entities

All entities belong to a single **KWL** device identified by MAC address. Entity IDs follow the pattern `domain.kwl_fraenkische_rohrwerke_<suffix>`.

Entities marked *(firmware)* are only created if your device's firmware exposes the required data — see [Capability Discovery](#how-capability-discovery-works).

### Fan
| Entity | Description |
|--------|-------------|
| `fan.kwl_fraenkische_rohrwerke` | Ventilation — levels 1–4, percentage, preset mode |

**Preset modes** — use these exact strings in automations (no umlauts):
| Preset | Level | % | Default power |
|--------|-------|----|---------------|
| `Stufe 1 - Feuchteschutz` | 1 | 25% | 11 W |
| `Stufe 2 - Reduziert` | 2 | 50% | 17.5 W |
| `Stufe 3 - Nennlueeftung` | 3 | 75% | 43.5 W |
| `Stufe 4 - Intensivlueeftung` | 4 | 100% | 80 W |

> ⚠️ Use `Nennlueeftung` not `Nennlüftung` — no umlauts in preset names.

### Sensors
| Suffix | Description | Unit | Firmware |
|--------|-------------|------|----------|
| `_aussenluft_temperatur` | Outdoor air temperature | °C | all |
| `_zuluft_temperatur` | Supply air temperature (after heat exchanger) | °C | all |
| `_abluft_temperatur` | Exhaust air temperature (indoor) | °C | all |
| `_fortluft_temperatur` | Extract air temperature (outgoing) | °C | all |
| `_aktuelle_leistung` | Current power consumption | W | all |
| `_energie_stufe_1` to `_4` | Cumulative energy per level | kWh | all |
| `_filter_gesamtlaufzeit` | Filter total lifetime | days | if supported |
| `_filter_restlaufzeit` | Filter remaining lifetime | days | if supported |
| `_aktuelle_stufe` | Current level (text) | — | all |
| `_bypass_status` | Bypass status | — | all |
| `_systemmeldung` | System message | — | all |
| `_party_timer_restzeit` | Party timer remaining | min | all |
| `_zuluft_motor_u_min` | Supply motor RPM | rpm | if supported |
| `_abluft_motor_u_min` | Exhaust motor RPM | rpm | if supported |
| `_zuluft_motor_spannung` | Supply motor voltage | V | if supported |
| `_abluft_motor_spannung` | Exhaust motor voltage | V | if supported |

**Disabled by default** (enable under Settings → Devices → KWL → sensors):
| Suffix | Description | Unit |
|--------|-------------|------|
| `_betriebsstunden_stufe_1` to `_4` | Operating hours per level | h |
| `_betriebsstunden_frostschutz` | Frost protection hours | h |
| `_betriebsstunden_vorheizregister` | Pre-heater hours | h |

### Binary sensors
| Suffix | Description | Firmware |
|--------|-------------|----------|
| `_filter_ok` | Filter OK / needs replacement | all |
| `_safety_manager` | Safety manager active | if supported |
| `_passivhaus_modus` | Passive house mode active | if supported |
| `_vorheizregister_aktiv` | Pre-heater active | if supported |
| `_digital_input_1` | Digital Input 1 (physical wiring) | if supported, disabled by default |
| `_digital_input_2` | Digital Input 2 (physical wiring) | if supported, disabled by default |
| `_digital_input_3` | Digital Input 3 (physical wiring) | if supported, disabled by default |

### Number entities
| Suffix | Description | Range | Firmware |
|--------|-------------|-------|----------|
| `_party_timer_nachlauf` | Party timer duration | 10–240 min | all |
| `_bypass_schwelle_aussenluft` | Bypass trigger — outdoor temp | 13–18 °C | all |
| `_bypass_schwelle_abluft` | Bypass trigger — exhaust temp | 18–25 °C | all |
| `_kalibrierung_abluft` | Exhaust temp correction | ±4.9 °C | if supported |
| `_kalibrierung_zuluft` | Supply temp correction | ±4.9 °C | if supported |
| `_kalibrierung_fortluft` | Extract temp correction | ±4.9 °C | if supported |
| `_kalibrierung_aussenluft` | Outdoor temp correction | ±4.9 °C | if supported |

Airflow voltage calibration per level — disabled by default, installer firmware only.

### Select entities
| Suffix | Options | Firmware |
|--------|---------|----------|
| `_bypass_steuerung` | Manuell offen / Manuell zu / Automatisch | all |
| `_steuerungsmodus` | Manual / Program | if `/wopla.htm` reachable |
| `_sprache` | Deutsch / English / Francais / Italiano / Nederlands | all |
| `_haustyp` | Eigenheim / Mietwohnung | installer only |
| `_vorheizregister_modus` | Aktiv / Passiv | installer only |
| `_safety_manager` | Mit / Ohne | installer only |
| `_ext_sensor_1_typ` to `_4_typ` | Keiner / Feuchte (%H) / CO2 (ppm) | if supported |

### Buttons
| Suffix | Description | Firmware |
|--------|-------------|----------|
| `_filterfehler_bestaetigen` | Acknowledge filter alert | all |
| `_externe_sensoren_umschalten` | Toggle external sensors | if supported |

---

## Energy Dashboard

Add the four energy sensors as **Individual devices** in the HA Energy panel:

**Settings → Energy → Individual devices → Add device**

Add all four: `sensor.kwl_fraenkische_rohrwerke_energie_stufe_1` through `_4`

HA automatically sums daily and monthly totals. Combined with the operating hours sensors you get a full picture of how your KWL distributes runtime across levels.

---

## Automation examples

### Increase ventilation on high CO2
```yaml
automation:
  triggers:
    - trigger: numeric_state
      entity_id: sensor.co2_living_room
      above: 1000
  actions:
    - action: fan.set_preset_mode
      target:
        entity_id: fan.kwl_fraenkische_rohrwerke
      data:
        preset_mode: "Stufe 3 - Nennlueeftung"
```

### Summer night pre-cooling (bypass + level 3)
```yaml
automation:
  alias: "KWL Summer Night Cooling"
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
    - condition: numeric_state
      entity_id: sensor.dwd_tagesmax_temperatur_morgen
      above: input_number.kwl_bypass_hitze_schwelle
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

### Morning — close bypass, reduce to level 1
```yaml
automation:
  alias: "KWL Summer Morning"
  triggers:
    - trigger: time
      at: "08:00:00"
  conditions:
    - condition: template
      value_template: "{{ now().month in [5, 6, 7, 8, 9] }}"
  actions:
    - action: select.select_option
      target:
        entity_id: select.kwl_fraenkische_rohrwerke_bypass_steuerung
      data:
        option: "Automatisch"
    - action: fan.set_preset_mode
      target:
        entity_id: fan.kwl_fraenkische_rohrwerke
      data:
        preset_mode: "Stufe 1 - Feuchteschutz"
```

### Filter replacement notification
```yaml
automation:
  triggers:
    - trigger: state
      entity_id: binary_sensor.kwl_fraenkische_rohrwerke_filter_ok
      to: "on"
  actions:
    - action: notify.mobile_app
      data:
        message: "KWL: Filter replacement needed!"
```

> **Tip:** Instead of this automation, use the built-in **Repair Issue** — HA shows a persistent notification with a one-click fix that automatically acknowledges the alert on the device.

---

## Feature comparison

### This integration vs. profi-air-touch

| Feature | This integration | [profi-air-touch](https://github.com/desue90/profi-air-touch) |
|---------|:---:|:---:|
| **Target models** | Profi-Air 400 classic, 250 Touch, 400 Touch (all auto-detected) | Profi-Air 250/400 Touch only |
| **Capability auto-detection** | ✅ v1.1.0 | ❌ |
| **Firmware-adaptive entities** | ✅ | ❌ |
| **DataUpdateCoordinator** | ✅ | ❌ planned |
| **Single poll for all entities** | ✅ | ❌ per-entity polls |
| **MAC as stable device ID** | ✅ | ❌ hardcoded string |
| **Connection test on setup** | ✅ | ❌ |
| **Re-auth flow** | ✅ | ❌ |
| **Reconfigure flow** | ✅ | ❌ |
| **Repair issues** | ✅ | ❌ |
| **Diagnostics with capability report** | ✅ | ❌ |
| **Time synchronisation** | ✅ auto-detected | ❌ |
| **Energy kWh sensors** | ✅ | ❌ |
| **Binary sensors** | ✅ | ❌ |
| **Motor RPM + voltage** | ✅ if firmware | ❌ |
| **Installer settings (BasicAuth)** | ✅ if firmware | ❌ |
| **Configurable watt values** | ✅ | ❌ |
| **Optimistic updates** | ✅ | ❌ |
| **Filter remaining days** | ✅ | ✅ |
| **Language select** | ✅ | ✅ |
| **Program/Manual control** | ✅ | ✅ |
| **Unit tests** | ✅ 151 | ❌ |
| **Quality Scale** | 🏆 Platinum | not declared |

### Feature availability by firmware version

| Feature | Full firmware | Minimal firmware |
|---------|:---:|:---:|
| All 4 temperatures | ✅ | ✅ |
| Bypass control | ✅ | ✅ |
| Filter status (OK/replace) | ✅ | ✅ |
| Filter remaining days | ✅ | ✅ |
| Language select | ✅ | ✅ |
| Program/Manual control | ✅ | ✅ |
| Energy kWh sensors | ✅ | ✅ |
| Operating hours per level | ✅ | ✅ |
| Motor RPM + voltage | ✅ | ❌ auto-hidden |
| Airflow voltage calibration | ✅ | ❌ auto-hidden |
| Temperature corrections | ✅ | ❌ auto-hidden |
| External sensors (CO2/humidity) | ✅ | ❌ auto-hidden |
| Safety manager | ✅ | ❌ auto-hidden |
| Pre-heater register | ✅ | ❌ auto-hidden |
| Installer settings (BasicAuth) | ✅ | ❌ auto-hidden |
| Time synchronisation | ✅ | depends on firmware |

**Auto-hidden** = entity is simply not created. No `unavailable` state, no clutter in your dashboard.

---

## Troubleshooting

### Integration fails to load
Check **Settings → System → Logs**. Common causes:
- Wrong files copied → replace the entire `kwl_fraenkische/` folder and restart HA
- HA version too old → 2026.3 minimum required

### Cannot connect during setup
- KWL and HA must be on the same network segment
- Browser test: `http://YOUR_KWL_IP/status.xml` must return XML
- Docker: check `host` network mode

### Entity unavailable
```bash
curl -s http://10.10.4.1/status.xml | head -5
```
No XML response → KWL not reachable. Check network and IP address.

### Expected entity not appearing
Since v1.1.0, entities are only created if your firmware supports them. Check what was detected:

**Settings → Devices & Services → KWL → ⋮ → Download diagnostics**

Look at `capabilities.available_tags` and `capabilities.reachable_endpoints` — if the required tag or endpoint is missing, the entity won't be created. To refresh after a firmware update: restart HA.

### Automation fails with `not_valid_preset_mode`
Preset names must match exactly — no umlauts:
```
Stufe 1 - Feuchteschutz
Stufe 2 - Reduziert
Stufe 3 - Nennlueeftung
Stufe 4 - Intensivlueeftung
```
Verify: **Developer Tools → States → `fan.kwl_fraenkische_rohrwerke`** → attribute `preset_modes`

### Wrong credentials (401)
HA shows a re-auth dialog automatically. Or manually:
**Settings → Devices & Services → KWL → ⋮ → Re-authenticate**

### Download diagnostics
**Settings → Devices & Services → KWL → ⋮ → Download diagnostics**

Includes: capability report, available tags, reachable endpoints, unknown tags, current sensor values. Password and MAC are automatically redacted.

---

## HTTP endpoints reference

| Endpoint | Method | Auth | Description | Auto-detected |
|----------|--------|------|-------------|:---:|
| `/status.xml` | GET | — | All status values (polled every 30 s) | always |
| `/stufe.cgi?stufe=N` | GET | — | Set ventilation level 1–4 | always |
| `/setup.htm` | POST | — | User settings (bypass, language, corrections) | always |
| `/wopla.htm` | POST | — | Weekly program / manual control switch | ✅ probed |
| `/time.htm` | POST | — | Time synchronisation | ✅ probed |
| `/filter.cgi?filter=1` | GET | — | Acknowledge filter alert | always |
| `/sensor.cgi?sensor=1` | GET | — | Toggle external sensors | always |
| `/install/install.htm` | POST | Basic Auth | Installer settings | ✅ probed |

Probed endpoints are tested once on startup (3 s timeout). If unreachable, they are never called again — no wasted requests.

---

## Known limitations

- The KWL **cannot be switched off** — level 1 is the minimum operation
- The device's built-in weekly schedule is not imported into HA — use HA automations for scheduling (more powerful anyway)
- External sensors (CO2, humidity) only appear when physically connected and configured on the device
- Auto-discovery of the KWL IP is not possible — no mDNS/SSDP on the device

---

## Changelog

### v1.2.0 (2026-05-22)
- Digital inputs DiIn1/2/3 as binary sensors (disabled by default)
- All firmware v2 tags (prg1–prg10, soze, time, date, events, langtxt0–154 etc.) added to known tags — zero unknown tag warnings after firmware update
- 161 automated tests

### v1.1.0 (2026-05-21)
- **Capability Discovery** — automatic detection of supported features on first poll
- **Firmware-adaptive entities** — only entities for features your device actually supports
- `required_tag` / `required_endpoint` on all EntityDescriptions
- Parallel endpoint probing on startup (3 s timeout, zero overhead in normal operation)
- Unknown firmware tags logged and shown in diagnostics
- Diagnostics extended with full capability report
- Time sync and installer access silently skipped if endpoint not reachable
- 34 new capability tests — 151 total

### v1.0.0 (2026-05-20)
- Initial release
- Ventilation levels 1–4 as fan entity with percentage and preset modes
- Full sensor mapping — temperatures, motor data, filter lifetime, energy
- Language selection and program/manual control mode
- Bypass control, temperature corrections, airflow calibration
- Automatic time synchronisation with DST
- HTTP Basic Auth for installer area
- Re-auth and reconfigure flows
- Configurable nominal power per level in setup wizard
- Repair issue for filter replacement with automatic acknowledgement
- Diagnostics with sensitive data redaction
- 117 automated tests, Quality Scale: 🏆 Platinum

---

## License

MIT License — see [LICENSE](LICENSE)
