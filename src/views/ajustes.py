import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class AjustesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        ttk.Label(self, text="Ajustes do Sistema", font=("TkDefaultFont", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        tema_frame = ttk.Labelframe(self, text="Tema", bootstyle="secondary")
        tema_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(tema_frame, text="Selecione o tema:").pack(side="left", padx=5, pady=5)

        temas = tb.Style().theme_names()

        self.tema_var = tk.StringVar(value=tb.Style().theme.name)
        self.tema_combo = ttk.Combobox(
            tema_frame,
            textvariable=self.tema_var,
            values=temas,
            state="readonly"
        )
        self.tema_combo.pack(side="left", padx=5)

        ttk.Button(
            tema_frame,
            text="Aplicar",
            bootstyle="secondary",
            command=self.trocar_tema
        ).pack(side="left", padx=5)

    def trocar_tema(self):
        """Troca o tema da aplica��o em tempo real"""
        novo_tema = self.tema_var.get()
        style = tb.Style()
        style.theme_use(novo_tema)
