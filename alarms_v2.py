# -*- coding: utf-8 -*-
"""
Countdown Timer v2.0 - Tkinter GUI + Optional Anti-Sleep Mouse Mover
Author: Avtomat Agentics
Updated: 2025-11-10

Description:
A modern Python countdown timer built with Tkinter.
It allows preset or custom times, includes pause/reset functionality,
and plays a sound when finished. Optionally, it can move the mouse
periodically to prevent screen lock ("hover mouse" mode).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from time import perf_counter, sleep
from threading import Thread, Event
import pyautogui
from pygame import mixer

# ============================================================
# PRESET ACTIVITIES (label, seconds)
# ============================================================

PRESETS = {
    "Abdominales": 1680,
    "Flexiones": 1200,
    "Flexibilidad": 600,
    "Muslos": 600,
    "Preparación": 240,
    "Machine Learning": 5400,
    "Python": 5400,
    "Languages": 5400,
    "TFG": 7200,
    "Custom": None
}


# ============================================================
# TIMER CLASS
# ============================================================

class CountdownTimer:
    """Handles timer logic, pausing, and optional anti-sleep mouse movement."""

    def __init__(self, update_callback, finish_callback):
        self.total_time = 0
        self.remaining_time = 0
        self.running = False
        self.paused = False
        self.hover_mode = False
        self._update_callback = update_callback
        self._finish_callback = finish_callback
        self._stop_event = Event()
        self._thread = None

    def start(self, seconds, hover=False):
        """Start the countdown timer."""
        if self.running:
            return
        self.total_time = seconds
        self.remaining_time = seconds
        self.hover_mode = hover
        self.running = True
        self.paused = False
        self._stop_event.clear()
        self._thread = Thread(target=self._run)
        self._thread.start()

    def _run(self):
        last_move = 0
        start_time = perf_counter()
        while self.remaining_time > 0 and not self._stop_event.is_set():
            if not self.paused:
                elapsed = perf_counter() - start_time
                self.remaining_time = self.total_time - elapsed

                # Move mouse every 5 seconds if hover mode is active
                if self.hover_mode and int(elapsed) - last_move >= 5:
                    x, y = pyautogui.position()
                    pyautogui.moveTo(x + 10, y + 10, duration=0.1)
                    pyautogui.moveTo(x, y, duration=0.1)
                    last_move = int(elapsed)

                # Update GUI every second
                self._update_callback(max(0, int(self.remaining_time)))
                sleep(0.2)
            else:
                start_time = perf_counter() - (self.total_time - self.remaining_time)
                sleep(0.1)

        if not self._stop_event.is_set():
            self.running = False
            self._finish_callback()

    def pause(self):
        """Pause the timer."""
        if self.running:
            self.paused = True

    def resume(self):
        """Resume the timer."""
        if self.running and self.paused:
            self.paused = False

    def reset(self):
        """Stop and reset timer."""
        self._stop_event.set()
        self.running = False
        self.paused = False
        self.remaining_time = 0
        self._update_callback(0)


# ============================================================
# GUI SETUP
# ============================================================

class TimerApp(tk.Tk):
    """Tkinter GUI for the countdown timer."""

    def __init__(self):
        super().__init__()
        self.title("Countdown Timer v2.0")
        self.geometry("400x380")
        self.resizable(False, False)

        self.timer = CountdownTimer(self.update_display, self.on_finish)

        # --- GUI Elements ---
        ttk.Label(self, text="⏱ Countdown Timer", font=("Arial", 16, "bold")).pack(pady=10)

        # Dropdown for presets
        self.choice_var = tk.StringVar(value="Abdominales")
        ttk.Label(self, text="Select activity:").pack()
        self.preset_menu = ttk.Combobox(self, textvariable=self.choice_var, values=list(PRESETS.keys()), state="readonly")
        self.preset_menu.pack(pady=5)

        # Manual time entry
        frame_time = ttk.Frame(self)
        frame_time.pack(pady=5)
        ttk.Label(frame_time, text="Hours:").grid(row=0, column=0)
        ttk.Label(frame_time, text="Minutes:").grid(row=0, column=2)
        ttk.Label(frame_time, text="Seconds:").grid(row=0, column=4)

        self.h_var = tk.IntVar(value=0)
        self.m_var = tk.IntVar(value=0)
        self.s_var = tk.IntVar(value=0)
        ttk.Entry(frame_time, textvariable=self.h_var, width=5).grid(row=0, column=1)
        ttk.Entry(frame_time, textvariable=self.m_var, width=5).grid(row=0, column=3)
        ttk.Entry(frame_time, textvariable=self.s_var, width=5).grid(row=0, column=5)

        # Hover checkbox
        self.hover_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Activate anti-sleep (hover mouse)", variable=self.hover_var).pack(pady=5)

        # Timer label
        self.time_label = ttk.Label(self, text="00:00:00", font=("Consolas", 28))
        self.time_label.pack(pady=10)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Start", command=self.start_timer).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Pause", command=self.timer.pause).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Resume", command=self.timer.resume).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.timer.reset).grid(row=0, column=3, padx=5)

        # Progress bar
        self.progress = ttk.Progressbar(self, maximum=100, length=250)
        self.progress.pack(pady=10)

    # ========================================================
    # TIMER CONTROL
    # ========================================================

    def start_timer(self):
        """Start the timer based on preset or manual input."""
        choice = self.choice_var.get()
        seconds = PRESETS.get(choice)

        if seconds is None:
            seconds = int(self.h_var.get()) * 3600 + int(self.m_var.get()) * 60 + int(self.s_var.get())

        if seconds <= 0:
            messagebox.showwarning("Invalid time", "Please enter a positive duration.")
            return

        hover = self.hover_var.get()
        self.timer.start(seconds, hover=hover)

    def update_display(self, seconds_left):
        """Update timer label and progress bar."""
        h = seconds_left // 3600
        m = (seconds_left % 3600) // 60
        s = seconds_left % 60
        self.time_label.config(text=f"{h:02}:{m:02}:{s:02}")

        # Progress percentage
        if self.timer.total_time > 0:
            progress = ((self.timer.total_time - seconds_left) / self.timer.total_time) * 100
            self.progress["value"] = progress

        self.update_idletasks()

    def on_finish(self):
        """Play sound and show message when time is up."""
        mixer.init()
        try:
            mixer.music.load("sirena.mp3")
            mixer.music.play()
        except Exception:
            messagebox.showinfo("Time's up!", "Countdown finished! (No sound file found)")

        messagebox.showinfo("Finished!", "⏰ Time is up!")

        # Reset display
        self.timer.reset()


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    app = TimerApp()
    app.mainloop()