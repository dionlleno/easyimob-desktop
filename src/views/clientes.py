import tkinter as tk
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from controllers.cliente import ClienteJson
from controllers.filtros import FiltrosJson
from models.anuncio import Anuncio
from models.cliente import Cliente
import ttkbootstrap as tb
import webbrowser
from ttkbootstrap.constants import *

from models.localidade import Localidade
from models.pesquisa import Pesquisa
from utils.extrator_anuncios import ExtratorAnuncios

class ClientesView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.fonte_label = font.Font(family="Helvetica", size=12, weight="bold", slant="italic")
        self.fonte_text  = font.Font(family="Helvetica", size=10)

        self.extrator = ExtratorAnuncios()

        self.jsonFiltros = FiltrosJson()

        self.localidades: list[Localidade] = self.jsonFiltros.listar_localidades()

        self.ufs = self.jsonFiltros.listar_estados()

        self.tipos_imovel = [
            "CASA",
            "APARTAMENTO",
            "QUARTO",
        ]
        self.tipos_aquisicao = [
            "VENDA",
            "ALUGUEL",
            "LANCAMENTOS",
            "COMERCIO-E-INDUSTRIA",
            "TERRENOS",
            "TEMPORADA"
        ]

        self.jsonCliente = ClienteJson()
        self.clientes    = self.jsonCliente.listar_clientes()

        self.cliente = Cliente(None,None,None,None,None,None,None,None,None,None,None,None,None)

        self.varId = tk.StringVar(value="")
        self.varNome = tk.StringVar(value="")
        self.varTelefone = tk.StringVar(value="")
        self.varEmail = tk.StringVar(value="")
        self.varEstado = tk.StringVar(value="")
        self.varCidade = tk.StringVar(value="")
        self.varTipoImovel = tk.StringVar(value="")
        self.varTipoAquisicao = tk.StringVar(value="")
        self.varOrcamento = tk.StringVar(value="")
        self.varPendente = tk.StringVar(value="")
        self.varQuantVagas = tk.StringVar(value="N/A")
        self.varQuantQuartos = tk.StringVar(value="N/A")
        self.varQuantBanheiros = tk.StringVar(value="N/A")
        self.varDetalhes = tk.StringVar(value=f"Vagas: {self.varQuantVagas.get()} - Quartos: {self.varQuantQuartos.get()} - Banheiros: {self.varQuantBanheiros.get()}")
        
        self.varCaixaPesquisa = tk.StringVar(value="")

        # --- Titulo ---
        tb.Label(self, text="Clientes", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=5, pady=5)

        # Frame principal dividido
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        left_frame = ttk.Frame(self.main_frame)
        left_frame.pack(side="left", fill="both", padx=5, pady=5, expand=True)

        right_frame = ttk.Frame(self.main_frame)
        right_frame.pack(side="right", fill="both", padx=5, pady=5, expand=True)

        # --- FILTROS ---
        filtros_frame = tb.Labelframe(left_frame, text="FILTROS", bootstyle="secondary")
        filtros_frame.pack(fill="both", padx=5, pady=5)

        # Nome
        nome_frame = ttk.Frame(filtros_frame)
        nome_frame.pack(fill="x", padx=2)
        self.nome_entry = ttk.Entry(nome_frame, textvariable=self.varCaixaPesquisa)
        self.nome_entry.pack(side="left", fill="x", expand=True, padx=2)
        tb.Button(nome_frame, text="PESQUISAR", command=self.pesquisar).pack(side="right", padx=2)

        # Botões de ações
        botoes_frame = ttk.Frame(filtros_frame)
        botoes_frame.pack(fill="x", pady=5, padx=3)
        tb.Button(botoes_frame, text="ADICIONAR", bootstyle="secondary", command=self.bt_adicionar).pack(side="left", padx=2)
        tb.Button(botoes_frame, text="EXCLUIR", bootstyle="secondary", command=self.bt_excluir).pack(side="left", padx=2)
        tb.Button(botoes_frame, text="ATUALIZAR", bootstyle="secondary", command=self.bt_atualizar).pack(side="left", padx=2)
        tb.Button(botoes_frame, text="IMPORTAR", bootstyle="secondary", command=self.bt_importar).pack(side="left", padx=2)

        # --- LISTAGEM ---
        listagem_frame = tb.Labelframe(left_frame, text="LISTAGEM", bootstyle="secondary")
        listagem_frame.pack(fill="both", padx=5, pady=5, expand=True)

        colunas = ("id", "nome", "tipo_imovel", "tipo_aquisicao", "uf_desejada", "orcamento")
        self.tree = ttk.Treeview(listagem_frame, columns=colunas, show="headings", height=12)

        self.tree.heading("nome", text="NOME")
        self.tree.heading("tipo_imovel", text="TIPO DE IMOVEL")
        self.tree.heading("tipo_aquisicao", text="TIPO DE AQUISICAO")
        self.tree.heading("uf_desejada", text="UF DESEJADA")
        self.tree.heading("orcamento", text="ORCAMENTO")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("nome")
        self.tree.column("orcamento", width=20, anchor="center")
        self.tree.column("uf_desejada", width=20, anchor="center")
        self.tree.column("tipo_imovel", width=30, anchor="center")
        self.tree.column("tipo_aquisicao", width=30, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.carregar_detalhes_cliente)

        # --- CLIENTE (lado direito) ---
        cliente_frame = tb.Labelframe(right_frame, text="CLIENTE", bootstyle="secondary", width=800)
        cliente_frame.pack(fill="both", padx=5, pady=5)

        tb.Label(cliente_frame, text="ID:", font=self.fonte_label).pack(anchor="w")
        tb.Label(cliente_frame, textvariable=self.varId, font=self.fonte_text).pack(fill="x", anchor="w")
        tb.Label(cliente_frame, text="NOME:", font=self.fonte_label).pack(anchor="w")
        tb.Label(cliente_frame, textvariable=self.varNome, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="TELEFONE:", font=self.fonte_label).pack(anchor="w")
        tb.Label(cliente_frame, textvariable=self.varTelefone, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="EMAIL:", font=self.fonte_label).pack(anchor="w")
        tb.Label(cliente_frame, textvariable=self.varEmail, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="ESTADO DESEJADO:", font=self.fonte_label).pack(anchor="w", pady=(5,0))
        tb.Label(cliente_frame, textvariable=self.varEstado, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="CIDADE DESEJADA:", font=self.fonte_label).pack(anchor="w", pady=(5,0))
        tb.Label(cliente_frame, textvariable=self.varCidade, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="TIPO DE IMOVEL:", font=self.fonte_label).pack(anchor="w", pady=(5,0))
        tb.Label(cliente_frame, textvariable=self.varTipoImovel, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="TIPO DE AQUISICAO:", font=self.fonte_label).pack(anchor="w", pady=(5,0))

        tb.Label(cliente_frame, textvariable=self.varTipoAquisicao, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="DETALHES:", font=self.fonte_label).pack(anchor="w", pady=(5,0))

        tb.Label(cliente_frame, textvariable=self.varDetalhes, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="ORCAMENTO:", font=self.fonte_label).pack(anchor="w", pady=(5,0))
        tb.Label(cliente_frame, textvariable=self.varOrcamento, font=self.fonte_text).pack(fill="x")
        tb.Label(cliente_frame, text="PENDENTE:", font=self.fonte_label).pack(anchor="w", pady=(5,0))
        tb.Label(cliente_frame, textvariable=self.varPendente, font=self.fonte_text).pack(fill="x")

        botoes_cliente = ttk.Frame(cliente_frame)
        botoes_cliente.pack(fill="x", pady=5)
        tb.Button(botoes_cliente, text="BUSCAR ANUNCIOS", command=self.buscar_anuncios).pack(side="left", expand=True, padx=2)
        tb.Button(botoes_cliente, text="MARCAR/DESMARCA PENDENTE", command=self.marcar_pendente).pack(side="left", expand=True, padx=2)

        # --- ANUNCIOS ---
        anuncios_frame = tb.Labelframe(right_frame, text="ANUNCIOS", bootstyle="secondary")
        anuncios_frame.pack(fill="both", padx=5, pady=5, expand=True)

        self.anuncios_tree = ttk.Treeview(anuncios_frame, columns=("id", "titulo", "endereco", "area", "valor", "link"), show="headings", height=8)
        self.anuncios_tree.heading("titulo", text="TITULO")
        self.anuncios_tree.heading("valor", text="VALOR")
        self.anuncios_tree.heading("endereco", text="ENDERECO")
        self.anuncios_tree.heading("area", text="AREA")
        self.anuncios_tree.pack(fill="both", expand=True)
        
        self.anuncios_tree.column("id", width=0, stretch=False)
        self.anuncios_tree.column("link", width=0, stretch=False)
        self.anuncios_tree.column("titulo", width=400, anchor="w", stretch=True)
        self.anuncios_tree.column("endereco", width=200, anchor="center")
        self.anuncios_tree.column("area", width=20, anchor="center")
        self.anuncios_tree.column("valor", width=20, anchor="center")

        self.anuncios_tree.bind("<Double-1>", self.abrir_anuncio)

        self.carregar_listagem_clientes(self.clientes)

    def limpar_listagem(self, itens) -> None:
        for item in itens.get_children():
            itens.delete(item)
    
    def limpar_detalhes(self):
        self.varId.set("")
        self.varNome.set("")
        self.varTelefone.set("")
        self.varEmail.set("")
        self.varObservacao.set("")
    
    def carregar_listagem_clientes(self, clientes) -> None:
        self.limpar_listagem(self.tree)
        clientes.sort(key=lambda c: c.nome)
        for cliente in clientes:
            self.tree.insert("", "end", values=[
                cliente.id_cliente,
                cliente.nome,
                cliente.tipo_imovel,
                cliente.tipo_aquisicao,
                cliente.uf_desejado,
                f"R$ {cliente.orcamento}"
            ])

    def carregar_listagem_anuncios(self, anuncios: list[Anuncio]) -> None:
        self.limpar_listagem(self.anuncios_tree)
        anuncios.sort(key=lambda a: a.cidade)
        for anuncio in anuncios:
            self.anuncios_tree.insert("", "end", values=[
                anuncio.id_anuncio,
                anuncio.titulo,
                f"{anuncio.uf} - {anuncio.cidade}",
                f"{anuncio.area} m²",
                f"R$ {anuncio.valor_imovel}",
                anuncio.link_anuncio
            ])

    def carregar_detalhes_cliente(self, event) -> None:
        selecionado = self.tree.focus()
        if selecionado:
            valores = self.tree.item(selecionado, "values")
            self.cliente = self.jsonCliente.buscar_cliente_id(int(valores[0]))
            print(self.cliente)
            self.varId.set(str(self.cliente.id_cliente))
            self.varNome.set(self.cliente.nome.upper())
            self.varTelefone.set(self.cliente.telefone)
            self.varEmail.set(self.cliente.email.upper())
            self.varEstado.set(self.cliente.uf_desejado)
            self.varCidade.set(self.cliente.cidade_desejada)
            self.varTipoImovel.set(self.cliente.tipo_imovel)
            self.varTipoAquisicao.set(self.cliente.tipo_aquisicao)
            self.varOrcamento.set(f"R$ {self.cliente.orcamento}")
            self.varPendente.set("SIM" if self.cliente.pendente else "NAO")
            self.varQuantBanheiros.set(str(self.cliente.quant_banheiros) if self.cliente.quant_banheiros else "N/A")
            self.varQuantQuartos.set(str(self.cliente.quant_quartos) if self.cliente.quant_quartos else "N/A")
            self.varQuantVagas.set(str(self.cliente.quant_vagas) if self.cliente.quant_vagas else "N/A")
            self.varDetalhes.set(f"Vagas: {self.varQuantVagas.get()} - Quartos: {self.varQuantQuartos.get()} - Banheiros: {self.varQuantBanheiros.get()}")

    def pesquisar(self):
        termo = self.varCaixaPesquisa.get().strip().upper()
        filtrados: list[Cliente]= []
        if termo == "":
            self.carregar_listagem_clientes(self.jsonCliente.listar_clientes())
        else:
            for cliente in self.jsonCliente.listar_clientes():
                if termo in cliente.nome.upper() or termo in cliente.telefone or termo in cliente.email.upper():
                    filtrados.append(cliente)
            self.carregar_listagem_clientes(filtrados)

    def buscar_anuncios(self):
        pesquisa = Pesquisa(
            tipo_busca = self.cliente.tipo_aquisicao.lower(),
            quant_paginas=5,
            uf=self.cliente.uf_desejado.lower() if self.cliente.uf_desejado.lower() != "todos" else None,
            orcamento_max=self.cliente.orcamento,
            quant_vagas=self.cliente.quant_vagas,
            quant_banheiros=self.cliente.quant_banheiros,
            quant_quartos=self.cliente.quant_quartos
        )
        anuncios = self.extrator.extrair_anuncios(pesquisa=pesquisa)
        anun = []
        for anuncio in anuncios:
            if anuncio.cidade.upper() == self.cliente.cidade_desejada.upper():
                anun.append(anuncio)
        if len(anun) == 0:
            msg.showinfo("INFO", "NENHUM ANUNCIO ENCONTRADO PARA ESSA CIDADE, MOSTRANDO OUTRAS CIDADES.")
            anun = anuncios
        self.carregar_listagem_anuncios(anuncios=anun)
    
    def abrir_anuncio(self, event):
        anuncio_selecionado = self.anuncios_tree.focus()
        if anuncio_selecionado:
            valores_anuncio = self.anuncios_tree.item(anuncio_selecionado, "values")
            print(f"Abrindo link do anúncio: {valores_anuncio[5]}")
            webbrowser.open(valores_anuncio[5])

    def marcar_pendente(self):
        if self.varId.get().strip() == "":
            msg.showerror("ERRO", "CLIENTE NAO SELECIONADO, SELECIONE UM.")
            return
        id_cliente = int(self.varId.get().strip())
        self.jsonCliente.marcar_pendente(id_cliente=id_cliente, pendente=not self.cliente.pendente)
        self.varPendente.set("SIM" if not self.cliente.pendente else "NAO")
        self.cliente.pendente = not self.cliente.pendente

    def bt_adicionar(self) -> None:
        pop_up = tk.Toplevel(self.main_frame)
        pop_up.title("Adicionar Cliente")
        pop_up.geometry("500x500")

        nome_var = tk.StringVar()
        email_var = tk.StringVar()
        telefone_var = tk.StringVar()
        orcamento_var = tk.StringVar()
        tipo_imovel_var = tk.StringVar()
        tipo_aquisicao_var = tk.StringVar()
        cidade_desejada_var = tk.StringVar()
        uf_desejada_var = tk.StringVar()
        quant_vagas_var = tk.StringVar()
        quant_quartos_var = tk.StringVar()
        quant_banheiros_var = tk.StringVar()

        tb.Label(pop_up, text="NOME:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=nome_var).grid(row=1, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="TELEFONE:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=telefone_var).grid(row=2, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="EMAIL:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=email_var).grid(row=3, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="ORCAMENTO:").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=orcamento_var).grid(row=4, column=1, padx=5, pady=5)

        tb.Label(pop_up, text="QUANT. QUARTOS:").grid(row=5, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=quant_quartos_var).grid(row=5, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="QUANT. BANHEIROS:").grid(row=6, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=quant_banheiros_var).grid(row=6, column=1, padx=5, pady=5)

        tb.Label(pop_up, text="QUANT. VAGAS:").grid(row=7, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=quant_vagas_var).grid(row=7, column=1, padx=5, pady=5)

        tb.Label(pop_up, text="Tipo de Imóvel").grid(row=8, column=0, padx=10, pady=5, sticky=W)
        cb_imovel = ttk.Combobox(pop_up, textvariable=tipo_imovel_var, values=self.tipos_imovel, state="readonly", width=28)
        cb_imovel.grid(row=8, column=1, padx=10, pady=5)
        cb_imovel.current(0)

        tb.Label(pop_up, text="Tipo de Aquisicao").grid(row=9, column=0, padx=10, pady=5, sticky=W)
        cb_aquisicao = ttk.Combobox(pop_up, textvariable=tipo_aquisicao_var, values=self.tipos_aquisicao, state="readonly", width=28)
        cb_aquisicao.grid(row=9, column=1, padx=10, pady=5)
        cb_aquisicao.current(0)
        
        tb.Label(pop_up, text="UF DESEJADA").grid(row=10, column=0, padx=10, pady=5, sticky=W)
        cb_uf = ttk.Combobox(pop_up, textvariable=uf_desejada_var, values=self.ufs, state="readonly", width=28)
        cb_uf.grid(row=10, column=1, padx=10, pady=5)
        cb_uf.current(0)


        tb.Label(pop_up, text="Cidade Desejada").grid(row=11, column=0, padx=10, pady=5, sticky=W)
        self.cb_cidade = ttk.Combobox(pop_up, textvariable=cidade_desejada_var, state="disabled", width=28)
        self.cb_cidade.grid(row=11, column=1, padx=10, pady=5)

        def cidade_filtro(event):
            uf = uf_desejada_var.get()
            for localidade in self.localidades:
                if localidade.uf != uf:
                    continue
                print(localidade.cidades)
                self.cb_cidade.config(values=localidade.cidades, state="readonly")
                self.cb_cidade.current(0)

        def adicionar():
            cliente = Cliente(
                id_cliente=None,
                nome=nome_var.get(),
                email=email_var.get(),
                telefone=telefone_var.get(),
                tipo_aquisicao=tipo_aquisicao_var.get(),
                tipo_imovel=tipo_imovel_var.get(),
                uf_desejado=uf_desejada_var.get(),
                cidade_desejada=cidade_desejada_var.get(),
                orcamento=float(orcamento_var.get()),
                pendente=False,
                quant_quartos=int(quant_quartos_var.get()) if quant_quartos_var.get().strip().isdigit() else None,
                quant_banheiros=int(quant_banheiros_var.get()) if quant_banheiros_var.get().strip().isdigit() else None,
                quant_vagas=int(quant_vagas_var.get()) if quant_vagas_var.get().strip().isdigit() else None,
            )
            self.jsonCliente.adicionar_cliente(cliente=cliente)
            msg.showinfo("SUCESSO", "CLIENTE ADICIONADO COM SUCESSO!")
            self.carregar_listagem_clientes(self.jsonCliente.listar_clientes())
            pop_up.destroy()

        bt_fechar = tb.Button(pop_up, text="FECHAR", command=pop_up.destroy)
        bt_fechar.grid(row=12, column=0)
        bt_avancar = tb.Button(pop_up, text="AVANCAR", command=adicionar)
        bt_avancar.grid(row=12, column=1)

        cb_uf.bind("<<ComboboxSelected>>", cidade_filtro)

    def bt_excluir(self) -> None:
        selecionado = self.tree.focus()
        if selecionado:
            print(msg.askyesno("EXCLUIR", "REALMENTE DESEJA EXCLUIR?"))
            valores = self.tree.item(selecionado, "values")
            if msg.askyesno("EXCLUIR", "REALMENTE DESEJA EXCLUIR?"):
                print(valores)
                self.jsonCliente.excluir_cliente(int(valores[0]))
                self.carregar_listagem_clientes(self.jsonCliente.listar_clientes())
        else:
            msg.showerror("ERRO", "CLIENTE NAO SELECIONADO, SELECIONE UM.")

    def bt_atualizar(self) -> None:
        selecionado = self.tree.focus()
        if not selecionado:
            print(msg.showerror("ERRO", "CLIENTE NAO SELECIONADO, SELECIONE UM."))
            return
        pop_up = tk.Toplevel(self.main_frame)
        pop_up.title("Adicionar Cliente")
        pop_up.geometry("500x500")

        self.cliente = self.jsonCliente.buscar_cliente_id(int(self.tree.item(selecionado, "values")[0]))

        id_var = tk.StringVar(value=self.cliente.id_cliente)
        nome_var = tk.StringVar(value=self.cliente.nome)
        email_var = tk.StringVar(value=self.cliente.email)
        telefone_var = tk.StringVar(value=self.cliente.telefone)
        orcamento_var = tk.StringVar(value=self.cliente.orcamento)
        tipo_imovel_var = tk.StringVar(value=self.cliente.tipo_imovel)
        tipo_aquisicao_var = tk.StringVar(value=self.cliente.tipo_aquisicao)
        cidade_desejada_var = tk.StringVar(value=self.cliente.cidade_desejada)
        uf_desejada_var = tk.StringVar(value=self.cliente.uf_desejado)
        quant_vagas_var = tk.StringVar(value=self.cliente.quant_vagas)
        quant_quartos_var = tk.StringVar(value=self.cliente.quant_quartos)
        quant_banheiros_var = tk.StringVar(value=self.cliente.quant_banheiros)

        tb.Label(pop_up, text="NOME:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=nome_var).grid(row=1, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="TELEFONE:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=telefone_var).grid(row=2, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="EMAIL:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=email_var).grid(row=3, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="ORCAMENTO:").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=orcamento_var).grid(row=4, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="QUANT. QUARTOS:").grid(row=5, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=quant_quartos_var).grid(row=5, column=1, padx=5, pady=5)
        tb.Label(pop_up, text="QUANT. BANHEIROS:").grid(row=6, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=quant_banheiros_var).grid(row=6, column=1, padx=5, pady=5)

        tb.Label(pop_up, text="QUANT. VAGAS:").grid(row=7, column=0, padx=5, pady=5, sticky=W)
        ttk.Entry(pop_up, textvariable=quant_vagas_var).grid(row=7, column=1, padx=5, pady=5)

        tb.Label(pop_up, text="Tipo de Imóvel").grid(row=8, column=0, padx=10, pady=5, sticky=W)
        cb_imovel = ttk.Combobox(pop_up, textvariable=tipo_imovel_var, values=self.tipos_imovel, state="readonly", width=28)
        cb_imovel.grid(row=8, column=1, padx=10, pady=5)
        cb_imovel.current(0)

        tb.Label(pop_up, text="Tipo de Aquisicao").grid(row=9, column=0, padx=10, pady=5, sticky=W)
        cb_aquisicao = ttk.Combobox(pop_up, textvariable=tipo_aquisicao_var, values=self.tipos_aquisicao, state="readonly", width=28)
        cb_aquisicao.grid(row=9, column=1, padx=10, pady=5)
        cb_aquisicao.current(0)
        
        tb.Label(pop_up, text="UF DESEJADA").grid(row=10, column=0, padx=10, pady=5, sticky=W)
        cb_uf = ttk.Combobox(pop_up, textvariable=uf_desejada_var, values=self.ufs, state="readonly", width=28)
        cb_uf.grid(row=10, column=1, padx=10, pady=5)
        cb_uf.current(self.ufs.index(self.cliente.uf_desejado) if self.cliente.uf_desejado in self.ufs else 0)


        tb.Label(pop_up, text="Cidade Desejada").grid(row=11, column=0, padx=10, pady=5, sticky=W)
        self.cb_cidade = ttk.Combobox(pop_up, textvariable=cidade_desejada_var, state="enabled", width=28)
        self.cb_cidade.grid(row=11, column=1, padx=10, pady=5)

        def cidade_filtro(event):
            uf = uf_desejada_var.get()
            for localidade in self.localidades:
                if localidade.uf != uf:
                    continue
                print(localidade.cidades)
                self.cb_cidade.config(values=localidade.cidades, state="readonly")

        def adicionar():
            cliente = Cliente(
                id_cliente=int(id_var.get().strip()),
                nome=nome_var.get(),
                email=email_var.get(),
                telefone=telefone_var.get(),
                tipo_aquisicao=tipo_aquisicao_var.get(),
                tipo_imovel=tipo_imovel_var.get(),
                uf_desejado=uf_desejada_var.get(),
                cidade_desejada=cidade_desejada_var.get(),
                orcamento=float(orcamento_var.get()),
                pendente=False,
                quant_quartos=int(quant_quartos_var.get()) if quant_quartos_var.get().strip().isdigit() else None,
                quant_banheiros=int(quant_banheiros_var.get()) if quant_banheiros_var.get().strip().isdigit() else None,
                quant_vagas=int(quant_vagas_var.get()) if quant_vagas_var.get().strip().isdigit() else None,
            )

            
            self.jsonCliente.atualizar_cliente(cliente=cliente)
            msg.showinfo("SUCESSO", "CLIENTE ADICIONADO COM SUCESSO!")
            self.carregar_listagem_clientes(self.jsonCliente.listar_clientes())
            pop_up.destroy()

        bt_fechar = tb.Button(pop_up, text="FECHAR", command=pop_up.destroy)
        bt_fechar.grid(row=12, column=0)
        bt_avancar = tb.Button(pop_up, text="AVANCAR", command=adicionar)
        bt_avancar.grid(row=12, column=1)

        cb_uf.bind("<<ComboboxSelected>>", cidade_filtro)

    def bt_importar(self) -> None:
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if not caminho_arquivo:
            print(f"Nao: {caminho_arquivo}")
            return
        self.jsonCliente.importar(caminho_arquivo.strip())
        self.carregar_listagem_clientes(self.jsonCliente.listar_clientes())

