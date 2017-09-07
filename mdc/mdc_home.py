#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *

from .apps import print_not_active_nw, refresh_nw, on_device

from .component import entries_button_grid, create_label, label_grid, create_entry_field, variable

from .design import  Design

from .edit_config import checking_vor_edit

from .engine import get_pc_gw, get_active_interfaces, get_work_network

from .init_menu import delete_all_inputs, make_menu

from .umg_config import UmgConfigurator

from .load_device import search_umg_devices

from .load_csv import import_csv_file, read_csv_file

from .config_from_csv import build_config_list


__all__ = ["Home"]


class Home(Frame):
    """Main Class of Measuring Device Configuration."""

    def __init__(self, parent):
        """__init__ Constructor."""

        self.design = Design()
        self.configurator = UmgConfigurator()

        Frame.__init__(self, parent)

        self.parent = parent

        # main frame contains bottom frame, listbox, and message_box.
        self.main_frame = Frame(self.parent, borderwidth=5, relief=RIDGE, background=self.design.color.primary)
        self.main_frame.pack(fill=BOTH, expand=YES)

        # sub frame from main frame contains form, cancel and save frame
        self.bottom_frame = Frame(self.main_frame)
        self.bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=YES)

        self.listbox = Listbox(self.main_frame, background=self.design.color.primary, height=50,
                               width=50, selectmode=EXTENDED, relief=RIDGE, borderwidth=5, font=('Arial', 13))
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1, )

        self.devices = []  # configurable devices list

        self.message_box = Frame(self.main_frame,
                                 borderwidth=5, relief=RIDGE,
                                 width=600, background=self.design.color.secondary, height=50, )
        self.message_box.pack(side=RIGHT, fill=BOTH, expand=YES, )

        self.form_box = Frame(self.bottom_frame, borderwidth=5, height=450, width=550,
                              relief=RIDGE, background=self.design.color.secondary)
        self.form_box.pack(fill=BOTH, expand=YES)

        self.save_cancel_box = Frame(self.bottom_frame, background=self.design.color.primary, borderwidth=5,
                                     height=50, width=500, relief=RIDGE, )
        self.save_cancel_box.pack(fill=BOTH, expand=YES)
        self.info_text = Text(self.message_box, background=self.design.color.primary, height=50,
                              foreground=self.design.color.secondary, font=('Arial', 15))
        self.info_text.pack(fill=BOTH)
        self.info_text.insert(END, "Hello!! \nStart...\n")

        self.active_networks = []

        # labels.
        create_label(self)

        # label_pack.
        label_grid(self)

        # label_grid.
        variable(self)

        self.current_list = []
        self.current_device = IntVar()

        # list of config.
        self.configurations = []

        # csv_file to list
        self.csv_data = []

        # input_fields.
        create_entry_field(self)

        # grid.
        entries_button_grid(self)

        # count save.
        self.save_count = 0
        self.init_ui = make_menu(self)

        # self.add_input_fields().
        delete_all_inputs(self)

        self.text_countdown = '45'

        get_active_interfaces(self)

    def search_device_home(self):
        """This function is required to make python and tkinter  treat the function as command and self instance."""
        search_umg_devices(self)

    def not_active_network(self):
        """This function is required to make python and tkinter  treat the function as command and self instance."""
        print_not_active_nw(self)

    def network_interface(self):
        """This function is required to make python and tkinter  treat the function as command and self instance."""
        get_pc_gw(self)

    def get_selected_item(self, event):
        """This function is required to make python and tkinter  treat the function as command and self instance.
             Args:
               self: .
               event: Tkinter instance.
        """
        on_device(self, event)

    def change_network(self, event):
        """This function is required to make python and tkinter  treat the function as command and self instance.
        Args:
           self: .
           event: Tkinter instance.

        """
        get_work_network(self, event)

    def import_read_file(self):
        """This function is required to make python and tkinter  treat the function as command and self instance.
        Args:
           self: .
        """
        import_csv_file(self)

    def read_file(self):
        """This function is required to make python and tkinter  treat the function as command and self instance.
        Args:
           self: .
        """
        read_csv_file(self)

    def reload(self):
        """This function is required to make python and tkinter  treat the function as command and self instance."""
        refresh_nw(self)

    def save_dialog(self):
        """This function is required to make python and tkinter  treat the function as command and self instance."""
        checking_vor_edit(self)

    def send_data_to_device(self):
        """This function is required to make python and tkinter  treat the function as command and self instance."""
        build_config_list(self)
