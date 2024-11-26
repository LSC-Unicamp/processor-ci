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

wire o_data_mem_en;        // Sinal de habilitação de leitura da memória de dados
wire o_data_mem_we;        // Sinal de habilitação de escrita da memória de dados
wire [31:0] o_data_mem_addr; // Endereço da memória de dados
wire [31:0] o_data_mem_data; // Dados a serem escritos na memória de dados
wire [31:0] i_data_mem_data; // Dados lidos da memória de dados
wire i_data_mem_valid;       // Sinal indicando que a memória de dados está pronta


wire o_code_mem_en;        // Sinal de habilitação de leitura da memória de instruções
wire [31:0] o_code_mem_addr; // Endereço da memória de instruções
wire [31:0] i_code_mem_data; // Dados lidos da memória de instruções
wire i_code_mem_valid;       // Sinal indicando que a memória de instruções está pronta



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
    
    // Código de interligação entre Controller e aukv
    .core_memory_response  (i_code_mem_valid),        // Resposta de memória de instruções
    .core_read_memory      (o_code_mem_en),          // Habilitação de leitura de instruções
    .core_write_memory     (1'b0),                   // Nenhuma escrita de instruções (fixo)
    .core_address_memory   (o_code_mem_addr),        // Endereço de memória de instruções
    .core_write_data_memory(32'h00000000),           // Sem escrita
    .core_read_data_memory (i_code_mem_data),        // Dados lidos da memória de instruções

    //sync memory bus (não utilizado)
    .core_read_data_memory_sync     (),
    .core_memory_read_response_sync (),
    .core_memory_write_response_sync(),

    // Data memory
    .core_memory_response_data  (i_data_mem_valid),  // Resposta de dados de memória
    .core_read_memory_data      (o_data_mem_en),     // Habilitação de leitura de memória de dados
    .core_write_memory_data     (o_data_mem_we),     // Habilitação de escrita de memória de dados
    .core_address_memory_data   (o_data_mem_addr),   // Endereço de memória de dados
    .core_write_data_memory_data(o_data_mem_data),   // Dados a serem escritos
    .core_read_data_memory_data (i_data_mem_data)    // Dados lidos da memória de dados
);

aukv aukv_inst(
    .i_clk          (clk_core),
    .i_rstn         (~reset_core),       // Reset ativo baixo
    .i_irq          (1'b0),              // IRQ fixo como inativo
    .o_ack          (),                  // Sem interligação de ACK

    // Sinais de memória de dados
    .o_data_mem_en      (o_data_mem_en),
    .o_data_mem_we      (o_data_mem_we),
    .o_data_mem_addr    (o_data_mem_addr),
    .o_data_mem_data    (o_data_mem_data),
    .o_data_mem_strobe  (),              // Sem strobe
    .i_data_mem_valid   (i_data_mem_valid),
    .i_data_mem_data    (i_data_mem_data),

    // Sinais de memória de instruções
    .o_code_mem_en      (o_code_mem_en),
    .o_code_mem_addr    (o_code_mem_addr),
    .i_code_mem_data    (i_code_mem_data),
    .i_code_mem_valid   (i_code_mem_valid)
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
