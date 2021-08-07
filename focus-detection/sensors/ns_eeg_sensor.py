import thinkgear
import logging
import time
import threading

from logging import basicConfig, getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

PORT = '/dev/rfcomm0'


class EEGSensor(threading.Thread):
    '''
    Class for NeuroSky MindWAve EEG Sensor
    This class works with threading module
    Set up bluetooth beforehand
    '''
    def __init__(self, port: str):
        threading.Thread.__init__(self)
        self.__port = port
        self.__terminate = False
        self.__pause = False
        self.delta = 0
        self.theta = 0
        self.low_alpha = 0
        self.high_alpha = 0
        self.low_beta = 0
        self.high_beta = 0
        self.low_gamma = 0
        self.mid_gamma = 0

    def run(self):
        ''' @Override threading method
        Start up the main process
        Execute with .start() '''
        logger.info('[MindWave]Connect to EEG Sensor...')
        try:
            self.__update_eeg_values()
        except KeyboardInterrupt:
            logger.info('[MindWave]Stopped with Ctrl+C')

    def __update_eeg_values(self):
        ''' Main process
        Keep getting data packets from the sensor '''
        while True:
            if self.__terminate == True:
                break
            if self.__pause == False:
                for pkt in thinkgear.ThinkGearProtocol(self.__port).get_packets():
                    for d in pkt:
                        if isinstance(d, thinkgear.ThinkGearPoorSignalData) and d.value > 10:
                            logger.info('[MindWave]Signal quality is poor')
                        if isinstance(d, thinkgear.ThinkGearEEGPowerData):
                            logger.debug('[MindWave]Scannig Sensor data...')
                            self.delta = d.value.delta
                            self.theta = d.value.theta
                            self.low_alpha = d.value.lowalpha
                            self.high_alpha = d.value.highalpha
                            self.low_beta = d.value.lowbeta
                            self.high_beta = d.value.highbeta
                            self.low_gamma = d.value.lowgamma
                            self.mid_gamma = d.value.midgamma
                            #self.printData()
                    if self.__pause == True: break

    def pause_eeg_sensor(self):
        ''' Stop the process temporary '''
        logger.info('[MindWave]Process has been stopped')
        self.__pause = True

    def continue_eeg_sensor(self):
        ''' Continue the stopped process '''
        logger.info('[MindWave]Continue updating values')
        self.__pause = False

    def terminate_eeg_sensor(self):
        ''' Terminate the connection of EEG sensor '''
        logger.info('[MindWave]Terminate connection')
        self.__pause = True
        self.__terminate = True

    def print_data(self):
        logger.debug(f'delta:{self.delta}')
        logger.debug(f'theta:{self.theta}')
        logger.debug(f'lowAlpha:{self.low_alpha}')
        logger.debug(f'highAlpha:{self.high_alpha}')
        logger.debug(f'lowBeta:{self.low_beta}')
        logger.debug(f'highBeta:{self.high_beta}')
        logger.debug(f'lowGamma:{self.low_gamma}')
        logger.debug(f'midGamma:{self.mid_gamma}')

    @property
    def EEG(self):
        return [self.delta, self.theta, self.low_alpha,
                self.high_alpha, self.low_beta, self.high_beta,
                self.low_gamma, self.mid_gamma]
    @property
    def is_working(self):
        return not self.__terminate


def test():
    logger.info('THREAD TESTING NOW')
    time.sleep(2)

def main():
    basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    bs = EEGSensor(port = PORT)
    t1 = threading.Thread(target=bs.start_process)
    # t1.setDaemon(True)
    t1.start()

    for i in range(5):
        t2 = threading.Thread(target=test)
        t2.start()
        t2.join()

    logger.info('STOP for now...')
    bs.stop_process()
    for i in range(5):
        t2 = threading.Thread(target=test)
        t2.start()
        t2.join()

    logger.info('CONTINUE from now on...')
    bs.continue_process()
    for i in range(5):
        t2 = threading.Thread(target=test)
        t2.start()
        t2.join()

    logger.info('TERMINATE process now...')
    bs.terminate_process()
    t1.join()

if __name__ == '__main__':
    main()
