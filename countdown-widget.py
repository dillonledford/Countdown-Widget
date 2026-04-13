import tkinter as tk
import customtkinter as ctk
from datetime import datetime, timedelta


# ---------------- INPUT UI ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

input_window = ctk.CTk()
input_window.configure(fg_color="#212121")
input_window.title("Countdown")
input_window.geometry("230x320")
input_window.resizable(False, False)

title_var = ctk.StringVar()
hours_var = ctk.StringVar()
minutes_var = ctk.StringVar()
seconds_var = ctk.StringVar()

frame = ctk.CTkFrame(input_window, corner_radius=12, fg_color="#212121")
frame.pack(padx=15, pady=15, fill="both", expand=True)

ctk.CTkLabel(frame, text="Title").pack(anchor="w")
ctk.CTkEntry(frame, textvariable=title_var).pack(fill="x", pady=5)

ctk.CTkLabel(frame, text="Hours").pack(anchor="w")
ctk.CTkEntry(frame, textvariable=hours_var).pack(fill="x")

ctk.CTkLabel(frame, text="Minutes").pack(anchor="w")
ctk.CTkEntry(frame, textvariable=minutes_var).pack(fill="x")

ctk.CTkLabel(frame, text="Seconds").pack(anchor="w")
ctk.CTkEntry(frame, textvariable=seconds_var).pack(fill="x")


# ---------------- HUD WINDOW ----------------
countdown_window = tk.Toplevel()
countdown_window.withdraw()
countdown_window.overrideredirect(True)
countdown_window.attributes("-topmost", True)
countdown_window.config(bg="black")
countdown_window.wm_attributes("-transparentcolor", "black")

title_label = tk.Label(
    countdown_window,
    text="",
    font=("Arial", 30),
    fg="white",
    bg="black"
)
title_label.pack(padx=10, pady=(10, 0))

countdown_label = tk.Label(
    countdown_window,
    text="",
    font=("Arial", 36),
    fg="white",
    bg="black"
)
countdown_label.pack(padx=10, pady=(0, 10))


# ---------------- DRAG SUPPORT ----------------
def start_move(event):
    countdown_window._drag_x = event.x
    countdown_window._drag_y = event.y

def do_move(event):
    x = event.x_root - countdown_window._drag_x
    y = event.y_root - countdown_window._drag_y
    countdown_window.geometry(f"+{x}+{y}")

countdown_window.bind("<Button-1>", start_move)
countdown_window.bind("<B1-Motion>", do_move)


# ---------------- RIGHT CLICK MENU ----------------
menu = tk.Menu(countdown_window, tearoff=0)
menu.configure(font=("Arial", 16))
menu.add_command(label="Exit", command=lambda: countdown_window.destroy())

def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

countdown_window.bind("<Button-3>", show_menu)


# ---------------- TIMER LOGIC ----------------
end_time = None
timer_running = False

def update_timer():
    global timer_running

    if not timer_running or end_time is None:
        return

    remaining = end_time - datetime.now()

    if remaining.total_seconds() <= 0:
        countdown_label.config(text="00:00:00")
        timer_running = False
        return

    time_str = str(remaining).split(".")[0]
    countdown_label.config(text=time_str)

    countdown_window.after(1000, update_timer)


def start_countdown():
    global end_time, timer_running

    try:
        h = int(hours_var.get() or 0)
        m = int(minutes_var.get() or 0)
        s = int(seconds_var.get() or 0)
    except ValueError:
        return

    end_time = datetime.now() + timedelta(hours=h, minutes=m, seconds=s)
    timer_running = True

    title_label.config(text=title_var.get())

    # ✅ FIX: don't destroy root window
    input_window.withdraw()
    countdown_window.deiconify()

    update_timer()


# ---------------- START BUTTON ----------------
ctk.CTkButton(frame, text="Start", command=start_countdown).pack(pady=10)


# ---------------- RUN ----------------
input_window.mainloop()
