from Tkinter import *
import netifaces
import os
import subprocess
import re
import _winreg as wr
from .load_device import insert_in_listbox

__all__ = ["insert_text", "mapping_avg_time", "get_connection", "get_pc_gw", "get_active_interfaces",
           "get_work_network",  "edit_ip_for_ping", "ping_all_ip", "search_devices", "is_valid_ip",
           "edit_multi_devices", "ip_to_int", "is_ip_in_subnet", "get_mask_length", "convert_nw_type    "]


def insert_text(self, text, color):
    """Insert a text into insert_test(frame).

       Args:
           self(instance of class object): info_text(Frame).
           text(text): Value of text to be insert.
           color(str): main Class.

    """
    self.info_text.delete(1.0, END)
    self.info_text.insert(END, text)
    self.info_text.tag_add('demo', 1.0, 3.0)
    self.info_text.tag_config('demo', foreground=color)


def convert_nw_type(nwt):
    """Convert network type to int, 2 if dynamic and 0 if static.
       Args:
           nwt: value of network type to be edit.
        Returns:
        2 if dynamic and 0 if static.

    """
    nwt = nwt.lower()
    if nwt == 'dynamic':
        nwt = 2
        return nwt
    elif nwt == 'static':
        nwt = 0
        return nwt


def mapping_avg_time(entry, list1, list2):
    """Mapping an entry(data) from a first list1 to a second list 2.

       Args:
           entry: to be mapped data (str or int).
           list1(list): first list.
           list2(list): second list.

        Returns:
        the mapped value from the list2.

    """

    item_index = list1.index(entry)
    return list2[item_index]


def get_connection(ni_interface_name):
    """Get meaningful network interface names instead of GUIDs.

       Args:
           ni_interface_name(str): netifaces network interface names .

        Returns:
        The meaningful network interface names or '(unknown)' .

    """

    interface_name = '(unknown)'
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')

    try:
        reg_subkey = wr.OpenKey(reg_key, ni_interface_name + r'\Connection')
        interface_name = wr.QueryValueEx(reg_subkey, 'Name')[0]
    except Exception:
        pass

    return interface_name


def get_pc_gw(self):
    """Get main Network gateway.

       Args:
           self:.

        Returns:
        The meaningful network interface names or '(unknown)'.
    """

    if len(self.active_networks) == 1:
        self.gw_ping = self.active_networks[0]
        self.main_gateway.set(self.gw_ping)
        insert_in_listbox(self)
    elif len(self.active_networks) > 1:
        self.listbox.delete(0, END)
        self.listbox.bind('<<ListboxSelect>>', self.change_network)
        for nw in self.active_networks:
            self.listbox.insert(END, nw)
            self.listbox.itemconfig(END, foreground=self.design.color.secondary)

        self.info_text.delete(1.0, END)
        self.info_text.insert(END, "Please select your network \n")


def get_active_interfaces(self):
    """Fill the active networks in a list(self.active_networks).

       Args:
           self: self.active_networks.
    """
    ni_gws = netifaces.gateways()
    try:
        active_interfaces = ni_gws[netifaces.AF_INET]
        active_gateways = [active_interface[0] for active_interface in active_interfaces]
        active_gateways = list(set(active_gateways))
        self.active_networks = active_gateways

    except Exception:
        message = "No  Network \n"
        insert_text(self, message, self.design.color.warning)


def get_work_network(self, evt):
    """Set the gw of the selected network as work_ip and search device.

       Args:
           self: nw_index, gw_ping, work_ip_address, active_networks, search_device_home().
           evt: Tkinter instance.


    """
    selected_nw = evt.widget
    nw_index = int(selected_nw.curselection()[0])
    self.nw_index.set(nw_index)
    self.gw_ping = self.active_networks[self.nw_index.get()]
    self.main_gateway.set(self.gw_ping)
    self.active_networks = [self.active_networks[self.nw_index.get()]]
    self.search_device_home()  # search


def edit_ip_for_ping(self):
    """Delete the three last characters from work_ip_address.

       Args:
           self(instance): nw_index, gw_ping, work_ip_address, active_networks, search_device_home() .

    """
    get_pc_gw(self)
    ip_address_basis = (self.main_gateway.get()).split('.')
    ip_address_basis = [(ip_address_basis[i] + '.') for i in range(3)]
    ip_address_basis = ''.join(ip_address_basis)
    self.ip_for_ping.set(ip_address_basis)

    return self.ip_for_ping.get()


def ping_all_ip(self):
    """ping all ip address from the network segment.

       Args:
           self: nw_index, gw_ping, work_ip_address, active_networks, search_device_home() .

    """

    ip = edit_ip_for_ping(self)

    with open(os.devnull, "wb") as limbo:  # pin
        # Get all hosts on that network  based on three first arg for ip_address
        for n in xrange(0, 256):
            new_ip = ip[:] + "{0}".format(n)
            subprocess.Popen(["ping", new_ip], stdout=limbo, stderr=limbo)



def search_devices(self):
    """Search connected devices of the active network
        Args:
            self: .


        Returns:
        a list of tuple of the devices[(ip address, mac address)].
    """

    ping_all_ip(self)
    # restrict to janiza devices
    search_character = '00-0e-6b-07'  #  umg basis mac address
    cmd = 'arp -a'
    try:
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

    except Exception:
        message = "error by search configurable device \n"
        insert_text(self, message, self.design.color.warning)


def is_valid_ip(ip):
    """Check if a str_input has a ip' s format.

        Args:
            ip(str): value of the ip.

        Returns:
        return True or False.
    """

    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


def edit_single_device(self, device_ip, p_c, s_c, a_t, nw_type, nw_ip, nw_sm, nw_gw):
    """Configuration the new Parameters  in single device.

        Args:
            self: Home.
            device_ip: old value of the ip from device to be edit.
            p_c: new value of primary current parameter.
            s_c: new value of secondary current parameter..
            a_t: new value of averaging time parameter.
            nw_type: new value of the network type parameter.
            nw_ip: new value of the ip parameter.
            nw_sm: new value of the subnet mask parameter.
            nw_gw: new value of the gateway parameter.

    """

    self.configurator.write_configuration(device_ip, {
        'device_config': {'secondary_current': s_c, 'primary_current': p_c,
                          'network': {'gw': nw_gw, 'ip': nw_ip, 'sm': nw_sm, 'nw_type': nw_type},
                          'average_time': a_t}})


def edit_multi_devices(self, device_ip, p_c, s_c, a_t, nw_type, ):
    """configuration the new Parameters  in more devices.

        Args:
            self: Home.
            device_ip: old value of the ip from device to be edit.
            p_c: new value of primary current parameter.
            s_c: new value of secondary current parameter..
            a_t: new value of averaging time parameter.
            nw_type: new value of the network type parameter.

    """

    self.configurator.write_configuration(device_ip, {
        'device_config': {'secondary_current': s_c, 'primary_current': p_c,
                          'network': {'nw_type': nw_type}, 'average_time': a_t}})


def ip_to_int(ip):
    """Returns int-encoded given IP address.

        Args:
            ip: value of IP address to encode.

        Returns:
        int-encoded given IP address.
    """
    o = map(int, ip.split('.'))
    res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    return res


def is_ip_in_subnet(ip, gateway, mask_length):
    """Check if gateway reside in the same network segment define by ip address and subnet.

        Args:
            ip: value of the ip.
            gateway: value of the gateway.
            mask_length: value of the subnet mask length.

        Returns:
        return True or False.
    """

    ip_int = ip_to_int(ip)  # my test ip, in int form

    mask_length_from_right = 32 - mask_length

    ip_network_int = ip_to_int(gateway)  # convert the ip network into integer form
    binstring = "{0:b}".format(ip_network_int)  # convert that into into binary (string format)

    chop_amount = 0  # find out how much of that int I need to cut off
    for i in range(mask_length_from_right):
        if i < len(binstring):
            chop_amount += int(binstring[len(binstring) - 1 - i]) * 2 ** i

    min_val = ip_network_int - chop_amount
    max_val = min_val + 2 ** mask_length_from_right - 1

    return min_val <= ip_int <= max_val


def get_mask_length(sm):
    """Address Prefix Length of a subnet mask.

        Args:
            sm: value of the ip.
        Returns:
        return the value of the Address Prefix Length.
    """
    subnet = sum([bin(int(x)).count('1') for x in sm.split('.')])
    return subnet
