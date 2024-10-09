
pipeline {
    agent any
    stages {
        stage('Git Clone') {
            steps {
                sh 'rm -rf Cores-SweRV-EH2'
                sh 'git clone --recursive https://github.com/chipsalliance/Cores-SweRV-EH2 Cores-SweRV-EH2'
            }
        }

        

        stage('Simulation') {
            steps {
                dir("Cores-SweRV-EH2") {
                    sh "iverilog -o simulation.out -g2012  -s eh2_veer -I design/include design/dmi/dmi_jtag_to_core_sync.v design/dmi/dmi_wrapper.v design/dmi/rvjtag_tap.v design/eh2_dma_ctrl.sv design/eh2_mem.sv design/eh2_pic_ctrl.sv design/eh2_veer.sv design/eh2_veer_wrapper.sv design/dbg/eh2_dbg.sv design/dec/eh2_dec.sv design/dec/eh2_dec_csr.sv design/dec/eh2_dec_decode_ctl.sv design/dec/eh2_dec_gpr_ctl.sv design/dec/eh2_dec_ib_ctl.sv design/dec/eh2_dec_tlu_ctl.sv design/dec/eh2_dec_tlu_top.sv design/dec/eh2_dec_trigger.sv design/exu/eh2_exu.sv design/exu/eh2_exu_alu_ctl.sv design/exu/eh2_exu_div_ctl.sv design/exu/eh2_exu_mul_ctl.sv design/ifu/eh2_ifu.sv design/ifu/eh2_ifu_aln_ctl.sv design/ifu/eh2_ifu_bp_ctl.sv design/ifu/eh2_ifu_compress_ctl.sv design/ifu/eh2_ifu_ic_mem.sv design/ifu/eh2_ifu_iccm_mem.sv design/ifu/eh2_ifu_ifc_ctl.sv design/ifu/eh2_ifu_mem_ctl.sv design/include/eh2_def.sv design/lib/ahb_to_axi4.sv design/lib/axi4_to_ahb.sv design/lib/beh_lib.sv design/lib/eh2_lib.sv design/lib/mem_lib.sv design/lsu/eh2_lsu.sv design/lsu/eh2_lsu_addrcheck.sv design/lsu/eh2_lsu_amo.sv design/lsu/eh2_lsu_bus_buffer.sv design/lsu/eh2_lsu_bus_intf.sv design/lsu/eh2_lsu_clkdomain.sv design/lsu/eh2_lsu_dccm_ctl.sv design/lsu/eh2_lsu_dccm_mem.sv design/lsu/eh2_lsu_ecc.sv design/lsu/eh2_lsu_lsc_ctl.sv design/lsu/eh2_lsu_trigger.sv "
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
                                dir("Cores-SweRV-EH2") {
                                    echo 'Iniciando síntese para FPGA colorlight_i9.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-SweRV-EH2 -b colorlight_i9'
                                }
                            }
                        }
                        stage('Flash colorlight_i9') {
                            steps {
                                dir("Cores-SweRV-EH2") {
                                    echo 'FPGA colorlight_i9 bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-SweRV-EH2 -b colorlight_i9 -l'
                                }
                            }
                        }
                        stage('Teste colorlight_i9') {
                            steps {
                                echo 'Testando FPGA colorlight_i9.'
                                dir("Cores-SweRV-EH2") {
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
                                dir("Cores-SweRV-EH2") {
                                    echo 'Iniciando síntese para FPGA digilent_nexys4_ddr.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-SweRV-EH2 -b digilent_nexys4_ddr'
                                }
                            }
                        }
                        stage('Flash digilent_nexys4_ddr') {
                            steps {
                                dir("Cores-SweRV-EH2") {
                                    echo 'FPGA digilent_nexys4_ddr bloqueada para flash.'
                                    sh 'python3 /eda/processor-ci/main.py -c /eda/processor-ci/config.json -p Cores-SweRV-EH2 -b digilent_nexys4_ddr -l'
                                }
                            }
                        }
                        stage('Teste digilent_nexys4_ddr') {
                            steps {
                                echo 'Testando FPGA digilent_nexys4_ddr.'
                                dir("Cores-SweRV-EH2") {
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
