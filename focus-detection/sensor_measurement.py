from sensors.grove_gsr_sensor import GroveGSRSensor
from sensors.ns_eeg_sensor import NSEEGSensor
import csv
import math
import time
import numpy as np
import threading

from logging import basicConfig, getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)
TEMP_CSV_PATH = './sensor_record.csv'
EEG_PORT = '/dev/rfcomm0'
GSR_PORT = 1


class SensorMeasurement(threading.Thread):
    '''
    Class for measuring sensors data
    '''
    def __init__(self, sessions: list, filename: str, eeg: NSEEGSensor, gsr: GroveGSRSensor, step = 0.5):
        threading.Thread.__init__(self)
        self.__sessions = sessions
        self.__step = step
        self.__filename = '../csv/' + filename
        self.data = None
        self.eeg_sensor = eeg
        self.gsr_sensor = gsr

    def run(self):
        self.__measure_data()

    def output_csv(self):
        ''' Recieve the data and write it in csv '''
        if self.data == None: raise RuntimeError('Data is empty. Not measured yet.')
        with open(TEMP_CSV_PATH, 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(['SEC', 'STATE', 'GSR','Delta','Theta','Low_Alpha',
                             'High_Alpha','Low_Beta','High_Beta','Low_Gamma','Mid_Gamma'])
            for row in self.data:
                writer.writerow(row)

    def __measure_data(self):
        ''' Gather sensors data
        and return data = [[sec, state, gsr, eeg]...] '''
        if self.eeg_sensor.is_working == False: raise RuntimeError('EEG Sensor is not working properly')
        if isinstance(self.gsr_sensor.GSR, int) == False: raise RuntimeError('GSR Sensor is not working properly')

        data = []
        state = 0
        for sec in np.arange(0, sum(self.__sessions), self.__step):
            if sum(self.__sessions[:state]) == sec:
                state += 1
            row = []
            row.extend([sec, state, self.gsr_sensor.GSR])
            row.extend(self.eeg_sensor.EEG)
            data.append(row)
            time.sleep(self.__step)

        self.data = data


def main():
    gsr_sensor = GroveGSRSensor(GSR_PORT)
    eeg_sensor = NSEEGSensor(EEG_PORT)
    sensors = SensorMeasurement(sessions = [10, 10, 10], filename = 'test.csv',
                                eeg = eeg_sensor, gsr = gsr_sensor)
    eeg_sensor.start()
    sensors.start()
    main_thread.join()
    eeg_sensor.terminate_process()
    eeg_sensor.join()
    sensors.output_csv()


if __name__ == '__main__':
    main()
