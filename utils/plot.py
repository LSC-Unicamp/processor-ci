import matplotlib.pyplot as plt

# Dados fornecidos
dados = {
    'Risco_5': {'LUT4': 3152, 'Frequency': 54.5},
    'DarkRISCV': {'LUT4': 2291, 'Frequency': 56.8},
    'SERV': {'LUT4': 301, 'Frequency': 121.7},
    'RISCV Steel': {'LUT4': 6040, 'Frequency': 39.03},
    'Mriscv': {'LUT4': 2658, 'Frequency': 66.84},
    'TinyRiscv': {'LUT4': 3964, 'Frequency': 59.85},
    'riskow': {'LUT4': 1957, 'Frequency': 63.45},
    'riscado-v': {'LUT4': 2246, 'Frequency': 45.22},
}

dados_xilinx = {
    'Risco_5': {'LUT4': 2359, 'Frequency': 70.8},
    'DarkRISCV': {'LUT4': 1189, 'Frequency': 74.0},
    'SERV': {'LUT4': 125, 'Frequency': 147.3},
    'RISCV Steel': {'LUT4': 2006, 'Frequency': 50.7},
    'Mriscv': {'LUT4': 1766, 'Frequency': 86.8},
    'TinyRiscv': {'LUT4': 2570, 'Frequency': 77.8},
    'riskow': {'LUT4': 1399, 'Frequency': 82.48},
    'riscado-v': {'LUT4': 990, 'Frequency': 58.7},
}

# Preparar dados para a tecnologia Lattice ECP45F (original)
lut4_values_lattice = [dados[key]['LUT4'] for key in dados]
frequencia_values_lattice = [dados[key]['Frequency'] for key in dados]
labels = list(dados.keys())

# Preparar dados para a tecnologia Xilinx XC7A100T (ajustes de área e frequência)
lut4_values_xilinx = [dados_xilinx[key]['LUT4'] for key in dados_xilinx]
frequencia_values_xilinx = [
    dados_xilinx[key]['Frequency'] for key in dados_xilinx
]

# Criar gráfico de pontos
plt.figure(figsize=(10, 6))

# Plot para Lattice ECP45F com pontos maiores
plt.scatter(
    frequencia_values_lattice,
    lut4_values_lattice,
    color='blue',
    label='Lattice ECP45F',
    s=150,
)

# Plot para Xilinx XC7A100T com pontos maiores
plt.scatter(
    frequencia_values_xilinx,
    lut4_values_xilinx,
    color='red',
    label='Xilinx XC7A100T',
    s=150,
)

# Adicionar rótulos aos pontos para Lattice com fonte maior e centralizado
for i, label in enumerate(labels):
    plt.text(
        frequencia_values_lattice[i],
        lut4_values_lattice[i] + 100,
        label,
        fontsize=14,
        ha='center',
        va='bottom',
    )

# Adicionar rótulos aos pontos para Xilinx com fonte maior e centralizado
for i, label in enumerate(labels):
    plt.text(
        frequencia_values_xilinx[i],
        lut4_values_xilinx[i] + 100,
        label,
        fontsize=14,
        ha='center',
        va='bottom',
    )

# Adicionar títulos e rótulos aos eixos com fonte aumentada
plt.title(
    'Frequency vs. LUT for Lattice ECP45F and Xilinx XC7A100T', fontsize=16
)
plt.xlabel('Frequency (MHz)', fontsize=18)
plt.ylabel('LUT', fontsize=18)

# Aumentar o tamanho da fonte dos ticks dos eixos
plt.tick_params(axis='both', which='major', labelsize=16)

# Adicionar uma grade
plt.grid(True)

# Aumentar o tamanho da fonte da legenda
plt.legend(fontsize=16)

# Mostrar gráfico
plt.savefig('plot.png', format='png')
plt.show()
