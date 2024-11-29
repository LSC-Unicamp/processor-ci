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

// Definição de fios
wire [31:0] instr_data, data_read, data_write;
wire [31:0] address_instr, address_data;
wire        instr_req, instr_ack;
wire        data_req, data_ack;
wire [3:0]  data_mask;
wire        data_wr_en, rw;
wire        core_memory_response, core_read_memory, core_write_memory;
wire        core_memory_response_data, core_read_memory_data, core_write_memory_data;



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
    // Instruções
    .core_memory_response  (instr_ack),
    .core_read_memory      (instr_req),
    .core_write_memory     (1'b0),
    .core_address_memory   (address_instr),
    .core_write_data_memory(32'h00000000),
    .core_read_data_memory (instr_data),

    // Dados
    .core_memory_response_data  (data_ack),
    .core_read_memory_data      (data_req & ~data_wr_en),
    .core_write_memory_data     (data_req & data_wr_en),
    .core_address_memory_data   (address_data),
    .core_write_data_memory_data(data_write),
    .core_read_data_memory_data (data_read)
);


// Core space

// Instância do processador kronos_core
kronos_core #(
    .BOOT_ADDR            (32'h00000000),
    .FAST_BRANCH          (1'b1),
    .EN_COUNTERS          (1'b1),
    .EN_COUNTERS64B       (1'b1),
    .CATCH_ILLEGAL_INSTR  (1'b1),
    .CATCH_MISALIGNED_JMP (1'b1),
    .CATCH_MISALIGNED_LDST(1'b1)
) kronos_core_inst (
    .clk            (clk_core),
    .rstz           (~reset_core),

    // Interface de instruções
    .instr_addr     (address_instr),
    .instr_data     (instr_data),
    .instr_req      (instr_req),
    .instr_ack      (instr_ack),

    // Interface de dados
    .data_addr      (address_data),
    .data_rd_data   (data_read),
    .data_wr_data   (data_write),
    .data_mask      (data_mask),
    .data_wr_en     (data_wr_en),
    .data_req       (data_req),
    .data_ack       (data_ack),

    // Interrupções
    .software_interrupt(1'b0),
    .timer_interrupt   (1'b0),
    .external_interrupt(1'b0)
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
