
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf Risco-5'
                sh 'git clone --recursive https://github.com/JN513/Risco-5.git Risco-5'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("Risco-5") {
                    sh "iverilog -o simulation.out -g2005  -s soc_tb  src/core/alu.v src/core/alu_control.v src/core/control_unit.v src/core/core.v src/core/csr_unit.v src/core/immediate_generator.v src/core/mdu.v src/core/mux.v src/core/pc.v src/core/registers.v tests/soc_test.v src/peripheral/bus.v src/peripheral/fifo.v src/peripheral/gpios.v src/peripheral/gpio.v src/peripheral/leds.v src/peripheral/memory.v src/peripheral/pwm.v src/peripheral/soc.v src/peripheral/uart_rx.v src/peripheral/uart_tx.v src/peripheral/uart.v"
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
                                dir("Risco-5") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Risco-5 -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("Risco-5") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Risco-5 -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("Risco-5") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT=/dev/ttyACM0 python /eda/processor-ci-communication/run_tests.py' 
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
                                dir("Risco-5") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Risco-5 -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("Risco-5") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Risco-5 -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("Risco-5") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT=/dev/ttyUSB1 python /eda/processor-ci-communication/run_tests.py' 
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
            junit '**/test-reports/*.xml'
        }
    }
}
