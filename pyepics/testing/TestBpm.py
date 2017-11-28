import unittest
from ..bpm import BPMdata, triggerAquisition


class TestBPMdata(unittest.TestCase):
    def test_aquisition_works(self):
        triggerAquisition()
        bpm = BPMdata(1)
        self.assertGreater(bpm.numSampPointsPV.get(), 0)
