#!/usr/bin/env python
# -*- coding: utf-8 -*-


from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import ipaddress

__all_ = ["UmgConfigurator"]


class UmgConfigurator(object):

    def write_configuration(self, umg_ip_address, configuration):
        """Writes configuration dictionary to UMG-device via MODBUS protocol.

            Args:
                umg_ip_address: IP address of the umg-device
                configuration: Example dictionary: {'device_config':{'primary_current':5,'secondary_current':5,
                                                           'average_time':6,'network':{'nw_type':'static','ip':'192.168.2.172',
                                                           'sm':'255.255.255.0','gw':'192.168.2.1'}}}.
        """

        self.umg_controller(umg_ip_address, 10, "float", mode="write",
                            data=configuration["device_config"]["primary_current"])
        self.umg_controller(umg_ip_address, 12, "float", mode="write",
                            data=configuration["device_config"]["secondary_current"])
        self.umg_controller(umg_ip_address, 18, "float", mode="write",
                            data=configuration["device_config"]["primary_current"])
        self.umg_controller(umg_ip_address, 20, "float", mode="write",
                            data=configuration["device_config"]["secondary_current"])
        self.umg_controller(umg_ip_address, 26, "float", mode="write",
                            data=configuration["device_config"]["primary_current"])
        self.umg_controller(umg_ip_address, 28, "float", mode="write",
                            data=configuration["device_config"]["secondary_current"])

        self.umg_controller(umg_ip_address, 40, "short", mode="write",
                            data=configuration["device_config"]["average_time"])
        self.umg_controller(umg_ip_address, 41, "short", mode="write",
                            data=configuration["device_config"]["average_time"])
        self.umg_controller(umg_ip_address, 42, "short", mode="write",
                            data=configuration["device_config"]["average_time"])

        if configuration["device_config"]["network"]["nw_type"] == 2:
            self.umg_controller(umg_ip_address, 7, "short", mode="write",
                                data=configuration["device_config"]["network"]["nw_type"])

        else:
            self.write_ip_stack(umg_ip_address, configuration["device_config"]["network"]["ip"],
                                configuration["device_config"]["network"]["gw"],
                                configuration["device_config"]["network"]["sm"],
                                configuration["device_config"]["network"]["nw_type"])

    def read_configuration(self, umg_ip_address):

        """Reads configuration from UMG-device via MODBUS protocol and returns data as dictionary.

            Args:
                umg_ip_address:.

            Returns
                Returns data dictionary, example dictionary: {'device_config':{'primary_current':5,
                                                                'secondary_current':5,'average_time':6,
                                                                'network':{'nw_type':'static','ip':'192.168.2.172',
                                                                'sm':'255.255.255.0','gw':'192.168.2.1'}}}.
        """
        data = {
            "device_config": {
                "primary_current_l1": self.umg_controller(umg_ip_address, 10, "float"),
                "primary_current_l2": self.umg_controller(umg_ip_address, 18, "float"),
                "primary_current_l3": self.umg_controller(umg_ip_address, 26, "float"),
                "secondary_current_l1": self.umg_controller(umg_ip_address, 12, "float"),
                "secondary_current_l2": self.umg_controller(umg_ip_address, 20, "float"),
                "secondary_current_l3": self.umg_controller(umg_ip_address, 28, "float"),
                "average_time_i": self.umg_controller(umg_ip_address, 40, "short"),
                "average_time_p": self.umg_controller(umg_ip_address, 41, "short"),
                "average_time_u": self.umg_controller(umg_ip_address, 42, "short"),
                "network": {
                    "nw_type": self.umg_controller(umg_ip_address, 7, "short"),
                    "ip": self.umg_controller(umg_ip_address, 1, "ip_address"),
                    "gw": self.umg_controller(umg_ip_address, 3, "ip_address"),
                    "sm": self.umg_controller(umg_ip_address, 5, "ip_address")
                }
            }
        }

        return data

    def umg_controller(self, umg_ip_address, umg_mb_address, data_type, mode="read", count=2, data=None):
        """Controls the writing- and reading process from functions write_configuration and read_configuration.

            Args:

                umg_ip_address: IP address of the Janitza-device.
                umg_mb_address: MODBUS address of wanted value.
                data_type: Data type of wanted value.
                mode: read or write MODBUS.
                count: Count of registers wanted.
                data: Data to write to Janitza-device.
                Returns data to read_configuration..
        """

        umg_device = ModbusClient(umg_ip_address)
        umg_device.connect()

        response = None

        if mode == "write":
            builder = BinaryPayloadBuilder(endian=Endian.Big)

            if data_type == "ip_adress":
                builder.add_32bit_uint(int(self.ip_to_int(data)))
            elif data_type == "float":
                builder.add_32bit_float(data)
            elif data_type == "short":
                builder.add_16bit_int(data)

            payload = builder.build()
            response = umg_device.write_registers(umg_mb_address, payload, skip_encode=True)
        elif mode == "read":
            result = umg_device.read_holding_registers(umg_mb_address, count)

            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, endian=Endian.Big)

            if data_type == "ip_address":
                decoded = {"32uint": decoder.decode_32bit_uint()}
            elif data_type == "float":
                decoded = {"float": decoder.decode_32bit_float()}
            elif data_type == "short":
                decoded = {"short": decoder.decode_16bit_int()}
            else:
                raise NotImplementedError("wrong data type.")

            for name, value in decoded.iteritems():
                if data_type == "ip_address":
                    response = ipaddress.IPv4Address(value)
                else:
                    response = value

        umg_device.close()

        return response

    def write_ip_stack(self, umg_ip_address, ip, gw, sm, nt):
        """Writes the IP configuration in one stack into the umg_device.

            Args:
                umg_ip_address: IP address of the umg -device
                ip: New IP address
                gw: New gateway address
                sm: New subnet mask address
                nt: Network type parameter - 0 = static / 2 = dynamic
        """

        builder = BinaryPayloadBuilder(endian=Endian.Big)
        builder.add_32bit_uint(int(self.ip_to_int(ip)))
        builder.add_32bit_uint(int(self.ip_to_int(sm)))
        builder.add_32bit_uint(int(self.ip_to_int(gw)))
        builder.add_16bit_int(nt)

        umg_device = ModbusClient(umg_ip_address)
        umg_device.connect()

        payload = builder.build()
        umg_device.write_registers(1, payload, skip_encode=True)

    @staticmethod
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


