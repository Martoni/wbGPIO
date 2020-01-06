# wbGPIO
Wishbone slave General purpose Input Output written in Chisel

Clone with submodule :
```bash 
git clone --recurse-submodules https://github.com/Martoni/wbGPIO.git
```

## Generate verilog

Dependencies:
- [WbPlumbing](https://github.com/Martoni/WbPlumbing)

## Test with cocotb

Dependencies:
- [cocomod-wishbone](https://github.com/wallento/cocomod-wishbone) is required to test the module with cocotb

To test with cocotb:
```bash
cd cocotb/gpio
make
```

