# RISC-V ISA CI

CI/CD para núcleos RISC-V

If you don't speak Portuguese, [click here](README_en.md)

Si no hablas portugués, [haz clic aquí](README_es.md)

![FPGAs usadas para teste](docs/imgs/fpgas.jpeg)

Software desenvolvido para testar processadores baseados na arquitetura RISC-V. O software abrange testes desde a síntese do processador em linguagem HDL (Verilog ou VHDL) até a execução de instruções com o processador operando em FPGA.

## Requisitos:

Para a execução do software, será necessária a instalação de algumas dependências. Dentre elas estão:

- Litex: [https://github.com/enjoy-digital/litex](https://github.com/enjoy-digital/litex)
- Requests: [https://pypi.org/project/requests/](https://pypi.org/project/requests/)
- GitPython: [https://pypi.org/project/GitPython/0.3.2/](https://pypi.org/project/GitPython/0.3.2/)
- OSS-Cad-Suite: [https://github.com/YosysHQ/oss-cad-suite-build](https://github.com/YosysHQ/oss-cad-suite-build)
- Toolchain da placa a ser utilizada: Gowin, Vivado, Quartus ...

## Hardware:

Para a execução dos processadores, será necessário o uso de pelo menos uma FPGA. Atualmente, são suportadas as seguintes FPGAs:

- Tang nano 20k
- Tang nano 9k
- Lattice ECP5 45F

## Partes implementadas

- [x] Clone e Pull de repositórios GIT
- [x] Síntese de Núcleo(s)/SoC(s)
- [ ] Padronização das pinagens para diversas FPGAs
- [ ] Verificação do processo de síntese
- [x] Gravação em FPGA
- [ ] Debugger serial com a FPGA
- [ ] Execução de instruções
- [ ] Envio automatizado de arquivos de memória para FPGA

## Dúvidas e Bugs:

Em caso de alguma dúvida, bug na aplicação ou sugestão, utilize o menu [issues](https://github.com/JN513/riscv-isa-ci/issues) do Github.

## Licença:

Este repositório está licenciado pela Licença GNU General Public License V3. As bibliotecas e softwares de terceiros seguem as licenças utilizadas pelos repositórios originais.

## Softwares de terceiros:

- Implementação do Módulo UART: [https://github.com/ben-marshall/uart](https://github.com/ben-marshall/uart)
