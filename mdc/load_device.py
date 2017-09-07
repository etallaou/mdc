#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import os
import subprocess

__all__ = ["insert_in_listbox", "search_umg_devices", "rebooting_window"]


def insert_in_listbox(self):
    """Insert Device from active network in listbox.

        Args:
            self: Home, self.listbox, self.devices, self.info_text.

    """
    from .init_menu import delete_all_inputs, make_input_field_disabled
    if self.ip_for_ping.get() != '':
        self.devices = reload_devices(self, self.ip_for_ping.get())
    delete_all_inputs(self)
    self.listbox.delete(0, END)

    if len(self.devices) == 0:
        self.info_text.delete(1.0, END)
        self.info_text.insert(END, "No devices found!\nCheck your connection and start again. \n")

    else:
        self.listbox.bind('<<ListboxSelect>>', self.get_selected_item)
        for device in self.devices:
            self.listbox.insert(END, ' {} with {} '.format(device[1], device[0]))
            self.listbox.itemconfig(END, foreground=self.design.color.secondary)

        self.info_text.delete(1.0, END)
        self.info_text.insert(END,
                              "{} Device(s) found  \n".format(
                                  len(self.devices)))

        if len(self.devices) > 0:
            self.info_text.insert(END, "Click to edit\n")

        make_input_field_disabled(self)

        if self.save_count > 0:
            self.info_text.insert(END, "-------------------------------------------\n ")
            self.info_text.insert(END, "Configurations:\n ")
            self.info_text.insert(END, self.configurations)


def search_umg_devices(self):
    """Run Loading Animation after rebooting and file > search and get configurable devices list .

        Args:
            self: Home, self.message_box, self.devices, self.design.

    """
    from .engine import search_devices
    self.info_text.delete(1.0, END)
    pipe_str = '|'

    loading_window = Toplevel(background=self.design.color.primary)  # new window
    loading_window.geometry("200x75")

    loading_pipe = Label(master=self.message_box, text='|', background=self.design.color.primary, font='Arial',
                         foreground=self.design.color.secondary)
    loading_pipe.pack(anchor=CENTER)

    loading_msg = Label(master=loading_window, background=self.design.color.primary,
                        text='Devices are loading... \nwait some seconds', foreground=self.design.color.secondary)
    loading_msg.pack(anchor=CENTER, fill=BOTH)

    self.info_text.insert(END, pipe_str)

    def loading_animation():
        """Loading Animation."""
        text = loading_pipe.cget('text')
        stand = len(text)

        if stand < 69:
            text += '|'
            loading_pipe.config(text=text)
            loading_pipe.after(10, loading_animation)
            self.info_text.insert(END, pipe_str)
        elif stand == 69:

            loading_window.destroy()
            self.info_text.delete(1.0, END)

            if self.ip_for_ping.get() == '':

                self.devices = search_devices(self)  # get devices list
            insert_in_listbox(self)

    loading_animation()


def rebooting_window(self, len_devices):
    """Rebooting window after configuration.

        Args:
            self: Home, self.listbox, self.devices, self.info_text.
            len_devices: number of devices to edit.

    """
    countdown_window = Toplevel(background=self.design.color.primary)
    countdown_window.geometry("300x300")

    label_timer = Label(master=countdown_window, text=self.text_countdown, background=self.design.color.primary,
                        font=('Arial', 100), foreground=self.design.color.secondary)
    label_timer.pack(anchor='c')  # center

    if len_devices == 1:
        start_countdown = Label(master=countdown_window, background=self.design.color.primary,
                                text='Device : \n %s \n %s \n is rebooting..' % (
                                    self.devices[self.current_device.get()][0],
                                    self.devices[self.current_device.get()][1]),
                                foreground=self.design.color.secondary)
        start_countdown.pack()

    elif len_devices > 1:
        label_text = Label(master=countdown_window, background=self.design.color.primary,
                           text='Devices are rebooting...', foreground=self.design.color.secondary)

        label_text.pack()

    def countdown():
        """Countdown window after Configuration."""
        stand = int(label_timer.cget('text'))
        if stand > 0:
            stand -= 1
            label_timer.config(text=str(stand))
            label_timer.after(1000, countdown)

        elif stand == 0:
            countdown_window.destroy()
            search_umg_devices(self)

    countdown()


def reload_devices(self, ip):
    """Reloading  devices for more active network.
        Args:
            self: Home, self.listbox, self.devices, self.info_text.
            ip: ip of devices to reload.

    """

    with open(os.devnull, "wb") as limbo:  # ping
        # Get all hosts on that network  based on three first arg for ip_address
        for n in xrange(0, 256):
            new_ip = ip[:] + "{0}".format(n)
            subprocess.Popen(["ping", new_ip], stdout=limbo, stderr=limbo)

    search_character = '00-0e-6b-07'
    cmd = 'arp -a'

    output = subprocess.check_output(cmd, shell=True)
    result = output.splitlines()
    devices_addresses = result[3::]
    machine_list = [item for item in devices_addresses if (search_character in item)]
    my_space = ' '
    interface_list = [i.split(my_space) for i in machine_list]
    new_list = [new_list[i] for new_list in interface_list for i in range(0, len(new_list)) if
                new_list[i] is not ""]
    machines = [(new_list[i], new_list[i + 1]) for i in xrange(0, len(new_list), 3)]

    # filter device with same ip address as gateway of active network.
    machines = [device for device in machines if (re.search(self.ip_for_ping.get(), device[0]))]
    return machines
