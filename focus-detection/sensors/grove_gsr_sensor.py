from grove.adc import ADC
import logging
logger = logging.getLogger(__name__)

PORT = 0


class GSRSensor:
    '''
    Class for Grove GSR sensor
    '''
    def __init__(self, port):
        self.__port = port
        self.__adc = ADC()
        logger.info('Connect to GSR sensor')

    @property
    def GSR(self):
        logger.debug('Scanning sensor data...')
        value = self.__adc.read(self.__port)
        return value


def main():
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger(__name__).setLevel(level = logging.DEBUG)

    gsr = GSRSensor(port = PORT)
    while True:
        logger.debug(f'GSR:{gsr.GSR}')

if __name__ == '__main__':
    main()
