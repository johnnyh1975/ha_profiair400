"""Tests fuer KWLCapabilities -- Capability Discovery Logic."""
from __future__ import annotations

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'custom_components'))

from kwl_fraenkische.coordinator import KWLCapabilities, _is_supported, _parse_xml
from kwl_fraenkische.const import (
    ENDPOINT_INSTALL, ENDPOINT_TIME, ENDPOINT_WOPLA, ALL_KNOWN_TAGS
)


class TestKWLCapabilitiesFull:
    """Tests fuer voll ausgestattete Firmware."""

    def test_has_motor_sensors(self, full_capabilities):
        assert full_capabilities.has_motor_sensors is True

    def test_has_airflow_voltage(self, full_capabilities):
        assert full_capabilities.has_airflow_voltage is True

    def test_has_temp_corrections(self, full_capabilities):
        assert full_capabilities.has_temp_corrections is True

    def test_has_ext_sensors(self, full_capabilities):
        assert full_capabilities.has_ext_sensors is True

    def test_has_filter_lifetime(self, full_capabilities):
        assert full_capabilities.has_filter_lifetime is True

    def test_has_operating_hours(self, full_capabilities):
        assert full_capabilities.has_operating_hours is True

    def test_has_safety_manager(self, full_capabilities):
        assert full_capabilities.has_safety_manager is True

    def test_has_preheater(self, full_capabilities):
        assert full_capabilities.has_preheater is True

    def test_has_installer_access(self, full_capabilities):
        assert full_capabilities.has_installer_access is True

    def test_has_time_sync(self, full_capabilities):
        assert full_capabilities.has_time_sync is True

    def test_has_program_control(self, full_capabilities):
        assert full_capabilities.has_program_control is True

    def test_summary_contains_features(self, full_capabilities):
        summary = full_capabilities.summary()
        assert "Motor-Diagnostik" in summary
        assert "Installer" in summary
        assert "Zeitsync" in summary

    def test_no_unknown_tags(self, full_capabilities):
        assert len(full_capabilities.unknown_tags) == 0


class TestKWLCapabilitiesMinimal:
    """Tests fuer minimale Firmware (Touch / neuere Version)."""

    def test_no_motor_sensors(self, minimal_capabilities):
        assert minimal_capabilities.has_motor_sensors is False

    def test_no_airflow_voltage(self, minimal_capabilities):
        assert minimal_capabilities.has_airflow_voltage is False

    def test_no_temp_corrections(self, minimal_capabilities):
        assert minimal_capabilities.has_temp_corrections is False

    def test_no_ext_sensors(self, minimal_capabilities):
        assert minimal_capabilities.has_ext_sensors is False

    def test_no_installer_access(self, minimal_capabilities):
        assert minimal_capabilities.has_installer_access is False

    def test_no_time_sync(self, minimal_capabilities):
        assert minimal_capabilities.has_time_sync is False

    def test_has_filter_lifetime(self, minimal_capabilities):
        """filtertime und rest_time sind auch im minimalen XML vorhanden."""
        assert minimal_capabilities.has_filter_lifetime is True

    def test_has_program_control(self, minimal_capabilities):
        """wopla.htm ist auch bei Touch erreichbar."""
        assert minimal_capabilities.has_program_control is True

    def test_summary_minimal(self, minimal_capabilities):
        summary = minimal_capabilities.summary()
        assert "Motor-Diagnostik" not in summary
        assert "Installer" not in summary


class TestIsSupported:
    """Tests fuer _is_supported Filterfunktion."""

    def test_no_requirements_always_supported(self, full_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default=None)
            required_endpoint: str | None = field(default=None)

        assert _is_supported(MockDesc(), full_capabilities) is True

    def test_required_tag_present(self, full_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default="MoStZlUm")
            required_endpoint: str | None = field(default=None)

        assert _is_supported(MockDesc(), full_capabilities) is True

    def test_required_tag_missing(self, minimal_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default="MoStZlUm")
            required_endpoint: str | None = field(default=None)

        assert _is_supported(MockDesc(), minimal_capabilities) is False

    def test_required_endpoint_present(self, full_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default=None)
            required_endpoint: str | None = field(default=ENDPOINT_INSTALL)

        assert _is_supported(MockDesc(), full_capabilities) is True

    def test_required_endpoint_missing(self, minimal_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default=None)
            required_endpoint: str | None = field(default=ENDPOINT_INSTALL)

        assert _is_supported(MockDesc(), minimal_capabilities) is False

    def test_both_requirements_met(self, full_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default="kor1")
            required_endpoint: str | None = field(default=ENDPOINT_INSTALL)

        assert _is_supported(MockDesc(), full_capabilities) is True

    def test_tag_ok_endpoint_missing(self, minimal_capabilities):
        from dataclasses import dataclass, field

        @dataclass(frozen=True, kw_only=True)
        class MockDesc:
            key: str = "test"
            required_tag: str | None = field(default="abl0")  # vorhanden
            required_endpoint: str | None = field(default=ENDPOINT_INSTALL)  # fehlt

        assert _is_supported(MockDesc(), minimal_capabilities) is False


class TestAllKnownTags:
    """Tests fuer ALL_KNOWN_TAGS Vollstaendigkeit."""

    def test_core_tags_known(self):
        core = {"abl0", "zul0", "aul0", "fol0", "bypass", "filter0",
                "stufe1", "stufe2", "stufe3", "stufe4", "config_mac"}
        assert core.issubset(ALL_KNOWN_TAGS)

    def test_motor_tags_known(self):
        motor = {"MoStZlUm", "MoStZlVo", "MoStAlUm", "MoStAlVo"}
        assert motor.issubset(ALL_KNOWN_TAGS)

    def test_filter_tags_known(self):
        assert "filtertime" in ALL_KNOWN_TAGS
        assert "rest_time" in ALL_KNOWN_TAGS

    def test_touch_tags_known(self):
        assert "SprachWahl" in ALL_KNOWN_TAGS
        assert "control0" in ALL_KNOWN_TAGS

    def test_sample_xml_all_known(self, sample_xml):
        """Alle Tags im Sample-XML muessen in ALL_KNOWN_TAGS sein."""
        from kwl_fraenkische.coordinator import _parse_xml
        raw = _parse_xml(sample_xml)
        unknown = frozenset(raw.keys()) - ALL_KNOWN_TAGS
        assert len(unknown) == 0, f"Unbekannte Tags: {unknown}"
