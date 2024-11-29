
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf F03x'
                sh 'git clone --recursive --depth=1 https://github.com/klessydra/F03x F03x'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("F03x") {
                    sh "ghdl -a --std=08               klessydra-f0-3th/PKG_RiscV_Klessydra_thread_parameters.vhd klessydra-f0-3th/PKG_RiscV_Klessydra.vhd klessydra-f0-3th/TMR_REG_PKG.vhd klessydra-f0-3th/CMP-TMR_REG.vhd klessydra-f0-3th/RTL-CSR_Unit_TMR.vhd klessydra-f0-3th/RTL-Debug_Unit.vhd klessydra-f0-3th/RTL-Processing_Pipeline_TMR.vhd klessydra-f0-3th/RTL-Program_Counter_unit_TMR.vhd klessydra-f0-3th/STR-Klessydra_top.vhd "
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
                                dir("F03x") {
                                    echo 'Starting synthesis for FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p F03x -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("F03x") {
                                    echo 'Flashing FPGA colorlight_i9.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p F03x -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Test colorlight_i9') {
                            steps {
                                echo 'Testing FPGA colorlight_i9.'
                                dir("F03x") {
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
                                dir("F03x") {
                                    echo 'Starting synthesis for FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p F03x -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("F03x") {
                                    echo 'Flashing FPGA digilent_nexys4_ddr.'
                                sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json \
                                            -p F03x -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Test digilent_nexys4_ddr') {
                            steps {
                                echo 'Testing FPGA digilent_nexys4_ddr.'
                                dir("F03x") {
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
