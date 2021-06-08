import gsr
import ml
from sensors.grove_gsr_sensor import GroveGSRSensor
import time
import copy as cp
import numpy as np

def main():

    """
    set 1 : calibration
    set 2 : focus data for train data
    set 3 : rest data for train data
    set 4 : focus data for validation
    set 5 : rest data for validation
    """
    sets = [60,120,120,120,120]
    filename = input("Name CSV File: ")+'.csv'
    
    #Collect GSR data for ML
    process_gsr = gsr.measure_gsr(sets,filename)
    process_gsr.measure()
    
    #Collect the best ml model based on the recorded data
    #and mean, std value
    model, mean, std = ml.auto_tuning()
    
    "Start real time detection"
    #record the data for 120sec
    sensor = GroveGSRSensor(0)
    values = []
    sec = 0.0

    for i in range(120):
        value = (sensor.GSR-mean)/std
        values.append(value)
        print('SEC:{0}-GSR:{1}'.format(sec,value))
        sec += 0.5
        time.sleep(0.5)

    gsr_values = np.array([values]).astype('float32')
    gsr_values = np.reshape(gsr_values,[gsr_values.shape[0],gsr_values.shape[1],1])
    
    while(1):
        #predict the result
        result = model.predict(gsr_values)
        #delete the oldest value
        gsr_values = np.delete(gsr_values, 0, axis=1)
        #update the new value
        value = (sensor.GSR - mean)/std
        gsr_values = np.insert(gsr_values, 119, [[value]], axis=1)
        print('SEC:{0}-GSR:{1}'.format(sec,value))
        print("FOCUS\n") if np.average(result)>0.5 else print("NOT FOCUS\n")
        sec += 0.5
        time.sleep(0.5)

if __name__ == '__main__':
    main()
