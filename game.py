import customtkinter as ctk
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- appearance ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FractalExplorer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Fractal Explorer")
        self.geometry("1000x650")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----- plot -----
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # ----- controls -----
        self.control_frame = ctk.CTkFrame(self, width=260)
        self.control_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        ctk.CTkLabel(self.control_frame, text="Fractal Controls", font=("Arial", 18)).pack(pady=10)

        # ===== VERTICES =====
        self.vertex_label = ctk.CTkLabel(self.control_frame, text="Vertices: 3")
        self.vertex_label.pack(pady=(10, 0))

        self.vertices = ctk.CTkSlider(
            self.control_frame,
            from_=3,
            to=10,
            number_of_steps=7,
            command=self.update_vertices
        )
        self.vertices.set(3)
        self.vertices.pack(fill="x", padx=20)

        # ===== AUTO RATIO TOGGLE =====
        self.auto_ratio = ctk.BooleanVar(value=True)

        self.auto_checkbox = ctk.CTkCheckBox(
            self.control_frame,
            text="Auto Ratio",
            variable=self.auto_ratio,
            command=self.toggle_auto_ratio
        )
        self.auto_checkbox.pack(pady=10)

        # ===== RATIO =====
        self.ratio_label = ctk.CTkLabel(self.control_frame, text="Ratio: auto")
        self.ratio_label.pack(pady=(10, 0))

        # slider (coarse control)
        self.ratio = ctk.CTkSlider(
            self.control_frame,
            from_=0.0,
            to=1.0,
            number_of_steps=100,  # 0.01 steps (easy dragging)
            command=self.update_ratio
        )
        self.ratio.set(0.5)
        self.ratio.pack(fill="x", padx=20)

        # fine input (precise control)
        self.ratio_entry = ctk.CTkEntry(self.control_frame)
        self.ratio_entry.insert(0, "0.500")
        self.ratio_entry.pack(padx=20, pady=5)

        # apply button for fine control
        ctk.CTkButton(
            self.control_frame,
            text="Set Ratio Precisely",
            command=self.set_precise_ratio
        ).pack(pady=5)

        # ===== POINTS =====
        self.points_label = ctk.CTkLabel(self.control_frame, text="Points: 50,000")
        self.points_label.pack(pady=(10, 0))

        self.points = ctk.CTkSlider(
            self.control_frame,
            from_=1000,
            to=200000,
            number_of_steps=50,
            command=self.update_points
        )
        self.points.set(50000)
        self.points.pack(fill="x", padx=20)

        ctk.CTkButton(self.control_frame, text="Generate Fractal", command=self.generate).pack(pady=20)

        self.toggle_auto_ratio()
        self.generate()

    # ----- UI updates -----
    def update_vertices(self, value):
        self.vertex_label.configure(text=f"Vertices: {int(value)}")
        if self.auto_ratio.get():
            self.update_auto_ratio_label()

    def update_ratio(self, value):
        if not self.auto_ratio.get():
            self.ratio_label.configure(text=f"Ratio: {value:.2f}")

    def update_points(self, value):
        self.points_label.configure(text=f"Points: {int(value):,}")

    def toggle_auto_ratio(self):
        if self.auto_ratio.get():
            self.ratio.configure(state="disabled")
            self.update_auto_ratio_label()
        else:
            self.ratio.configure(state="normal")
            self.update_ratio(self.ratio.get())

    def update_auto_ratio_label(self):
        n = int(self.vertices.get())
        base_ratio = 1 / (1 + 2 * np.cos(np.pi / n))
        ratio = 1 - base_ratio
        self.ratio_label.configure(text=f"Ratio: {ratio:.3f} (auto)")

    def set_precise_ratio(self):
        try:
            value = float(self.ratio_entry.get())
            value = max(0.001, min(0.999, value))  # clamp
            self.ratio.set(value)
            self.update_ratio(value)
        except ValueError:
            pass

    # ----- fractal generation -----
    def generate(self):

        vertices = int(self.vertices.get())
        points = int(self.points.get())

        if self.auto_ratio.get():
            base_ratio = 1 / (1 + 2 * np.cos(np.pi / vertices))
            ratio = 1 - base_ratio
        else:
            ratio = self.ratio.get()

        angles = np.linspace(0, 2*np.pi, vertices, endpoint=False)
        verts = np.column_stack((np.cos(angles), np.sin(angles)))

        xs = np.empty(points)
        ys = np.empty(points)

        x, y = np.random.uniform(-1, 1, 2)

        for i in range(points):
            vx, vy = random.choice(verts)
            x = x + ratio * (vx - x)
            y = y + ratio * (vy - y)
            xs[i] = x
            ys[i] = y

        self.ax.clear()
        self.ax.scatter(xs, ys, s=0.2)
        self.ax.scatter(verts[:, 0], verts[:, 1], s=60)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.canvas.draw()


# ----- run -----
if __name__ == "__main__":
    app = FractalExplorer()
    app.mainloop()