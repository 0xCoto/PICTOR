#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Jun 13 02:23:19 2019
##################################################


from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy as np
import osmosdr
import time


class top_block(gr.top_block):

    def __init__(self, c_freq=1420000000, nbin=1000, nchan=1024, obs_time=60, samp_rate=2400000):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.c_freq = c_freq
        self.nbin = nbin
        self.nchan = nchan
        self.obs_time = obs_time
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.gain = gain = 10000

        ##################################################
        # Blocks
        ##################################################
        self.fft_vxx_0 = fft.fft_vcc(nchan, True, (window.blackmanharris(nchan)), True, 1)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, nchan)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(nbin, nchan)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(obs_time*samp_rate))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*nchan, 'observation.dat', True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(nchan)
        self.RTL820T = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.RTL820T.set_sample_rate(samp_rate)
        self.RTL820T.set_center_freq(c_freq, 0)
        self.RTL820T.set_freq_corr(0, 0)
        self.RTL820T.set_dc_offset_mode(0, 0)
        self.RTL820T.set_iq_balance_mode(0, 0)
        self.RTL820T.set_gain_mode(False, 0)
        self.RTL820T.set_gain(30, 0)
        self.RTL820T.set_if_gain(30, 0)
        self.RTL820T.set_bb_gain(30, 0)
        self.RTL820T.set_antenna('', 0)
        self.RTL820T.set_bandwidth(0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.RTL820T, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))

    def get_c_freq(self):
        return self.c_freq

    def set_c_freq(self, c_freq):
        self.c_freq = c_freq
        self.RTL820T.set_center_freq(self.c_freq, 0)

    def get_nbin(self):
        return self.nbin

    def set_nbin(self, nbin):
        self.nbin = nbin

    def get_nchan(self):
        return self.nchan

    def set_nchan(self, nchan):
        self.nchan = nchan

    def get_obs_time(self):
        return self.obs_time

    def set_obs_time(self, obs_time):
        self.obs_time = obs_time
        self.blocks_head_0.set_length(int(self.obs_time*self.samp_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_head_0.set_length(int(self.obs_time*self.samp_rate))
        self.RTL820T.set_sample_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--c-freq", dest="c_freq", type="eng_float", default=eng_notation.num_to_str(1420000000),
        help="Set c_freq [default=%default]")
    parser.add_option(
        "", "--nbin", dest="nbin", type="intx", default=1000,
        help="Set nbin [default=%default]")
    parser.add_option(
        "", "--nchan", dest="nchan", type="intx", default=1024,
        help="Set nchan [default=%default]")
    parser.add_option(
        "", "--obs-time", dest="obs_time", type="eng_float", default=eng_notation.num_to_str(60),
        help="Set obs_time [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(2400000),
        help="Set samp_rate [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(c_freq=options.c_freq, nbin=options.nbin, nchan=options.nchan, obs_time=options.obs_time, samp_rate=options.samp_rate)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
