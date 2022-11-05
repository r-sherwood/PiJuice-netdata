# -*- coding: utf-8 -*-
# Description: PiJuice netdata collector to monitor battery and voltage, python.d module
# Author: (r-sherwood)
# Source: https://github.com/r-sherwood/PiJuice-netdata
# SPDX-License-Identifier: GPL-3.0-or-later

from bases.FrameworkServices.SimpleService import SimpleService
from pijuice import PiJuice
from pijuice import __version__ as library_version




NETDATA_UPDATE_EVERY=1
priority = 90000

ORDER = [
    "charge_current",
    "batteryVoltage_current",
    "batteryCurrent_current",
    "temp_current",
    "ioVoltage_current",
    "ioCurrent_current"
]

CHARTS = {
    "temp_current": {
        'options': ['batteryTemperature', 'Battery temperature', 'Celsius', 'battery', 'pijuice.GetBatteryTemperature', 'line'],
        'lines': [
            ['tempHot','hot temperature', 'absolute', 1, 1],
            ['batteryTemperature','current temperature', 'absolute', 1, 1],
            ['tempCold','cold temperature', 'absolute', 1, 1],
        ]
     },
    "charge_current": {
        'options': ['batteryCharge', 'Battery charge level', '%', 'battery', 'pijuice.GetChargeLevel', 'stacked'],
        'lines': [
            ['batteryChargeFull', 'till fully charged'],
            ['batteryCharge', 'charge level', 'absolute', 1, 1],
        ]
     },
     "batteryVoltage_current": {
        'options': ['batteryVoltage', 'Battery voltage', 'V', 'battery', 'pijuice.GetBatteryVoltage', 'line'],
        'lines': [
            ['regulationVoltage', 'regulation voltage', 'absolute', 1, 1000],
            ['batteryVoltage', 'voltage', 'absolute', 1, 1000],
            ['cutoffVoltage', 'cutoff voltage', 'absolute', 1, 1000],
        ]
     },
    "batteryCurrent_current": {
        'options': ['batteryCurrent', 'Battery current', 'A', 'battery', 'pijuice.GetBatteryCurrent', 'line'],
        'lines': [
            ['batteryCurrent', 'current', 'absolute', 1, 1000],
        ]
     },
    "ioVoltage_current": {
        'options': ['ioVoltage', 'Voltage supplied from the GPIO power output from the PiJuice or when charging', 'V', 'power input', 'pijuice.GetIoVoltage', 'line'],
        'lines': [
            ['ioVoltage', 'voltage', 'absolute', 1, 1000]
        ]
     },
    "ioCurrent_current": {
        'options': ['ioCurrent', 'Current supplied from the GPIO power output from the PiJuice or when charging. Positive current is from PiJuice to Raspberry Pi', 'A', 'power input', 'pijuice.GetIoCurrent', 'line'],
        'lines': [
            ['ioCurrent', 'current', 'absolute', 1, 1000],
        ]
     }
}

class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        #values to show at graphs
        self.values=dict()

    @staticmethod
    def check():
        return True


    def logMe(self,msg):
        self.debug(msg)


    def get_data(self):
        #The data dict is basically all the values to be represented
        # The entries are in the format: { "dimension": value}
        #And each "dimension" should belong to a chart.
        data = dict()
        pij_data = dict()

        pijuice = PiJuice(1, 0x14)  # Instantiate PiJuice interface object

        status = pijuice.status.GetStatus()["data"]
        profile = pijuice.config.GetBatteryProfile()["data"]
        
        pij_data = {
            "batteryCharge": pijuice.status.GetChargeLevel()["data"],
            "batteryVoltage": pijuice.status.GetBatteryVoltage()["data"],
            "batteryCurrent": pijuice.status.GetBatteryCurrent()["data"],
            "batteryTemperature": pijuice.status.GetBatteryTemperature()["data"],
            "batteryStatus": status["battery"],
            "powerInput": status["powerInput"],
            "powerInput5vIo": status["powerInput5vIo"],
            "ioVoltage": pijuice.status.GetIoVoltage()["data"],
            "ioCurrent": pijuice.status.GetIoCurrent()["data"],
            "regulationVoltage":  pijuice.config.GetBatteryProfile()["data"],
        }
        data['batteryCharge'] = pij_data['batteryCharge']
        data['batteryChargeFull'] = 100-pij_data['batteryCharge']
        data['batteryVoltage'] = pij_data['batteryVoltage']
        data['batteryCurrent'] = pij_data['batteryCurrent']
        data['batteryTemperature'] = pij_data['batteryTemperature']
        data['ioVoltage'] = pij_data['ioVoltage']
        data['ioCurrent'] = pij_data['ioCurrent']
        data['batteryStatus'] = pij_data['batteryStatus']
        data['regulationVoltage'] = profile['regulationVoltage'] 
        data['cutoffVoltage'] = profile['cutoffVoltage'] 
        data['tempHot'] = profile['tempHot']
        data['tempCold'] = profile['tempCold']

        return data
