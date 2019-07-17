# PICTOR
PICTOR is an open-source radio telescope that allows anyone to observe the radio sky, using its convenient web platform for free: https://www.pictortelescope.com

![alt text](https://i.imgur.com/MjS3WcT.jpg "The PICTOR Radio Telescope")

## About PICTOR
PICTOR consists of a 1.5-meter parabolic antenna that allows anyone to make continuous and spectral (i.e. [hydrogen line](https://www.cv.nrao.edu/course/astr534/HILine.html)) drift-scan observations of the radio sky in the **1300~1700 MHz** regime for free. 

The goal of this effort is to introduce students, educators, astronomers and others to the majesty of the radio sky, **promoting radio astronomy education**, *without* the need of building a large and expensive radio telescope. 

PICTOR is a **fully open source** (software & hardware) project.

## Technical Details (Telescope Specifications)
**Telescope diameter:** 1.5m (4.92 ft = 59.05")  
**Focal Ratio (F/D):** 0.411 (prime focus antenna)  
**Beamwidth (HPBW @ 1420 MHz):** \~8.95° (*k* factor = 63.64)  
**Operating frequency range:** 1300\~1700 MHz ([L band](https://www.techopedia.com/definition/30820/l-band))  
**Two-stage low-noise amplifier (LNA):** Gain: 30 ± 2 dB - Noise figure (NF): < 0.5 dB  
**High-pass filter:** -30 dBc below 900 MHz  
~~**Third-stage LNA (used as an in-line amplifier):** Gain: > 9 dB~~ *  
~~**Band-pass filter:** f_center = 1420 MHz (designed for [hydrogen line](https://www.cv.nrao.edu/course/astr534/HILine.html) observations)~~ *  
**Instantaneous bandwidth (IBW):** up to 3.2 MHz (sufficient for spectral observations) *[to be upgraded to 30.72 MHz]*  
**Number of channels:** up to 2048 (for high frequency-resolution observations) *[to be upgraded to 16384]*  

*\*Deemed unnecessary hence removed*

## Feedhorn Dimensions
![alt text](https://i.imgur.com/557vUio.png "Feedhorn dimensions")

## S-Parameters
S-Parameter of the monopole inside the feed:
![alt text](https://i.imgur.com/XLsuTv4.png "S-Parameter of the monopole")

S-Parameter of the feedhorn (with rod) - **this should be the considered S-Parameter of the antenna in its entirety**:
![alt text](https://i.imgur.com/6cMjMpz.png "S-Parameter of the feedhorn")

Measured with the Keysight N5221A PNA Network Analyzer (10 MHz~13.5 GHz):
![alt text](https://i.imgur.com/i9wenwo.jpg "Measurement of the monopole at the lab")
![alt text](https://i.imgur.com/f2LOvkE.jpg "Measurement of the feedhorn at the lab")

## Telescope Block Diagram
![alt text](https://i.imgur.com/C9ow5Fk.jpg "Block Diagram")

## Wish to observe with PICTOR?
Take a look at the [PDF guide](https://www.pictortelescope.com/Observing_the_radio_sky_with_PICTOR.pdf) containing all the information you need to know in order to conduct your first observation of the radio sky!

## A description/role for each file
File | Description
--- | --- 
`observe.py` | Listens for observation requests & conducts observations
`plot.py` | Produces plots from observation data
`id_history.txt` | Serves as an observation ID history database
`pictor.grc` | [GRC](https://wiki.gnuradio.org/index.php/GNURadioCompanion) Flowgraph for recording the data
`top_block.py` | Embedded Python Block for `pictor.grc`
`observe.php` | Includes server-side PHP code for [/observe](https://www.pictortelescope.com/observe)

## Credits
PICTOR was built by [Apostolos Spanakis-Misirlis](https://www.github.com/0xCoto/).

Special thanks to **Dr. Cameron Van Eck** for his thorough guidance throughout the development of PICTOR, the **[Telecommunication Systems Laboratory](http://tsl.ds.unipi.gr/)** of the [Department of Digital Systems](https://www.ds.unipi.gr/en/) at the [University of Piraeus](https://www.unipi.gr/unipi/en/) for allowing us to conduct decisive antenna measurements, the [Dwingeloo Radio Observatory](https://www.camras.nl/en/) (**Paul Boven** & **Cees Bassa**) for helping with the recording & the plotting of the data and **[Yannick](https://www.github.com/YannickDC)** & **[Tino](https://www.github.com/RononDex/)** for their back-end contribution to `observe.php`.
