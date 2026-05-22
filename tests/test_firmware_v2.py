"""Tests for firmware v2 features: scheduler, digital inputs, passive thresholds."""
from __future__ import annotations

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'custom_components'))

from kwl_fraenkische.coordinator import KWLData, _parse_xml


class TestDigitalInputs:
    """Tests for DiIn1/2/3 binary sensors."""

    def test_input_1_off(self, sample_xml):
        data = KWLData(_parse_xml(sample_xml))
        assert data.digital_input_1 is False

    def test_input_2_off(self, sample_xml):
        data = KWLData(_parse_xml(sample_xml))
        assert data.digital_input_2 is False

    def test_input_3_on(self, sample_xml):
        """DiIn3 is 'Ein' in sample XML."""
        data = KWLData(_parse_xml(sample_xml))
        assert data.digital_input_3 is True

    def test_input_on_case_insensitive(self):
        data = KWLData({"DiIn1": "EIN"})
        assert data.digital_input_1 is True

    def test_input_absent_defaults_off(self):
        data = KWLData({})
        assert data.digital_input_1 is False
        assert data.digital_input_2 is False
        assert data.digital_input_3 is False


class TestAllKnownTagsUpdated:
    """Verify all new firmware tags are in ALL_KNOWN_TAGS."""

    def test_digital_inputs_known(self):
        from kwl_fraenkische.const import ALL_KNOWN_TAGS
        assert "DiIn1" in ALL_KNOWN_TAGS
        assert "DiIn2" in ALL_KNOWN_TAGS
        assert "DiIn3" in ALL_KNOWN_TAGS

    def test_passive_thresholds_known(self):
        from kwl_fraenkische.const import ALL_KNOWN_TAGS
        assert "PassivHE" in ALL_KNOWN_TAGS
        assert "PassivHA" in ALL_KNOWN_TAGS

    def test_scheduler_tags_known(self):
        from kwl_fraenkische.const import ALL_KNOWN_TAGS
        for i in range(1, 11):
            assert f"prg{i}" in ALL_KNOWN_TAGS
            assert f"prg_start{i}" in ALL_KNOWN_TAGS
            assert f"prg_stop{i}" in ALL_KNOWN_TAGS
            assert f"prg_wota{i}" in ALL_KNOWN_TAGS

    def test_langtxt_known(self):
        from kwl_fraenkische.const import ALL_KNOWN_TAGS
        for i in range(0, 155):
            assert f"langtxt{i}" in ALL_KNOWN_TAGS

    def test_status_tags_known(self):
        from kwl_fraenkische.const import ALL_KNOWN_TAGS
        for tag in ["soze", "time", "date", "events", "sensor0"]:
            assert tag in ALL_KNOWN_TAGS

    def test_sample_xml_no_unknown_tags(self, sample_xml):
        """Full sample XML should have zero unknown tags."""
        from kwl_fraenkische.coordinator import _parse_xml
        from kwl_fraenkische.const import ALL_KNOWN_TAGS
        raw = _parse_xml(sample_xml)
        unknown = frozenset(raw.keys()) - ALL_KNOWN_TAGS
        assert len(unknown) == 0, f"Unknown tags: {unknown}"
