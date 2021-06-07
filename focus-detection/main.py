import gsr
import ml

import copy as cp

def main():

    """
    set 1 : calibration
    set 2 : focus data for train data
    set 3 : rest data for train data
    set 4 : focus data for validation
    set 5 : rest data for validation
    """
    sets = [60,180,180,180,180]
    filename = input("Name CSV File: ")+'.csv'
    
    #Collect GSR data for ML
    process_gsr = gsr.measure_gsr(sets,filename)
    process_gsr.measure()
    
    #Collect the best ml model based on the recorded data
    model = ml.best_model()
    
    #Start real time detection
   
    #record the data for 120sec
    sensor = GroveGSRSensor(0)
    values = []
    for i in range(120):
        values.append(sensor.GSR)
    gsr = np.array(values).astype('float32')
    
    #Normalize the data
    mean, std = ml.mean_and_std(gsr)
    gsr -= mean
    gsr /= std
    
    gsr = np.reshape(array,[array.shape[0],array.shape[1],1])
    
    while(1):
        #predict the result
        result = model.predict(gsr)
        #delete the oldest value
        gsr = np.delete(gsr, 119, axis=1)
        #update the new value
        value = (sensor.GSR - mean)/std
        gsr = np.insert(gsr, 120, [[value]], axis=1)
        
        print("FOCUS") if np.average(result)>0.5 else print("NOT FOCUS")
    

if __name__ == '__main__':
    main()
