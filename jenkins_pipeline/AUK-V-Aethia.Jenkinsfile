
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf AUK-V-Aethia'
                sh 'git clone --recursive https://github.com/veeYceeY/AUK-V-Aethia.git AUK-V-Aethia'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("AUK-V-Aethia") {
                    sh "iverilog -o simulation.out -g2005 -s aukv  rtl/core/aukv.v rtl/core/aukv_alu.v rtl/core/aukv_csr_regfile.v rtl/core/aukv_decode.v rtl/core/aukv_execute.v rtl/core/aukv_fetch.v rtl/core/aukv_gpr_regfilie.v rtl/core/aukv_mem.v  && vvp simulation.out"
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("AUK-V-Aethia") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p AUK-V-Aethia -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("AUK-V-Aethia") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p AUK-V-Aethia -b digilent_nexys4_ddr'
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
            dir("AUK-V-Aethia") {
                sh 'rm -rf *'
            }
        }
    }
}
