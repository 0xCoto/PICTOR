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
|      -d	   |    Day	        |   The day to execute the observation	   |    {01, … , 31}           |
|      -hr	   |    Hour	    |   The hour to execute the observation	   |    {00, … , 23}           |
|      -mn	   |    Minute	    |   The minute to execute the observation  |    {00, …, 59}            |
|      -rt	   |    Repeat times|	Times to repeat observation	           |    An integer             |
|      -i	   |    Interval	|   Time between observations	           |    An integer             |
+------------------------------------------------------------------------------------------------------+

'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import argparse
import os

PICTOR = "https://pictortelescope.com/observe.php"  #pictor url

parser = argparse.ArgumentParser()

#observation name parameter
parser.add_argument('-n', metavar="name", type=str, required=True, help="observation name")
#cetner frequency parameter
parser.add_argument('-cf', metavar="frequency", type=str, required=False, help="center frequency")
#bandwidth parameter
parser.add_argument('-bw', metavar="bandwidth", type=str, required=False, help="frequency range")
#bins parameter
parser.add_argument('-b', metavar="bins", type=str, required=False, help="duration of each sample")
#channels parameter
parser.add_argument('-ch', metavar="channels", type=str, required=False, help="data points in freq axis")
#duration parameter
parser.add_argument('-du', metavar="duration", type=str, required=True, help="duration of observation")
#raw data parameter
parser.add_argument('-rd', metavar="data", type=str, required=False, help="raw data")
#email parameter
parser.add_argument('-e', metavar="email", type=str, required=True, help="email address to deliver the data")
#day parameter
parser.add_argument('-d', metavar="day", type=int, required=False, help="day to execute observation")
#hour parameter
parser.add_argument('-hr', metavar="hour", type=int, required=False, help="hour to execute observation")
#minute parameter
parser.add_argument('-mn', metavar="minute", type=int, required=False, help="minute to execute observation")
#repeat times parameter
parser.add_argument('-rt', metavar="repeat", type=int, required=False, help="times to repeat observaton", default=1)
#interval parameter
parser.add_argument('-i', metavar="interval", type=int, required=False, help="time between observations")

args = parser.parse_args()

options = Options()

#options to make webdriver silent
os.environ['WDM_LOG_LEVEL'] = '0'  # Disable ChromeDriver logs
options.add_argument("--headless")
options.add_argument("--disable-logging")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")
options.add_argument("--log-level=OFF")  # Disable Chrome browser logs
options.add_argument("service_log_path='NUL'")  # Redirect output to /dev/null

def send_data(name='', freq='', bandwidth='', bins='', channels='', duration='', raw='', email=''):
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)

    # Open the desired webpage
    driver.get(PICTOR)

    # Find the form elements and populate them with data
    ####################################################

    #observation name OK
    input_field = driver.find_element(By.ID,'obs_name')
    input_field.send_keys(name)

    #center frequency OK
    input_field = driver.find_element(By.ID,'f_center')
    input_field.clear()
    input_field.send_keys(freq)

    #bandwidth 
    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "bandwidth")))
    dd = Select(input_field)
    index = 0
    if bandwidth == "500":#500kHz
        index = 0
    if bandwidth == "1":#1MHz
        index = 1
    if bandwidth == "2":#2Mhz
        index = 2
    if bandwidth == "2.4":#2.4MHz
        index = 3
    if bandwidth == "3.2":#3.2MHz
        index = 4
    #fix index
    dd.select_by_index(index)

    #channels
    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "channels")))
    dd = Select(input_field)
    index = 0
    if channels == 256:
        index = 0
    if channels == 512:
        index = 1
    if channels == 1024:
        index = 3
    if channels == 2048:
        index = 4
    #fix index
    dd.select_by_index(index)

    #bins
    input_field = driver.find_element(By.ID,'nbins')
    input_field.clear()
    input_field.send_keys(bins)

    #duration
    input_field = driver.find_element(By.ID,'duration')
    input_field.send_keys(duration)

    #email
    input_field = driver.find_element(By.ID,'email')
    input_field.send_keys(email)

    #raw data
    input_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "raw_data")))
    dd = Select(input_field)
    index = 0
    if raw == '1':
        index = 1
    #fix index
    dd.select_by_index(index)

    # Submit the form
    submit_button = driver.find_element(By.NAME,'submit_btn')
    submit_button.click()

    # Close the browser
    driver.quit()

#init datetime
dt = datetime.now()

#set target date and time
target_dt = datetime(dt.year, dt.month, args.d, args.hr, args.mn)#target datetime year, month, day, hours, minutes

#get current date and time
current_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute) 

print("Waiting....")

#wait until time has come
while target_dt != current_dt:
    dt = datetime.now()
    current_dt = current_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    sleep(1)

print("Starting....")
for i in range (0, args.rt):

    name = args.n+'_'+str(i+1)#rename observation according to iteration
    print(name)
    send_data(name=name, freq=args.cf, bandwidth=args.bw, bins=args.b, channels=args.ch, duration=args.du, raw=args.rd, email=args.e)
    print("Done interation: ", i+1, "of:", args.rt, ",", ((i+1)/args.rt)*100, "%")

    #wait for the next iteration
    if (args.rt > 1 and i != args.rt):
        sleep(args.i)

print("Data obtained")
exit(0)
