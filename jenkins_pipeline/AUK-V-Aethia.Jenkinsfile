
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf AUK-V-Aethia'
                sh 'git clone --recursive https://github.com/veeYceeY/AUK-V-Aethia AUK-V-Aethia'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("AUK-V-Aethia") {
                    sh "iverilog -o simulation.out -g2005  -s aukv  rtl/core/aukv.v rtl/core/aukv_alu.v rtl/core/aukv_csr_regfile.v rtl/core/aukv_decode.v rtl/core/aukv_execute.v rtl/core/aukv_fetch.v rtl/core/aukv_gpr_regfilie.v rtl/core/aukv_mem.v "
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
                                dir("AUK-V-Aethia") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p AUK-V-Aethia -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("AUK-V-Aethia") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p AUK-V-Aethia -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("AUK-V-Aethia") {
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
                                dir("AUK-V-Aethia") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p AUK-V-Aethia -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("AUK-V-Aethia") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p AUK-V-Aethia -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("AUK-V-Aethia") {
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
