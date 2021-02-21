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
        self.writer.writerow(['GSR','STATE','SEC'])

    def measure(self, state):
        sensor = GroveGSRSensor(int(sys.argv[1]))

        sec=0
        if(state==0):
            print('---CALIBRATION---')
            for sec in range(60):
                value = sensor.GSR
                self.writer.writerow([sec, value, state])
                print('SEC:{0}-GSR:{1}-STATE:{2}'.format(sec,value,state))
                time.sleep(1)

        if(state==1 or state==2):
            print('---STATE {0}---'.format(state))
            for sec in range(180):
                value = sensor.GSR
                self.writer.writerow([sec, value, state])
                print('SEC:{0}-GSR:{1}-STATE:{2}'.format(sec,value,state))
                time.sleep(1)
            if(state == 2):
                self.file.close()
                print("---FINISH---")

def main():
    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)

    """
    state 0 : calibration
    state 1 : focus
    state 2 : rest
    """

    result = MeasureGSR()
    for state in range(0,3):
        result.measure(state)

if __name__ == '__main__':
    main()
