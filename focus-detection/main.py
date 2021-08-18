import ml
from sensor_measurement import SensorMeasurement
import numpy as np
from time import sleep
import os
from shutil import copyfile
from tensorflow.keras.models import load_model

import logging
logger = logging.getLogger(__name__)

EEG_PORT = '/dev/rfcomm0'
GSR_PORT = 1
TEMP_CSV_PATH = '../csv/tmp.csv'
STEP = 0.5

def main():
    '''
    This module is used for real time classification.
    '''
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    module_levels = {'sensor_measurement':logging.INFO, 'sensors': logging.INFO, __name__: logging.DEBUG}
    for module, level in module_levels.items():
        logging.getLogger(module).setLevel(level=level)


    copy_filename = input("Name CSV File: ")

    # If the file name already exist, proceed to load model
    if os.path.isdir('../model/' + copy_filename):
        choice = input('Found the same name of the file. Load the model? [y/n]:').lower()
        if choice == 'y':
            copyfile('../csv/' + copy_filename + '.csv', TEMP_CSV_PATH)
            _, _, _, _, mean, std = ml.data()
            model = load_model('../model/' + copy_filename)
        else: choice = 'n'

    sensor = SensorMeasurement(eeg_port = EEG_PORT, gsr_port = GSR_PORT)
    sensor.start_sensor_connection()


    """
    set 1 : calibration
    set 2 : focus data for train data
    set 3 : rest data for train data
    set 4 : focus data for validation
    set 5 : rest data for validation
    """
    if choice == 'n':
        sensor.collect_data_for_ml(sessions = [60, 120, 120, 120, 120],
                                    filename = copy_filename,
                                    step = STEP) # Collect EEG, GSR data for ML
        sensor.pause_sensor_connection()
        model, mean, std = ml.auto_tuning(copy_filename) # Collect the best ml model based on the recorded data
        sensor.continue_eeg_sensor()

    #Start real time detection
    values = []
    sec = 0.0

    for i in range(30):
        row = []
        row.extend([sensor.GSR])
        row.extend(sensor.EEG)
        values.append(row)
        logger.info(f'{sec} sec : {row}')
        sec += STEP
        sleep(STEP)

    values = np.array(values).reshape(1, 30, 9)

    while(1):
        try:
            #predict the result
            norm_value = (values - mean) / std
            result = model.predict(norm_value)
            logger.info("FOCUS\n") if result >= 0.5 else logger.info("NOT FOCUS\n")

            #delete the oldest value
            values = np.delete(values, 0, axis = 1)

            #update the new value
            row = []
            row.extend([sensor.GSR])
            row.extend(sensor.EEG)
            values = np.insert(values, 29, row, axis = 1)
            logger.debug(f'{sec} sec : {row}')

            sec += STEP
            sleep(STEP)

        except KeyboardInterrupt:
            logger.info('Keyboard Interrupt')
            sensor.terminate_sensor_connection()
            exit(0)

if __name__ == '__main__':
    main()
