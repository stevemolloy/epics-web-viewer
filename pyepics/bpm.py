from epics import PV
import os
from scipy.fftpack import rfft
import numpy as np


PVROOT = "BPM:"
os.environ['EPICS_CA_ADDR_LIST'] = '10.0.16.173'
os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'NO'
os.environ['EPICS_CA_MAX_ARRAY_BYTES'] = '200000000'


def triggerAquisition():
    aquisitionPV = PV(f'{PVROOT}Acquire')
    aquisitionPV.value = 1


class BPMdata:
    def __init__(self, BPMnum):
        PVNameRoot = f'{PVROOT}TS{BPMnum}:'
        
        self.numSampPointsPV = PV(f'{PVROOT}NumBPMSamples_RBV')
        
        self.sumSigAmpPV = PV(f'{PVNameRoot}2:TimeSeries')
        self.sumSigPhasePV = PV(f'{PVNameRoot}3:TimeSeries')
        self.xPosPV = PV(f'{PVNameRoot}0:TimeSeries')
        self.yPosPV = PV(f'{PVNameRoot}1:TimeSeries')
        
    def sumSigAmp(self):
        num_samps = self.numSampPointsPV.get()
        return self.sumSigAmpPV.get()[-num_samps:]
    
    def sumSigPhase(self):
        num_samps = self.numSampPointsPV.get()
        return self.sumSigPhasePV.get()[-num_samps:]
    
    def xPos(self):
        num_samps = self.numSampPointsPV.get()
        return self.xPosPV.get()[-num_samps:-2]
    
    def yPos(self):
        num_samps = self.numSampPointsPV.get()
        return self.yPosPV.get()[-num_samps:-2]
    
    def sumSigAmpSpectrum(self):
        p = self.sumSigAmp()
        return 1000 * abs(rfft(p)[1:])**2 / 50
    
    def sumSigPhaseSpectrum(self):
        p = self.sumSigPhase()
        return abs(rfft(p - np.mean(p))[1:])
