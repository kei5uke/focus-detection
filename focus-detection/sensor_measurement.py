from sensors.grove_gsr_sensor import GSRSensor
from sensors.ns_eeg_sensor import EEGSensor
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


class SensorMeasurement(GSRSensor, EEGSensor):
    '''
    Class for gathering sensors data
    '''
    def __init__(self, sessions: list, filename: str, eeg_port, gsr_port, step = 0.5):
        self.__sessions = sessions
        self.__step = step
        self.__filename = '../csv/' + filename
        self.data = None

        super().__init__(gsr_port) # Inheritence of EEG
        super(GSRSensor, self).__init__(port = eeg_port) # Inheritence of GSR
        super(EEGSensor, self).__init__()

    def start_sensor_connection(self):
        '''
        Start up the all sensor connection '''
        logger.info('Connect to all of sensors...')
        #super(GSRSensor, self).run()
        EEGSensor.start(self)
        # Add other sensor function below for future use

    def pause_sensor_connection(self):
        ''' Stop all connections temporary '''
        logger.info('Pause connection...')
        super(GSRSensor, self).pause_eeg_sensor()

    def continue_sensor_connection(self):
        ''' Continue getting sensor values '''
        logger.info('Continue getting values...')
        super(GSRSensor, self).continue_eeg_sensor()

    def terminate_sensor_connection(self):
        ''' Terminate all connections '''
        logger.info('Terminate all the connection...')
        super(GSRSensor, self).terminate_eeg_sensor()

    def collect_data_for_ml(self):
        if not super(GSRSensor, self).is_working : raise RuntimeError('EEG is not working. run .start() beforehand')
        if isinstance(super().GSR, int) == False: raise RuntimeError('GSR Sensor is not working properly')
        self.__measure_data()
        self.pause_sensor_connection()
        self.output_csv()
        self.terminate_sensor_connection()

    def output_csv(self):
        ''' Recieve the data and write it in csv '''
        if self.data == None: raise RuntimeError('Data is empty. Not measured yet.')
        logger.info('Output csv')
        with open(TEMP_CSV_PATH, 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(['SEC', 'STATE', 'GSR','Delta','Theta','Low_Alpha',
                             'High_Alpha','Low_Beta','High_Beta','Low_Gamma','Mid_Gamma'])
            for row in self.data:
                writer.writerow(row)
        logger.info('Finish outputting csv')

    def __measure_data(self):
        ''' Gather sensors data
        and return data = [[sec, state, gsr, eeg]...] '''
        logger.info('Start gathering sensors data')
        data = []
        state = 0
        for sec in np.arange(0, sum(self.__sessions), self.__step):
            if sum(self.__sessions[:state]) == sec:
                state += 1
            row = []
            row.extend([sec, state, super().GSR])
            row.extend(super(GSRSensor, self).EEG)
            data.append(row)
            time.sleep(self.__step)

        logger.info('Finish gathering sensors data')
        self.data = data


def main():
    basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    print(SensorMeasurement.mro())
    sensor = SensorMeasurement(sessions = [10, 10, 10], filename = 'test.csv',
                               eeg_port = EEG_PORT, gsr_port = GSR_PORT)
    sensor.start()
    sensor.collect_data_for_ml()

if __name__ == '__main__':
    main()
