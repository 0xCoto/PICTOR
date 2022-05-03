#from random import randrange
import asyncio
import requests
import os
import discord
import time
import virgo
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

test = np.loadtxt('/home/pi/Desktop/pictortelescope/map.txt')
brr = np.flip(test, 1)
#hpbw = 70*(0.21/3.2)


#time.sleep(20)
while True:
    if True:
        #load_dotenv()
        token = 'xxx'
        client = discord.Client()
        
        @client.event
        async def on_ready():
            await client.change_presence(status=discord.Status.online, activity=discord.Game('pictortelescope.com'))
            print(f'{client.user.name} has connected to Discord!')
        
        observing = False
        @client.event
        async def on_message(message):
            global observing
            print(message.content)
            #if randrange(10) > 2:
            #    response = requests.get('https://pictortelescope.com/last_obs_duration.txt')
            #    if response.status_code == 200:
            #        exec(response.content)
            #        if int(time.time()) <= int(obs_time)+int(duration):
            #            observing = True
            #            client.change_presence(status=discord.Status.idle, activity=discord.Game('Observing...'))
            #        else:
            #            observing = False
            #            client.change_presence(status=discord.Status.online, activity=discord.Game('pictortelescope.com'))
            if message.author == client.user:
                return
            if 'restart_pictor' in message.content:
                os.system("sudo /bin/systemctl restart pictor.service")
                os.system("sudo /bin/systemctl restart disc_bot.service")
            if ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and observing and 'observe' in (message.content).lower():
                await message.add_reaction('❌')
                await message.channel.send('The telescope is currently observing. Please wait until it\'s done before submitting your observation...')
                return
            elif ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and 'observe' not in (message.content).lower()  and 'map' not in (message.content).lower() and 'simulate' not in (message.content).lower():
                print(3)
                await message.channel.send('**PICTOR** is an open-source radio telescope that allows anyone to observe the radio sky using its convenient web platform for **free**! This bot allows you to submit observations directly from Discord. For more info, visit <https://www.pictortelescope.com> or ping <@!234246004424179712> for help!\n\n**Usage:**\n```@PICTOR observe <duration (in seconds)>\n@PICTOR map\n@PICTOR simulate <l> <b>```\n**Example:**\n```@PICTOR observe 60```\n**Default observation parameters:**\n```\nCenter frequency: 1420 MHz\nBandwidth: 2.4 MHz\nNumber of channels: 2048\nNumber of bins: 100```')
                return
            elif ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and 'map' in (message.content).lower():
                await message.add_reaction('🌌')
                plt.rcParams["figure.figsize"] = (20,20)
                a = plt.imshow(brr, extent=[24,0,-90,90], aspect=0.07, interpolation = 'none')
                plt.xticks(np.arange(0, 24.01, 2))
                plt.text(4.75, 91.8, 'LAB HI Survey (Kalberla et al., 2005)', fontsize=14, bbox={'facecolor': 'white', 'pad': 4})
                plt.title('PICTOR Telescope | All-Sky Map', fontsize=28, y=1.01)
                plt.xlabel('Right Ascension (hours)', fontsize=20)
                plt.ylabel('Declination (deg)', fontsize=20)
                plt.xticks(fontsize=16)
                plt.yticks(fontsize=16)
                ra, dec = virgo.equatorial(88, 0, 38.6245, 21.4096)
                #if flag:
                plt.axvline(ra, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                plt.axhline(dec, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                #else:
                #    v.set_ydata(ra)
                #    h.set_ydata(dec)
                #plt.axhline(dec-float(hpbw)/2, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                #plt.axhline(dec+float(hpbw)/2, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                plt.scatter(ra, dec, s=350, color=[214/255, 39/255, 40/255])
                plt.tight_layout()
                plt.savefig('/home/pi/Desktop/pictortelescope/map.png', bbox_inches='tight')
                plt.clf()
                await message.channel.send('<@!'+str(message.author.id)+ '> The telescope is currently pointing to **RA = '+str(round(ra,1))+' h**, **Dec. = '+str(round(dec,1))+'°** (**𝑙 = '+str(round(virgo.galactic(ra,dec)[0],1))+'°**, **𝑏 = '+str(round(virgo.galactic(ra,dec)[1],1))+'°**):', file=discord.File('/home/pi/Desktop/pictortelescope/map.png'))
                return
            print(2)
            if ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and len(message.content.split()) == 4 and (((message.content).split())[1]).lower() == 'simulate':
                if  message.content.split()[2].isdigit() and float(message.content.split()[2]) >= 0 and float(message.content.split()[2]) < 360 and float(message.content.split()[3]) >= -90 and float(message.content.split()[3]) <= 90:
                    l_sim = float(message.content.split()[2])
                    b_sim = float(message.content.split()[3])
                    await message.add_reaction('📡')
                    try:
                        os.remove('/home/pi/Desktop/pictortelescope/sim.png')
                        print(8)
                    except OSError:
                        pass
                    virgo.simulate(l=l_sim, b=b_sim, v_min=-167.541627, v_max=339.294995, beamwidth=9.4, plot_file='/home/pi/Desktop/pictortelescope/sim.png')
                    time.sleep(1)
                    while not os.path.exists('/home/pi/Desktop/pictortelescope/sim.png'):
                        print('doesnt exist')
                        await asyncio.sleep(1)
                    time.sleep(2)
                    await message.channel.send('<@!'+str(message.author.id)+ '> Simulated HI profile for **𝑙 = '+str(l_sim)+'°**, **𝑏 = '+str(b_sim)+'°**:', file=discord.File('/home/pi/Desktop/pictortelescope/sim.png'))
                    plt.close()
                else:
                    await message.add_reaction('❌')
                    await message.channel.send('Please ensure the given galactic longitude (𝑙) amd latitude (𝑏) are in the range [0, 360) and [-90, 90] respectively.')
            if not observing and ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and len(message.content.split()) == 3 and (((message.content).split())[1]).lower() == 'observe':
                if  message.content.split()[2].isdigit() and int(message.content.split()[2]) >= 10 and int(message.content.split()[2]) <= 600:
                    duration = message.content.split()[2]
                    try:
                        os.remove('/home/pi/Desktop/pictortelescope/observation.dat')
                        os.remove('/home/pi/Desktop/pictortelescope/plot.png')
                        os.remove('/home/pi/Desktop/pictortelescope/spectrum.csv')
                        os.remove('/home/pi/Desktop/pictortelescope/time_series.csv')
                    except OSError:
                        pass
                    await message.add_reaction('✅')
                    await message.channel.send('Observing for **'+duration+' seconds** with PICTOR. Please wait...')
                    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Observing...'))
                    observing = True
                    obs_args = {'obs_name': 'discord_obs', 'f_center': '1420', 'bandwidth': '2.4mhz', 'channels': '2048', 'nbins': '100', 'duration': duration, 'email': 'coto_dup@hotmail.com', 'submit_btn': '1'}
                    requests.post('https://pictortelescope.com/observe.php', data = obs_args)
                    try:
                        os.remove('/home/pi/Desktop/pictortelescope/observation.dat')
                        os.remove('/home/pi/Desktop/pictortelescope/plot.png')
                        print(8)
                    except OSError:
                        pass
                    
                    time.sleep(5)
                    while not os.path.exists('/home/pi/Desktop/pictortelescope/plot.png'):
                        print('doesnt exist')
                        await asyncio.sleep(1)
                    time.sleep(4)
                    print('out')
                    await message.channel.send('<@!'+str(message.author.id)+ '> **Your observation has been carried out by PICTOR successfully!**\nHere is your observation\'s data:', file=discord.File('/home/pi/Desktop/pictortelescope/plot.png'))
                    await client.change_presence(status=discord.Status.online, activity=discord.Game('pictortelescope.com'))
                    observing = False
                else:
                    await message.add_reaction('❌')
                    await message.channel.send('Please ensure the given observation duration is greater than 10 and less than 600 seconds.')
            
            elif ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and 'map' not in (message.content).lower() and ('simulate' in (message.content).lower() and len(message.content.split()) != 4):
                await message.channel.send('**PICTOR** is an open-source radio telescope that allows anyone to observe the radio sky using its convenient web platform for **free**! This bot allows you to submit observations directly from Discord. For more info, visit <https://www.pictortelescope.com> or ping <@!234246004424179712> for help!\n\n**Usage:**\n```@PICTOR observe <duration (in seconds)>\n@PICTOR map\n@PICTOR simulate <l> <b>```\n**Example:**\n```@PICTOR observe 60```\n**Default observation parameters:**\n```\nCenter frequency: 1420 MHz\nBandwidth: 2.4 MHz\nNumber of channels: 2048\nNumber of bins: 100```')
            elif ((message.content).startswith('<@!639462') or (message.content).startswith('<@639462') or ((message.content).lower()).startswith('@pictor')) and '639462705723605013>' in message.content and 'map' in (message.content).lower():
                await message.add_reaction('🌌')
                ra, dec = virgo.equatorial(88, 0, 38.6245, 21.4096)
                plt.axvline(ra, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                plt.axhline(dec, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                #plt.axhline(dec-float(hpbw)/2, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                #plt.axhline(dec+float(hpbw)/2, 0, 1, linestyle='--', linewidth=2, color=(214/255, 39/255, 40/255, 0.9))
                plt.scatter(ra, dec, s=350, color=[214/255, 39/255, 40/255])#[1., 0.3, 0.3])
                plt.tight_layout()
                plt.savefig('/home/pi/Desktop/pictortelescope/map.png', bbox_inches='tight')
                await message.channel.send('<@!'+str(message.author.id)+ '> The telescope is currently pointing to **RA = '+str(round(ra,1))+'°**, **Dec. = '+str(round(dec,1))+'°** (**𝑙 = '+str(round(virgo.galactic(ra,dec)[0],1))+'°**, **𝑏 = '+str(round(virgo.galactic(ra,dec)[1],1))+'°**):', file=discord.File('/home/pi/Desktop/pictortelescope/map.png'))
        client.run(token)
    #except Exception as e:
    #    print(e)
    #    time.sleep(10)
    #    os.system("sudo /bin/systemctl restart disc_bot.service")
