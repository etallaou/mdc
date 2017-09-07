#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from .load_device import rebooting_window
from .engine import is_ip_in_subnet, insert_text, get_mask_length, edit_single_device, mapping_avg_time, \
    edit_multi_devices


__all__ = ["checking_vor_edit", "config_one_device", "config_more_device", "on_save_button"]


def checking_vor_edit(self):
    """Check parameters before editing (check_pmc_sdc, check_avg_time, is_ip_in_subnet).

       Args:
           self: insert_text(Frame) design(class).
    """

    from .apps import check_ip, check_pmc_sdc, check_avg_time, cancel_or_save
    currents = check_pmc_sdc(self)  # check pmc and sdc
    avg_t = check_avg_time(self)  # check avg

    if len(self.current_list) == 1:

        ip_a = check_ip(self, self.df_nw_ip.get())
        gw_nw = check_ip(self, self.df_nw_gw.get())
        sm_nw = check_ip(self, self.df_nw_sm.get())

        try:
            #  check network's params
            if currents and avg_t and not is_ip_in_subnet(ip_a, gw_nw, get_mask_length(sm_nw)):
                message = "Warning the default gateway is not located on the same network segment as " \
                          "defined by the IP and Subnet mask.\nShould this configuration be stored "

                cancel_or_save(self, message)

            elif currents and avg_t:
                message = "Do you really want to edit the device"
                cancel_or_save(self, message)

        except AttributeError:
            message = "Configuration failed\n"
            insert_text(self, message, self.design.color.warning)

    elif currents and avg_t and len(self.current_list) > 1:
        # if multi device configuration, do'nt need to check check network's params
        message = "Do you really want to edit the %s selected devices" % len(self.current_list)
        cancel_or_save(self, message)


def config_one_device(self, device_ip, pm_c, sd_c, avg_t, nw_t, ip_a, gw_nw, sm_nw):
    """Configuration of only one device.

       Args:
           self: insert_text(Frame) design(class).
           device_ip: ip address of the device to be edit.
           pm_c: new value of primary current.
           sd_c: new value of secondary current.
           avg_t: new value of averaging time.
           nw_t: new value of network type.
           ip_a: new value of ip address.
           gw_nw: new value of gateway.
           sm_nw: new value of subnet mask.

    """
    item = self.current_device.get()
    from .apps import update_countdown
    try:
        data_device = self.configurator.read_configuration(self.devices[item][0])
        old_nwt_device = data_device["device_config"]["network"]["nw_type"]
        update_countdown(self, old_nwt_device, nw_t)
        edit_single_device(self, device_ip, pm_c, sd_c, avg_t, nw_t, ip_a, gw_nw, sm_nw)
        message = "Mac : %s ....................[OK]\n" % self.devices[item][1]
        insert_text(self, message, self.design.color.secondary)

    except Exception:
        message = "Mac:%s connection failed\n" % self.devices[item][1]
        insert_text(self, message, self.design.color.warning)

    config = [pm_c, sd_c, mapping_avg_time(avg_t, self.janitza_umg_avg_times, self.user_average_times), nw_t,
              ip_a, gw_nw, sm_nw]
    device_id = [self.devices[item]]
    self.save_count += 1
    my_config = {self.save_count: [device_id, config]}
    self.configurations.append(my_config)
    rebooting_window(self, len(self.current_list))


def config_more_device(self, pm_c, sd_c, avg_t):
    """Configuration of more than one device at once.

       Args:
           self: insert_text(Frame) design(class).
           pm_c: new value of primary current.
           sd_c: new value of secondary current.
           avg_t: new value of averaging time.

    """

    nw_t = self.nw_t_var.get()

    config = [pm_c, sd_c, mapping_avg_time(avg_t, self.janitza_umg_avg_times, self.user_average_times), nw_t]

    self.info_text.delete(1.0, END)
    device_id = []

    for item in self.current_list:
        try:
            data_device = self.configurator.read_configuration(self.devices[item][0])
            old_nwt_device = data_device["device_config"]["network"]["nw_type"]
            edit_multi_devices(self, self.devices[item][0], pm_c, sd_c, avg_t, nw_t)  # configuration list
            if old_nwt_device == nw_t:
                self.text_countdown = '5'
            else:
                self.text_countdown = '45'

            self.info_text.insert(END, "Mac : %s ....................[OK]\n" % self.devices[item][1])
            device_id.append(self.devices[item])

        except Exception:
            message = "Mac: %s connection failed..[X]\n" % self.devices[item][1]
            insert_text(self, message, self.design.color.warning)

    self.save_count += 1
    my_config = {self.save_count: [device_id, config]}
    self.configurations.append(my_config)
    rebooting_window(self, len(self.current_list))


def on_save_button(self):
    """If user want to save his configuration: check parameters and call configuration's functions.

       Args:
           self: main Class.

    """

    from .apps import check_ip, check_pmc_sdc, check_avg_time
    avg_t = check_avg_time(self)
    current = check_pmc_sdc(self)
    pm_c = current[0]
    sd_c = current[1]
    ip_a = check_ip(self, self.df_nw_ip.get())
    gw_nw = check_ip(self, self.df_nw_gw.get())
    sm_nw = check_ip(self, self.df_nw_sm.get())
    item = self.current_device.get()
    device_ip = self.devices[item][0]
    nw_t = self.nw_t_var.get()

    if len(self.current_list) == 1:
        config_one_device(self, device_ip, pm_c, sd_c, avg_t, nw_t, ip_a, gw_nw, sm_nw)
    else:
        config_more_device(self, pm_c, sd_c, avg_t)
