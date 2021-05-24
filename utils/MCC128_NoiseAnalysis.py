# -*- coding: utf-8 -*-
"""
RPi Alkalinity
Version: v0.4 Beta
Licensed under {License info} for general use with attribution.

MCC128 Noise Analyzer
Aquires a high-density timeseries of voltage measurements from a channel on
the MCC128 DAQ HAT and applies a FFT to identify potential noise frequencies.
"""
#Basics
from time import sleep
from sys import stdout
import pandas as pd
from scipy.fft import fft, ifft, fftfreq
import numpy as np
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from utils.daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string

# Constants
CURSOR_BACK_2 = '\x1b[2D'
ERASE_TO_END_OF_LINE = '\x1b[0K'

sample_int = 0.1
timeseries_len  = 10

def get_mV_timeseries(sample_interval = 0.1, timeseries_length = 10):
    """
    

    Parameters
    ----------
    sample_interval : TYPE, optional
        DESCRIPTION. The default is 0.1.
    timeseries_length : TYPE, optional
        DESCRIPTION. The default is 10.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    value_array : TYPE
        DESCRIPTION.

    """
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 3
    input_mode = AnalogInputMode.SE #SE/single-ended DIFF/differential
    input_range = AnalogInputRange.BIP_1V #CHANGED FROM 10V TO 1V

    mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]
    
    try:
        # Ensure low_chan and high_chan are valid.
        if low_chan < 0 or low_chan >= mcc_128_num_channels:
            error_message = ('Error: Invalid low_chan selection - must be '
                             '0 - {0:d}'.format(mcc_128_num_channels - 1))
            raise Exception(error_message)
        if high_chan < 0 or high_chan >= mcc_128_num_channels:
            error_message = ('Error: Invalid high_chan selection - must be '
                             '0 - {0:d}'.format(mcc_128_num_channels - 1))
            raise Exception(error_message)
        if low_chan > high_chan:
            error_message = ('Error: Invalid channels - high_chan must be '
                             'greater than or equal to low_chan')
            raise Exception(error_message)

        # Get an instance of the selected hat device object.
        address = select_hat_device(HatIDs.MCC_128)
        hat = mcc128(address)

        hat.a_in_mode_write(input_mode)
        hat.a_in_range_write(input_range)
        
        try:
            value_array = np.empty([timeseries_length/sample_interval])
            for i in range(timeseries_length/sample_interval):
                value = hat.a_in_read(low_chan, options)
                stdout.flush()
                value_array[i] = value

        except KeyboardInterrupt:
            # Clear the '^C' from the display.
            print(CURSOR_BACK_2, ERASE_TO_END_OF_LINE, '\n')

    except (HatError, ValueError) as error:
        print('\n', error)
        
        
    return value_array

x = np.linspace(0, timeseries_len, num = timeseries_len/sample_int)
y = get_mV_timeseries(sample_interval = sample_int, timeseries_length = timeseries_len)
yf = fft(y)
xf = fftfreq(timeseries_len, sample_int)#[:N//2]

df = pd.DataFrame({
    'x': x,
    'y': y,
    'xf': xf,
    'yf': np.abs(yf)
    })