from grove.adc import ADC
import logging

from logging import basicConfig, getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

class GSRSensor:
    '''
    Class for Grove GSR sensor
    '''
    def __init__(self, channel):
        self._channel = channel
        self._adc = ADC()

    @property
    def GSR(self):
        logger.info('[GSR]Scanning sensor data...')
        value = self._adc.read(self._channel)
        return value
