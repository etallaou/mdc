#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Tkinter import *
from .init_menu import make_input_field_enabled, delete_all_inputs, make_input_field_disabled
from .edit_config import insert_text, mapping_avg_time

__all__ = ["get_pc_sc_avg", "get_nw_params", "show_parameters_device"]


def get_pc_sc_avg(self, ip):
    """Read primary, secondary current and averaging time of a device und set into respectively window.

        Args:
            self: self.df_pc, self.df_sc, self.df_avg_t, self.info_text.
            ip: value of ip address from the device to read.


    """
    from .apps import are_phase_equals

    try:
        data_device = self.configurator.read_configuration(ip)
        # set device params
        pm_l1 = int(data_device["device_config"]["primary_current_l1"])
        pm_l2 = int(data_device["device_config"]["primary_current_l2"])
        pm_l3 = int(data_device["device_config"]["primary_current_l3"])

        pm_c_ip = are_phase_equals(self, pm_l1, pm_l2, pm_l3)
        self.df_pc.set(pm_c_ip)

        sd_c_l1 = int(data_device["device_config"]["secondary_current_l1"])
        sd_c_l2 = int(data_device["device_config"]["secondary_current_l2"])
        sd_c_l3 = int(data_device["device_config"]["secondary_current_l3"])
        sd_c_ip = are_phase_equals(self, sd_c_l1, sd_c_l2, sd_c_l3)
        self.df_sc.set(sd_c_ip)

        avg_t_i = data_device["device_config"]["average_time_i"]
        avg_t_p = data_device["device_config"]["average_time_p"]
        avg_t_u = data_device["device_config"]["average_time_u"]

        avg_t = are_phase_equals(self, avg_t_i, avg_t_p, avg_t_u)

        if int(avg_t):

            avg_t_ip = mapping_avg_time(avg_t, self.janitza_umg_avg_times,
                                        self.user_average_times)
        else:
            avg_t_ip = avg_t

        self.df_avg_t.set(avg_t_ip)

    except Exception:
        message = "Mac: connection failed\n"
        insert_text(self, message, self.design.color.warning)


def get_nw_params(self, ip):
    """Read network parameters (nw_t, ip, gateway, subnet mask) of a device und set into respectively window.

        Args:
            self: self.nw_t_var, self.df_nw_ip, self.df_nw_gw, self.df_nw_sm.
            ip: value of ip address from the device to read.


    """
    data_device = self.configurator.read_configuration(ip)

    nw_t = data_device["device_config"]["network"]["nw_type"]
    self.old_nwt_device = nw_t

    self.nw_t_var.set(nw_t)

    self.reload()  # update radiobutton

    nw_ip = data_device["device_config"]["network"]["ip"]
    self.df_nw_ip.set(nw_ip)

    nw_gw = data_device["device_config"]["network"]["gw"]
    self.df_nw_gw.set(nw_gw)

    nw_sm = data_device["device_config"]["network"]["sm"]
    self.df_nw_sm.set(nw_sm)


def show_parameters_device(self, ip, mc_ad):
    """Show device parameters.
        Args:
            self: self.df_pc, self.df_sc, self.df_avg_t, self.info_text.
            ip: value of ip address from the device to read.
            mc_ad: value of mac address from the device to read.
    """
    make_input_field_enabled(self)
    delete_all_inputs(self)
    try:
        get_pc_sc_avg(self, ip)
        get_nw_params(self, ip)

        self.df_mc_a.set(mc_ad)

        self.info_text.delete(1.0, END)
        self.info_text.insert(END,
                              "Janitza UMG96 RM-EL \n"
                              "MAC : {} ".format(mc_ad))

    except Exception:
        make_input_field_disabled(self)
        message = "Connection to Device failed !"
        insert_text(self, message, self.design.color.warning)
