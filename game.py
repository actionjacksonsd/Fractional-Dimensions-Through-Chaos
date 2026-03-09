import customtkinter as ctk
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class FractalExplorer(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Fractal Explorer")
        self.geometry("1000x650")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----- plot area -----
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # ----- control panel -----
        self.control_frame = ctk.CTkFrame(self, width=250)
        self.control_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        title = ctk.CTkLabel(self.control_frame, text="Controls", font=("Arial",18))
        title.pack(pady=10)

        # vertices
        ctk.CTkLabel(self.control_frame, text="Vertices").pack(pady=(10,0))
        self.vertices = ctk.CTkSlider(self.control_frame, from_=3, to=10, number_of_steps=7)
        self.vertices.set(3)
        self.vertices.pack(fill="x", padx=20)

        # ratio
        ctk.CTkLabel(self.control_frame, text="Ratio").pack(pady=(10,0))
        self.ratio = ctk.CTkSlider(self.control_frame, from_=0.1, to=0.9)
        self.ratio.set(0.5)
        self.ratio.pack(fill="x", padx=20)

        # density
        ctk.CTkLabel(self.control_frame, text="Points").pack(pady=(10,0))
        self.points = ctk.CTkSlider(self.control_frame, from_=1000, to=200000)
        self.points.set(50000)
        self.points.pack(fill="x", padx=20)

        generate_btn = ctk.CTkButton(self.control_frame, text="Generate", command=self.generate)
        generate_btn.pack(pady=20)

        self.generate()

    def generate(self):

        vertices = int(self.vertices.get())
        ratio = self.ratio.get()
        points = int(self.points.get())

        angles = np.linspace(0, 2*np.pi, vertices, endpoint=False)
        verts = np.column_stack((np.cos(angles), np.sin(angles)))

        # FAST: preallocate arrays
        xs = np.empty(points)
        ys = np.empty(points)

        x, y = np.random.uniform(-1,1,2)

        for i in range(points):
            vx, vy = random.choice(verts)
            x = x + ratio*(vx-x)
            y = y + ratio*(vy-y)
            xs[i] = x
            ys[i] = y

        self.ax.clear()
        self.ax.scatter(xs, ys, s=0.2)
        self.ax.scatter(verts[:,0], verts[:,1], s=60)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        self.canvas.draw()


app = FractalExplorer()
app.mainloop()