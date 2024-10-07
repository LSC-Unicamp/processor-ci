set_device -name GW2AR-18C GW2AR-LV18QN88C8/I7

add_file /eda/processor-ci/constraints/gowin_tangnano_20k.cst
add_file /eda/processor-ci/constraints/gowin_tangnano_20k.sdc

add_file /eda/processor-ci-controller/modules/uart.v
add_file /eda/processor-ci-controller/modules/UART/rtl/uart_rx.v
add_file /eda/processor-ci-controller/modules/UART/rtl/uart_tx.v
add_file /eda/processor-ci-controller/src/fifo.v
add_file /eda/processor-ci-controller/src/reset.v
add_file /eda/processor-ci-controller/src/clk_divider.v
add_file /eda/processor-ci-controller/src/memory.v
add_file /eda/processor-ci-controller/src/interpreter.v
add_file /eda/processor-ci-controller/src/controller.v

set_option -top_module processorci 

set_option -use_mspi_as_gpio 1
set_option -use_sspi_as_gpio 1
set_option -use_ready_as_gpio 1
set_option -use_done_as_gpio 1
set_option -rw_check_on_ram 1
run all