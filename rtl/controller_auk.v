module core_top #(
    // Clock frequency in hertz.
    parameter CLK_HZ = 27000000,
    parameter BIT_RATE =   9600,
    parameter PAYLOAD_BITS = 8
) (
    input wire clk, // Top level system clock input.
    input wire serial_rx, // UART Recieve pin.
    output wire serial_tx, // UART transmit pin.
    output wire led_n0,
    output wire led_n1,
    output wire led_n2,
    output wire led_n3,
    output wire led_n4,
    output wire led_n5,
    input wire switch_n0,
    input wire switch_n1,
    input wire switch_n2,
    input wire switch_n3,
    input wire switch_n4,
    input wire switch_n5 // Sistema temporario, futuramente tais pinos podem ser simulados pela serial
);

wire [2:0] leds;
wire [5:0]switch;

assign led_n0 = leds[0];
assign led_n1 = leds[1];
assign led_n2 = leds[2];

assign switch[0] = switch_n0;
assign switch[1] = switch_n1;
assign switch[2] = switch_n2;
assign switch[3] = switch_n3;
assign switch[4] = switch_n4;
assign switch[5] = switch_n5;


wire [PAYLOAD_BITS-1:0]  uart_rx_data, uart_tx_data;
wire uart_rx_valid, uart_rx_break, uart_tx_busy, uart_tx_en;
wire tx_module, tx_soc, rx_soc, clk_soc;

reg [PAYLOAD_BITS-1:0] uart_data;
reg [7:0] counter;
reg led, reset, output_sel, input_sel, clk_enable;

initial begin
    counter = 8'b0;
    reset = 1'b0;
    output_sel = 1'b0;
    led = 1'b1;
    input_sel = 1'b0;
    clk_enable = 1'b1;
    uart_data = 8'b11111111;
end

assign serial_tx = (output_sel == 1'b1) ? tx_module : tx_soc;
assign rx_soc = (input_sel == 1'b0) ? serial_rx : 1'b0;
assign clk_soc = (clk_enable == 1'b1) ? clk : 1'b0;
assign uart_tx_data = uart_rx_data;
assign uart_tx_en   = uart_rx_valid;
assign led_n3 = led;


always @(posedge clk ) begin
    if(counter < 50 && reset == 1) begin
        counter <= counter + 1;
    end else if (reset == 1 && counter >= 50) begin
        reset <= 0;
        led <= 1;
    end
    
    if(uart_rx_valid == 1'b1 && uart_data != uart_rx_data) begin
        uart_data <= uart_rx_data;

        case (uart_rx_data)
            8'b00000000 : begin // disable soc clock
                clk_enable <= 1'b0;
            end
            8'b00000001 : begin // enable soc clock
                clk_enable <= 1'b1;
            end
            8'b00000010 : begin // enable reset over 50 clocks cycles
                led <= 0;
                reset <= 1;
                counter <= 0;
            end
            8'b00000011 : begin // disable reset
                led <= 1;
                reset <= 0;
            end
            8'b00000100 : begin // change tx to soc
                output_sel <= 1'b0;
            end
            8'b00000101 : begin // change tx to controler
                output_sel <= 1'b1;
            end
            8'b00000110 : begin // enable rx to soc
                input_sel <= 1'b0;
            end
            8'b00000111 : begin // disable rx to soc
                input_sel <= 1'b1;
            end
            default: begin

            end
        endcase
    end
end

// ------------------------------------------------------------------------- 

//
// UART RX
uart_tool_rx #(
    .BIT_RATE(BIT_RATE),
    .PAYLOAD_BITS(PAYLOAD_BITS),
    .CLK_HZ  (CLK_HZ  )
) i_uart_rx(
    .clk          (clk          ), // Top level system clock input.
    .resetn       (1            ), // Asynchronous active low reset.
    .uart_rxd     (serial_rx    ), // UART Recieve pin.
    .uart_rx_en   (1'b1         ), // Recieve enable
    .uart_rx_break(uart_rx_break), // Did we get a BREAK message?
    .uart_rx_valid(uart_rx_valid), // Valid data recieved and available.
    .uart_rx_data (uart_rx_data )  // The recieved data.
);

//
// UART Transmitter module.
//
uart_tool_tx #(
    .BIT_RATE(BIT_RATE),
    .PAYLOAD_BITS(PAYLOAD_BITS),
    .CLK_HZ  (CLK_HZ  )
) i_uart_tx(
    .clk          (clk          ),
    .resetn       (1            ),
    .uart_txd     (tx_module    ), // serial_tx
    .uart_tx_en   (uart_tx_en   ),
    .uart_tx_busy (uart_tx_busy ),
    .uart_tx_data (uart_tx_data ) 
);

// parte do soc,
// pinos disponiveis, rx_soc, tx_soc, reset, clk_soc

aukv_eggs_soc DUT0(
	.i_clk(clk),
	.i_rstn(reset),
	.i_rx(rx_soc),
	.o_tx(tx_soc),
	.o_led(leds),
	.i_switch(switch)
);


endmodule