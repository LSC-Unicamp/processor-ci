import os
import sys
from time import time
from litex_boards.platforms import (
    sipeed_tang_nano_9k,
    sipeed_tang_nano_20k,
    lattice_ecp5_evn,
    lattice_ecp5_vip,
    colorlight_i5,
)
from platforms.ios import ios_tang_nano_20k, ios_tang_nano_9k, ios_colorlight_i9
from migen import Module


def check_core(
    board: str,
) -> int:  # 0 - ok, 1 - erro ao sintetizar, 2 - erro de execução
    if not os.path.isfile("build/top.fs") and (
        board == "tangnano9k" or board == "tangnano20k"
    ):
        print("Core não sintetizado")
        return 1
    elif not os.path.isfile("build/top.bit") and board == "ecp5_45f":
        print("Core não sintetizado")
        return 1

    return 0


def build_and_flash_core(
    name: str, board: str, files: list[str], constraints: list[str]
) -> None:
    platform = None

    if board == "tangnano9k":
        platform = sipeed_tang_nano_9k.Platform()
        platform.add_extension(ios_tang_nano_9k)
        platform.add_source("rtl/boards/tangnano.v")
    elif board == "ecp5_45f":
        platform = colorlight_i5.Platform(
            board="i9", revision="7.2", toolchain="trellis"
        )
        platform.add_extension(ios_colorlight_i9)
        platform.add_source("rtl/boards/ecp5.v")
    else:
        platform = sipeed_tang_nano_20k.Platform()
        platform.add_extension(ios_tang_nano_20k)
        platform.add_source("rtl/boards/tangnano.v")

    for constraint in constraints:
        ops = constraint.split(":")
        if len(ops) == 1:
            platform.request(ops[0])
        else:
            platform.request(ops[0], int(ops[1]))

    for file in files:
        platform.add_source(file)

    module = Module()

    platform.build(module)

    programer = platform.create_programmer()

    if board == "tangnano9k":
        programer.load_bitstream("build/top.fs")
    elif board == "ecp5_45f":
        programer.load_bitstream("build/top.bit")
    else:
        programer.load_bitstream("build/top.fs")


def build_and_check_cores(data: dict[str, any], board: str = "tangnano20k") -> None:
    if not "cores" in data:
        sys.exit(f"[ {time()} ] Error: cores key not found in config file")

    for i, core in enumerate(data["cores"]):
        if not core["enable"]:
            continue
        name: str = core["name"]
        repository: str = core["repository"]
        folder: str = core["folder"]
        files: list[str] = core["files"]
        constraints: str = core["constraints"]

        print(f"Log: Testing repository {i + 1} processor: {name}")

        build_and_flash_core(name, board, files, constraints)

        check_core(board)
