
set ID 0x6a6a6a6a
set CLOCK_FREQ 100000000

read_verilog /eda/processor-ci-controller/modules/uart.v
read_verilog /eda/processor-ci-controller/modules/UART/rtl/uart_rx.v
read_verilog /eda/processor-ci-controller/modules/UART/rtl/uart_tx.v
read_verilog /eda/processor-ci-controller/src/fifo.v
read_verilog /eda/processor-ci-controller/src/reset.v
read_verilog /eda/processor-ci-controller/src/clk_divider.v
read_verilog /eda/processor-ci-controller/src/memory.v
read_verilog /eda/processor-ci-controller/src/interpreter.v
read_verilog /eda/processor-ci-controller/src/controller.v

set ID [lindex $argv 0]
set CLOCK_FREQ [lindex $argv 1]
set MEMORY_SIZE [lindex $argv 2]

read_xdc "/eda/processor-ci/constraints/xilinx_vc709.xdc"
set_property PROCESSING_ORDER EARLY [get_files /eda/processor-ci/constraints/xilinx_vc709.xdc]

# synth
synth_design -top "top" -part "xc7vx690tffg1761-2" -verilog_define $ID -verilog_define $CLOCK_FREQ -verilog_define $MEMORY_SIZE

# place and route
opt_design
place_design

report_utilization -hierarchical -file virtex_utilization_hierarchical_place.rpt
report_utilization -file virtex_utilization_place.rpt
report_io -file virtex_io.rpt
report_control_sets -verbose -file virtex_control_sets.rpt
report_clock_utilization -file virtex_clock_utilization.rpt

route_design

report_timing_summary -no_header -no_detailed_paths
report_route_status -file virtex_route_status.rpt
report_drc -file virtex_drc.rpt
report_timing_summary -datasheet -max_paths 10 -file virtex_timing.rpt
report_power -file virtex_power.rpt

# write bitstream
write_bitstream -force "xilinx_vc709.bit"

exit