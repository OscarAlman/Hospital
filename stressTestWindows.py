import ctypes
import math
import multiprocessing as mp
import os
import queue
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox


# -------------------- CPU workload --------------------

def stress_cpu(stop):
    value = 0.5

    while not stop.is_set():
        for i in range(20_000):
            value = (
                math.sin(value + i * 0.001) ** 2
                + math.sqrt(value + 1.0)
            )


# -------------------- GPU workload --------------------

def stress_gpu(stop, messages, passes):
    """Render rotating 3D meshes using Windows OpenGL."""
    window = None
    dc = context = None
    hwnd = None

    try:
        if sys.platform != "win32":
            raise RuntimeError("GPU mode requires Windows.")

        from ctypes import wintypes as wt

        user = ctypes.WinDLL("user32")
        gdi = ctypes.WinDLL("gdi32")
        gl = ctypes.WinDLL("opengl32")

        pointer = ctypes.c_void_p
        integer = ctypes.c_int
        uint = ctypes.c_uint
        floating = ctypes.c_float

        def function(library, name, result, *arguments):
            fn = getattr(library, name)
            fn.restype = result
            fn.argtypes = list(arguments)
            return fn

        # Windows pixel-format structure.
        class PixelFormat(ctypes.Structure):
            _fields_ = [
                ("size", wt.WORD),
                ("version", wt.WORD),
                ("flags", wt.DWORD),
                *[
                    (name, ctypes.c_ubyte)
                    for name in (
                        "pixel_type", "color_bits",
                        "red_bits", "red_shift",
                        "green_bits", "green_shift",
                        "blue_bits", "blue_shift",
                        "alpha_bits", "alpha_shift",
                        "accum_bits", "accum_red", "accum_green",
                        "accum_blue", "accum_alpha",
                        "depth_bits", "stencil_bits", "aux_buffers",
                        "layer_type", "reserved",
                    )
                ],
                ("layer_mask", wt.DWORD),
                ("visible_mask", wt.DWORD),
                ("damage_mask", wt.DWORD),
            ]

        get_dc = function(user, "GetDC", pointer, pointer)
        release_dc = function(
            user, "ReleaseDC", integer, pointer, pointer
        )
        choose_format = function(
            gdi, "ChoosePixelFormat", integer,
            pointer, ctypes.POINTER(PixelFormat)
        )
        set_format = function(
            gdi, "SetPixelFormat", integer,
            pointer, integer, ctypes.POINTER(PixelFormat)
        )
        swap_buffers = function(
            gdi, "SwapBuffers", integer, pointer
        )
        create_context = function(
            gl, "wglCreateContext", pointer, pointer
        )
        make_current = function(
            gl, "wglMakeCurrent", integer, pointer, pointer
        )
        delete_context = function(
            gl, "wglDeleteContext", integer, pointer
        )

        # Define the OpenGL calls used by our renderer.
        signatures = {
            "glClearColor": (None, [floating] * 4),
            "glClear": (None, [uint]),
            "glEnable": (None, [uint]),
            "glViewport": (None, [integer] * 4),
            "glMatrixMode": (None, [uint]),
            "glLoadIdentity": (None, []),
            "glFrustum": (None, [ctypes.c_double] * 6),
            "glTranslatef": (None, [floating] * 3),
            "glRotatef": (None, [floating] * 4),
            "glScalef": (None, [floating] * 3),
            "glPushMatrix": (None, []),
            "glPopMatrix": (None, []),
            "glBegin": (None, [uint]),
            "glEnd": (None, []),
            "glVertex3f": (None, [floating] * 3),
            "glColor3f": (None, [floating] * 3),
            "glGenLists": (uint, [integer]),
            "glNewList": (None, [uint, uint]),
            "glEndList": (None, []),
            "glCallList": (None, [uint]),
            "glFinish": (None, []),
            "glGetString": (ctypes.c_char_p, [uint]),
        }

        functions = {
            name: function(gl, name, result, *args)
            for name, (result, args) in signatures.items()
        }

        def call(name, *args):
            return functions[name](*args)

        window = tk.Tk()
        window.title("GPU rendering — Escape to stop")
        window.geometry("1280x720")

        surface = tk.Frame(window, background="black")
        surface.pack(fill="both", expand=True)
        window.update()

        hwnd = surface.winfo_id()
        dc = get_dc(hwnd)
        if not dc:
            raise RuntimeError("Could not obtain a drawing surface.")

        pixel_format = PixelFormat()
        pixel_format.size = ctypes.sizeof(PixelFormat)
        pixel_format.version = 1
        # Draw to window + support OpenGL + double buffering.
        pixel_format.flags = 0x25
        pixel_format.color_bits = 24
        pixel_format.depth_bits = 24

        selected = choose_format(dc, ctypes.byref(pixel_format))
        if not selected or not set_format(
            dc, selected, ctypes.byref(pixel_format)
        ):
            raise RuntimeError("Could not configure OpenGL.")

        context = create_context(dc)
        if not context or not make_current(dc, context):
            raise RuntimeError("Could not activate OpenGL.")

        renderer = (
            call("glGetString", 0x1F01) or b"Unknown GPU"
        ).decode(errors="replace")

        if any(
            name in renderer.lower()
            for name in ("gdi generic", "llvmpipe", "softpipe")
        ):
            raise RuntimeError(
                "Software rendering detected. "
                "GPU mode needs a working graphics driver."
            )

        messages.put(("gpu", renderer))

        # Disable VSync when the driver exposes this option.
        get_proc = function(
            gl, "wglGetProcAddress", pointer, ctypes.c_char_p
        )
        address = get_proc(b"wglSwapIntervalEXT")

        invalid_addresses = (
            None, 0, 1, 2, 3, ctypes.c_void_p(-1).value
        )
        if address not in invalid_addresses:
            ctypes.WINFUNCTYPE(integer, integer)(address)(0)

        # Generate a dense 3D torus from its mathematical coordinates.
        mesh = call("glGenLists", 1)
        if not mesh:
            raise RuntimeError("Could not allocate the 3D mesh.")

        call("glNewList", mesh, 0x1300)  # GL_COMPILE

        for ring in range(128):
            call("glBegin", 0x0008)  # GL_QUAD_STRIP

            for segment in range(65):
                v = 2 * math.pi * segment / 64

                for edge in (ring, ring + 1):
                    u = 2 * math.pi * edge / 128
                    radius = 1 + 0.35 * math.cos(v)

                    x = radius * math.cos(u)
                    y = radius * math.sin(u)
                    z = 0.35 * math.sin(v)

                    shade = 0.5 + 0.5 * math.cos(v)
                    call(
                        "glColor3f",
                        0.15 + 0.8 * shade,
                        0.3 + 0.5 * math.sin(u) ** 2,
                        0.85,
                    )
                    call("glVertex3f", x, y, z)

            call("glEnd")

        call("glEndList")
        call("glEnable", 0x0B71)  # GL_DEPTH_TEST
        call("glClearColor", 0.015, 0.025, 0.05, 1.0)

        window.bind("<Escape>", lambda event: stop.set())
        window.protocol("WM_DELETE_WINDOW", stop.set)

        started = last_report = time.perf_counter()
        frames = 0

        while not stop.is_set():
            window.update()

            if stop.is_set():
                break

            if window.state() == "iconic":
                time.sleep(0.05)
                continue

            width = max(1, surface.winfo_width())
            height = max(1, surface.winfo_height())
            aspect = width / height

            call("glViewport", 0, 0, width, height)
            call("glMatrixMode", 0x1701)  # GL_PROJECTION
            call("glLoadIdentity")
            call("glFrustum", -aspect, aspect, -1, 1, 1, 100)

            elapsed = time.perf_counter() - started

            # More passes mean more geometry and pixel processing.
            for _ in range(passes):
                if stop.is_set():
                    break

                call("glClear", 0x4100)  # Color and depth
                call("glMatrixMode", 0x1700)  # GL_MODELVIEW
                call("glLoadIdentity")
                call("glTranslatef", 0, 0, -12)

                for row in range(5):
                    for column in range(7):
                        call("glPushMatrix")
                        call(
                            "glTranslatef",
                            (column - 3) * 2.1,
                            (row - 2) * 2.1,
                            0,
                        )
                        call(
                            "glRotatef",
                            elapsed * 40 + row * 17 + column * 11,
                            1, 0.7, 0.3,
                        )
                        call("glScalef", 0.7, 0.7, 0.7)
                        call("glCallList", mesh)
                        call("glPopMatrix")

            call("glFinish")
            if not swap_buffers(dc):
                raise RuntimeError("OpenGL buffer swap failed.")

            frames += 1
            now = time.perf_counter()

            if now - last_report >= 1:
                fps = frames / (now - last_report)
                window.title(
                    f"{renderer} | {fps:.1f} FPS | Escape to stop"
                )
                messages.put(("fps", fps))
                frames = 0
                last_report = now

    except Exception as error:
        messages.put(("error", str(error)))

    finally:
        stop.set()

        if context:
            make_current(None, None)
            delete_context(context)

        if dc:
            release_dc(hwnd, dc)

        if window:
            window.destroy()


# -------------------- Control panel --------------------

def main():
    root = tk.Tk()
    root.title("CPU and GPU Stress Test")
    root.geometry("520x430")

    panel = ttk.Frame(root, padding=20)
    panel.pack(fill="both", expand=True)

    ttk.Label(
        panel,
        text="CPU and GPU Stress Test",
        font=("Segoe UI", 18, "bold"),
    ).pack(anchor="w", pady=(0, 15))

    cpu_enabled = tk.BooleanVar(value=True)
    gpu_enabled = tk.BooleanVar(value=True)

    ttk.Checkbutton(
        panel, text="Stress CPU", variable=cpu_enabled
    ).pack(anchor="w")

    ttk.Checkbutton(
        panel, text="Stress GPU with 3D rendering",
        variable=gpu_enabled,
    ).pack(anchor="w")

    logical_cores = os.cpu_count() or 1

    workers = tk.StringVar(value=str(max(1, logical_cores - 1)))
    seconds = tk.StringVar(value="60")
    passes = tk.StringVar(value="8")

    settings = ttk.Frame(panel)
    settings.pack(fill="x", pady=15)

    for row, (label, variable) in enumerate([
        ("CPU processes", workers),
        ("Duration in seconds", seconds),
        ("GPU render passes: 1–64", passes),
    ]):
        ttk.Label(settings, text=label).grid(
            row=row, column=0, sticky="w", pady=4
        )
        ttk.Entry(
            settings, textvariable=variable, width=12
        ).grid(row=row, column=1, padx=20)

    status = tk.StringVar(value="Ready")
    gpu_info = tk.StringVar(value="GPU: not started")

    ttk.Label(panel, textvariable=gpu_info, wraplength=470).pack(
        anchor="w", pady=5
    )
    ttk.Label(panel, textvariable=status, wraplength=470).pack(
        anchor="w", pady=5
    )
    ttk.Label(
        panel,
        text="Monitor temperatures separately; no thermal cutoff.",
        wraplength=470,
    ).pack(anchor="w", pady=10)

    controls = ttk.Frame(panel)
    controls.pack(anchor="w")

    context = mp.get_context("spawn")
    processes = []
    stop_event = None
    messages = None
    start_time = 0
    duration = 0
    stop_deadline = None
    closing = False
    failure = None
    last_fps = None

    def stop_test():
        nonlocal stop_deadline

        if stop_event is not None:
            stop_event.set()

            if stop_deadline is None:
                stop_deadline = time.monotonic() + 3

            stop_button.config(state="disabled")

    def start_test():
        nonlocal processes, stop_event, messages
        nonlocal start_time, duration, stop_deadline
        nonlocal failure, last_fps

        try:
            if not cpu_enabled.get() and not gpu_enabled.get():
                raise ValueError("Select CPU, GPU, or both.")

            duration = int(seconds.get())
            count = int(workers.get()) if cpu_enabled.get() else 1
            repeats = int(passes.get()) if gpu_enabled.get() else 1

            if not 1 <= duration <= 86400:
                raise ValueError("Duration must be 1–86400 seconds.")

            if not 1 <= count <= logical_cores:
                raise ValueError(
                    f"CPU processes must be 1–{logical_cores}."
                )

            if not 1 <= repeats <= 64:
                raise ValueError("GPU passes must be 1–64.")

            if gpu_enabled.get() and sys.platform != "win32":
                raise ValueError("GPU mode requires Windows.")

        except ValueError as error:
            messagebox.showerror("Settings", str(error))
            return

        stop_event = context.Event()
        messages = context.Queue()
        stop_deadline = None
        failure = None
        last_fps = None
        processes = []

        if cpu_enabled.get():
            for index in range(count):
                processes.append(context.Process(
                    target=stress_cpu,
                    args=(stop_event,),
                    name=f"CPU {index + 1}",
                ))

        if gpu_enabled.get():
            processes.append(context.Process(
                target=stress_gpu,
                args=(stop_event, messages, repeats),
                name="GPU",
            ))

        gpu_info.set(
            "GPU: starting…" if gpu_enabled.get() else "GPU: disabled"
        )
        start_time = time.monotonic()
        start_button.config(state="disabled")
        stop_button.config(state="normal")

        try:
            for process in processes:
                process.start()
        except Exception as error:
            failure = f"Could not start: {error}"
            stop_test()

    def poll():
        nonlocal processes, stop_event, messages, failure, last_fps

        if messages is not None:
            try:
                while True:
                    kind, value = messages.get_nowait()

                    if kind == "gpu":
                        gpu_info.set("GPU: " + value)
                    elif kind == "fps":
                        last_fps = value
                    elif kind == "error":
                        failure = value
                        stop_test()
            except queue.Empty:
                pass

        if processes:
            elapsed = time.monotonic() - start_time

            for process in processes:
                if (
                    process.pid is not None
                    and process.exitcode not in (None, 0)
                    and stop_deadline is None
                ):
                    failure = f"{process.name} exited unexpectedly."
                    stop_test()

            if elapsed >= duration or stop_event.is_set():
                stop_test()

            if failure:
                status.set("Error: " + failure)
            elif stop_deadline is not None:
                status.set("Stopping…")
            else:
                text = f"Running: {elapsed:.0f} / {duration} seconds"
                if last_fps is not None:
                    text += f" | {last_fps:.1f} FPS"
                status.set(text)

            if (
                stop_deadline is not None
                and time.monotonic() >= stop_deadline
            ):
                for process in processes:
                    if process.pid is not None and process.is_alive():
                        process.terminate()

            if all(
                process.pid is None or not process.is_alive()
                for process in processes
            ):
                for process in processes:
                    if process.pid is not None:
                        process.join(timeout=0)

                processes = []
                stop_event = None
                start_button.config(state="normal")
                stop_button.config(state="disabled")

                if not failure:
                    status.set("Test stopped.")

        if closing and not processes:
            root.destroy()
            return

        root.after(100, poll)

    def close():
        nonlocal closing
        closing = True
        stop_test()

        if not processes:
            root.destroy()

    start_button = ttk.Button(
        controls, text="Start", command=start_test
    )
    start_button.pack(side="left")

    stop_button = ttk.Button(
        controls, text="Stop", command=stop_test, state="disabled"
    )
    stop_button.pack(side="left", padx=10)

    root.protocol("WM_DELETE_WINDOW", close)
    root.after(100, poll)
    root.mainloop()


if __name__ == "__main__":
    mp.freeze_support()
    main()