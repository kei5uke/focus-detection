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

class MeasureGSR:
    def __init__(self):
        #Create CSV File
        filename = input("Name CSV File: ")+'.csv'
        self.file = open(filename, 'w')
        self.writer=csv.writer(self.file,lineterminator='\n')
        self.writer.writerow(['SEC','GSR','STATE'])

    def measure(self, sets):
        """
        sets = [set1, set2, set3]
        """
        if len(sets) != 3:
            print('Number of sets must be 3')
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
            time.sleep(1)

        self.file.close()
        print("---FINISH---")

def main():

    """
    state 1 : calibration
    state 2 : focus
    state 3 : rest
    """

    sets = [int(i) for i in sys.argv[1:]]
    print(sets)
    result = MeasureGSR()
    result.measure(sets)

if __name__ == '__main__':
    main()
