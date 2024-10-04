
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf Risco-5'
                sh 'git clone --recursive https://github.com/JN513/Risco-5.git Risco-5'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("Risco-5") {
                    sh "iverilog -o simulation.out -g2005 -s soc_tb  src/core/alu.v src/core/alu_control.v src/core/control_unit.v src/core/core.v src/core/csr_unit.v src/core/immediate_generator.v src/core/mdu.v src/core/mux.v src/core/pc.v src/core/registers.v tests/soc_test.v src/peripheral/bus.v src/peripheral/fifo.v src/peripheral/gpios.v src/peripheral/gpio.v src/peripheral/leds.v src/peripheral/memory.v src/peripheral/pwm.v src/peripheral/soc.v src/peripheral/uart_rx.v src/peripheral/uart_tx.v src/peripheral/uart.v && vvp simulation.out"
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("Risco-5") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p Risco-5 -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("Risco-5") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p Risco-5 -b digilent_nexys4_ddr'
                            }
                        }
                    }
                }
            }
        }

        stage('Run Tests') {
            parallel {
                stage('colorlight_i9 Tests') {
                    steps {
                        echo 'Executando testes para FPGA colorlight_i9.'
                        unlock(resource: 'colorlight_i9')
                    }
                }
                stage('digilent_nexys4_ddr Tests') {
                    steps {
                        echo 'Executando testes para FPGA digilent_nexys4_ddr.'
                        unlock(resource: 'digilent_nexys4_ddr')
                    }
                }
            }
        }
    }
    post {
        always {
            dir("Risco-5") {
                sh 'rm -rf *'
            }
        }
    }
}
