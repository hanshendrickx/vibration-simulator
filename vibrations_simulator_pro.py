#!/usr/bin/env python3
"""
Vibration Simulator - Working Version
"""

import tkinter as tk
from tkinter import ttk
import math

class VibrationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Vibration Simulator v1.0")
        self.root.geometry("900x700")
        
        # Default values
        self.damping = 0.15
        self.natural_freq = 5.0
        self.drive_freq = 5.0
        self.input_amp = 0.1
        
        self.setup_ui()
        self.update_plot()
    
    def setup_ui(self):
        # Control Frame
        control = ttk.Frame(self.root, padding="10")
        control.pack()
        
        # Damping slider
        ttk.Label(control, text="Damping (ζ):").grid(row=0, column=0, sticky="w")
        self.damping_slider = ttk.Scale(control, from_=0.02, to=0.5, 
                                        value=0.15, orient=tk.HORIZONTAL,
                                        length=300, command=self.on_update)
        self.damping_slider.grid(row=0, column=1, padx=10)
        self.damping_label = ttk.Label(control, text="0.150")
        self.damping_label.grid(row=0, column=2)
        
        # Natural Frequency slider
        ttk.Label(control, text="Natural Freq (Hz):").grid(row=1, column=0, sticky="w")
        self.freq_slider = ttk.Scale(control, from_=2, to=12, value=5.0,
                                     orient=tk.HORIZONTAL, length=300,
                                     command=self.on_update)
        self.freq_slider.grid(row=1, column=1, padx=10)
        self.freq_label = ttk.Label(control, text="5.0")
        self.freq_label.grid(row=1, column=2)
        
        # Drive Frequency slider
        ttk.Label(control, text="Drive Freq (Hz):").grid(row=2, column=0, sticky="w")
        self.drive_slider = ttk.Scale(control, from_=1, to=20, value=5.0,
                                      orient=tk.HORIZONTAL, length=300,
                                      command=self.on_update)
        self.drive_slider.grid(row=2, column=1, padx=10)
        self.drive_label = ttk.Label(control, text="5.0")
        self.drive_label.grid(row=2, column=2)
        
        # Canvas for plotting
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg='white')
        self.canvas.pack(pady=20)
        
        # Info text
        self.info = tk.Text(self.root, height=10, width=85, font=("Courier", 9))
        self.info.pack(pady=10)
    
    def transmissibility(self, freq):
        if freq == 0 or self.natural_freq == 0:
            return 1
        r = freq / self.natural_freq
        zeta = self.damping
        num = math.sqrt(1 + (2*zeta*r)**2)
        den = math.sqrt((1 - r**2)**2 + (2*zeta*r)**2)
        return num / den if den != 0 else 1
    
    def head_amplitude(self, freq):
        return self.input_amp * self.transmissibility(freq)
    
    def on_update(self, event=None):
        self.damping = self.damping_slider.get()
        self.natural_freq = self.freq_slider.get()
        self.drive_freq = self.drive_slider.get()
        
        self.damping_label.config(text=f"{self.damping:.3f}")
        self.freq_label.config(text=f"{self.natural_freq:.1f}")
        self.drive_label.config(text=f"{self.drive_freq:.1f}")
        
        self.update_plot()
        self.update_info()
    
    def update_plot(self):
        self.canvas.delete("all")
        
        # Calculate curve
        freqs = [i/10 for i in range(10, 200)]  # 1 to 20 Hz
        amps = [self.head_amplitude(f) for f in freqs]
        
        # Canvas dimensions
        width = 800
        height = 400
        margin = 50
        
        max_amp = max(amps) * 1.1
        if max_amp < 0.1:
            max_amp = 0.5
        
        def x_coord(f):
            return margin + (f - 1) * (width - 2*margin) / 19
        
        def y_coord(a):
            return margin + height - 2*margin - (a * (height - 2*margin) / max_amp)
        
        # Draw axes
        self.canvas.create_line(margin, margin, margin, height-margin, width=2)
        self.canvas.create_line(margin, height-margin, width-margin, height-margin, width=2)
        
        # Draw grid
        for i in range(5):
            x = margin + i * (width - 2*margin) / 4
            self.canvas.create_line(x, margin, x, height-margin, fill="#ccc", dash=(2,2))
        
        for i in range(5):
            y = margin + i * (height - 2*margin) / 4
            self.canvas.create_line(margin, y, width-margin, y, fill="#ccc", dash=(2,2))
        
        # Draw curve
        points = []
        for f, a in zip(freqs, amps):
            points.extend([x_coord(f), y_coord(a)])
        self.canvas.create_line(points, fill='blue', width=2)
        
        # Mark current point
        current_amp = self.head_amplitude(self.drive_freq)
        cx = x_coord(self.drive_freq)
        cy = y_coord(current_amp)
        self.canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill='red', outline='darkred', width=2)
        
        # Mark resonance
        res_x = x_coord(self.natural_freq)
        self.canvas.create_line(res_x, margin, res_x, height-margin, fill='green', dash=(4,2), width=2)
        
        # Labels
        self.canvas.create_text(width/2, height-10, text="Frequency (Hz)", font=("Arial", 10, "bold"))
        self.canvas.create_text(20, height/2, text="Head Amplitude (mm)", angle=90, font=("Arial", 10, "bold"))
    
    def update_info(self):
        current_amp = self.head_amplitude(self.drive_freq)
        peak_amp = self.head_amplitude(self.natural_freq)
        amplification = current_amp / 0.1
        peak_amplification = peak_amp / 0.1
        
        safety = "SAFE"
        safety_color = "green"
        if current_amp >= 1.0:
            safety = "RISK - AVOID"
            safety_color = "red"
        elif current_amp >= 0.3:
            safety = "CAUTION"
            safety_color = "orange"
        
        at_resonance = abs(self.drive_freq - self.natural_freq) < 0.2
        
        info = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         VIBRATION SIMULATOR RESULTS                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PARAMETERS:                                                                 ║
║    Damping Ratio (ζ):     {self.damping:.3f}                                                 ║
║    Natural Frequency:     {self.natural_freq:.1f} Hz                                            ║
║    Drive Frequency:       {self.drive_freq:.1f} Hz                                            ║
║                                                                              ║
║  RESULTS:                                                                    ║
║    Head Amplitude:        {current_amp:.3f} mm                                              ║
║    Amplification:         {amplification:.1f}x                                                ║
║    Peak Amplitude:        {peak_amp:.3f} mm (at {self.natural_freq:.1f} Hz)                              ║
║    Peak Amplification:    {peak_amplification:.1f}x                                             ║
║                                                                              ║
║  SAFETY ASSESSMENT (ISO 2631-1):                                             ║
║    Status:                {safety}                                                      ║
║                                                                              ║
║  RESONANCE STATUS:                                                          ║
║    {'🔴 AT RESONANCE! Maximum energy transfer!' if at_resonance else '🟢 OFF RESONANCE - Safe operation'}              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

💡 TIP: Drag the Drive Frequency slider across {self.natural_freq:.1f} Hz to see resonance!
"""
        self.info.delete(1.0, tk.END)
        self.info.insert(1.0, info)

if __name__ == "__main__":
    root = tk.Tk()
    app = VibrationSimulator(root)
    root.mainloop()