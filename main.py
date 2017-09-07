#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main function for measurement device configuration.
    This file is required to make python treat the directories as packages.
    :copyright: (c) 2016 by Edmond Talla Ouafeu.
    :license: Apache 2.0 see LICENSE.
"""

from mdc import mdc_home
from Tkinter import *


def main():
    """Main function"""
    root = Tk()
    root.geometry("900x800")
    app = mdc_home.Home(root)
    app.mainloop()


if __name__ == '__main__':
    main()
