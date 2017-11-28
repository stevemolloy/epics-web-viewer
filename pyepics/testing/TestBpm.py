import unittest
from ..bpm import BPMdata, triggerAquisition


class TestBPMdata(unittest.TestCase):
    def setUp(self):
        triggerAquisition()
        self.bpm1 = BPMdata(1)
        self.bpm2 = BPMdata(2)

    def test_aquisition_works(self):
        self.assertGreater(self.bpm1.numSampPointsPV.get(), 0)
