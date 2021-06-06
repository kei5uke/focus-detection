import math
import sys
import time
import csv
import datetime
import shutil
from sensors.grove_gsr_sensor import GroveGSRSensor

TEMP_CSV_PATH = "./gsr_record.csv"

class measure_gsr:
    def __init__(self, sets, filename):
        self.sets = sets
        self.filename = '../csv/'+filename

    def measure(self):
        """
        sets = [set1, set2, set3...]
        """
        #Create temporary CSV File
        file = open(TEMP_CSV_PATH, 'w')
        writer=csv.writer(file,lineterminator='\n')
        writer.writerow(['SEC','GSR','STATE'])
        
        sensor = GroveGSRSensor(0)

        sec = 0
        state = 0
        for sec in range(sum(self.sets)):
            if sum(self.sets[:state]) == sec :
                state += 1
                print('---{}---'.format(state))
            value = sensor.GSR
            writer.writerow([sec, value, state])
            print('SEC:{0}-GSR:{1}-STATE:{2}'.format(sec,value,state))
            time.sleep(0.5)

        file.close()
        
        #Move temporary csv to csv folder with name input
        shutil.copy(TEMP_CSV_PATH,self.filename)
        print("---FINISH---")