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

wire clk_core, reset_core, reset_o,
    memory_read, memory_write;

wire [31:0] core_read_data, core_write_data, address,
    data_address, data_read, data_write;


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
    .core_memory_response  (),
    .core_read_memory      (1'b1),
    .core_write_memory     (1'b0),
    .core_address_memory   (address),
    .core_write_data_memory(32'h00000000),
    .core_read_data_memory (),

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

riscv_core
u_dut
//-----------------------------------------------------------------
// Ports
//-----------------------------------------------------------------
(
    // Inputs
     .clk_i(clk_core)
    ,.rst_i(reset_core)
    ,.mem_d_data_rd_i(data_read)
    ,.mem_d_accept_i(1'b1)
    ,.mem_d_ack_i(1'b1)
    ,.mem_d_error_i(1'b0)
    ,.mem_d_resp_tag_i()
    ,.mem_i_accept_i(1'b1)
    ,.mem_i_valid_i(1'b1)
    ,.mem_i_error_i(1'b0)
    ,.mem_i_inst_i(core_read_data)
    ,.intr_i(1'b0)
    ,.reset_vector_i(32'h80000000)
    ,.cpu_id_i('b0)

    // Outputs
    ,.mem_d_addr_o(data_address)
    ,.mem_d_data_wr_o(data_write)
    ,.mem_d_rd_o(data_read)
    ,.mem_d_wr_o(data_write)
    ,.mem_d_cacheable_o()
    ,.mem_d_req_tag_o()
    ,.mem_d_invalidate_o()
    ,.mem_d_writeback_o()
    ,.mem_d_flush_o()
    ,.mem_i_rd_o()
    ,.mem_i_flush_o()
    ,.mem_i_invalidate_o()
    ,.mem_i_pc_o(address)
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
