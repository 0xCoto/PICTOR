import requests
from time import sleep
from datetime import datetime
import argparse
import os

PICTOR = "https://pictortelescope.com/observe"  # pictor url

"""
To make continuous observations, the step (time from last observation) 
should be half the telsescope's beamwidth (~10 deg => step = 5 deg)
Time interval is calculated from the earth's rotation frequency:

The Earth completes one full rotation on its axis approximately every 24 hours. 
Therefore, the Earth spins through 360 degrees in 24 hours. 
To determine when it would spin 5 degrees,we can calculate the time
it takes for the Earth to rotate through that angle.

First, we need to calculate the fraction of time it takes for the Earth to rotate 1 degree. 
Since the Earth takes 24 hours (or 1440 minutes) to complete a full rotation of 360 degrees, 
the fraction of time it takes for the Earth to rotate 1 degree is:

1 degree / 360 degrees = 1/360

To find the time it takes for the Earth to rotate 5 degrees, 
we can multiply the fraction we calculated by 5:

(1/360) x 5 = 5/360 = 1/72

Therefore, the Earth will spin 5 degrees in approximately 1/72 of a day
or about 20 minutes and 53 seconds.
"""

STEP = 21 * 60  # turn to seconds by doing minutes*60

# init datetime
dt = datetime.now()

parser = argparse.ArgumentParser(
    description="PICTOR Radio-telescope Observation Scheduler",
    add_help=False
)

# help parameter
parser.add_argument('--help',
    '-h', 
    action='help'
    )

# observation name parameter
parser.add_argument(
    "-n",
    metavar="name",
    type=str,
    required=False,
    help="Observation name: Any String",
    default="demo",
)

# cetner frequency parameter
parser.add_argument(
    "-cf",
    metavar="frequency",
    type=str,
    required=False,
    help="Frequency to observe at: 1300-1700 (MHz)",
    default="1420",
)

# bandwidth parameter
parser.add_argument(
    "-bw",
    metavar="bandwidth",
    type=str,
    required=False,
    help="Frequency range: {500, 1, 2, 2.4, 3.2}",
    default="2.4",
)

# bins parameter
parser.add_argument(
    "-b",
    metavar="bins",
    type=str,
    required=False,
    help="Duration of each sample: Up to 20000",
    default="100",
)

# channels parameter
parser.add_argument(
    "-ch",
    metavar="channels",
    type=str,
    required=False,
    help="Data points in frequency axis: {256, 512, 1024, 2048}",
    default="2048",
)

# duration parameter
parser.add_argument(
    "-du",
    metavar="duration",
    type=str,
    required=False,
    help="Duration of observation: Up to 600",
    default="10",
)

# raw data parameter
parser.add_argument(
    "-rd",
    metavar="data",
    type=str,
    required=False,
    help="Sends raw data from observation: {0, 1}",
    default="0",
)

# email parameter
parser.add_argument(
    "-e",
    metavar="email",
    type=str,
    required=False,
    help="email address to deliver the data: Any existing email",
    default="example@email.com",
)

# day parameter
parser.add_argument(
    "-d",
    metavar="day",
    type=int,
    required=False,
    help="Day to execute observation: {01, … , 31} ",
    default=dt.day,
)

# hour parameter
parser.add_argument(
    "-hr",
    metavar="hour",
    type=int,
    required=False,
    help="Hour to execute observation: {00, … , 23}",
    default=dt.hour,
)

# minute parameter
parser.add_argument(
    "-mn",
    metavar="minute",
    type=int,
    required=False,
    help="Minute to execute observation: {00, …, 59} ",
    default=dt.minute,
)

# repeat times parameter
parser.add_argument(
    "-rt",
    metavar="repeat",
    type=int,
    required=False,
    help="Times to repeat observaton: An integer ",
    default=1,
)

# interval parameter
parser.add_argument(
    "-i",
    metavar="interval",
    type=int,
    required=False,
    help="Time between observations: An integer ",
    default=STEP,
)

args = parser.parse_args()

def send_data(
    name="", freq="", bandwidth="", bins="", channels="", duration="", raw="", email=""
):
    """
    Create payload and send HTTP Post request
    """
    if bandwidth == "500":
        bandwidth = bandwidth + "khz"
    else:
        bandwidth = bandwidth + "mhz"

    payload = {
        "obs_name": name,
        "f_center": freq,
        "bandwidth": bandwidth,
        "channels": channels,
        "nbins": bins,
        "duration": duration,
        "raw_data": raw,
        "email": email,
        "submit_btn": "1",
    }

    requests.post(PICTOR, payload)


# set target date and time
target_dt = datetime(
    dt.year, dt.month, args.d, args.hr, args.mn
)  # target datetime year, month, day, hours, minutes

print("Waiting....")

# get current date and time
current_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

# wait until time has come
while target_dt != current_dt:
    dt = datetime.now()
    current_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    sleep(1)

print("Starting Datetime:", datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute))
for i in range(args.rt):
    name = args.n + "_" + str(i + 1)  # create name
    # call send_data function

    send_data(
        name=name,
        freq=args.cf,
        bandwidth=args.bw,
        bins=args.b,
        channels=args.ch,
        duration=args.du,
        raw=args.rd,
        email=args.e,
    )

    # print the progress
    progress = ((i + 1) / args.rt) * 100
    print("Done interation: ", i + 1, "of:", args.rt, ", ", "%.2f" % progress, "%")

    # wait for the next iteration
    if args.rt > 1 and i+1 != args.rt:
        if args.i > 60:
            print("Next Observation in: ", args.i//60, "minutes")
        else:
            print("Next Observation in: ", args.i, "seconds")
        sleep(args.i)

# print ok message
print("Observation Request Sent!")
