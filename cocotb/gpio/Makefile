###############################################################################
# Copyright (c) 2013 Potential Ventures Ltd
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of Potential Ventures Ltd,
#       SolarFlare Communications Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL POTENTIAL VENTURES LTD BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
# Makefile copied from cocotb example:
# https://github.com/cocotb/cocotb/blob/master/examples/ping_tun_tap/tests/Makefile

TOPLEVEL_LANG ?= verilog
SIM?=icarus

ifeq ($(SIM),verilator)
EXTRA_ARGS += --trace --trace-structs
endif

ifneq ($(TOPLEVEL_LANG),verilog)

all:
	@echo "Skipping example due to TOPLEVEL_LANG=$(TOPLEVEL_LANG) not being verilog"

clean::

else

TOPLEVEL=WbGpio

ifeq ($(OS),Msys)
WPWD=$(shell sh -c 'pwd -W')
else
WPWD=$(shell pwd)
endif

PWD=$(shell pwd)

VERILOG_DIR=$(PWD)/verilog
VERILOG_SOURCES=$(VERILOG_DIR)/$(TOPLEVEL).sv
MODULE=test_wbgpio

include $(shell cocotb-config --makefiles)/Makefile.sim

endif

$(VERILOG_SOURCES): ../../src/main/scala/gpio/wbgpio.scala
	cd $(PWD)/../../;sbt "runMain gpio.WbGpio --target-dir "$(VERILOG_DIR)""

cleanverilog:
	-rm -rf $(VERILOG_DIR)

mrproper:
	-rm results.xml
	-rm dump.vcd
	-rm -rf $(VERILOG_DIR)
