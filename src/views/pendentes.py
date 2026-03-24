import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from tkinter import messagebox as msg
from ttkbootstrap.constants import *

from controllers.cliente import ClienteJson
from controllers.pendencia import PendenciaJson
from models.pesquisa import Pesquisa
from utils.extrator_anuncios import ExtratorAnuncios

class PendentesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.jsonCliente = ClienteJson()
        self.jsonPendencia = PendenciaJson()
        self.extrator = ExtratorAnuncios()

        ttk.Label(self, text="Pendencias", font=("TkDefaultFont", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        colunas = ("id", "nome", "tipo_imovel", "tipo_aquisicao", "uf_desejada", "orcamento", "total_anuncios")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings", height=12)

        self.tree.heading("nome", text="NOME")
        self.tree.heading("tipo_imovel", text="TIPO DE IMOVEL")
        self.tree.heading("tipo_aquisicao", text="TIPO DE AQUISICAO")
        self.tree.heading("uf_desejada", text="UF DESEJADA")
        self.tree.heading("orcamento", text="ORCAMENTO")
        self.tree.heading("total_anuncios", text="TOTAL ANUNCIOS")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome")
        self.tree.column("orcamento", width=20, anchor="center")
        self.tree.column("uf_desejada", width=20, anchor="center")
        self.tree.column("tipo_imovel", width=30, anchor="center")
        self.tree.column("tipo_aquisicao", width=30, anchor="center")
        self.tree.column("total_anuncios", width=30, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.carregar_popup_listagem_anuncios)

        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(botoes_frame, text="REMOVER", command=self.remover_pendente, bootstyle="danger").pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="ATUALIZAR", command=self.atualizar_pendentes, bootstyle="secondary").pack(side="left", padx=5)
        ttk.Button(botoes_frame, text="BUSCAR ANUNCIOS", command=self.buscar_anuncios_pendentes, bootstyle="secondary").pack(side="left", padx=5)

        self.carregar_clientes_pendentes()
    
    def limpar_listagem(self, itens) -> None:
        for item in itens.get_children():
            itens.delete(item)
    
    def carregar_clientes_pendentes(self):
        self.limpar_listagem(self.tree)
        for cliente in self.jsonCliente.listar_clientes_pendentes():
            self.tree.insert("", "end", values=(
                cliente.id_cliente,
                cliente.nome,
                cliente.tipo_imovel,
                cliente.tipo_aquisicao,
                cliente.uf_desejado,
                f"R$ {cliente.orcamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                len(self.jsonPendencia.listar_anuncios_pendentes(id_cliente=cliente.id_cliente))
            ))
    
    def atualizar_pendentes(self):
        self.carregar_clientes_pendentes()

    def remover_pendente(self) -> None:
        selecionado = self.tree.focus()
        if selecionado:
            valores = self.tree.item(selecionado, "values")
            self.jsonCliente.marcar_pendente(id_cliente=int(valores[0]), pendente=False)
            self.carregar_clientes_pendentes()
        else:
            msg.showwarning("ATENCAO", "NENHUM CLIENTE SELECIONADO.")

    def carregar_popup_listagem_anuncios(self, event) -> None:
        selecionado = self.tree.focus()
        if not selecionado:
            msg.showwarning("ATENCAO", "NENHUM CLIENTE SELECIONADO.")
            return None
        valores = self.tree.item(selecionado, "values")
        id_cliente = int(valores[0])

        pop_up = tk.Toplevel(self)
        pop_up.title("Adicionar Cliente")
        pop_up.geometry("500x500")

        anuncios_frame = tb.Labelframe(pop_up, text="ANUNCIOS", bootstyle="secondary")
        anuncios_frame.pack(fill="both", padx=5, pady=5, expand=True)

        anuncios_tree = ttk.Treeview(anuncios_frame, columns=("id", "titulo", "endereco", "area", "valor", "link"), show="headings", height=8)
        anuncios_tree.heading("titulo", text="TITULO")
        anuncios_tree.heading("valor", text="VALOR")
        anuncios_tree.heading("endereco", text="ENDERECO")
        anuncios_tree.heading("area", text="AREA")
        anuncios_tree.pack(fill="both", expand=True)
        
        anuncios_tree.column("id", width=0, stretch=False)
        anuncios_tree.column("link", width=0, stretch=False)
        anuncios_tree.column("titulo", width=400, anchor="w", stretch=True)
        anuncios_tree.column("endereco", width=200, anchor="center")
        anuncios_tree.column("area", width=20, anchor="center")
        anuncios_tree.column("valor", width=20, anchor="center")

        self.limpar_listagem(anuncios_tree)

        anuncios = self.jsonPendencia.listar_anuncios_pendentes(id_cliente=id_cliente)
        for anuncio in anuncios:
            anuncios_tree.insert("", "end", values=(
                anuncio.id_anuncio,
                anuncio.titulo,
                f"{anuncio.bairro} - {anuncio.cidade}/{anuncio.uf}",
                f"{anuncio.area} m²" if anuncio.area else "N/A",
                f"R$ {anuncio.valor_imovel:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if anuncio.valor_imovel else "N/A",
                anuncio.link_anuncio
            ))
        def abrir_anuncio(event) -> None:
            selecionado = anuncios_tree.focus()
            if not selecionado:
                msg.showwarning("ATENCAO", "NENHUM ANUNCIO SELECIONADO.")
                return None
            valores = anuncios_tree.item(selecionado, "values")
            link = valores[5]
            import webbrowser
            webbrowser.open(link)

        anuncios_tree.bind("<Double-1>", abrir_anuncio)

    def buscar_anuncios_pendentes(self) -> None:
        selecionado = self.tree.focus()
        if not selecionado:
            msg.showwarning("ATENCAO", "NENHUM CLIENTE SELECIONADO.")
            return None
        valores = self.tree.item(selecionado, "values")
        id_cliente = int(valores[0])
        cliente = self.jsonCliente.buscar_cliente_id(id_cliente=id_cliente)
        msg.showinfo("INFO", f"Iniciando busca de novos anuncios para o cliente {cliente.id_cliente} - {cliente.nome}...")
        pesquisa: Pesquisa = cliente.gerar_pesquisa()
        pesquisa.quant_paginas = 5
        anuncios = self.extrator.extrair_anuncios(pesquisa=pesquisa)
        a = []
        for anuncio in anuncios:
            if anuncio.cidade.upper() == cliente.cidade_desejada.upper():
                a.append(anuncio)
        msg.showinfo("INFO", f"Foram encontrados {len(a)} novos anuncios para o cliente {cliente.id_cliente} - {cliente.nome}.")
        if len(a) == 0:
            msg.showinfo("INFO", f"Nenhum novo anuncio encontrado para o cliente {cliente.id_cliente} - {cliente.nome}.")
            return None
        self.jsonPendencia.adicionar_anuncio_pendente(id_cliente=cliente.id_cliente, anuncios=a)
        self.carregar_clientes_pendentes()

