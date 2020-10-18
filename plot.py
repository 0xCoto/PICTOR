#!/usr/bin/env python
try:
    import matplotlib
    matplotlib.use('Agg')
    
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse
    from matplotlib.gridspec import GridSpec
    
    parser = argparse.ArgumentParser()
    parser.add_argument('freq')
    parser.add_argument('samp_rate')
    parser.add_argument('nchan')
    parser.add_argument('nbin')
    args = parser.parse_args()
    
    def decibel(x):
        #return 10.0*np.log10(x)
        return x
    
    if __name__ == "__main__":
        #Observation parameters
        exec(args.freq)
        exec(args.samp_rate)
        exec(args.nchan)
        exec(args.nbin)
        fname = "/home/pi/Desktop/pictortelescope/observation.dat"
        
        #Load data
        z = np.fromfile(fname, dtype="float32").reshape(-1, nchan)/nbin
        #z = np.delete(z, (0), axis=0)
        #z = z[n:, :]
        z = z*10000
        z = np.delete(z, (0), axis=0)
        
        #Define numpy array for Power vs Time plot
        w = np.mean(a=z, axis=1)
        
        #Number of sub-integrations
        nsub = z.shape[0]
        
        #Compute average spectrum
        zmean = np.mean(z, axis=0)
        
        #Compute time axis
        tint = float(nbin*nchan)/samp_rate
        t = tint*np.arange(nsub)
        
        #Compute frequency axis (convert to MHz)
        freq = np.linspace(freq-0.5*samp_rate, freq+0.5*samp_rate, nchan, endpoint=False)*1e-6
        
        #Initialize plot
        fig = plt.figure(figsize=(20,15))
        gs = GridSpec(2,2)

        #Create spectrum array
        data_freq = ['freq:']
        for i in range(len(freq)):
            data_freq.append(freq[i])
        data_zmean = ['average relative power by frequency:']
        for i in range(len(freq)):
            data_zmean.append(zmean[i])

        data_freq_zmean = np.array([data_freq, data_zmean])
        
        #Plot average spectrum
        ax1 = fig.add_subplot(gs[0,0])
        ax1.plot(freq, decibel(zmean))
        ax1.set_xlim(np.min(freq), np.max(freq))
        ax1.ticklabel_format(useOffset=False)
        ax1.set_xlabel("Frequency (MHz)")
        ax1.set_ylabel("Relative Power")
        ax1.set_title("Averaged Spectrum")
        
        #Plot dynamic spectrum
        ax2 = fig.add_subplot(gs[0,1])
        ax2.imshow(decibel(z), origin="lower", interpolation="None", aspect="auto",
                   extent=[np.min(freq), np.max(freq), np.min(t), np.max(t)])
        ax2.ticklabel_format(useOffset=False)
        ax2.set_xlabel("Frequency (MHz)")
        ax2.set_ylabel("Time (s)")
        
        ax2.set_title("Dynamic Spectrum (Waterfall)")

        #Create power vs time dataframe
        data_t = ['time:']
        for i in range(len(t)):
            data_t.append(t[i])
        data_w = ['relative power:']
        for i in range(len(w)):
            data_w.append(w[i])
        data_t_w = np.array([data_t, data_w])
        
        #Plot Power vs Time
        ax3 = fig.add_subplot(gs[1,:])
        ax3.plot(t,w)
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Relative Power")
        ax3.set_title("Power vs Time")
        
        plt.tight_layout()
        
        #Save files
        plt.savefig("/home/pi/Desktop/pictortelescope/plot.png")
        np.savetxt("/home/pi/Desktop/pictortelescope/data_spectrum.csv", np.transpose(data_freq_zmean), delimiter = ',', fmt = '%s')
        np.savetxt("/home/pi/Desktop/pictortelescope/data_time_power.csv", np.transpose(data_t_w), delimiter = ',', fmt = '%s')
except Exception as e:
    print(e)
    pass
