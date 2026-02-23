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
import random
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from cocotb.triggers import FallingEdge
from cocotb.triggers import ClockCycles

class GpioPortIntercon(object):
    """ test class for Spi2KszTest
    """
    LOGLEVEL = logging.INFO

    # clock frequency is 50Mhz
    PERIOD = (20, "ns")

    GPIO_MAP = [range(0, 1),
                range(2, 6),
                range(8, 9),
                range(10, 16)]
    PORT_SIZE = 16

    def __init__(self, dut):
        if sys.version_info[0] < 3:
            raise Exception("Must be using Python 3")
        self._dut = dut
        self.log = dut._log
        self._dut._log.setLevel(self.LOGLEVEL)
        self.log.setLevel(self.LOGLEVEL)
        self.clock = Clock(self._dut.clock, self.PERIOD[0], self.PERIOD[1])
        self._clock_thread = cocotb.start_soon(self.clock.start())

        self.GPIO_MASK = 0
        for r in self.GPIO_MAP:
            for b in r:
                self.GPIO_MASK = self.GPIO_MASK | (1 << b)

    def _get_vec(self, port):
        val = 0
        for idx,r in enumerate(self.GPIO_MAP):
            v = int(eval("self._dut.io_portVec_{}_{}.value".format(idx, port)))
            val = val | (v << r.start)
        return val

    async def reset(self):
        self._dut.reset.value = 1
        short_per = Timer(100, unit="ns")
        await short_per
        self._dut.reset.value = 1
        await short_per
        self._dut.reset.value = 0
        await short_per

    def set_output(self, val):
        self._dut.io_port_outport.value = val

    def set_en(self, en):
        self._dut.io_port_enport.value = en

    def get_output_vec(self):
        return self._get_vec('outport')

    def get_en_vec(self):
        return self._get_vec('enport')

    def get_input(self):
        return self._dut.io_port_inport.value.to_unsigned()

    def set_input_vec(self, val):
        for idx,r in enumerate(self.GPIO_MAP):
            v = val >> r.start
            mask = int(pow(2, len(r))) - 1
            v = v & mask
            exec("self._dut.io_portVec_{}_inport.value = {}".format(idx, v))

random.seed(864379)

SAMPLE_NUM = 256
MAX_VAL = int(pow(2, GpioPortIntercon.PORT_SIZE)) - 1

@cocotb.parametrize(
    samples = [[random.randrange(0, MAX_VAL) for _ in range(SAMPLE_NUM)]]
)
async def test_vec_input(dut, samples):
    port = GpioPortIntercon(dut)
    await port.reset()

    await FallingEdge(dut.clock)

    for s in samples:
        port.set_input_vec(s)

        await FallingEdge(dut.clock)

        assert port.get_input() == (s & port.GPIO_MASK)

    await Timer(1, unit="us")

@cocotb.parametrize(
    samples = [[random.randrange(0, MAX_VAL) for _ in range(SAMPLE_NUM)]]
)
async def test_vec_output(dut, samples):
    port = GpioPortIntercon(dut)
    await port.reset()

    await FallingEdge(dut.clock)

    for s in samples:
        port.set_output(s)

        await FallingEdge(dut.clock)

        assert port.get_output_vec() == (s & port.GPIO_MASK)

    await Timer(1, unit="us")

@cocotb.parametrize(
    en = [[random.randrange(0, MAX_VAL) for _ in range(SAMPLE_NUM)]]
)
async def test_vec_en(dut, en):
    port = GpioPortIntercon(dut)
    await port.reset()

    await FallingEdge(dut.clock)

    for e in en:
        port.set_en(e)

        await FallingEdge(dut.clock)

        assert port.get_en_vec() == (e & port.GPIO_MASK)

    await Timer(1, unit="us")
