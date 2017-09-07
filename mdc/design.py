#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["Color", "Design"]


class Color(object):
    """Main design Class."""
    def __init__(self):
        """__init__ Constructor."""
        self.primary = "#313333"
        self.secondary = "#ECEFF1"
        self.fallback = "#0FC2E3"
        self.accent = "#0FC2E3"
        self.warning = "#FF0000"


class Design(object):
    def __init__(self):
        """__init__ Constructor."""
        self.color = Color()
        self.button_relief = "sunken"

