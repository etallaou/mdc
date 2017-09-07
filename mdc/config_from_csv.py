from Tkinter import *
import csv
from .engine import mapping_avg_time, convert_nw_type, edit_single_device, insert_text
from .load_csv import read_csv_file, file_to_list

__all__ = ["import_csv_file", "read_csv_file", "file_to_list"]


def find_element_in_list(a_list, index):
    """Find element in a list by indey.

        Args:
            a_list: the vale of list.
            index: the index.

        Returns
                Returns the value of the list index or False.

    """
    try:
        device = a_list[index]
        return device
    except IndexError:
        return False


def build_config_list(self):
    """Build the configuration List.

        Args:
            self: .

    """
    devices_index = -1

    # get all config from the csv_list where mac address is 'tbd'
    self.config_list = [self.csv_list[row][2] for row in range(0, len(self.csv_list)) if self.csv_list[row][2] == 'tbd']
    self.config_devices = []
    self.config_params = []
    self.write_in_data = False

    if not self.current_list:

        # selected devices from listbox
        self.info_text.delete(1.0, END)
        self.info_text.insert(END, "no devices selected")

    elif not self.config_list:
        self.info_text.delete(1.0, END)
        self.info_text.insert(END, "no devices to edit in csv file")
    elif self.config_list and self.current_list:
        self.to_edit_device = [self.devices[item] for item in self.current_list]
        for row in range(0, len(self.csv_list)):
            if self.csv_list[row][2] == 'tbd' and find_element_in_list(self.to_edit_device, devices_index + 1):
                self.csv_list[row][2] = self.to_edit_device[devices_index + 1][1]

                self.config_params = [
                    self.to_edit_device[devices_index + 1][0], int(self.csv_list[row][3]), int(self.csv_list[row][4]),
                    mapping_avg_time(int(self.csv_list[row][5]), self.user_average_times, self.janitza_umg_avg_times),
                    convert_nw_type(self.csv_list[row][6]), self.csv_list[row][7],
                    self.csv_list[row][8], self.csv_list[row][9]
                ]

                try:
                    edit_device_row(self, self.config_params)

                except Exception:
                    self.config_devices.append((self.csv_list[row][1], self.to_edit_device[devices_index + 1][1], "X"))
                    devices_index += 1

                else:

                    self.config_devices.append((self.csv_list[row][1], self.to_edit_device[devices_index + 1][1], "OK"))
                    write_mac(self, self.csv_list, self.filename)

                    devices_index += 1

        show_devices_nr(self, self.config_devices, (devices_index + 1))
        if self.send_btn:
            self.send_btn.grid_forget()


def write_mac(self, lines, filename):
    """Write a list into a file.

        Args:
            self: .
            lines: value of the list to write.
            filename: full filename of the list.

    """

    try:
        f = open(filename, 'wb')
    except IOError:
        message = "Cannot Write into csv file. check if file is closed"
        insert_text(self, message, self.design.color.warning)
        self.write_in_data = False
    else:
        if lines[0] != self.headers:
            lines.insert(0, self.headers)
        writer = csv.writer(f, delimiter=';')  # Here your csv file
        writer.writerows(lines)
        f.close()
        self.write_in_data = True


def show_devices_nr(self, devices, total_edit):
    """Show all the be edited devices  and the Configuration's result(OK or X) .

        Args:
            self: .
            devices: to be edit devices.
            total_edit: number of to be edit devices.

    """
    if self.write_in_data:
        self.info_text.delete(1.0, END)
        self.info_text.insert(1.0, "%s Devices have been edit check result:\n\n" % total_edit)
        for device in devices:
            self.info_text.insert(END, "{:10}{:10}  {:10}".format(device[0], device[1], device[2]))
            self.info_text.insert(END, "\n")
    else:
        self.info_text.insert(1.0, "Configuration done but. Write in csv file failed \n \n")
        self.info_text.tag_add('demo', 1.0, 2.0)
        self.info_text.tag_config('demo', foreground=self.design.color.warning)


def edit_device_row(self, parameters):
    """Edit the Parameters into device.

        Args:
            self: .
            parameters: Parameters of the devices.


    """
    edit_single_device(self, parameters[0], parameters[1], parameters[2], parameters[3],
                       parameters[4], parameters[5], parameters[6], parameters[7])


