
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf Tethorax'
                sh 'git clone --recursive https://github.com/NikosDelijohn/Tethorax Tethorax'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("Tethorax") {
                    sh "ghdl -a --std=08   PIPELINE.vhd RV32I.vhd TOOLBOX.vhd PIPELINE Components/EXE.vhd PIPELINE Components/INSTRUCTION_DECODE.vhd PIPELINE Components/INSTRUCTION_FETCH.vhd PIPELINE Components/MEMORY.vhd PIPELINE Components/PC_REGISTER.vhd PIPELINE Components/PIPE_EXE_TO_MEM_REGISTER.vhd PIPELINE Components/PIPE_ID_TO_EXE_REGISTER.vhd PIPELINE Components/PIPE_IF_TO_ID_REGISTER.vhd PIPELINE Components/PIPE_MEM_TO_WB_REGISTER.vhd PIPELINE Components/WRITE_BACK.vhd TOOLBOX Components/ADDER_2B.vhd TOOLBOX Components/ADDER_2B_MSB.vhd TOOLBOX Components/BARREL_CELL.vhd TOOLBOX Components/BARREL_SHIFTER.vhd TOOLBOX Components/CONTROL_WORD_REGROUP.vhd TOOLBOX Components/DEC5X32.vhd TOOLBOX Components/DECODE_TO_EXECUTE.vhd TOOLBOX Components/EXE_ADDER_SUBBER.vhd TOOLBOX Components/EXE_ADDER_SUBBER_CELL.vhd TOOLBOX Components/EXE_ADDER_SUBBER_CELL_MSB.vhd TOOLBOX Components/EXE_BRANCH_RESOLVE.vhd TOOLBOX Components/EXE_LOGIC_MODULE.vhd TOOLBOX Components/EXE_SLT_MODULE.vhd TOOLBOX Components/ID_ADDER.vhd TOOLBOX Components/ID_DECODER.vhd TOOLBOX Components/ID_IMM_GENERATOR.vhd TOOLBOX Components/IF_INSTRMEM.vhd TOOLBOX Components/MEM_DATAMEM.vhd TOOLBOX Components/MEM_LOADS_MASKING.vhd TOOLBOX Components/MEM_STORE_BYTEEN.vhd TOOLBOX Components/MEM_TO_WB.vhd TOOLBOX Components/MUX2X1.vhd TOOLBOX Components/MUX2X1_BIT.vhd TOOLBOX Components/MUX32X1.vhd TOOLBOX Components/MUX4X1.vhd TOOLBOX Components/MUX8X1.vhd TOOLBOX Components/PC_PLUS_4.vhd TOOLBOX Components/REGISTER_FILE.vhd TOOLBOX Components/REG_32B_CASUAL.vhd TOOLBOX Components/REG_32B_ZERO.vhd TOOLBOX Components/STALL_FWD_PREDICT.vhd "
                }
            }
        }
        
        stage('FPGA Build Pipeline') {
            parallel {
                
                stage('colorlight_i9') {
                    options {
                        lock(resource: 'colorlight_i9')
                    }
                    stages {
                        stage('Síntese e PnR') {
                            steps {
                                dir("Tethorax") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Tethorax -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("Tethorax") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Tethorax -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("Tethorax") {
                                    // Insira aqui os comandos de teste necessários
                                }
                            }
                        }
                    }
                }
                
                stage('digilent_nexys4_ddr') {
                    options {
                        lock(resource: 'digilent_nexys4_ddr')
                    }
                    stages {
                        stage('Síntese e PnR') {
                            steps {
                                dir("Tethorax") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Tethorax -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("Tethorax") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Tethorax -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("Tethorax") {
                                    // Insira aqui os comandos de teste necessários
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            dir("Tethorax") {
                sh 'rm -rf *'
            }
        }
    }
}