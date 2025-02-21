#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pytest

from utils.helpers import human_readable_size


class TestHumanReadableSize:
    def test_human_readable_size_zero_expect_zero_bytes(self):
        assert human_readable_size(0) == "0.00 B"

    def test_human_readable_size_byte_range_expect_bytes(self):
        assert human_readable_size(1) == "1.00 B"
        assert human_readable_size(1023) == "1023.00 B"

    def test_human_readable_size_kilo_byte_range_expect_kilo_bytes(self):
        kilo_byte = 1024
        assert human_readable_size(kilo_byte * 1) == "1.00 KB"
        assert human_readable_size(kilo_byte * 1023) == "1023.00 KB"

    def test_human_readable_size_mega_byte_range_expect_mega_bytes(self):
        mega_byte = 1024 * 1024
        assert human_readable_size(mega_byte * 1) == "1.00 MB"
        assert human_readable_size(mega_byte * 1023) == "1023.00 MB"

    def test_human_readable_size_giga_byte_range_expect_giga_bytes(self):
        giga_byte = 1024 * 1024 * 1024
        assert human_readable_size(giga_byte * 1) == "1.00 GB"
        assert human_readable_size(giga_byte * 1023) == "1023.00 GB"

    def test_human_readable_size_tera_byte_range_expect_tera_bytes(self):
        tera_byte = 1024 * 1024 * 1024 * 1024
        assert human_readable_size(tera_byte * 1) == "1.00 TB"
        assert human_readable_size(tera_byte * 1023) == "1023.00 TB"

    def test_human_readable_size_peta_byte_range_expect_peta_bytes(self):
        peta_byte = 1024 * 1024 * 1024 * 1024 * 1024
        assert human_readable_size(peta_byte * 1) == "1.00 PB"
        assert human_readable_size(peta_byte * 1023) == "1023.00 PB"

    def test_human_readable_size_exa_byte_range_expect_exa_bytes(self):
        exa_byte = 1024 * 1024 * 1024 * 1024 * 1024 * 1024
        assert human_readable_size(exa_byte * 1) == "1.00 EB"
        assert human_readable_size(exa_byte * 1023) == "1023.00 EB"

    def test_human_readable_size_yotta_byte_range_expect_yotta_bytes(self):
        yotta_byte = 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024
        assert human_readable_size(yotta_byte * 1) == "1.00 ZB"
        assert human_readable_size(yotta_byte * 1023) == "1023.00 ZB"


if __name__ == "__main__":
    pytest.main(["-v"])
