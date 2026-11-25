import math
import random
import tkinter as tk
from tkinter import messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VypocetApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Zadanie 2 – Výpočet reznej rýchlosti vc")
        self.root.geometry("980x700")

        # 1. Pole vstupných hodnôt (min. 50 náhodných hodnôt – otáčky vretena n [ot/min])
        self.vstupne_pole = []

        # --- Horný panel ovládania (GUI: Label, Input, Button) ---
        control_frame = tk.Frame(root, pady=10, padx=10)
        control_frame.pack(fill=tk.X)

        self.lbl_input = tk.Label(
            control_frame,
            text="Priemer nástroja D [mm] (ľubovoľné číslo):",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_input.pack(side=tk.LEFT, padx=(0, 8))

        self.entry_d = tk.Entry(control_frame, width=12, font=("Segoe UI", 10))
        self.entry_d.insert(0, "50")  # predvolená hodnota D = 50 mm
        self.entry_d.pack(side=tk.LEFT, padx=(0, 12))

        self.btn_vypocet = tk.Button(
            control_frame,
            text="Vypočítať a vykresliť graf",
            command=self.vypocitat_a_vykreslit,
            bg="#2b579a",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=10
        )
        self.btn_vypocet.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_nove_pole = tk.Button(
            control_frame,
            text="Nové náhodné pole (50 prvkov)",
            command=self.generovat_nove_pole,
            font=("Segoe UI", 10),
            padx=10
        )
        self.btn_nove_pole.pack(side=tk.LEFT)

        # --- Panel s výsledkami (Labels) ---
        info_frame = tk.Frame(root, padx=10, pady=5)
        info_frame.pack(fill=tk.X)

        self.lbl_jednotlivy_vypocet = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="#1b5e20",
            anchor="w"
        )
        self.lbl_jednotlivy_vypocet.pack(fill=tk.X, pady=2)

        self.lbl_statistika = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 10),
            anchor="w"
        )
        self.lbl_statistika.pack(fill=tk.X, pady=2)

        self.lbl_zoradene_pole = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 9),
            fg="#333333",
            justify=tk.LEFT,
            wraplength=940,
            anchor="w"
        )
        self.lbl_zoradene_pole.pack(fill=tk.X, pady=4)

        # --- Plocha pre graf (Matplotlib v Tkinter) ---
        chart_frame = tk.Frame(root, padx=10, pady=5)
        chart_frame.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(9, 4.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Prvotné vygenerovanie poľa a vykreslenie pri štarte aplikácie
        self.generovat_nove_pole()

    def generovat_nove_pole(self):
        """Vygeneruje 50 náhodných hodnôt otáčok n v rozsahu 500 až 3000 ot/min."""
        self.vstupne_pole = [random.randint(500, 3000) for _ in range(50)]
        self.vypocitat_a_vykreslit()

    def vypocitat_a_vykreslit(self):
        """Vykoná operácie s poľom, výpočet podľa vzorca z Mendixu a vykreslí graf."""
        raw_text = self.entry_d.get().strip().replace(",", ".")
        try:
            priemer_d = float(raw_text)
            if priemer_d <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Chyba vstupu",
                "Zadajte kladné číslo pre priemer D [mm] (napr. 50 alebo 32.5)."
            )
            return

        # 2. Práca s poľom hodnôt (zoradenie od najmenšieho, min, max, priemer)
        zoradene_n = sorted(self.vstupne_pole)
        min_n = min(zoradene_n)
        max_n = max(zoradene_n)
        priemer_n = round(sum(zoradene_n) / len(zoradene_n), 2)

        # 3. Výpočet podľa vzorca z Mendixu: vc = (pi * D * n) / 1000 [m/min]
        vypocitane_vc = [round((math.pi * priemer_d * n) / 1000, 2) for n in zoradene_n]

        # Výpočet vzorca pre ľubovoľné zadané číslo D (pri referenčných otáčkach n = 1000 ot/min)
        vc_pre_zadane_d = round((math.pi * priemer_d * 1000) / 1000, 2)

        # Aktualizácia textových popisov (Labels)
        self.lbl_jednotlivy_vypocet.config(
            text=f"Výpočet pre zadané D = {priemer_d} mm (pri n = 1000 ot/min): "
                 f"vc = (π · {priemer_d} · 1000) / 1000 = {vc_pre_zadane_d} m/min"
        )
        self.lbl_statistika.config(
            text=f"Štatistika poľa (50 prvkov) | Min: {min_n} ot/min | "
                 f"Max: {max_n} ot/min | Priemer: {priemer_n} ot/min"
        )
        self.lbl_zoradene_pole.config(
            text=f"Zoradené vstupné pole n (od najmenšieho po najväčšie): {zoradene_n}"
        )

        # 4. Zobrazenie pôvodných aj vypočítaných hodnôt v jednom grafe
        self.fig.clear()
        ax1 = self.fig.add_subplot(111)
        ax2 = ax1.twinx()

        indexy = list(range(1, len(zoradene_n) + 1))

        line1 = ax1.plot(
            indexy,
            zoradene_n,
            color="#1f77b4",
            marker="o",
            markersize=4,
            linewidth=1.5,
            label="Pôvodné hodnoty: otáčky n [ot/min]"
        )
        line2 = ax2.plot(
            indexy,
            vypocitane_vc,
            color="#d62728",
            linestyle="--",
            marker="s",
            markersize=4,
            linewidth=1.5,
            label=f"Vypočítané hodnoty: rezná rýchlosť vc [m/min] (D = {priemer_d} mm)"
        )

        ax1.set_title("Porovnanie pôvodných (n) a vypočítaných (vc) hodnôt")
        ax1.set_xlabel("Index prvku v zoradenom poli (1 – 50)")
        ax1.set_ylabel("Otáčky vretena n [ot/min]", color="#1f77b4")
        ax2.set_ylabel("Rezná rýchlosť vc [m/min]", color="#d62728")
        ax1.grid(True, linestyle=":", alpha=0.6)

        # Spojená legenda pre obe krivky v jednom grafe
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc="upper left")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = VypocetApp(root)
    root.mainloop()