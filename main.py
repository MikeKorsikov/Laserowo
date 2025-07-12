# --- main.py ---
import tkinter as tk
from views.main_window import MainWindow
from config.database import init_db

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
