# 🎀 TO-DO LIST APP
# Built using Python & Tkinter

import tkinter as tk

# PASTEL PINK COLOR PALETTE

PRIMARY_PINK = "#F8A5C2"
DARK_PINK = "#F78FB3"
LIGHT_PINK = "#FFF0F6"
CARD_BG = "#FFFFFF"
BORDER = "#FADADD"
TEXT_COLOR = "#5E5E5E"
DONE_TEXT = "#B5B5B5"
HIGHLIGHT_DONE = "#FFE3EC"


# MAIN APP CLASS

class ToDoApp:

    def __init__(self, window):
        self.window = window
        self.window.title("My Planner")
        self.window.geometry("460x560")
        self.window.resizable(False, False)
        self.window.configure(bg=LIGHT_PINK)

        self.tasks = []

        self.build_ui()
        self.refresh_list()


    # BUILD UI

    def build_ui(self):

        # Header
        header = tk.Frame(self.window, bg=PRIMARY_PINK, pady=20)
        header.pack(fill="x")

        tk.Label(
            header,
            text="🎀 MY TO-DO PLANNER",
            bg=PRIMARY_PINK,
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack()

        tk.Label(
            header,
            text="Stay productive ✨",
            bg=PRIMARY_PINK,
            fg="white",
            font=("Segoe UI", 9)
        ).pack()

        # Input Section
        input_frame = tk.Frame(self.window, bg=LIGHT_PINK, pady=15, padx=20)
        input_frame.pack(fill="x")

        self.task_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg="white",
            fg=TEXT_COLOR,
            relief="flat"
        )
        self.task_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        add_btn = tk.Button(
            input_frame,
            text="➕ Add 💗",
            font=("Segoe UI", 10, "bold"),
            bg=PRIMARY_PINK,
            fg="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.add_task
        )
        add_btn.pack(side="left")

        add_btn.bind("<Enter>", lambda e: add_btn.config(bg=DARK_PINK))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=PRIMARY_PINK))

        # Counter
        self.counter_label = tk.Label(
            self.window,
            text="",
            bg=LIGHT_PINK,
            fg="#A66C87",
            font=("Segoe UI", 9)
        )
        self.counter_label.pack(anchor="w", padx=22)

        # Task List Container
        list_frame = tk.Frame(self.window, bg=LIGHT_PINK)
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.canvas = tk.Canvas(list_frame, bg=LIGHT_PINK, highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical",
                                 command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.task_container = tk.Frame(self.canvas, bg=LIGHT_PINK)
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.task_container, anchor="nw"
        )

        self.task_container.bind("<Configure>", self.update_scroll)
        self.canvas.bind("<Configure>", self.resize_canvas_window)

        # Clear Button
        tk.Button(
            self.window,
            text="Clear All Tasks :)",
            bg=LIGHT_PINK,
            fg="#C44569",
            relief="flat",
            cursor="hand2",
            command=self.clear_all
        ).pack(pady=8)

    # ADD TASK

    def add_task(self):
        text = self.task_entry.get().strip()
        if text == "":
            return

        self.tasks.append({"text": text, "done": False})

        self.task_entry.delete(0, "end")
        self.refresh_list()


    # TOGGLE DONE
    
    def toggle_done(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.refresh_list()


    # DELETE TASK

    def delete_task(self, index):
        self.tasks.pop(index)
        self.refresh_list()


    # CLEAR ALL

    def clear_all(self):
        self.tasks = []
        self.refresh_list()


    # REFRESH LIST

    def refresh_list(self):

        for widget in self.task_container.winfo_children():
            widget.destroy()

        total = len(self.tasks)
        pending = sum(1 for t in self.tasks if not t["done"])

        if total == 0:
            self.counter_label.config(text="Nothing here yet. Add something! 💕")
            return
        else:
            self.counter_label.config(
                text=f"{pending} remaining  ·  {total - pending} done"
            )

        for i, task in enumerate(self.tasks):
            self.draw_task_row(i, task)


    # DRAW TASK ROW

    def draw_task_row(self, index, task):

        is_done = task["done"]

        row = tk.Frame(
            self.task_container,
            bg=CARD_BG,
            pady=12,
            padx=12,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        row.pack(fill="x", pady=6)

        # Checkbox
        check_symbol = "✓" if is_done else "○"
        check_color = PRIMARY_PINK if is_done else "#D8A7C7"

        check_btn = tk.Button(
            row,
            text=check_symbol,
            font=("Segoe UI", 14),
            bg=CARD_BG,
            fg=check_color,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda i=index: self.toggle_done(i)
        )
        check_btn.pack(side="left", padx=(0, 10))

        # Task Text
        task_color = DONE_TEXT if is_done else TEXT_COLOR

        tk.Label(
            row,
            text=task["text"],
            bg=CARD_BG,
            fg=task_color,
            font=("Segoe UI", 10),
            anchor="w",
            wraplength=300,
            justify="left"
        ).pack(side="left", fill="x", expand=True)

        # Delete Button
        del_btn = tk.Button(
            row,
            text="✕",
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg="#E6A4B4",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda i=index: self.delete_task(i)
        )
        del_btn.pack(side="right")

        del_btn.bind("<Enter>", lambda e: del_btn.config(fg="#C44569"))
        del_btn.bind("<Leave>", lambda e: del_btn.config(fg="#E6A4B4"))


    # SCROLL HELPERS

    def update_scroll(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_canvas_window(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)


# RUN APP

if __name__ == "__main__":
    window = tk.Tk()
    app = ToDoApp(window)
    window.mainloop()