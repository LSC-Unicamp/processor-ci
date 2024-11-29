
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf riskow'
                sh 'git clone --recursive --depth=1 https://github.com/racerxdl/riskow riskow'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("riskow") {
                    sh "/eda/oss-cad-suite/bin/iverilog -o simulation.out -g2005                  -s CPU  cpu/alu.v cpu/comp.v cpu/cpu.v cpu/instruction_decoder.v cpu/program_counter.v cpu/register_bank.v "
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
                        stage('Synthesis and PnR') {
                            steps {
                                dir("riskow") {
                                    echo 'Starting synthesis for FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p riskow -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("riskow") {
                                    echo 'Flashing FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p riskow -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Test colorlight_i9') {
                            steps {
                                echo 'Testing FPGA colorlight_i9.'
                                dir("riskow") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT="/dev/ttyACM0" \
                                    python /eda/processor-ci-communication/run_tests.py'
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
                        stage('Synthesis and PnR') {
                            steps {
                                dir("riskow") {
                                    echo 'Starting synthesis for FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p riskow -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("riskow") {
                                    echo 'Flashing FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p riskow -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Test digilent_nexys4_ddr') {
                            steps {
                                echo 'Testing FPGA digilent_nexys4_ddr.'
                                dir("riskow") {
                                    sh 'PYTHONPATH=/eda/processor-ci-communication PORT="/dev/ttyUSB1" \
                                    python /eda/processor-ci-communication/run_tests.py'
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
