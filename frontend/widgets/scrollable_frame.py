import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    """Frame con scrollbar vertical. El contenido va en self.inner."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self._canvas.yview)

        self.inner = ttk.Frame(self._canvas)
        self.inner.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )

        self._win_id = self._canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self._canvas.configure(yscrollcommand=scrollbar.set)
        self._canvas.bind(
            "<Configure>",
            lambda e: self._canvas.itemconfig(self._win_id, width=e.width)
        )

        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._canvas.bind("<Enter>", self._bind_wheel)
        self._canvas.bind("<Leave>", self._unbind_wheel)

    def _bind_wheel(self, _event):
        self._canvas.bind_all("<MouseWheel>", self._on_wheel)

    def _unbind_wheel(self, _event):
        self._canvas.unbind_all("<MouseWheel>")

    def _on_wheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def scroll_to_top(self):
        self._canvas.yview_moveto(0)


def make_scrollable(window, title_widget=None, buttons_widget=None, padx=15, pady=15):
    """
    Envuelve una ventana Toplevel en un layout scrollable estándar.
    Retorna (container, scroll_area) donde scroll_area.inner es donde va el contenido.
    """
    container = ttk.Frame(window)
    container.pack(fill="both", expand=True, padx=padx, pady=pady)

    if title_widget:
        title_widget(container)

    if buttons_widget:
        buttons_widget(container)

    scroll = ScrollableFrame(container)
    scroll.pack(fill="both", expand=True)

    return container, scroll
