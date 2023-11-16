module top (
    input wire clk27,
    input wire serial_rx,
    output wire serial_tx,
    output wire led_n1
);
    
core_top #(
    .CLK_HZ(27000000),
    .BIT_RATE(9600),
    .PAYLOAD_BITS(8)
) core (
    .clk(clk27),
    .serial_rx(serial_rx),
    .serial_tx(serial_tx),
    .led_n1(led_n1)
);

endmodule
