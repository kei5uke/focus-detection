from sensors.grove_gsr_sensor import GSRSensor
from sensors.ns_eeg_sensor import EEGSensor
import csv
import math
import time
import numpy as np
import concurrent.futures
import logging
logger = logging.getLogger(__name__)

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

        super().__init__(gsr_port) # Inheritence of EEG
        super(GSRSensor, self).__init__(port = eeg_port) # Inheritence of GSR

    def start_sensor_connection(self):
        ''' Start up the all sensor connection '''
        logger.info('Connect to all of sensors...')
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        executor.submit(EEGSensor.start_eeg_sensor, self)
        #Future use: Add new sensor class and executor

    def pause_sensor_connection(self):
        ''' Stop updating values temporary '''
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
        if not super(GSRSensor, self).is_working : raise RuntimeError('EEG is not working. Make connection beforehand')
        if isinstance(super().GSR, int) == False: raise RuntimeError('GSR Sensor is not working properly.')
        data = self.__measure_data()
        self.pause_sensor_connection()
        self.__output_csv(data)
        self.continue_sensor_connection()

    def __measure_data(self):
        ''' Gather sensors data
        and return data = [[sec, state, gsr, eeg]...] '''
        logger.info('Start gathering sensors data')
        data = []
        state = 0
        for sec in np.arange(0, sum(self.__sessions), self.__step):
            if sum(self.__sessions[:state]) == sec:
                state += 1
                logger.info(f'---SESSION {state}---')
            row = []
            row.extend([sec, state, super().GSR])
            row.extend(super(GSRSensor, self).EEG)
            data.append(row)
            time.sleep(self.__step)

        logger.info('Finish gathering sensors data')
        return data

    def __output_csv(self, data):
        ''' Recieve the data and write it in csv '''
        if data == None: raise RuntimeError('Data is empty. Not measured yet.')
        logger.info('Output csv')
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(['SEC', 'STATE', 'GSR','Delta','Theta','Low_Alpha',
                             'High_Alpha','Low_Beta','High_Beta','Low_Gamma','Mid_Gamma'])
            for row in data:
                writer.writerow(row)
        logger.info('Finish outputting csv')


def main():
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    module_levels = {'sensors': logging.INFO, __name__: logging.INFO}
    for module, level in module_levels.items():
        logging.getLogger(module).setLevel(level=level)

    print(SensorMeasurement.mro())
    sensor = SensorMeasurement(sessions = [12, 12, 12], filename = 'test.csv',
                               eeg_port = EEG_PORT, gsr_port = GSR_PORT)
    sensor.start_sensor_connection()
    sensor.collect_data_for_ml()
    sensor.terminate_sensor_connection()

if __name__ == '__main__':
    main()
