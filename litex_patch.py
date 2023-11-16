import os
from migen import *
from migen.fhdl.structure import _Fragment


def _build(
    self,
    platform,
    fragment,
    build_dir="build",
    build_name="top",
    synth_opts="",
    run=True,
    build_backend="litex",
    **kwargs
):
    self._build_name = build_name
    self._build_dir = build_dir
    self._synth_opts += synth_opts
    self.platform = platform
    self.fragment = fragment

    # Create Build Directory.
    os.makedirs(self._build_dir, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(self._build_dir)

    # Finalize Design.
    if not isinstance(self.fragment, _Fragment):
        self.fragment = self.fragment.get_fragment()
    platform.finalize(self.fragment)

    # Generate Verilog.
    v_output = platform.get_verilog(self.fragment, name=build_name, **kwargs)
    self._vns = v_output.ns
    v_file = build_name + ".v"
    v_output.write(v_file)

    # Finalize toolchain (after gateware is complete)
    self.finalize()

    # Get signals and platform constraints
    self.named_sc, self.named_pc = platform.resolve_signals(self._vns)
    # platform.add_source(v_file)

    # Generate Design Timing Constraints File.
    tim_cst_file = self.build_timing_constraints(v_output.ns)

    # Generate Design IO Constraints File.
    io_cst_file = self.build_io_constraints()

    # Generate Design Placement Constraints File.
    place_cst_file = self.build_placement_constraints()

    if build_backend not in self.supported_build_backend:
        raise NotImplementedError(
            "Build backend {build_backend} is not supported by {toolchain} toolchain".format(
                build_backend=build_backend, toolchain=type(self).__name__
            )
        )

    # LiteX backend.
    if build_backend == "litex":
        # Generate project.
        self.build_project()

        # Generate build script.
        script = self.build_script()

        # Run.
        if run:
            self.run_script(script)

    # Edalize backend.
    else:
        from edalize import get_edatool

        # Get tool name and options
        (tool, tool_options) = self.get_tool_options()

        # Files list
        files = []
        for filename, language, library, *copy in self.platform.sources:
            ext = {
                "verilog": "verilogSource",
                "systemverilog": "systemVerilogSource",
                "vhdl": "vhdlSource",
            }[language]
            files.append({"name": filename, "file_type": ext})

        # IO/timings constraints
        files.append(
            {"name": os.path.abspath(io_cst_file[0]), "file_type": io_cst_file[1]}
        )
        if tim_cst_file[0] != "":
            files.append(
                {"name": os.path.abspath(tim_cst_file[0]), "file_type": tim_cst_file[1]}
            )
        if place_cst_file[0] != "":
            files.append(
                {
                    "name": os.path.abspath(place_cst_file[0]),
                    "file_type": place_cst_file[1],
                }
            )

        edam = {
            "name": self._build_name,
            "files": files,
            **tool_options,
            "toplevel": self._build_name,
        }

        backend = get_edatool(tool)(edam=edam, work_root=self._build_dir)
        backend.configure()
        if run:
            backend.build()

    os.chdir(cwd)

    return v_output.ns
