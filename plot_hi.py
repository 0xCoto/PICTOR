#!/usr/bin/env python
try:
    import matplotlib
    matplotlib.use('Agg')
    
    import numpy as np
    import pandas as pd
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
    
    def estimate_k_factor_simple(on,off,mask=np.array([])):
        """Simple estimation of 'k' factor, by median of ratios.
        (By 'k' factor, it is assumed k is applied to the ON measurement. Take 1/k if applied to OFF.)
        Will likely fail if significant part of (unmasked) spectrum contains signal.
        Inputs: on, off: input spectra (assumed 1D arrays)
                mask: optional mask of ignored channels. Non-zero values are not used by estimator.
        Output: k"""
        if mask.size == 0:
            mask=np.zeros_like(on)
        
        ratio=off/on
        k=np.nanmedian(ratio[mask == 0])
        return k
    
    def estimate_S_N_simple(spectrum,mask=np.array([])):
        """Simple estimation of signal_to_noise, with optional masking.
        If mask not given, then all channels will be used in estimating noise
            (will drastically underestimate S:N! Not robust to outliers!)
        Inputs: spectrum: 1D array.
                mask: optional mask of ignored channels. Non-zero values are not used by estimator.
        Output: k"""
        if mask.size == 0:
            mask=np.zeros_like(spectrum)
        
        noise=np.std((spectrum[2:]-spectrum[:-2])[mask[1:-1] == 0])/np.sqrt(2)
        background=np.nanmean(spectrum[mask == 0])
        return (spectrum-background)/noise
    
    if __name__ == "__main__":
        #Observation parameters
        exec(args.freq)
        exec(args.samp_rate)
        exec(args.nchan)
        exec(args.nbin)
        obs_on = "/home/pictor/Desktop/pictortelescope/observation.dat"
        obs_off = "/home/pictor/Desktop/pictortelescope/off"+str(nchan)+".dat"
        
        #Load ON data
        z = np.fromfile(obs_on, dtype="float32").reshape(-1, nchan)/nbin
        z = z*10000
        
        #RFI mitigation
        z[z > 2000] = np.nan
        
        zmean = np.nanmean(z,axis=0)
        
        #Load OFF data
        z_off = np.fromfile(obs_off, dtype="float32").reshape(-1, nchan)/10000
        z_off = z_off*10000
        z_offmean = np.nanmean(z_off,axis=0)
        
        #Compute frequency axis (convert to MHz)
        freq = np.linspace(freq-0.5*samp_rate, freq+0.5*samp_rate, nchan, endpoint=False)*1e-6
        
        #Apply mask
        mask=np.zeros_like(zmean)
        mask[np.logical_and(freq > 1420.3, freq < 1421.2)]=1
        if np.nan in z:
            mask[np.logical_and(freq > 1419.4, freq < 1419.75)]=1
        
        #Estimate k factor
        k = estimate_k_factor_simple(zmean,z_offmean,mask)
        
        #Perform subtraction
        spectrum=(zmean/z_offmean)
        
        #Define numpy array for Power vs Time plot
        w = np.nanmean(a=z, axis=1)
        
        #Number of sub-integrations
        nsub = z.shape[0]
        
        #Compute average spectrum
        mean = np.nanmean(z, axis=0)
        
        #Compute time axis
        tint = float(nbin*nchan)/samp_rate
        t = tint*np.arange(nsub)
        
        #Initialize plot
        fig = plt.figure(figsize=(30,14))
        gs = GridSpec(2,3,
                      height_ratios=[2, 1.5]
                      )
        #Initialize frequency dataframe
        data_freq = pd.DataFrame(freq, columns = ['frequency'])
        
        #Plot Averaged Spectrum
        ax1 = fig.add_subplot(gs[0,0])
        ax1.plot(freq, decibel(zmean))
        ax1.set_xlim(np.min(freq), np.max(freq))
        ax1.axvline(x=1420.4057517667, color='brown', linestyle='--', linewidth=2) #xy=(447, 471)
        ax1.annotate('Hydrogen Line\nReference Frequency', xy=(450, 5), xycoords='axes points', size=14, ha='left', va='bottom', color='brown')
        ax1.ticklabel_format(useOffset=False)
        ax1.set_xlabel("Frequency (MHz)")
        ax1.set_ylabel("Relative Power")
        ax1.set_title("Averaged Spectrum")
        #ax1.set_xticks(np.arange(np.min(freq),np.max(freq), step=0.3))
        ax1.grid()

        #Add zmean to dataframe
        data_freq['zmean'] = decibel(zmean)
        
        #Plot Calibrated Spectrum
        ax2 = fig.add_subplot(gs[0,1])
        ax2.plot(freq, estimate_S_N_simple(spectrum, mask))
        ax2.set_xlim(np.min(freq), np.max(freq))
        ax2.axvline(x=1420.4057517667, color='brown', linestyle='--', linewidth=2)
        ax2.annotate('Hydrogen Line\nReference Frequency', xy=(450, 5), xycoords='axes points', size=14, ha='left', va='bottom', color='brown')
        ax2.ticklabel_format(useOffset=False)
        ax2.set_xlabel("Frequency (MHz)")
        ax2.set_ylabel("Signal-to-Noise Ratio (S/N)")
        ax2.set_title("Calibrated Spectrum")
        ax2.grid()

        #Add S/N to dataframe
        data_freq['S/N'] = estimate_S_N_simple(spectrum, mask)
        
        #Plot Dynamic Spectrum (Waterfall)
        ax3 = fig.add_subplot(gs[0,2])
        ax3.imshow(decibel(z), origin="lower", interpolation="None", aspect="auto",
                   extent=[np.min(freq), np.max(freq), np.min(t), np.max(t)])
        ax3.ticklabel_format(useOffset=False)
        ax3.set_xlabel("Frequency (MHz)")
        ax3.set_ylabel("Time (s)")
        ax3.set_title("Dynamic Spectrum (Waterfall)")

        #Create power vs time dataframe
        data_time = pd.DataFrame(t, columns = ['time'])
        data_time['w'] = w
        
        #Plot Power vs Time
        ax4 = fig.add_subplot(gs[1,:])
        ax4.plot(t,w)
        ax4.set_xlim(0,np.max(t)+tint)
        ax4.set_xlabel("Time (s)")
        ax4.set_ylabel("Relative Power")
        ax4.set_title("Power vs Time")
        ax4.grid()
        
        plt.tight_layout()

        #Save files
        plt.savefig("/home/pictor/Desktop/pictortelescope/plot.png")
        data_freq.to_csv("home/pictor/Desktop/pictortelescope\data_freq.csv")
        data_time.to_csv("home/pictor/Desktop/pictortelescope\data_time.csv")
except Exception as e:
    print(e)
    pass
