from litex.build.generic_platform import *

ios_tang_nano_20k = [
    ("clk", 0, Pins("4"), IOStandard("LVCMOS33")),
    ("reset", 0, Pins("88"), IOStandard("LVCMOS33")),
]

ios_tang_nano_9k = [
    ("clk", 0, Pins("4"), IOStandard("LVCMOS33")),
    ("reset", 0, Pins("88"), IOStandard("LVCMOS33")),
    ("led_n", 0, Pins("10"), IOStandard("LVCMOS18")),
    ("led_n", 1, Pins("11"), IOStandard("LVCMOS18")),
    ("led_n", 2, Pins("13"), IOStandard("LVCMOS18")),
    ("led_n", 3, Pins("14"), IOStandard("LVCMOS18")),
    ("led_n", 4, Pins("15"), IOStandard("LVCMOS18")),
    ("led_n", 5, Pins("16"), IOStandard("LVCMOS18")),
]

ios_colorlight_i9 = [
    ("led_n", 0, Pins("R3"), IOStandard("LVCMOS33")),
    ("led_n", 1, Pins("M4"), IOStandard("LVCMOS33")),
    ("led_n", 2, Pins("L5"), IOStandard("LVCMOS33")),
    ("led_n", 3, Pins("J16"), IOStandard("LVCMOS33")),
    ("led_n", 4, Pins("N4"), IOStandard("LVCMOS33")),
    ("led_n", 5, Pins("L4"), IOStandard("LVCMOS33")),
    ("led_n", 6, Pins("P16"), IOStandard("LVCMOS33")),
    ("led_n", 7, Pins("J18"), IOStandard("LVCMOS33")),
    ("btn_n", 0, Pins("R1"), IOStandard("LVCMOS33")),
    ("btn_n", 1, Pins("U1"), IOStandard("LVCMOS33")),
    ("btn_n", 2, Pins("W1"), IOStandard("LVCMOS33")),
    ("btn_n", 3, Pins("M1"), IOStandard("LVCMOS33")),
    ("btn_n", 4, Pins("T1"), IOStandard("LVCMOS33")),
    ("btn_n", 5, Pins("Y2"), IOStandard("LVCMOS33")),
    ("btn_n", 6, Pins("V1"), IOStandard("LVCMOS33")),
    ("btn_n", 7, Pins("N2"), IOStandard("LVCMOS33")),
]
