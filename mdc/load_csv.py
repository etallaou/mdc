from Tkinter import *
import tkFileDialog
import csv
from .engine import insert_text
from .csv_validator import check_csv_row
from pprint import pprint

__all__ = ["import_csv_file", "read_csv_file", "file_to_list"]


def import_csv_file(self):
    """Import CSV file: askopenfilename, check if format is valid and read.

        Args:
            self: .

    """

    self.csv_data = []
    # get selected full file path
    file_path = tkFileDialog.askopenfilename(filetypes=(("csv files", "*.csv"), ("All files", "*.*")))

    if file_path:
        # check if file is valid
        self.filename = (check_csv_row(self, file_path))

        if self.filename:
            self.csv_data = file_to_list(self, self.filename)
            read_csv_file(self)
            self.send_btn.grid(row=11, column=4, sticky="e", pady=4, padx=3)

        else:
            message = "cannot open the selected file\n"
            self.info_text.insert(1.0, message)
            self.info_text.tag_add('demo', 1.0, 2.0)
            self.info_text.tag_config('demo', foreground=self.design.color.warning)
    else:
        message = 'no file selected'
        insert_text(self, message, self.design.color.warning)


def file_to_list(self, filename):
    """Open a filename from a path and convert contents as list .

        Args:
            self: .
            filename: path of the data to convert.

        Returns
                Returns the converted list self.csv_list or false if path is empty.

    """
    if filename:
        try:
            with open(filename, 'rb') as f:

                r = csv.reader(f, delimiter=';')
                # cut the header file
                self.headers = f.next()
                self.headers = [int(e) if e.isdigit() else e for e in self.headers.split(';')]

                self.headers[9] = self.headers[9].replace("\r\n", "")
                self.csv_list = [l for l in r]
                f.close()
                return self.csv_list
        except IOError:
            pprint('cannot convert')
    else:
        message = "cannot open the selected file"
        self.info_text.insert(1.0, message)


def read_csv_file(self):
    """Read the value of the csv list.

        Args:
            self: .


    """
    self.info_text.delete(1.0, END)
    if self.filename:
        self.csv_data = file_to_list(self, self.filename)

        # pretty print
        if self.csv_data:
            for row in self.csv_data:
                self.info_text.insert(END, '{r[0]} : [\n{space}IDENTIFIER GEE: {r[1]},'
                                           '\n{space}MAC-Address: {r[2]},'
                                           '\n{space}Primary Current [A]: {r[3]},'
                                           '\n{space}Secondary Current [A]: {r[4]},'
                                           '\n{space}Time Interval [Sec]: {r[5]},'
                                           '\n{space}Network Type: {r[6]},'
                                           '\n{space}IP-Address: {r[7]},'
                                           '\n{space}Gateway: {r[8]},'
                                           '\n{space}Subnet-Mask: {r[9]}'
                                           '\n{space}]'.format(space=' ' * 5, r=row))
                self.info_text.insert(END, "\n \n")
        else:
            message = 'csv format is invalid!'
            self.info_text.insert(1.0, message)
    else:
        message = 'no file selected'
        insert_text(self, message, self.design.color.warning)
