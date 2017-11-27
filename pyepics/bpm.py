from epics import PV
import os

PVROOT = "BPM:"

def triggerAquisition():
    aquisitionPV = PV(f'{PVROOT}Acquire')
    aquisitionPV.value = 1

os.environ['EPICS_CA_ADDR_LIST'] = '10.0.16.173'
os.environ['EPICS_CA_AUTO_ADDR_LIST'] = 'NO'
os.environ['EPICS_CA_MAX_ARRAY_BYTES'] = '200000000'

