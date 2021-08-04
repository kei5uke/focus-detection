from grove.adc import ADC
import logging

logger = logging.getLogger(__name__)


class GroveGSRSensor:
    def __init__(self, channel):
        self._channel = channel
        self._adc = ADC()

    @property
    def GSR(self):
        value = self._adc.read(self._channel)
        return value
