
pipeline {
    agent any
    stages {
        stage('Git Clone and Cleanup') {
            steps {
                sh 'rm -rf darkriscv'
                sh 'git clone --recursive https://github.com/darklife/darkriscv.git darkriscv'
            }
        }
        
        stage('Simulation') {
            steps {
                dir("darkriscv") {
                    sh "iverilog -o simulation.out -g2005 -s core  rtl/darkriscv.v  && vvp simulation.out"
                }
            }
        }
        
        stage('FPGA Synthesis') {
            parallel {
                stage('colorlight_i9') {
                    steps {
                        lock(resource: 'colorlight_i9') {
                            echo 'FPGA colorlight_i9 bloqueada para síntese.'
                            dir("darkriscv") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p darkriscv -b colorlight_i9'
                            }
                        }
                    }
                }
                stage('digilent_nexys4_ddr') {
                    steps {
                        lock(resource: 'digilent_nexys4_ddr') {
                            echo 'FPGA digilent_nexys4_ddr bloqueada para síntese.'
                            dir("darkriscv") {
                                sh 'python3 main_script_path -c /eda/processor-ci/config.json -p darkriscv -b digilent_nexys4_ddr'
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
            dir("darkriscv") {
                sh 'rm -rf *'
            }
        }
    }
}
