import virgo
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
    
    #Delete pre-existing observation.dat, plot.png, data_freq.csv, & data_time.csv files
    try:
        os.remove('/home/pi/Desktop/pictortelescope/observation.dat')
        os.remove('/home/pi/Desktop/pictortelescope/plot.png')
        os.remove('/home/pi/Desktop/pictortelescope/spectrum.csv')
        os.remove('/home/pi/Desktop/pictortelescope/time_series.csv')
    except OSError:
        pass
    
    try:
        #Note current datetime
        currentDT = datetime.datetime.now()
        obsDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        obsDTfile = currentDT.strftime("%Y%m%d%H%M%S")
        #Execute observation with parameters
        # Define observation parameters
        t_sample = int(nbins)*int(channels)/float(bandwidth)
        observation = {
    'dev_args': '',
    'rf_gain': 30,
    'if_gain': 30,
    'bb_gain': 30,
    'frequency': float(f_center),
    'bandwidth': float(bandwidth),
    'channels': int(channels),
    't_sample': t_sample,
    'duration': float(duration)
        }
        # Data acquisition
        #Execute top_block.py with parameters
        #sys.argv = ['top_block.py', '--c-freq='+f_center, '--samp-rate='+bandwidth, '--nchan='+channels, '--nbin='+nbins, '--obs-time='+duration]
        #execfile('/home/pi/Desktop/pictortelescope/top_block.py')
        virgo.observe(obs_parameters=observation, spectrometer='wola', obs_file='/home/pi/Desktop/pictortelescope/observation.dat')
        copy2('/home/pi/Desktop/pictortelescope/observation.dat', '/home/pi/Desktop/pictortelescope/obs_archive/'+str(obsDTfile)+'.dat')
        #Execute plotter
        if f_center == '1420000000.0' and (bandwidth == '2400000' or bandwidth == '3200000') and (channels == '1024' or channels == '2048'):
                if channels == '1024' and bandwidth == '2400000':
                        cal_file = '/home/pi/Desktop/pictortelescope/off1024.dat'
                elif channels == '2048' and bandwidth == '2400000':
                        cal_file = '/home/pi/Desktop/pictortelescope/off2048.dat'
                elif channels == '2048' and bandwidth == '3200000':
                        cal_file = '/home/pi/Desktop/pictortelescope/off2048_3_2.dat'
                else:
                        cal_file = ''
        else:
                cal_file = ''
        
        # Data analysis
        virgo.plot(obs_parameters=observation, n=20, m=20, f_rest=1420.4057517667e6,
                   obs_file='/home/pi/Desktop/pictortelescope/observation.dat', cal_file=cal_file,
                   spectra_csv='/home/pi/Desktop/pictortelescope/spectrum.csv', power_csv='/home/pi/Desktop/pictortelescope/time_series.csv', plot_file='/home/pi/Desktop/pictortelescope/plot.png')
        
        with open('/home/pi/Desktop/pictortelescope/id_history.txt', 'a') as id_logfile:
            id_logfile.write(id+'\n')
        
        if obs_name == 'off1024':
            copy2('/home/pi/Desktop/pictortelescope/observation.dat', '/home/pictor/Desktop/pictortelescope/off1024.dat')
        elif obs_name == 'off2048':
            copy2('/home/pi/Desktop/pictortelescope/observation.dat', '/home/pictor/Desktop/pictortelescope/off2048.dat')
        
        #Send plot to observer's email
        fromaddr = 'pictortelescope@gmail.com'
        toaddr = email
        
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        
        msg['Subject'] = '['+id+'] Observation Data'
        
        body = '''Your observation has been carried out by PICTOR successfully!
Observation name: '''+obs_name+'''
Observation datetime: '''+obsDT+''' (UTC+2)
Center frequency: '''+f_center+''' Hz
Bandwidth: '''+bandwidth+''' Hz
Sample rate: '''+bandwidth+''' samples/sec
Number of channels: '''+channels+'''
Number of bins: '''+nbins+'''
Observation duration: '''+duration+''' sec
Observation ID: '''+id+'''
Your observation's averaged spectrum, dynamic spectrum (waterfall) and Power vs Time plot are attached in this email as an image.'''
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename1 = 'plot.png'
        attachment1 = open("/home/pi/Desktop/pictortelescope/"+filename1, 'rb')
        
        p1 = MIMEBase('application', 'octet-stream')
        p1.set_payload((attachment1).read())
        
        encoders.encode_base64(p1)
        p1.add_header('Content-Disposition', 'attachment; filename= %s' % filename1)
        msg.attach(p1)
        if (raw_data == '1'):
            #Add spectrum Data
            filename2 = 'spectrum.csv'
            attachment2 = open("/home/pi/Desktop/pictortelescope/"+filename2, 'rb')

            p2 = MIMEBase('application', 'octet-stream')
            p2.set_payload((attachment2).read())

            encoders.encode_base64(p2)
            p2.add_header('Content-Disposition', 'attachment; filename= %s' % filename2)
            msg.attach(p2)

            #Add Time vs. Power Data
            filename3 = 'time_series.csv'
            attachment3 = open("/home/pi/Desktop/pictortelescope/"+filename3, 'rb')

            p3 = MIMEBase('application', 'octet-stream')
            p3.set_payload((attachment3).read())

            encoders.encode_base64(p3)
            p3.add_header('Content-Disposition', 'attachment; filename= %s' % filename3)
            msg.attach(p3)

            #Add .dat data
            #filename4 = 'observation.dat'
            #attachment4 = open("/home/pi/Desktop/pictortelescope/"+filename4, 'rb')

            #p4 = MIMEBase('application', 'octet-stream')
            #p4.set_payload((attachment4).read())

            #encoders.encode_base64(p4)
            #p4.add_header('Content-Disposition', 'attachment; filename= %s' % filename4)
            #msg.attach(p4)
            
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
Observation datetime: '''+obsDT+''' (UTC+2)
Center frequency: '''+f_center+''' Hz
Bandwidth: '''+bandwidth+''' Hz
Sample rate: '''+bandwidth+''' samples/sec
Number of channels: '''+channels+'''
Number of bins: '''+nbins+'''
Observation duration: '''+duration+''' sec
Observation ID: '''+id+'''
Your observation's averaged spectrum, dynamic spectrum (waterfall) and Power vs Time plot are attached in this email as an image.'''
        
        msg.attach(MIMEText(body, 'plain'))
        
        filename1 = 'observation.dat'
        attachment1 = open("/home/pi/Desktop/pictortelescope/"+filename1, 'rb')
        
        p1 = MIMEBase('application', 'octet-stream')
        p1.set_payload((attachment1).read())
        
        encoders.encode_base64(p1)
        p1.add_header('Content-Disposition', 'attachment; filename= %s' % filename1)
        msg.attach(p1)

        #Add spectrum Data
        filename2 = 'spectrum.csv'
        attachment2 = open("/home/pi/Desktop/pictortelescope/"+filename2, 'rb')

        p2 = MIMEBase('application', 'octet-stream')
        p2.set_payload((attachment2).read())

        encoders.encode_base64(p2)
        p2.add_header('Content-Disposition', 'attachment; filename= %s' % filename2)
        msg.attach(p2)

        #Add Time vs. Power Data
        filename3 = 'time_series.csv'
        attachment3 = open("/home/pi/Desktop/pictortelescope/"+filename3, 'rb')

        p3 = MIMEBase('application', 'octet-stream')
        p3.set_payload((attachment2).read())

        encoders.encode_base64(p3)
        p3.add_header('Content-Disposition', 'attachment; filename= %s' % filename3)
        msg.attach(p3)
        
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(fromaddr, 'XXX') #plaintext email password
        
        text = msg.as_string()
        
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
        
    except Exception as e:
        print(e)
        pass
