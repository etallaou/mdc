#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *


__all__ = ["multi_select_input", "one_select_input"]


def multi_select_input(self):
    """Hide ip, subnet mask and gateway entry from form_box, disable static button and show mac address in info_text.

        Args:
            self(instance): Home.

    """
    # set default value
    self.df_pc.set(5)
    self.df_sc.set(5)
    self.df_avg_t.set(900)
    self.df_nw_ip.set('')
    self.df_nw_gw.set('')
    self.df_nw_sm.set('')

    # hide entry field

    self.e_ip.delete(END)

    self.e_gw.delete(0, END)

    self.e_sm.delete(0, END)

    self.nw_t_var.set(2)

    self.e_ip.grid_remove()
    self.nw_ip_label.grid_remove()

    self.e_gw.grid_remove()
    self.nw_gw_label.grid_remove()

    self.e_sm.grid_remove()
    self.nw_sm_label.grid_remove()

    self.e_mc_a.grid_remove()
    self.nw_mca_label.grid_remove()

    self.e_st_nw_t.configure(state='disabled')
    self.nw_t_var.set(2)

    self.info_text.delete(1.0, END)

    selected_devices = self.listbox.curselection()

    # insert mac address in info_text

    for item in selected_devices:
        self.info_text.insert(END,
                              "Janitza UMG96 RM-EL \n"
                              "MAC: {} \n\n".format(self.devices[item][1]))


def one_select_input(self):
    """show ip, subnet mask and gateway entry from form_box, enable static button.

        Args:
            self(instance): Home.

    """

    self.e_ip.grid()
    self.nw_ip_label.grid()

    self.e_gw.grid()
    self.nw_gw_label.grid()

    self.e_sm.grid()
    self.nw_sm_label.grid()

    self.e_mc_a.grid()
    self.nw_mca_label.grid()

    self.e_st_nw_t.configure(state='normal')
