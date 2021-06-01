import math
import sys
import time
from grove.adc import ADC
import csv
import datetime

class GroveGSRSensor:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def GSR(self):
        value = self.adc.read(self.channel)
        return value

class measure_gsr:
    def __init__(self):
        #Create CSV File
        filename = input("Name CSV File: ")+'.csv'
        self.file = open(filename, 'w')
        self.writer=csv.writer(self.file,lineterminator='\n')
        self.writer.writerow(['SEC','GSR','STATE'])

    def measure(self, sets):
        """
        sets = [set1, set2, set3...]
        """
        if len(sets) != 5:
            print('Number of sets must be 5')
            sys.exit(1)

        sensor = GroveGSRSensor(0)

        sec = 0
        state = 0
        for sec in range(sum(sets)):
            if sum(sets[:state]) == sec :
                state += 1
                print('---{}---'.format(state))
            value = sensor.GSR
            self.writer.writerow([sec, value, state])
            print('SEC:{0}-GSR:{1}-STATE:{2}'.format(sec,value,state))
            time.sleep(0.5)

        self.file.close()
        print("---FINISH---")