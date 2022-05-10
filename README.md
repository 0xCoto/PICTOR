# PICTOR: A free-to-use Radio Telescope
PICTOR is an open-source radio telescope that allows anyone to observe the radio sky, using its convenient web platform for free: https://www.pictortelescope.com

![alt text](https://i.imgur.com/Gnr6tar.jpg "The PICTOR Radio Telescope")

![alt text](https://i.imgur.com/u7b7s5h.jpg "The PICTOR Radio Telescope")


## About PICTOR
PICTOR consists of a 1.5-meter parabolic antenna that allows anyone to make continuous and spectral (i.e. [hydrogen line](https://en.wikipedia.org/wiki/Hydrogen_line)) drift-scan observations of the radio sky in the **1300~1700 MHz** regime for free. 

The goal of this effort is to introduce students, educators, astronomers and others to the majesty of the radio sky, **promoting radio astronomy education**, *without* the need of building a large and expensive radio telescope. 

PICTOR is a **fully open source** (software & hardware) project.

## Northern Sky HI Survey obtained with PICTOR
![alt text](https://i.imgur.com/pYgMAhW.png "PICTOR HI Survey")

## Technical Details (Telescope Specifications)
**Telescope diameter:** 1.5m (4.92 ft = 59.05")  
**Focal Ratio (F/D):** 0.411 (prime focus antenna)  
**Beamwidth (HPBW @ 1420 MHz):** \~8.95° (*k* factor = 63.64)  
**Operating frequency range:** 1300\~1700 MHz ([L band](https://en.wikipedia.org/wiki/L_band))  
**Two-stage low-noise amplifier (LNA):** Gain: 30 ± 2 dB - Noise figure (NF): < 0.5 dB  
**High-pass filter:** -30 dBc below 900 MHz  
~~**Third-stage LNA (used as an in-line amplifier):** Gain: > 9 dB~~ *  
~~**Band-pass filter:** f_center = 1420 MHz (designed for [hydrogen line](https://en.wikipedia.org/wiki/Hydrogen_line) observations)~~ *  
**Instantaneous bandwidth (IBW):** up to 3.2 MHz (sufficient for spectral observations) *[to be upgraded to 30.72 MHz]*  
**Number of channels:** up to 2048 (for high frequency-resolution observations) *[to be upgraded to 16384]*  

*\*Deemed unnecessary hence removed*

## Telescope Block Diagram
![alt text](https://i.imgur.com/C9ow5Fk.jpg "Telescope Block Diagram")

## PICTOR System Flowgraph
![alt text](https://i.imgur.com/AOdftxe.png "PICTOR flowgraph")

## GRC Data Acquisition Flowgraph (old)
![alt text](https://i.imgur.com/5R3f6Fx.png "Data Acquisition Flowgraph (old)")

## GRC Data Acquisition Flowgraph (4-tap weighted overlap-add (WOLA) Fourier transform spectrometer)
![alt text](https://i.imgur.com/2Xp8qnZ.png "Data Acquisition Flowgraph")

## Feedhorn Dimensions
![alt text](https://i.imgur.com/557vUio.png "Feedhorn dimensions")

## S-Parameters
S-Parameter of the monopole inside the feed:
![alt text](https://i.imgur.com/S7xh9bg.png "S-Parameter of the monopole")

S-Parameter of the feedhorn (with rod) - **this should be the considered S-Parameter of the antenna in its entirety**:
![alt text](https://i.imgur.com/6cMjMpz.png "S-Parameter of the feedhorn")

Measured with the **Keysight N5221A PNA Network Analyzer (10 MHz~13.5 GHz)**:
![alt text](https://i.imgur.com/i9wenwo.jpg "Measurement of the monopole at the lab")
![alt text](https://i.imgur.com/f2LOvkE.jpg "Measurement of the feedhorn at the lab")

## Example Observation
![alt text](https://i.imgur.com/K8g0wVd.png "Example Observation")

## Wish to observe with PICTOR?
Take a look at the [PDF guide](https://www.pictortelescope.com/Observing_the_radio_sky_with_PICTOR.pdf) containing all the information you need to know in order to conduct your first observation of the radio sky!

<p align="center">
  <img src="https://i.imgur.com/qrkJkZw.png?raw=true" alt="PICTOR Telescope Logo"/>
</p>

## A description/role for each file
File | Description
--- | --- 
`observe.py` | Listens for observation requests & conducts observations
`plot.py` | Produces plots from observation data
`plot_hi.py` | Produces HI-tailored plots (i.e. +calibrated spectrum) from observation data
`id_history.txt` | Serves as an observation ID history database
`fft_integration.grc` | [GRC](https://wiki.gnuradio.org/index.php/GNURadioCompanion) Flowgraph previously used for the recording and processing of the data
`top_block_old.py` | Embedded Python Block for `fft_integration.grc`
`pfb.grc` | [GRC](https://wiki.gnuradio.org/index.php/GNURadioCompanion) Polyphase Filterbank Flowgraph for efficient data acquisition
`top_block.py` | Embedded Python Block for `pfb.grc`
`observe.php` | Includes server-side PHP code for [/observe](https://www.pictortelescope.com/observe)
`Waveguide.stl` | STL file for feedhorn visualization

## Credits
**PICTOR** was built by **[Apostolos Spanakis-Misirlis](https://www.github.com/0xCoto)**.

Special thanks to **Dr. Cameron Van Eck** for his thorough guidance throughout the development of PICTOR, the **[Telecommunication Systems Laboratory](http://tsl.ds.unipi.gr/)** of the [Department of Digital Systems](https://www.ds.unipi.gr/en/) at the [University of Piraeus](https://www.unipi.gr/unipi/en/) for allowing us to conduct decisive antenna measurements, the [Dwingeloo Radio Observatory](https://www.camras.nl/en/) (**Paul Boven** & **Dr. Cees Bassa**) for helping with the recording & the plotting of the data, **[Vasilis Spanakis-Misirlis](mailto:meiko_dew@hotmail.com)** for his engineering assistance, Konstantinos Bakolitsas for his support and **[ynk](https://www.github.com/ynk)** & **[Tino](https://www.github.com/RononDex/)** for their back-end contribution to `observe.php`.
