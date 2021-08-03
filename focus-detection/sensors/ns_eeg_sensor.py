import thinkgear
import time
import threading
from logging import basicConfig, getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

PORT = '/dev/rfcomm0'

class NSBrainSensor:
    def __init__(self):
        self.loop = True
        self.delta = 0
        self.theta = 0
        self.lowAlpha = 0
        self.highAlpha = 0
        self.lowBeta = 0
        self.highBeta = 0
        self.lowGamma = 0
        self.midGamma = 0

    def start(self):
        self._update()

    def _update(self):
        while self.loop:
            for pkt in thinkgear.ThinkGearProtocol(PORT).get_packets():
                for d in pkt:
                    if isinstance(d, thinkgear.ThinkGearPoorSignalData) and d.value > 10:
                        print("[MindWave]:Signal quality is poor.")

                    if isinstance(d, thinkgear.ThinkGearEEGPowerData):
                        self.delta = d.value.delta
                        self.theta = d.value.theta
                        self.lowAlpha = d.value.lowalpha
                        self.highAlpha = d.value.highalpha
                        self.lowBeta = d.value.lowbeta
                        self.highBeta = d.value.highbeta
                        self.lowGamma = d.value.lowgamma
                        self.midGamma = d.value.midgamma
                        print('[MindWave]Scannig Sensor data...')
                        print(f'delta:{self.delta}')
                        print(f'theta:{self.theta}')
                        print(f'lowAlpha:{self.lowAlpha}')
                        print(f'highAlpha:{self.highAlpha}')
                        print(f'lowBeta:{self.lowBeta}')
                        print(f'highBeta:{self.highBeta}')
                        print(f'lowGamma:{self.lowGamma}')
                        print(f'midGamma:{self.midGamma}')

    def test(self):
        print('THREAD TESTING NOW')
        time.sleep(2)

    def terminate(self):
        self.loop = False

    def getData(self):
        return [self.delta, self.theta, self.lowAlpha,
                self.highAlpha, self.lowBeta, self.highBeta,
                self.lowGamma, self.midGamma]

if __name__ == '__main__':
    bs = NSBrainSensor()
    # t1 = threading.Thread(target=bs.update)
    # t1.setDaemon(True)
    # t1.start()
    #
    # for i in range(5):
    #     t2 = threading.Thread(target=bs.test)
    #     t2.start()
    #     t2.join()
    #
    # bs.terminate()
    # t1.join()
    bs.update()
