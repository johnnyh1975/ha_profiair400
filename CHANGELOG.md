# Changelog

Alle wichtigen Änderungen an dieser Integration werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).
Die Versionierung folgt [Semantic Versioning](https://semver.org/lang/de/).

---

## [1.2.0] - 2026-05-22

### Added — Firmware v2 Support
- **Digital inputs** — DiIn1/2/3 as binary sensors (disabled by default)
  Useful if physical inputs (door contacts, CO2 sensors, occupancy) are wired to the KWL
- **All 155 langtxt UI strings** added to ALL_KNOWN_TAGS — no more unknown tag warnings
- **All new firmware v2 tags** (prg*, soze, time, date, events, PassivHE/PassivHA, sensor0)
  added to ALL_KNOWN_TAGS — zero unknown tags logged after firmware update

### Not implemented (deliberately)
- Scheduler programs (prg1–prg10): read-only from status.xml, no write endpoint.
  Use HA automations instead — more powerful and already documented
- PassivHE/PassivHA: rarely-changed installer values, no operational value
- soze/time/date/events: diagnostic only, redundant with existing sensors

### Changed
- ALL_KNOWN_TAGS extended with 200+ new firmware v2 tags
- 161 tests — cleaned up after feature scope reduction
- manifest.json version bumped to 1.2.0

---

## [1.1.0] - 2026-05-21

### Added
- **Capability Discovery** — automatically detects supported features on first poll
  - Reads available XML tags from `status.xml`
  - Probes `/install/install.htm`, `/time.htm`, `/wopla.htm` in parallel
  - Only creates entities for features the firmware actually supports
  - Works with all Profi-Air firmware versions (Touch, non-Touch, old, new)
- **`required_tag` / `required_endpoint`** on all EntityDescriptions
  - Motor sensors only created if `MoStZlUm` tag present
  - Temperature corrections only if `kor1` tag present
  - Installer entities only if `/install/install.htm` reachable
  - Program control only if `/wopla.htm` reachable
- **Unknown tag detection** — new firmware tags logged with GitHub issue link
- **Diagnostics extended** — full capabilities report including available tags,
  reachable endpoints, unknown tags and feature flags
- **34 new capability tests** — full and minimal firmware fixtures

### Changed
- Time sync silently skipped if `/time.htm` not reachable
- `async_post_install` raises `HomeAssistantError` if installer not reachable
- `manifest.json` version bumped to `1.1.0`

### Fixed
- All 6 platforms now filter entities by capabilities at setup time

---

## [1.0.0] - 2026-05-19

### Hinzugefügt
- Lüftungsstufen 1–4 als Fan-Entity mit Prozent-Schieberegler und Preset-Modi
- Automatische Zeitsynchronisation (Start + alle 24 h) inkl. Sommer-/Winterzeit
- Energie-Dashboard: kumulativer kWh-Verbrauch pro Stufe (basierend auf Betriebsstunden)
- Vollständiges Sensor-Mapping: Temperaturen, Motor-RPM, Motorspannung, Wärmerückgewinnung
- Bypass-Steuerung: Manuell offen / Manuell zu / Automatisch
- Temperaturkorrekturen für alle vier Messfühler (±4.9 °C)
- Luftmengen-Konfiguration pro Stufe (Experten, standardmäßig deaktiviert)
- Haustyp, Vorheizregister, Safety Manager über Select-Entities konfigurierbar
- Ext. Sensor-Typen (Feuchte %H / CO2 ppm) konfigurierbar
- HTTP Basic Auth für den Installateur-Bereich
- Optimistic Updates — UI reagiert sofort ohne Wartezeit
- Re-Auth Flow bei abgelaufenen Zugangsdaten (ConfigEntryAuthFailed)
- Reconfigure Flow — IP und Zugangsdaten ohne Neueinrichtung änderbar
- Konfigurierbare Nennleistung pro Stufe im Setup-Wizard (Standardwerte: 11/17.5/43.5/80 W)
- Diagnostics mit automatischem Redacting sensitiver Daten
- Repair Issue für Filterwechsel-Alarm mit automatischer Quittierung
- 117 automatisierte Tests (Unit + Config Flow)
- Vollständige Übersetzungen: Deutsch und Englisch
- HACS-kompatibel mit GitHub Actions CI (HACS Validation + Hassfest)
- Quality Scale: 🏆 Platinum

### Technische Details
- `entry.runtime_data` Pattern (HA 2024.4+)
- `async_get_clientsession(hass)` statt eigener aiohttp Session
- `DataUpdateCoordinator` mit `config_entry=entry` (HA 2025.11 Deadline)
- `@dataclass(frozen=True, kw_only=True)` für alle EntityDescriptions (HA 2025.1+)
- `PARALLEL_UPDATES` konfiguriert: 1 für schreibende, 0 für lesende Plattformen
- Minimale HA-Version: 2026.3

---

## [Unveröffentlicht]

Keine ausstehenden Änderungen.
