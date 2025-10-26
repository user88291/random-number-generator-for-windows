import tkinter as tk
import random

# ----- Config -----
NUMBERS = 6           # how many lotto numbers to pick
POOL_MIN = 1          # inclusive
POOL_MAX = 49         # inclusive
BUTTON_COUNT = 6      # number of visible buttons for picks (matches NUMBERS by default)

# ----- App -----
class LottoPicker(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lotto Random Number Picker")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)

        # Top controls
        controls = tk.Frame(self)
        controls.grid(row=0, column=0, sticky="w", pady=(0,8))

        tk.Label(controls, text="Pool:").grid(row=0, column=0, padx=(0,6))
        self.pool_label = tk.Label(controls, text=f"{POOL_MIN}–{POOL_MAX}")
        self.pool_label.grid(row=0, column=1, padx=(0,12))

        tk.Label(controls, text="Pick:").grid(row=0, column=2, padx=(0,6))
        self.pick_label = tk.Label(controls, text=str(NUMBERS))
        self.pick_label.grid(row=0, column=3, padx=(0,12))

        self.generate_btn = tk.Button(controls, text="Generate", command=self.generate)
        self.generate_btn.grid(row=0, column=4, padx=(0,6))

        self.quick_clear_btn = tk.Button(controls, text="Clear", command=self.clear)
        self.quick_clear_btn.grid(row=0, column=5)

        # Buttons showing numbers
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=1, column=0)

        self.num_buttons = []
        for i in range(BUTTON_COUNT):
            b = tk.Button(self.buttons_frame, text="--", width=6, height=2, command=lambda idx=i: self.toggle_pick(idx))
            b.grid(row=0, column=i, padx=6, pady=6)
            self.num_buttons.append(b)

        # Result / history
        self.result_label = tk.Label(self, text="Click Generate to pick numbers", fg="blue")
        self.result_label.grid(row=2, column=0, pady=(8,0))

        self.history_label = tk.Label(self, text="History:", anchor="w", justify="left")
        self.history_label.grid(row=3, column=0, sticky="w", pady=(6,0))

        self.history_text = tk.Text(self, height=6, width=52, state="disabled", wrap="word")
        self.history_text.grid(row=4, column=0, pady=(4,0))

        # internal state
        self.current_picks = []

    def generate(self):
        # pick unique random numbers from pool
        picks = random.sample(range(POOL_MIN, POOL_MAX + 1), NUMBERS)
        picks.sort()
        self.current_picks = picks

        # fill buttons (show first BUTTON_COUNT picks; if fewer, show --)
        for i, btn in enumerate(self.num_buttons):
            if i < len(picks):
                btn.config(text=str(picks[i]), bg="#f0f0f0")
            else:
                btn.config(text="--", bg="#f0f0f0")

        self.result_label.config(text="Picked: " + ", ".join(map(str, picks)))
        self._append_history(picks)

    def clear(self):
        self.current_picks = []
        for btn in self.num_buttons:
            btn.config(text="--", bg="SystemButtonFace")
        self.result_label.config(text="Cleared")

    def toggle_pick(self, idx):
        # allow user to toggle a button to mark/unmark as a favourite
        btn = self.num_buttons[idx]
        txt = btn.cget("text")
        if txt == "--":
            return
        # toggle background color for marking
        cur_bg = btn.cget("bg")
        new_bg = "#ffd700" if cur_bg != "#ffd700" else "#f0f0f0"
        btn.config(bg=new_bg)

    def _append_history(self, picks):
        line = ", ".join(map(str, picks)) + "\n"
        self.history_text.configure(state="normal")
        self.history_text.insert("end", line)
        self.history_text.configure(state="disabled")
        # auto-scroll
        self.history_text.see("end")

if __name__ == "__main__":
    app = LottoPicker()
    app.mainloop()
                                
