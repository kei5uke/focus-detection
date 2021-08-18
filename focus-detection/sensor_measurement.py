from sensors.grove_gsr_sensor import GSRSensor
from sensors.ns_eeg_sensor import EEGSensor
import csv
import math
import shutil
from time import sleep
import numpy as np
import concurrent.futures
import logging
logger = logging.getLogger(__name__)

TEMP_CSV_PATH = '../csv/tmp.csv'
EEG_PORT = '/dev/rfcomm0'
GSR_PORT = 1


class SensorMeasurement(GSRSensor, EEGSensor):
    '''
    Class for gathering sensors data
    '''
    def __init__(self, eeg_port, gsr_port):
        super().__init__(gsr_port) # Inheritence of EEG
        super(GSRSensor, self).__init__(port = eeg_port) # Inheritence of GSR

    def start_sensor_connection(self):
        ''' Start up the all sensor connection '''
        logger.info('Connect to all of sensors...')
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        executor.submit(EEGSensor.start_eeg_sensor, self)
        #Future use: Add new sensor class and put it in executor

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

    def collect_data_for_ml(self, filename: str, sessions: list, step = 0.5):
        if not super(GSRSensor, self).is_eeg_working:
            raise RuntimeError('EEG is not working. Make connection beforehand')
            self.terminate_sensor_connection()
            sys.exit()

        if isinstance(super().GSR, int) == False:
            raise RuntimeError('GSR Sensor is not working properly.')
            self.terminate_sensor_connection()
            sys.exit()

        data = self.__measure_data(sessions, step)
        self.pause_sensor_connection()
        self.__output_csv(data, filename)
        self.continue_sensor_connection()

    def __measure_data(self, sessions: list, step: float):
        ''' Gather sensors data
        and return data = [[sec, state, gsr, eeg]...] '''
        logger.info('Start gathering sensors data')
        data = []
        state = 0
        for sec in np.arange(0, sum(sessions), step):
            if sum(sessions[:state]) == sec:
                state += 1
                logger.info(f'---SESSION {state}---')
            row = []
            row.extend([sec, state, super().GSR])
            row.extend(super(GSRSensor, self).EEG)
            data.append(row)
            sleep(step)

        logger.info('Finish gathering sensors data')
        return data

    def __output_csv(self, data, filename: str):
        ''' Recieve the data and write it in csv '''
        if data == None:
            raise RuntimeError('Data is empty. Not measured yet.')
            self.terminate_sensor_connection()
            sys.exit()

        logger.info('Output csv')
        with open(TEMP_CSV_PATH, 'w') as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerow(['SEC', 'STATE', 'GSR','Delta','Theta','Low_Alpha',
                             'High_Alpha','Low_Beta','High_Beta','Low_Gamma','Mid_Gamma'])
            for row in data:
                writer.writerow(row)
        shutil.copyfile(TEMP_CSV_PATH, '../csv/' + filename + 'csv')
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
    sensor = SensorMeasurement(eeg_port = EEG_PORT, gsr_port = GSR_PORT)
    sensor.start_sensor_connection()
    sensor.collect_data_for_ml(sessions = [60, 120, 120, 120, 120], filename = 'test')
    sensor.terminate_sensor_connection()

if __name__ == '__main__':
    main()
