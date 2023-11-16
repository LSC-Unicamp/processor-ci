module top (
    input wire clk25,
    input wire serial_rx,
    output wire serial_tx,
    output wire led_n1
);
    
core_top #(
    .CLK_HZ(25000000),
    .BIT_RATE(9600),
    .PAYLOAD_BITS(8)
) core (
    .clk(clk25),
    .serial_rx(serial_rx),
    .serial_tx(serial_tx),
    .led_n1(led_n1),
);

endmodule
