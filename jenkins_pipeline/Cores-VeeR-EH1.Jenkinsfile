
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf Cores-VeeR-EH1'
                sh 'git clone --recursive https://github.com/chipsalliance/Cores-VeeR-EH1 Cores-VeeR-EH1'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("Cores-VeeR-EH1") {
                    sh "iverilog -o simulation.out -g2012  -s veer -I design/include design/dmi/dmi_jtag_to_core_sync.v design/dmi/dmi_wrapper.v design/dma_ctrl.sv design/mem.sv design/pic_ctrl.sv design/veer.sv design/veer_wrapper.sv design/dbg/dbg.sv design/dec/dec.sv design/dec/dec_decode_ctl.sv design/dec/dec_gpr_ctl.sv design/dec/dec_ib_ctl.sv design/dec/dec_tlu_ctl.sv design/dec/dec_trigger.sv design/dmi/rvjtag_tap.sv design/exu/exu.sv design/exu/exu_alu_ctl.sv design/exu/exu_div_ctl.sv design/exu/exu_mul_ctl.sv design/ifu/ifu.sv design/ifu/ifu_aln_ctl.sv design/ifu/ifu_bp_ctl.sv design/ifu/ifu_compress_ctl.sv design/ifu/ifu_ic_mem.sv design/ifu/ifu_iccm_mem.sv design/ifu/ifu_ifc_ctl.sv design/ifu/ifu_mem_ctl.sv design/include/veer_types.sv design/lib/ahb_to_axi4.sv design/lib/axi4_to_ahb.sv design/lib/beh_lib.sv design/lib/mem_lib.sv design/lib/svci_to_axi4.sv design/lsu/lsu.sv design/lsu/lsu_addrcheck.sv design/lsu/lsu_bus_buffer.sv design/lsu/lsu_bus_intf.sv design/lsu/lsu_clkdomain.sv design/lsu/lsu_dccm_ctl.sv design/lsu/lsu_dccm_mem.sv design/lsu/lsu_ecc.sv design/lsu/lsu_lsc_ctl.sv design/lsu/lsu_trigger.sv "
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
                                dir("Cores-VeeR-EH1") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-VeeR-EH1 -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("Cores-VeeR-EH1") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-VeeR-EH1 -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("Cores-VeeR-EH1") {
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
                                dir("Cores-VeeR-EH1") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-VeeR-EH1 -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("Cores-VeeR-EH1") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-VeeR-EH1 -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("Cores-VeeR-EH1") {
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
