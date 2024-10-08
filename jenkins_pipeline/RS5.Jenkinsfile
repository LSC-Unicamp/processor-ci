
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf RS5'
                sh 'git clone --recursive https://github.com/gaph-pucrs/RS5 RS5'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("RS5") {
                    sh "iverilog -o simulation.out -g2012  -s RS5 -I rtl/ rtl/CSRBank.sv rtl/RS5.sv rtl/aes_unit.sv rtl/align.sv rtl/decode.sv rtl/decompresser.sv rtl/div.sv rtl/execute.sv rtl/fetch.sv rtl/mmu.sv rtl/mul.sv rtl/mulNbits.sv rtl/regbank.sv rtl/retire.sv rtl/vectorALU.sv rtl/vectorCSRs.sv rtl/vectorLSU.sv rtl/vectorRegbank.sv rtl/vectorUnit.sv rtl/aes/riscv_crypto_aes_fwd_sbox.sv rtl/aes/riscv_crypto_aes_sbox.sv rtl/aes/riscv_crypto_sbox_aes_out.sv rtl/aes/riscv_crypto_sbox_aes_top.sv rtl/aes/riscv_crypto_sbox_inv_mid.sv "
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
                                dir("RS5") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p RS5 -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("RS5") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p RS5 -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("RS5") {
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
                                dir("RS5") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p RS5 -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("RS5") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p RS5 -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("RS5") {
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
            dir("RS5") {
                sh 'rm -rf *'
            }
        }
    }
}
