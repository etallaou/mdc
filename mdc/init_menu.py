# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *


__all__ = ["delete_all_inputs", "make_menu", "make_input_field_disabled", "make_input_field_enabled"]


def delete_all_inputs(self):
    """Delete all input from all entry field.

        Args:
            self: Home.

    """
    self.df_pc.set('')
    self.df_sc.set('')
    self.df_avg_t.set('')
    self.df_avg_t.set('')
    self.nw_t_var.set(1)
    self.df_nw_ip.set('')
    self.df_nw_gw.set('')
    self.df_nw_sm.set('')
    self.df_mc_a.set('')


def make_menu(self):
    """MenuBar Configuration.

        Args:
            self: Home.

    """

    from .engine import get_active_interfaces

    get_active_interfaces(self)
    self.parent.title("Measuring Device Configuration")
    delete_all_inputs(self)
    menu_bar = Menu(self.parent)
    self.parent.config(menu=menu_bar)
    menu_bar.add_separator()
    file_menu = Menu(menu_bar)
    import_menu = Menu(menu_bar)
    help_menu = Menu(menu_bar)
    sub_file_menu = Menu(file_menu)
    sub_import_menu = Menu(import_menu)

    help_menu.add_cascade(label="How to use?", underline=0, foreground=self.design.color.primary, font=('Arial', 10))

    if len(self.active_networks) == 1:

        sub_file_menu.add_command(label="Janitza UMG96 RM-EL", command=self.search_device_home,
                                  foreground=self.design.color.primary, font=('Arial', 10))
    elif len(self.active_networks) > 1:

        sub_file_menu.add_command(label="Janitza UMG96 RM-EL", command=self.network_interface,
                                  foreground=self.design.color.primary, font=('Arial', 10))
    else:

        sub_file_menu.add_command(label="Janitza UMG96 RM-EL", command=self.not_active_network,
                                  foreground=self.design.color.primary, font=('Arial', 10))
    sub_file_menu.add_separator()
    sub_file_menu.add_command(label="Siemens Sentron PAC3200", foreground=self.design.color.primary, font=('Arial', 10))
    sub_file_menu.add_separator()
    sub_file_menu.add_command(label="Moxa", foreground=self.design.color.primary, font=('Arial', 10))
    sub_file_menu.add_separator()
    file_menu.add_cascade(label='Search', menu=sub_file_menu, underline=0, foreground=self.design.color.primary,
                          font=('Arial', 10))
    file_menu.add_separator()
    file_menu.add_cascade(label='CSV', menu=sub_import_menu, underline=0, foreground=self.design.color.primary,
                          font=('Arial', 10))
    sub_import_menu.add_command(label="Import CSV", underline=0, command=self.import_read_file, foreground=self.design.color.primary,
                          font=('Arial', 10))
    sub_import_menu.add_separator()
    sub_import_menu.add_command(label="Read CSV", underline=0, command=self.read_file, foreground=self.design.color.primary,
                          font=('Arial', 10))

    sub_import_menu.add_separator()

    file_menu.add_separator()
    file_menu.add_command(label="Exit", underline=0, command=quit, foreground=self.design.color.primary,
                          font=('Arial', 10))
    menu_bar.add_cascade(label="File", underline=1, menu=file_menu, foreground=self.design.color.primary,
                         font=('Arial', 10))
    menu_bar.add_cascade(label="Help", underline=1, menu=help_menu, foreground=self.design.color.primary,
                         font=('Arial', 10))
    # Greeting text
    self.info_text.delete(1.0, END)
    self.info_text.insert(END, "Welcome to MDC")


def make_input_field_disabled(self):
    """Disable all entry fields.

        Args:
            self: Home.

    """
    self.e_pm_c.configure(state='disabled')
    self.e_sd_c.configure(state='disabled')
    self.e_avg_t.configure(state='disabled')
    self.e_dn_nw_t.configure(state='disabled')
    self.e_st_nw_t.configure(state='disabled')
    self.save_btn.configure(state='disabled')
    self.cancel_btn.configure(state='disabled')
    self.e_ip.configure(state='disabled')
    self.e_gw.configure(state='disabled')
    self.e_sm.configure(state='disabled')


def make_input_field_enabled(self):
    """Enable all entry fields.

        Args:
            self: Home.

    """
    self.e_pm_c.configure(state='normal')
    self.e_sd_c.configure(state='normal')
    self.e_avg_t.configure(state='normal')
    self.e_dn_nw_t.configure(state='normal')
    self.e_st_nw_t.configure(state='normal')
    self.save_btn.configure(state='normal')
    self.cancel_btn.configure(state='normal')
    self.e_gw.configure(state='normal')
    self.e_sm.configure(state='normal')
