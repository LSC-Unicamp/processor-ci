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

wire clk_core, reset_core,
    memory_read, memory_write;

wire [31:0] core_read_data, core_write_data, address,
    data_address, data_read, data_write;

// Instância do tinyriscv
wire [31:0] m0_addr_i, m0_data_i, m0_data_o;
wire m0_req_i, m0_we_i;
wire [31:0] m1_addr_i, m1_data_o;
wire rib_hold_flag_o;
wire int_flag = 1'b0; // Sinal de interrupção fixo em 0
wire jtag_reg_addr_o = 1'b0; // Ignorando sinais JTAG
wire jtag_reg_data_o = 1'b0;
wire jtag_reg_we_o = 1'b0;
wire jtag_reg_data_i;
wire jtag_halt_req_o = 1'b0;
wire jtag_reset_req_o = 1'b0;

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
    .core_read_memory      (1'b1),
    .core_write_memory     (1'b0),
    .core_address_memory   (m1_addr_i),
    .core_write_data_memory(32'h00000000),
    .core_read_data_memory (m1_data_o),

    // Sync main memory bus
    .core_read_data_memory_sync     (),
    .core_memory_read_response_sync (),
    .core_memory_write_response_sync(),

    // Data memory
    .core_memory_response_data  (),
    .core_read_memory_data      (m0_req_i & ~m0_we_i),
    .core_write_memory_data     (m0_req_i & m0_we_i),
    .core_address_memory_data   (m0_addr_i),
    .core_write_data_memory_data(m0_data_i),
    .core_read_data_memory_data (m0_data_o)
);

// Instância do tinyriscv
tinyriscv u_tinyriscv (
    .clk(clk_core), // Conectando clk_core como clock do processador
    .rst(reset_core), // Conectando reset_core como reset do processador
    .rib_ex_addr_o(m0_addr_i),
    .rib_ex_data_i(m0_data_o),
    .rib_ex_data_o(m0_data_i),
    .rib_ex_req_o(m0_req_i),
    .rib_ex_we_o(m0_we_i),
    .rib_pc_addr_o(m1_addr_i),
    .rib_pc_data_i(m1_data_o),
    .jtag_reg_addr_i(jtag_reg_addr_o),
    .jtag_reg_data_i(jtag_reg_data_o),
    .jtag_reg_we_i(jtag_reg_we_o),
    .jtag_reg_data_o(jtag_reg_data_i),
    .rib_hold_flag_i(rib_hold_flag_o),
    .jtag_halt_flag_i(jtag_halt_req_o),
    .jtag_reset_flag_i(jtag_reset_req_o),
    .int_i(int_flag)
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
