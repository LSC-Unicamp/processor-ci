module processorci_top (
    `ifdef DIFERENCIAL_CLK
    input  wire clk_ref_p,
    input  wire clk_ref_n,
    `else
    input  wire clk,
    `endif

    input  wire reset,

    // UART pins
    input  wire rx,
    output wire tx
    `ifndef DIFERENCIAL_CLK
    ,

    // SPI pins
    input wire sck,
    input wire cs,
    input wire mosi,
    output wire miso,

    //SPI control pins
    input wire rw,
    output wire intr
    `endif
);

wire clk_core, reset_core, reset_o;

wire [31:0] instruction_address, instruction_data;
wire [31:0] data_address, data_write_data, data_read_data;
wire data_read, data_write, instruction_response, data_memory_response;

Controller #(
    .CLK_FREQ          (`CLOCK_FREQ),
    .BIT_RATE          (115200),
    .PAYLOAD_BITS      (8),
    .BUFFER_SIZE       (8),
    .PULSE_CONTROL_BITS(32),
    .BUS_WIDTH         (32),
    .WORD_SIZE_BY      (4),
    .ID                (0),
    .RESET_CLK_CYCLES  (20),
    .MEMORY_FILE       (""),
    .MEMORY_SIZE       (`MEMORY_SIZE)
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
    .core_memory_response  (instruction_response), // Memory response signal, 1 means that the memory operation is done
    .core_read_memory      (1'b1),                 // Read memory signal
    .core_write_memory     (1'b0),                 // Write memory signal
    .core_address_memory   (instruction_address),  // Address to read or write
    .core_write_data_memory(32'h00000000),         // Data to write
    .core_read_data_memory (instruction_data),     // Data read from memory

    // Data memory
    .core_memory_response_data  (data_memory_response), // Memory response signal, 1 means that the memory operation is done
    .core_read_memory_data      (data_read),            // Read memory signal
    .core_write_memory_data     (data_write),           // Write memory signal
    .core_address_memory_data   (data_address),         // Address to read or write
    .core_write_data_memory_data(data_write_data),      // Data to write
    .core_read_data_memory_data (data_read_data)        // Data read from memory
);


// Core space

Grande_Risco5 Core(
    .clk  (clk_core),
    .reset(reset_core),

    .instruction_response(instruction_response),
    .instruction_address (instruction_address),
    .instruction_data    (instruction_data),

    .data_memory_response(data_memory_response),
    .data_address        (data_address),
    .data_memory_read    (data_read),
    .data_memory_write   (data_write),
    .write_data          (data_write_data),
    .read_data           (data_read_data)
);

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
