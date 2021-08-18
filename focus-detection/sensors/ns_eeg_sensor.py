import thinkgear
import logging
import time
import threading
import logging
logger = logging.getLogger(__name__)

PORT = '/dev/rfcomm0'


class EEGSensor:
    '''
    Class for NeuroSky MindWAve EEG Sensor
    Use threading module if you want to record the data along with @property method
    Set up bluetooth beforehand
    '''
    def __init__(self, port: str, show_progress = False):
        self.__port = port
        self.__terminate = False
        self.__pause = False
        self.__show_progress = show_progress
        self.delta = 0
        self.theta = 0
        self.low_alpha = 0
        self.high_alpha = 0
        self.low_beta = 0
        self.high_beta = 0
        self.low_gamma = 0
        self.mid_gamma = 0

    def start_eeg_sensor(self):
        ''' Main process
        Keep getting data packets from the sensor '''
        logger.info('Connect to EEG sensor')
        for pkt in thinkgear.ThinkGearProtocol(self.__port).get_packets():
            if self.__terminate == True: break
            if self.__pause == False:
                for d in pkt:
                    if isinstance(d, thinkgear.ThinkGearPoorSignalData) and d.value > 10:
                        logger.warning('Signal quality is poor')
                    if isinstance(d, thinkgear.ThinkGearEEGPowerData):
                        logger.debug('Scannig Sensor data...')
                        self.delta = d.value.delta
                        self.theta = d.value.theta
                        self.low_alpha = d.value.lowalpha
                        self.high_alpha = d.value.highalpha
                        self.low_beta = d.value.lowbeta
                        self.high_beta = d.value.highbeta
                        self.low_gamma = d.value.lowgamma
                        self.mid_gamma = d.value.midgamma
                        logger.debug(f'delta:{self.delta}')
                        logger.debug(f'theta:{self.theta}')
                        logger.debug(f'lowAlpha:{self.low_alpha}')
                        logger.debug(f'highAlpha:{self.high_alpha}')
                        logger.debug(f'lowBeta:{self.low_beta}')
                        logger.debug(f'highBeta:{self.high_beta}')
                        logger.debug(f'lowGamma:{self.low_gamma}')
                        logger.debug(f'midGamma:{self.mid_gamma}')

    def pause_eeg_sensor(self):
        ''' Stop the process temporary '''
        logger.info('Stop updating values')
        self.__pause = True

    def continue_eeg_sensor(self):
        ''' Continue the stopped process '''
        logger.info('Continue updating values')
        self.__pause = False

    def terminate_eeg_sensor(self):
        ''' Terminate the connection of EEG sensor '''
        logger.info('Terminate connection')
        # self.__pause = True
        self.__terminate = True


    @property
    def EEG(self):
        return [self.delta, self.theta, self.low_alpha,
                self.high_alpha, self.low_beta, self.high_beta,
                self.low_gamma, self.mid_gamma]
    @property
    def is_eeg_working(self):
        return not self.__terminate


def main():
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.getLogger(__name__).setLevel(level = logging.DEBUG)
    eeg = EEGSensor(port = PORT, show_progress = True)
    eeg.start_eeg_sensor()

if __name__ == '__main__':
    main()
