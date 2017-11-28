import unittest
import numpy as np
from time import sleep
from ..bpm import BPMdata, triggerAquisition


class TestBPMdata(unittest.TestCase):
    def setUp(self):
        triggerAquisition()
        self.bpm1 = BPMdata(1)
        self.bpm2 = BPMdata(2)

    def test_aquisition_works(self):
        self.assertGreater(self.bpm1.numSampPointsPV.get(), 0)
        self.assertGreater(self.bpm2.numSampPointsPV.get(), 0)

    def test_sumsignal(self):
        numpts = self.bpm1.numSampPointsPV.get()
        sumsigamp_len1 = len(self.bpm1.sumSigAmp())
        sumsigphase_len1 = len(self.bpm1.sumSigPhase())
        self.assertEqual(numpts, sumsigamp_len1)
        self.assertEqual(numpts, sumsigphase_len1)

        numpts = self.bpm2.numSampPointsPV.get()
        sumsigamp_len2 = len(self.bpm2.sumSigAmp())
        sumsigphase_len2 = len(self.bpm2.sumSigPhase())
        self.assertEqual(numpts, sumsigamp_len2)
        self.assertEqual(numpts, sumsigphase_len2)

    def test_xpossignal(self):
        numpts = self.bpm1.numSampPointsPV.get()
        xpos_len1 = len(self.bpm1.xPos())
        self.assertEqual(numpts - 2, xpos_len1)  # Huh!?

        numpts = self.bpm2.numSampPointsPV.get()
        xpos_len2 = len(self.bpm2.xPos())
        self.assertEqual(numpts - 2, xpos_len2)  # Huh!?

    def test_ypossignal(self):
        numpts = self.bpm1.numSampPointsPV.get()
        ypos_len1 = len(self.bpm1.yPos())
        self.assertEqual(numpts - 2, ypos_len1)  # Huh!?

        numpts = self.bpm2.numSampPointsPV.get()
        ypos_len2 = len(self.bpm2.yPos())
        self.assertEqual(numpts - 2, ypos_len2)  # Huh!?

    def test_sumsignal_changes(self):
        original_sumsignal1 = self.bpm1.sumSigAmp()
        original_sumsignal2 = self.bpm2.sumSigAmp()

        sleep(1.5)

        self.assertTrue(~np.all(original_sumsignal1 == self.bpm1.sumSigAmp()))
        self.assertTrue(~np.all(original_sumsignal2 == self.bpm2.sumSigAmp()))
