from tkinter import ttk
import sv_ttk

def setup_theme():
    sv_ttk.set_theme("light")

    style = ttk.Style()
    style.configure("TButton", padding=6)
    style.configure("TLabel", padding=4)
    style.configure("Treeview", rowheight=28)
