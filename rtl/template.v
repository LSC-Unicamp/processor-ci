module top (
    `ifdef DIFERENCIAL_CLK
    input  wire clk_ref_p,
    input  wire clk_ref_n,
    `else
    input  wire clk,
    `endif

    input  wire reset,

    // UART pins
    input  wire rx,
    output wire tx,

    // SPI pins
    input wire sck,
    input wire cs,
    input wire mosi,
    output wire miso,

    //SPI control pins
    input wire rw,
    output wire intr,

    output wire [7:0]led
);

wire clk_core, reset_core, reset_o,
    memory_read, memory_write;

wire [31:0] core_read_data, core_write_data, address,
    data_address, data_read, data_write;


Controller #(
    .CLK_FREQ(25000000),
    .BIT_RATE(115200),
    .PAYLOAD_BITS(8),
    .BUFFER_SIZE(8),
    .PULSE_CONTROL_BITS(32),
    .BUS_WIDTH(32),
    .WORD_SIZE_BY(4),
    .ID(32'h0000004A),
    .RESET_CLK_CYCLES(20),
    .MEMORY_FILE(""),
    .MEMORY_SIZE(4096)
) Controller(
    `ifdef HIGH_CLK
    .clk  (clk_o),
    `else
    .clk  (clk),
    `endif

    .reset(reset_o),

    .tx(tx),
    .rx(rx),

    .sck (sck),
    .cs  (cs),
    .mosi(mosi),
    .miso(miso),

    .rw  (rw),
    .intr(intr),

    .clk_core  (clk_core),
    .reset_core(reset_core),
    
    // main memory - instruction memory
    .core_memory_response  (),
    .core_read_memory      (memory_read),
    .core_write_memory     (1'b0),
    .core_address_memory   (address),
    .core_write_data_memory(32'h00000000),
    .core_read_data_memory (1'b1)

    //sync main memory bus
    .core_read_data_memory_sync     (),
    .core_memory_read_response_sync (),
    .core_memory_write_response_sync(),

    // Data memory
    .core_memory_response_data  (),
    .core_read_memory_data      (memory_read),
    .core_write_memory_data     (memory_write),
    .core_address_memory_data   (data_address),
    .core_write_data_memory_data(data_write),
    .core_read_data_memory_data (data_read)
);


// Core space




// Clock inflaestructure

`ifdef HIGH_CLK

reg clk_o;

initial begin
    clk_o = 1'b0; // 50mhz or 100mhz
end

`ifdef DIFERENCIAL_CLK
wire clk_ref; // Sinal de clock single-ended

// Instância do buffer diferencial
IBUFDS #(
    .DIFF_TERM("FALSE"),     // Habilita ou desabilita o terminador diferencial
    .IBUF_LOW_PWR("TRUE"),   // Ativa o modo de baixa potência
    .IOSTANDARD("DIFF_SSTL15")
) ibufds_inst (
    .O(clk_ref),    // Clock single-ended de saída
    .I(clk_ref_p),  // Entrada diferencial positiva
    .IB(clk_ref_n)  // Entrada diferencial negativa
);


always @(posedge clk_ref) begin
    clk_o = ~clk_o;
end
`else
always @(posedge clk) begin
    clk_o = ~clk_o;
end
`endif

`endif

// Reset Inflaestructure

wire reset_o;

ResetBootSystem #(
    .CYCLES(20)
) ResetBootSystem(
    `ifdef HIGH_CLK
    .clk    (clk_o),
    `else
    .clk    (clk),
    `endif
    
    .reset_o(reset_o)
);
    
endmodule
