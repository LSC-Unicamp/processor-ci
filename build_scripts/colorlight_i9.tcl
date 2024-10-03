read_verilog /eda/processorci-controller/src/fifo.v
read_verilog /eda/processorci-controller/src/reset.v
read_verilog /eda/processorci-controller/src/clk_divider.v
read_verilog /eda/processorci-controller/src/memory.v
read_verilog /eda/processorci-controller/src/interpreter.v
read_verilog /eda/processorci-controller/src/controller.v

synth_ecp5 -json out.json -abc9