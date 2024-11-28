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

    // SPI control pins
    input wire rw,
    output wire intr
    `endif
);

// Sinais intermediários
wire clk_core, reset_core;
wire [31:0] core_read_data, core_write_data, address;
wire [31:0] data_address, data_read, data_write;
wire memory_req, memory_rw;

// Instância do controlador
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
    
    // Main memory - instruction memory
    .core_memory_response  (),
    .core_read_memory      (1'b1), // Ler memória de instruções
    .core_write_memory     (1'b0),        // Não escreve instruções
    .core_address_memory   (address),
    .core_write_data_memory(32'h00000000),
    .core_read_data_memory (core_read_data),

    // Sync main memory bus
    .core_read_data_memory_sync     (),
    .core_memory_read_response_sync (),
    .core_memory_write_response_sync(),


    // Memória de dados
    .core_memory_response_data  (),
    .core_read_memory_data      (memory_req & ~memory_rw),
    .core_write_memory_data     (memory_req & memory_rw),
    .core_address_memory_data   (data_address),
    .core_write_data_memory_data(data_write),
    .core_read_data_memory_data (data_read)
);

// Instância do tinyriscv
tinyriscv u_tinyriscv (
    .clk(clk_core),
    .rst(reset_core),

    // Barramento de memória de dados
    .rib_ex_addr_o(data_address),       // Endereço de dados
    .rib_ex_data_i(data_read),          // Dados lidos
    .rib_ex_data_o(data_write),         // Dados a escrever
    .rib_ex_req_o(memory_req),         // Sinal de leitura
    .rib_ex_we_o(memory_rw),         // Sinal de escrita

    // Barramento de memória de instruções
    .rib_pc_addr_o(address),            // Endereço de instruções
    .rib_pc_data_i(core_read_data),     // Instrução lida

    // Sinais JTAG (não utilizados aqui)
    .jtag_reg_addr_i(5'b0),
    .jtag_reg_data_i(32'b0),
    .jtag_reg_we_i(1'b0),
    .jtag_reg_data_o(),

    .rib_hold_flag_i(1'b0),
    .jtag_halt_flag_i(1'b0),
    .jtag_reset_flag_i(1'b0),

    // Interrupções
    .int_i(32'b0)
);
// Clock infrastructure

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

// Reset infrastructure

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
