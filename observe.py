import os
import sys
import requests
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from shutil import copy2
from time import sleep

while True:
    while True:
        #Get observation parameters
        sleep(10)
        try:
            response = requests.get('https://pictortelescope.com/last_obs.txt', auth=('pictor', 'XXX')) #plaintext credentials
            if response.status_code == 200:
                exec(response.content)
                if id not in open('/home/pi/Desktop/pictortelescope/id_history.txt').read() and 'notpictor' not in obs_name:
                    break
            else:
                print(response.status_code)
        except Exception as e:
            print('pictor error on observe.py')
            print(e)
            pass
    
    #Reformat & define GRC observation parameters
    f_center = str(float(f_center)*10**6)
    
    if bandwidth == '500khz':
        bandwidth = '500000'
    elif bandwidth == '1mhz':
        bandwidth = '1000000'
    elif bandwidth == '2mhz':
        bandwidth = '2000000'
    elif bandwidth == '2.4mhz':
        bandwidth = '2400000'
    elif bandwidth == '3.2mhz':
        bandwidth = '3200000'
    
    #Delete pre-existing observation.dat & plot.png files
    try:
        os.remove('/home/pi/Desktop/pictortelescope/observation.dat')
        os.remove('/home/pi/Desktop/pictortelescope/plot.png')
    except OSError:
        pass
    
    try:
        #Note current datetime
        currentDT = datetime.datetime.now()
        obsDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        obsDTfile = currentDT.strftime("%Y%m%d%H%M%S")
        #Execute top_block.py with parameters
        sys.argv = ['top_block.py', '--c-freq='+f_center, '--samp-rate='+bandwidth, '--nchan='+channels, '--nbin='+nbins, '--obs-time='+duration]
        execfile('/home/pi/Desktop/pictortelescope/top_block.py')
        copy2('/home/pi/Desktop/pictortelescope/observation.dat', '/home/pi/Desktop/pictortelescope/obs_archive/'+str(obsDTfile)+'.dat')
        #Execute plotter
        if f_center == '1420000000.0' and bandwidth == '2400000' and (channels == '1024' or channels == '2048'):
            sys.argv = ['plot_hi.py', 'freq='+f_center, 'samp_rate='+bandwidth, 'nchan='+channels, 'nbin='+nbins]
            execfile('/home/pi/Desktop/pictortelescope/plot_hi.py')
        else:
            sys.argv = ['plot.py', 'freq='+f_center, 'samp_rate='+bandwidth, 'nchan='+channels, 'nbin='+nbins]
            execfile('/home/pi/Desktop/pictortelescope/plot.py')
        
        with open('/home/pi/Desktop/pictortelescope/id_history.txt', 'a') as id_logfile:
            id_logfile.write(id+'\n')
        
        if obs_name == 'off1024':
            copy2('/home/pi/Desktop/pictortelescope/observation.dat', '/home/pi/Desktop/pictortelescope/off1024.dat')
        elif obs_name == 'off2048':
            copy2('/home/pi/Desktop/pictortelescope/observation.dat', '/home/pi/Desktop/pictortelescope/off2048.dat')
        
        #Send plot to observer's email
        fromaddr = 'pictortelescope@gmail.com'
        toaddr = email
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        
        msg['Subject'] = '['+id+'] Observation Data'
        
        body = '''Your observation has been carried out by PICTOR successfully!

Observation name: '''+obs_name+'''
Observation datetime: '''+obsDT+''' (UTC+3)
Center frequency: '''+f_center+''' Hz
Bandwidth: '''+bandwidth+''' Hz
Sample rate: '''+bandwidth+''' samples/sec
Number of channels: '''+channels+'''
Number of bins: '''+nbins+'''
Observation duration: '''+duration+''' sec
Observation ID: '''+id+'''

Your observation's averaged spectrum, dynamic spectrum (waterfall) and Power vs Time plot are attached in this email as an image.'''
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename = 'plot.png'
        attachment = open("/home/pi/Desktop/pictortelescope/"+filename, 'rb')
        
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
        msg.attach(p)
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, 'XXX') #plaintext email password
        
        text = msg.as_string()
        
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        
        #Send raw data to archive
        fromaddr = 'pictortelescope@gmail.com'
        toaddr = fromaddr
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        
        msg['Subject'] = '['+id+'] Raw Observation Data'
        
        body = '''Your observation has been carried out by PICTOR successfully!

Observer email: '''+email+'''
Observation name: '''+obs_name+'''
Observation datetime: '''+obsDT+''' (UTC+3)
Center frequency: '''+f_center+''' Hz
Bandwidth: '''+bandwidth+''' Hz
Sample rate: '''+bandwidth+''' samples/sec
Number of channels: '''+channels+'''
Number of bins: '''+nbins+'''
Observation duration: '''+duration+''' sec
Observation ID: '''+id+'''

Your observation's averaged spectrum, dynamic spectrum (waterfall) and Power vs Time plot are attached in this email as an image.'''
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename = 'observation.dat'
        attachment = open("/home/pi/Desktop/pictortelescope/"+filename, 'rb')
        
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
        msg.attach(p)
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, 'XXX') #plaintext email password
        
        text = msg.as_string()
        
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        
    except Exception as e:
        print(e)
        pass
