'''
    It is possible that webdriver outputs errors and/or warnings. 
    Please Ignore them, as they do not affect the script's functionality
'''

'''
                            Parameters:
+------------------------------------------------------------------------------------------------------+
|   Parameter  | Variable name	|               Use	                       | Accepted values           |
+--------------+----------------+------------------------------------------+---------------------------+
|      -n	   |    Name	    |   Name for the observation	           |    Any String             |
|      -cf	   |    Frequency	|   Frequency you want to observe at       |    1300-1700MHz           |    
|      -bw	   |    Bandwidth	|   The frequency range you want to observe|    {500, 1, 2, 2.4,3.2}   |    
|      -ch	   |    Channels	|   Data points on frequency axis	       |    {256, 512, 1024, 2048} |
|      -b	   |    Bins	    |   Duration of each sample	               |    Up to 20000            |
|      -du	   |    Duration	|   Duration of observation	               |    Up to 600              |
|      -rd	   |    Raw Data	|   Sends .csv data from observation	   |    {0, 1}                 |
|      -e	   |    Email	    |   The email to send the data	           |    Any existing email     |
+--------------+----------------+------------------------------------------+---------------------------+
|      -d	   |    Day	        |   The day to execute the observation	   |    {01, … , 31}           |
|      -hr	   |    Hour	    |   The hour to execute the observation	   |    {00, … , 23}           |
|      -mn	   |    Minute	    |   The minute to execute the observation  |    {00, …, 59}            |
|      -rt	   |    Repeat times|	Times to repeat observation	           |    An integer             |
|      -i	   |    Interval	|   Time between observations	           |    An integer             |
+------------------------------------------------------------------------------------------------------+

'''

import requests
from time import sleep
from datetime import datetime
import argparse
import os

PICTOR = "https://pictortelescope.com/observe"  #pictor url

'''
To make continuous observations, the step (degrees from last observation) should be half the telsescope's beamwidth (~10 deg => step = 5 deg)
Time interval is calculated from the earth's rotation frequency:

The Earth completes one full rotation on its axis approximately every 24 hours. 
Therefore, the Earth spins through 360 degrees in 24 hours. To determine when it would spin 5 degrees,
we can calculate the time it takes for the Earth to rotate through that angle.

First, we need to calculate the fraction of time it takes for the Earth to rotate 1 degree. 
Since the Earth takes 24 hours (or 1440 minutes) to complete a full rotation of 360 degrees, 
the fraction of time it takes for the Earth to rotate 1 degree is:

1 degree / 360 degrees = 1/360

To find the time it takes for the Earth to rotate 5 degrees, 
we can multiply the fraction we calculated by 5:

(1/360) x 5 = 5/360 = 1/72

Therefore, the Earth will spin 5 degrees in approximately 1/72 of a day
or about 20 minutes and 53 seconds.
'''

STEP = 21*60 #turn to seconds by doing minutes*60

#init datetime
dt = datetime.now()

parser = argparse.ArgumentParser()

#observation name parameter
parser.add_argument('-n', metavar="name", type=str, required=True, help="observation name: Any String")
#cetner frequency parameter
parser.add_argument('-cf', metavar="frequency", type=str, required=False, help="center frequency: 1300-1700 (MHz)")
#bandwidth parameter
parser.add_argument('-bw', metavar="bandwidth", type=str, required=False, help="frequency range: {500, 1, 2, 2.4,3.2}")
#bins parameter
parser.add_argument('-b', metavar="bins", type=str, required=False, help="duration of each sample: {256, 512, 1024, 2048}")
#channels parameter
parser.add_argument('-ch', metavar="channels", type=str, required=False, help="data points in freq axis: Up to 20000")
#duration parameter
parser.add_argument('-du', metavar="duration", type=str, required=True, help="duration of observation: Up to 600  ")
#raw data parameter
parser.add_argument('-rd', metavar="data", type=str, required=False, help="raw data: {0, 1} ")
#email parameter
parser.add_argument('-e', metavar="email", type=str, required=True, help="email address to deliver the data: Any existing email ")
#day parameter
parser.add_argument('-d', metavar="day", type=int, required=False, help="day to execute observation: {01, … , 31} ", default=dt.day)
#hour parameter
parser.add_argument('-hr', metavar="hour", type=int, required=False, help="hour to execute observation: {00, … , 23}", default=dt.hour)
#minute parameter
parser.add_argument('-mn', metavar="minute", type=int, required=False, help="minute to execute observation: {00, …, 59} ", default=dt.minute)
#repeat times parameter
parser.add_argument('-rt', metavar="repeat", type=int, required=False, help="times to repeat observaton: An integer ", default=1)
#interval parameter
parser.add_argument('-i', metavar="interval", type=int, required=False, help="time between observations: An integer ", default=STEP)

args = parser.parse_args()

def send_data(name='', freq='', bandwidth='', bins='', channels='', duration='', raw='', email=''):
    '''
    Create payload and send HTTP Post request
    '''

    if bandwidth == '500':
        bandwidth = bandwidth + 'khz'
    else:
        bandwidth = bandwidth + 'mhz'

    payload = {
        'obs_name': name,
        'f_center': freq, 
        'bandwidth': bandwidth, 
        'channels': channels, 
        'nbins': bins, 
        'duration': duration, 
        'email': email, 
        'submit_btn': '1'
        }
    
    requests.post(PICTOR, payload)

#set target date and time
target_dt = datetime(dt.year, dt.month, args.d, args.hr, args.mn)#target datetime year, month, day, hours, minutes

print()
print("Waiting....")

#get current date and time
current_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute) 

#wait until time has come
while target_dt != current_dt:
    dt = datetime.now()
    current_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    sleep(1)

print("Starting....")
for i in range (0, args.rt):

    name = args.n+'_'+str(i+1)#create name
    #call send_data function
    send_data(name=name, freq=args.cf, bandwidth=args.bw, bins=args.b, channels=args.ch, duration=args.du, raw=args.rd, email=args.e)

    #print the progress
    print("Done interation: ", i+1, "of:", args.rt, ",", ((i+1)/args.rt)*100, "%")

    #wait for the next iteration
    if (args.rt > 1 or i == args.rt):
        sleep(args.i)

#print ok message and exit
print("Data obtained")
exit(0)
