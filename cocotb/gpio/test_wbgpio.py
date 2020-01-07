#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  06/01/2020
#-----------------------------------------------------------------------------
""" test_wbgpio
"""
import os
import sys
import cocotb
import logging
from cocotb import SimLog
from cocotb.triggers import Timer
from cocotb.result import raise_error
from cocotb.result import TestError
from cocotb.result import ReturnValue
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb.triggers import ClockCycles
from cocotb.binary import BinaryValue

from cocomod.wishbone.driver import WishboneMaster
from cocomod.wishbone.driver import WBOp

class WbGpio(object):
    """ test class for Spi2KszTest
    """
    LOGLEVEL = logging.INFO

    # clock frequency is 50Mhz
    PERIOD = (20, "ns")

    STATUSADDR = 0
    DIRADDR    = 1
    READADDR   = 2
    WRITEADDR  = 3

    def __init__(self, dut):
        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")
        self._dut = dut
        self.log = SimLog("wbGpio.{}".format(self.__class__.__name__))
        self._dut._log.setLevel(self.LOGLEVEL)
        self.log.setLevel(self.LOGLEVEL)
        self.clock = Clock(self._dut.clock, self.PERIOD[0], self.PERIOD[1])
        self._clock_thread = cocotb.fork(self.clock.start())

        self.wbs = WishboneMaster(dut, "io_wbs", dut.clock,
                          width=16,   # size of data bus
                          timeout=10, # in clock cycle number
                          signals_dict={"cyc":  "cyc_i",
                                      "stb":  "stb_i",
                                      "we":   "we_i",
                                      "adr":  "adr_i",
                                      "datwr":"dat_i",
                                      "datrd":"dat_o",
                                      "ack":  "ack_o" })
    def get_dut_version_str(self):
        return "{}".format(self._dut.version)

    @cocotb.coroutine
    def reset(self):
        self._dut.reset <= 1
        short_per = Timer(100, units="ns")
        yield short_per
        self._dut.reset <= 1
        yield short_per
        self._dut.reset <= 0
        yield short_per

@cocotb.test()#skip=True)
def test_read_version(dut):
    wbgpio = WbGpio(dut)
    yield wbgpio.reset()
    dut.log.info(f"Version {wbgpio.get_dut_version_str()}")
    wbRes = yield wbgpio.wbs.send_cycle([WBOp(addr) for addr in range(4)])
    rvalues = [wb.datrd for wb in wbRes]
    dut.log.info(f"Returned values : {rvalues}")
    if rvalues[0].binstr[-8:] != wbgpio.get_dut_version_str():
        msg = (f"wrong version read {rvalues[0].binstr[-8:]}, " +
              f"should be {wbgpio.get_dut_version_str()}")
        dut.log.error(msg)
        raise TestError(msg)
    yield Timer(1, units="us")

@cocotb.test()#skip=True
def test_change_dir_read_value(dut):
    """ Changing direction of some bits and read value """
    wbgpio = WbGpio(dut)
    yield wbgpio.reset()
    dut.log.info(f"Version {wbgpio.get_dut_version_str()}")
    dirv = 0xCAFE
    wbRes = yield wbgpio.wbs.send_cycle([WBOp(wbgpio.DIRADDR, dirv),
                                         WBOp(wbgpio.DIRADDR)])
    rvalues = [wb.datrd.integer for wb in wbRes]
    dut.log.info(f"Returned values : {[hex(v) for v in rvalues]}")
    if rvalues[-1] != dirv:
        msg = (f"Wrong direction value {hex(rvalues[-1])}, " +
               f" should be {hex(dirv)}")

    testv = 0xCAFE
    dut.io_inport = testv
    wbRes = yield wbgpio.wbs.send_cycle([WBOp(wbgpio.READADDR)])
    readvalue = wbRes[0].datrd.integer
    wbgpio.log.info(f"read register : {hex(readvalue)}")
    if readvalue != testv:
        msg = (f"Wrong value {hex(readvalue)} read," +
               f" should be {hex(testv)}")
        wbgpio.log.error(msg)
        raise TestError(msg)
    
