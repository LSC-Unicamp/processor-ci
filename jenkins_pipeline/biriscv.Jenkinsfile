
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf biriscv'
                sh 'git clone --recursive https://github.com/ultraembedded/biriscv biriscv'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("biriscv") {
                    sh "iverilog -o simulation.out -g2005  -s riscv_core -I src/core src/core/biriscv_alu.v src/core/biriscv_csr.v src/core/biriscv_csr_regfile.v src/core/biriscv_decode.v src/core/biriscv_decoder.v src/core/biriscv_defs.v src/core/biriscv_divider.v src/core/biriscv_exec.v src/core/biriscv_fetch.v src/core/biriscv_frontend.v src/core/biriscv_issue.v src/core/biriscv_lsu.v src/core/biriscv_mmu.v src/core/biriscv_multiplier.v src/core/biriscv_npc.v src/core/biriscv_pipe_ctrl.v src/core/biriscv_regfile.v src/core/biriscv_trace_sim.v src/core/biriscv_xilinx_2r1w.v src/core/riscv_core.v "
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
                                dir("biriscv") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p biriscv -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("biriscv") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p biriscv -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("biriscv") {
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
                                dir("biriscv") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p biriscv -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("biriscv") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p biriscv -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("biriscv") {
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
            dir("biriscv") {
                sh 'rm -rf *'
            }
        }
    }
}
