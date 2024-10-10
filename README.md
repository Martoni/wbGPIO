# wbGPIO
Wishbone slave General purpose Input Output written in Chisel

Clone :
```bash
git clone https://github.com/Martoni/wbGPIO.git
```

## Generate verilog

Dependencies:
- [WbPlumbing](https://github.com/Martoni/WbPlumbing)

## Test with cocotb

Dependencies:
- [cocotbext-wishbone](https://github.com/wallento/cocotbext-wishbone) is required to test the module with cocotb

To test with cocotb:
```bash
cd cocotb/gpio
make
```

