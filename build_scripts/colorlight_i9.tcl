yosys read_verilog /eda/processor-ci-controller/modules/uart.v
yosys read_verilog /eda/processor-ci-controller/modules/UART/rtl/uart_rx.v
yosys read_verilog /eda/processor-ci-controller/modules/UART/rtl/uart_tx.v

yosys read_verilog /eda/processor-ci-controller/src/fifo.v
yosys read_verilog /eda/processor-ci-controller/src/reset.v
yosys read_verilog /eda/processor-ci-controller/src/clk_divider.v
yosys read_verilog /eda/processor-ci-controller/src/memory.v
yosys read_verilog /eda/processor-ci-controller/src/interpreter.v
yosys read_verilog /eda/processor-ci-controller/src/controller.v

yosys synth_ecp5 -json colorlight_i9.json -top processorci_top -abc9