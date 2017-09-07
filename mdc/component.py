#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import ttk

__all__ = ["entries_button_grid", "create_label", "label_grid", "create_entry_field", "variable"]


def entries_button_grid(self):
    """Set entries and button to a appropriate place (column, row, x, y) of the grid.

       Args:
        self: entries and buttons'instances.
    """

    self.e_pm_c.grid(row=0, column=1, sticky="e", pady=4, padx=3)
    self.e_sd_c.grid(row=1, column=1, sticky="e", pady=4, padx=3)
    self.e_avg_t.grid(row=2, column=1, sticky="e", pady=4, padx=3)
    self.e_st_nw_t.grid(row=4, column=1, sticky="e", pady=4, padx=3)
    self.e_st_nw_t.place(x=410, y=124, width=120, height=23)
    self.e_dn_nw_t.grid(row=4, column=1, sticky="e", pady=4, padx=3)
    self.e_dn_nw_t.place(x=510, y=124, width=120, height=23)
    self.e_ip.grid(row=5, column=1, sticky="e", pady=4, padx=3)
    self.e_gw.grid(row=6, column=1, sticky="e", pady=4, padx=3)
    self.e_sm.grid(row=7, column=1, sticky="e", pady=4, padx=3)
    self.e_mc_a.grid(row=8, column=1, sticky="e", pady=4, padx=3)
    self.cancel_btn.grid(row=11, column=1, )
    self.save_btn.grid(row=11, column=3, sticky="e", pady=4, padx=3)


def create_label(self):
    """create label instances for  entries and button.

       Args:
           self: form_box(Frame), design(class object) from Home.
    """

    self.pc_label = Label(self.form_box, text="Primary Current [A]:", anchor='nw', width=32,
                          bg=self.design.color.secondary, font=('Arial', 15))
    self.sc_label = Label(self.form_box, text="Secondary Current [A]:", anchor='nw', width=32,
                          bg=self.design.color.secondary, font=('Arial', 15))
    self.avg_t_label = Label(self.form_box, text="Average Time [s]: ", anchor='nw', width=32,
                             bg=self.design.color.secondary, font=('Arial', 15))
    self.nwt_label = Label(self.form_box, text="network type (static/dynamic):", anchor='nw', width=32,
                           bg=self.design.color.secondary, font=('Arial', 15))
    self.nw_ip_label = Label(self.form_box, text="IpAddress:", anchor='nw', width=32,
                             bg=self.design.color.secondary, font=('Arial', 15))
    self.nw_gw_label = Label(self.form_box, text="Gateway:", anchor='nw', width=32, bg=self.design.color.secondary,
                             font=('Arial', 15))
    self.nw_sm_label = Label(self.form_box, text="subnet mask:", anchor='nw', width=32,
                             bg=self.design.color.secondary, font=('Arial', 15))
    self.nw_mca_label = Label(self.form_box, text="Mac Address:", anchor='nw', width=32,
                              bg=self.design.color.secondary, font=('Arial', 15))


def label_grid(self):
    """Set labels to a appropriate place (column, row, x, y) of the grid.

       Args:
           self: labels'instances.
    """

    self.pc_label.grid(row=0, sticky="nw", pady=2, padx=3)
    self.sc_label.grid(row=1, sticky="nw", pady=2, padx=3)
    self.avg_t_label.grid(row=2, sticky="nw", pady=2, padx=3)
    self.nwt_label.grid(row=4, sticky="nw", pady=2, padx=3)
    self.nw_ip_label.grid(row=5, sticky="nw", pady=2, padx=3)
    self.nw_gw_label.grid(row=6, sticky="nw", pady=2, padx=3)
    self.nw_sm_label.grid(row=7, sticky="nw", pady=2, padx=3)
    self.nw_mca_label.grid(row=8, sticky="nw", pady=2, padx=3)


def create_entry_field(self):
    """Create entries and buttons instances.

       Args:
           self: form_box(Frame), save_cancel_box(Frame), variable(df_sc, df_avg_t, ...),design(class object),

    """
    self.e_pm_c = Entry(self.form_box, textvariable=self.df_pc, state='disabled', width=32,
                        bg=self.design.color.secondary, font=('Arial', 15))

    self.secondary_currents = [1, 5]
    self.e_sd_c = ttk.Combobox(self.form_box, textvariable=self.df_sc, state='disabled', width=30,
                               font=('Arial', 15))
    self.e_sd_c['values'] = self.secondary_currents
    self.e_sd_c.config(background=self.design.color.secondary)

    self.user_average_times = [5, 10, 15, 30, 60, 300, 480, 600, 900]
    self.janitza_umg_avg_times = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    self.e_avg_t = ttk.Combobox(self.form_box, textvariable=self.df_avg_t, state='disabled', width=30,
                                font=('Arial', 15))
    self.e_avg_t['values'] = self.user_average_times
    self.e_avg_t.config(background=self.design.color.secondary)

    self.e_st_nw_t = Radiobutton(self.form_box, text="static", variable=self.nw_t_var, value=0,
                                 relief=self.design.button_relief,
                                 command=self.reload, state='disabled', font=('Arial', 15))
    self.e_dn_nw_t = Radiobutton(self.form_box, text="dynamic", variable=self.nw_t_var, value=2,
                                 relief=self.design.button_relief,
                                 command=self.reload, state='disabled', font=('Arial', 15))

    self.e_ip = Entry(self.form_box, textvariable=self.df_nw_ip, state='disabled', width=32,
                      bg=self.design.color.secondary, font=('Arial', 15))
    self.e_gw = Entry(self.form_box, textvariable=self.df_nw_gw, state='disabled', width=32,
                      bg=self.design.color.secondary, font=('Arial', 15))
    self.e_sm = Entry(self.form_box, textvariable=self.df_nw_sm, state='disabled', width=32,
                      bg=self.design.color.secondary, font=('Arial', 15))
    self.e_mc_a = Entry(self.form_box, state='disabled', textvariable=self.df_mc_a, width=32,
                        bg=self.design.color.secondary, font=('Arial', 15))

    # button

    self.cancel_btn = Button(self.save_cancel_box, text='Cancel', command=self.save_cancel_box.quit,
                             state='disabled', font=('Arial', 15), bg=self.design.color.secondary)

    self.save_btn = Button(self.save_cancel_box, text='Save', command=self.save_dialog, state='disabled',
                           foreground=self.design.color.secondary, font=('Arial', 15), bg=self.design.color.primary)

    self.send_btn = Button(self.save_cancel_box, text='Send', command=self.send_data_to_device, state='normal',
                           foreground=self.design.color.secondary, font=('Arial', 15), bg=self.design.color.primary)


def variable(self):
    """Declaration for the variable to define the device's parameters .

       Args:
           self: initialisation of variable
    """

    self.df_pc = IntVar()
    self.df_sc = IntVar()
    self.df_avg_t = StringVar()
    self.nw_t_var = IntVar()
    self.df_nw_ip = StringVar()
    self.df_nw_gw = StringVar()
    self.df_nw_sm = StringVar()
    self.df_mc_a = StringVar()
    self.nw_index = IntVar()
    self.work_ip_address = StringVar()
    self.ip_for_ping = StringVar()
    self.main_gateway = StringVar()
    self.loading_count = 17
    self.MAX_PC = 1000000
    self.test = StringVar()
    self.filename = ''

