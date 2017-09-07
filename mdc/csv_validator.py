from Tkinter import *
import csv
from .engine import insert_text


def csv_extension(self, filename):
    self.info_text.delete(1.0, END)
    file_extension = filename[-4:]
    if file_extension != ".csv":
        message = 'Format invalid .%s not csv file \n' % (file_extension.partition(".")[2])
        insert_text(self, message, self.design.color.warning)
        return False
    else:
        return filename


def csv_delimiter(self, filename):
    filename = csv_extension(self, filename)

    if filename:
        with open(filename, 'rb') as f:
            try:
                dialect = csv.Sniffer().sniff(f.read(1024))
                f.seek(0)
            except csv.Error:
                message = 'csv format is invalid! Nb: it muss be (comma delimited)CSV\n'
                insert_text(self, message, self.design.color.warning)
            else:
                delimiter = repr(dialect.delimiter)
                if delimiter == "';'":
                    return filename
                else:
                    message = 'file has not common delimiter (;)\n'
                    insert_text(self, message, self.design.color.warning)
                    return False

    else:
        return False


def avg_valid(self, avg):
    try:
        avg_t_row = int(avg)
        if avg_t_row in [5, 10, 15, 30, 60, 300, 480, 600, 900]:
            return True

        else:
            text = 'Time Interval invalid\n'
            insert_text(self, text, self.design.color.warning)
            return False

    except ValueError:
        text = 'Time Interval invalid\n'
        insert_text(self, text, self.design.color.warning)
        return False


def secondary_current_valid(self, sd_c):
    try:
        sd_c_row = int(sd_c)

        if sd_c_row in [1, 5]:

            return True

        else:
            text = 'Secondary Current invalid\n'
            insert_text(self, text, self.design.color.warning)
            return False

    except ValueError:
        text = 'ValueError Secondary Current invalid\n'
        insert_text(self, text, self.design.color.warning)
        return False


def pm_c_greater_sd_c(self, pmc_c, sd_c):
    try:

        pmc_c_row = int(pmc_c)
        sd_c_row = int(sd_c)
        if pmc_c_row >= sd_c_row and (pmc_c_row <= 1000000):
            return True

        else:
            text = 'invalid Primary or Secondary Current\n(Primary > Secondary Current and Primary <= 1000000)\n'
            insert_text(self, text, self.design.color.warning)
            return False

    except ValueError:
        text = 'ValueError\ninvalid Primary or Secondary Current\n' \
               '(Primary > Secondary Current and Primary <= 1000000)\n'
        insert_text(self, text, self.design.color.warning)
        return False


def nwt_static_dynamic(self, nwt):
    try:
        nwt_row = nwt.lower()

        if nwt_row in ['dynamic', 'static']:
            return True

        else:
            text = 'Invalid network type (dynamic or static)\n'
            insert_text(self, text, self.design.color.warning)
            return False

    except ValueError:
        text = 'ValueError Invalid network type (dynamic or static)\n'
        insert_text(self, text, self.design.color.warning)
        return False


def ip_valid(self, nwt, ip):
    """Check if a str_input has a ip' s format.

        Args:
            ip(str): value of the ip.
            nwt(str): value of the network type.
            self: .

        Returns:
        return True or False.
    """

    if nwt.lower() == 'static':
        m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
        is_ip = bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))
        if is_ip:
            return True
        else:
            text = 'invalid Ip Format\n'
            insert_text(self, text, self.design.color.warning)
            return False
    elif nwt.lower() == 'dynamic':
        return True
    else:
        text = 'invalid network type\n'
        insert_text(self, text, self.design.color.warning)
        return False


def is_header_valid(self, filename):
    filename = csv_delimiter(self, filename)
    columns_to_analyze = ['If. Nr.', 'IDENTIFIER GEE', 'MAC-Address', 'Primary Current [A]', 'Secondary Current [A]',
                          'Time Interval [Sec]', 'Network Type', 'IP-Address', 'Gateway', 'Subnet-Mask']
    if filename:
        with open(filename, 'rb') as f:
            headers = f.next()
            headers = [int(e) if e.isdigit() else e for e in headers.split(';')]
            headers[9] = headers[9].replace("\r\n", "")
            compare = (set(headers) == set(columns_to_analyze))
            if compare:
                return filename
            else:
                text = 'invalid headers\n'
                insert_text(self, text, self.design.color.warning)
                return False


def check_csv_row(self, filename):
    filename = is_header_valid(self, filename)
    if filename:
        with open(filename, 'rb') as f:
            f.next()
            r = csv.reader(f, delimiter=';')
            try:

                for row in r:
                    if avg_valid(self, row[5]) and \
                            secondary_current_valid(self, row[4]) and \
                            pm_c_greater_sd_c(self, row[3], row[4]) and \
                            nwt_static_dynamic(self, row[6]) and \
                            ip_valid(self, row[6], row[7]) and \
                            ip_valid(self, row[6], row[8]) and \
                            ip_valid(self, row[6], row[9]):
                        continue

                    else:

                        text = 'format invalid\n'
                        self.info_text.insert(END, text)

                        return False
            except Exception:

                text = 'An Exception error has occurred\n'
                insert_text(self, text, self.design.color.warning)
                return False
            else:
                return filename
    else:
        text = 'format invalid\n'
        self.info_text.insert(END, text)
        return False
