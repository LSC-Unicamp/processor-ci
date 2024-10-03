
read_verilog /eda/processor-ci-controller/modules/uart.v
read_verilog /eda/processor-ci-controller/modules/UART/rtl/uart_rx.v
read_verilog /eda/processor-ci-controller/modules/UART/rtl/uart_tx.v

read_verilog /eda/processor-ci-controller/modules/spi.v;
read_verilog /eda/processor-ci-controller/modules/SPI-Slave/rtl/spi_slave.v;

read_verilog /eda/processor-ci-controller/src/fifo.v
read_verilog /eda/processor-ci-controller/src/reset.v
read_verilog /eda/processor-ci-controller/src/clk_divider.v
read_verilog /eda/processor-ci-controller/src/memory.v
read_verilog /eda/processor-ci-controller/src/interpreter.v
read_verilog /eda/processor-ci-controller/src/controller.v

read_xdc "/eda/processor-ci/constraints/digilent_arty_a7_100t.xdc"

# synth
synth_design -top "top" -part "xc7a100tcsg324-1"

# place and route
opt_design
place_design

report_utilization -hierarchical -file digilent_arty_a7_utilization_hierarchical_place.rpt
report_utilization -file digilent_arty_a7_utilization_place.rpt
report_io -file digilent_arty_a7_io.rpt
report_control_sets -verbose -file digilent_arty_a7_control_sets.rpt
report_clock_utilization -file digilent_arty_a7_clock_utilization.rpt

route_design

report_timing_summary -no_header -no_detailed_paths
report_route_status -file digilent_arty_a7_route_status.rpt
report_drc -file digilent_arty_a7_drc.rpt
report_timing_summary -datasheet -max_paths 10 -file digilent_arty_a7_timing.rpt
report_power -file digilent_arty_a7_power.rpt

# write bitstream
write_bitstream -force "out.bit"

exit