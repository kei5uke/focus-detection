import thinkgear
import logging
import time
import threading

logger = logging.getLogger(__name__)
PORT = '/dev/rfcomm0'


'''
This class works with threading module
Set up bluetooth beforehand
'''
class NSEEGSensor:
    def __init__(self):
        self._terminate = False
        self._stop = False
        self.delta = 0
        self.theta = 0
        self.low_alpha = 0
        self.high_alpha = 0
        self.low_beta = 0
        self.high_beta = 0
        self.low_gamma = 0
        self.mid_gamma = 0

    def start_process(self):
        ''' Start up the main process '''
        self._terminate, self._stop = False, False
        self._update_sensor_values()

    def stop_process(self):
        ''' Stop the process temporary '''
        self._stop = True

    def continue_process(self):
        ''' Continue the stopped process '''
        self._stop = False

    def terminate_process(self):
        ''' Terminate the working process '''
        self._stop = True
        self._terminate = True

    def _update_sensor_values(self):
        ''' Main process
        Keep getting data packets from the sensor '''
        while True:
            if self._terminate == True:
                break
            if self._stop == False:
                for pkt in thinkgear.ThinkGearProtocol(PORT).get_packets():
                    if self._stop == True: break
                    for d in pkt:
                        if isinstance(d, thinkgear.ThinkGearPoorSignalData) and d.value > 10:
                            print("[MindWave]Signal quality is poor")
                        if isinstance(d, thinkgear.ThinkGearEEGPowerData):
                            self.delta = d.value.delta
                            self.theta = d.value.theta
                            self.low_alpha = d.value.lowalpha
                            self.high_alpha = d.value.highalpha
                            self.low_beta = d.value.lowbeta
                            self.high_beta = d.value.highbeta
                            self.low_gamma = d.value.lowgamma
                            self.mid_gamma = d.value.midgamma
                            logger.debug('[MindWave]Scannig Sensor data...')
                            #self.printData()
            else: print('[MindWave]Process stopped currently')

    def print_data(self):
        print(f'delta:{self.delta}')
        print(f'theta:{self.theta}')
        print(f'lowAlpha:{self.low_alpha}')
        print(f'highAlpha:{self.high_alpha}')
        print(f'lowBeta:{self.low_beta}')
        print(f'highBeta:{self.high_beta}')
        print(f'lowGamma:{self.low_gamma}')
        print(f'midGamma:{self.mid_gamma}')

    @property
    def EEG(self):
        return [self.delta, self.theta, self.low_alpha,
                self.high_alpha, self.low_beta, self.high_beta,
                self.low_gamma, self.mid_gamma]

def test():
    logger.info('THREAD TESTING NOW')
    time.sleep(2)

def main():
    bs = NSEEGSensor()
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
