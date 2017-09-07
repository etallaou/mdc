#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Dialog import Dialog

from .update_form_structure import one_select_input, multi_select_input
from .engine import insert_text, mapping_avg_time, is_valid_ip
from .edit_config import on_save_button
from .read_config import show_parameters_device

from Tkinter import *

__all__ = ["print_not_active_nw", "are_phase_equals", "refresh_nw", "check_avg_time", "check_ip", "check_pmc_sdc",
           "cancel_or_save", "on_device", "update_countdown"]


def print_not_active_nw(self):
    """Display "not active network" in info_text(Frame).

       Args:
           self: netifaces network interface names.

        Returns:
        The meaningful network interface names or '(unknown)'.

    """

    message = "No active Network \n"
    insert_text(self, message, self.design.color.warning)


def are_phase_equals(self, phase1, phase2, phase3):
    """Prove if parameter's phases are equals.

       Args:
           self(instance of class object): info_text(Frame) from Home.
           phase1: the value to compare.
           phase2: the value to compare.
           phase3: the value to compare.

        Returns:
        the value of parameters (pmc, sdc, or avg) or input error ("---").
    """

    if phase1 == phase2 == phase3:
        return int(phase1)

    else:
        phase1 = "---"  # set entry as invalid
        self.info_text.delete(1.0, END)
        self.info_text.insert(END, "Device is  invalid for setting, because/nSome Phase are not same!")
        return phase1


def refresh_nw(self):
    """enable or disable input of the network (nw)'s parameter.

       Args:
           self: e_ip(entry), e_gw(entry), e_sm(entry) and design from Home.

    """
    nw_types = int(self.nw_t_var.get())

    if nw_types == 2:  # nw_type is dynamic
        self.e_ip.configure(state='disabled')
        self.e_gw.configure(state='disabled')
        self.e_sm.configure(state='disabled')
    elif nw_types == 0:  # nw_type is static
        self.e_ip.configure(state='normal')
        self.e_gw.configure(state='normal')
        self.e_sm.configure(state='normal')

    else:
        # nw_type (1, 3, 4 or 5) is not allow
        message = "The Network type of this device is not allow"
        insert_text(self, message, self.design.color.warning)


def check_avg_time(self):
    """Prove if prompted averaging time (avg_t) is in allowed List.

       Args:
           self: df_avg_t(StringVar), user_average_times(list), janitza_umg_avg_times(list), design from Home.

        Returns:
        the value of allowed avg_t or message error.
    """
    try:
        avg_t_input = int(self.df_avg_t.get())
        if avg_t_input in self.user_average_times:

            # mapping avg to device's configuration
            avg_t = mapping_avg_time(avg_t_input, self.user_average_times, self.janitza_umg_avg_times)
            return avg_t

        else:
            message = "invalid average time not in list"
            insert_text(self, message, self.design.color.warning)

    except ValueError:
        message = "average time not in list"
        insert_text(self, message, self.design.color.warning)


def check_ip(self, ip):
    """Prove if ip's format is valid.

       Args:
           self: self.design(object) from Home.
           ip: value of ip.

        Returns:
        the value of valid ip or message error.
    """

    if is_valid_ip(ip):
        return ip

    else:
        message = "invalid ip' format"
        insert_text(self, message, self.design.color.warning)


def cancel_or_save(self, message):
    """Dialog box to save or cancel.

       Args:
           self: info_text(Frame) and design(object) from Home.
           message: question (yes or cancel ?).
    """

    answer = Dialog(self, title='Save', background=self.design.color.primary,
                    text=message, bitmap='questhead', default=0, strings=('Yes', 'Cancel'),
                    foreground=self.design.color.secondary)

    if answer.num == 0:  # if answer is yes execute  this function
        self.info_text.delete(1.0, END)
        on_save_button(self)


def check_pmc_sdc(self):
    """Check if the prompted Parameters (pmc and sdc) are conform.

       Args:
           self: design(Frame), e_pm_c(), e_sd_c from Home.

        Returns:
        A list with valid pmc and sdc [pmc, sdc] or message error.

    """
    try:
        pm_c = int(self.e_pm_c.get())
        sd_c = int(self.e_sd_c.get())

        if (pm_c < 0) or (sd_c < 0):
            message = "invalid current, input must be integer"
            insert_text(self, message, self.design.color.warning)

        elif pm_c > self.MAX_PC:
            message = "invalid current, primary current must be between 1[A] and 100000[A]"
            insert_text(self, message, self.design.color.warning)

        elif pm_c < sd_c:
            message = "invalid current, primary current greater or equal to secondary current."
            insert_text(self, message, self.design.color.warning)

        elif sd_c not in self.secondary_currents:
            message = "invalid current, secondary current must be 1 or 5"
            insert_text(self, message, self.design.color.warning)
        else:
            return [pm_c, sd_c]

    except ValueError:
        message = "invalid current, the input must be integer"
        insert_text(self, message, self.design.color.warning)


def update_countdown(self, old_nwt_device, nw_t):
    """change rebooting 's countdown second.

       Args:
           self: text_countdown from Home.
           old_nwt_device: default or old network's type.
           nw_t: user or new network's type.

    """
    if old_nwt_device == nw_t:
        self.text_countdown = '5'
    else:
        self.text_countdown = '45'


def on_device(self, event):
    """get the index of selected device from listbox and read the selected device.

       Args:
           self: current_list(list), current_device(list), devices(list) from Home.
           event: tkinter object.
    """

    self.current_list = []
    selected_item = event.widget
    index = int(selected_item.curselection()[0])

    self.current_device.set(index)
    selected_devices = selected_item.curselection()

    for index in selected_item.curselection():
        self.current_list.append(index)

    if len(selected_devices) == 1:  # if only one device is selected
        one_select_input(self)
        show_parameters_device(self, self.devices[index][0], self.devices[index][1])

    else:  # if more than one device are selected
        multi_select_input(self)
