import json
import os
from controllers.logs import LogGerador
from controllers.pendencia import PendenciaJson
from models.cliente import Cliente

class ClienteJson:
  def __init__(self):
    self.path_clientes = os.path.join("data", "clientes.json")
    self.log = LogGerador()
    self.jsonPendencia = PendenciaJson()

  def carregar_json(self, path) -> dict:
    if not os.path.exists(path):
      return []
    try:
      with open(path, '+r', encoding='utf-8') as arquivo:
        return json.load(arquivo)
    except FileNotFoundError as erro:
      self.log.salvar_log(titulo="Arquivo", conteudo="Arquivo de 'Cliente' nao foi encontrado", erro=erro)
    except Exception as erro:
      self.log.salvar_log(titulo="Geral", conteudo="Erro durante a leitura do arquivo de 'Clientes'", erro=erro)
      return []
  
  def salvar_json(self, path, dados: dict) -> None:
    try:
      with open(path, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    except Exception as erro:
      self.log.salvar_log(titulo="Geral", conteudo="Erro durante a escrita do arquivo de 'Clientes'", erro=erro)
  
  def gerar_id(self, dados: dict):
    if not dados:
      return 1
    ultimo_id = max(dado.get("id_cliente") for dado in dados)
    return ultimo_id + 1
  
  def cliente_existe(self, cliente: Cliente, dados: dict) -> bool:
    clientes: list[Cliente] = self.listar_clientes()
    for c in clientes:
      if cliente.nome == c.nome and cliente.email == c.email and cliente.telefone == c.telefone:
        return True
    return False
  
  def buscar_cliente_id(self, id_cliente: int) -> Cliente:
    clientes: list[Cliente]= self.listar_clientes()
    for c in clientes:
      if c.id_cliente == id_cliente:
        return c
    return None

  def listar_clientes(self) -> list[Cliente]:
    dados = self.carregar_json(self.path_clientes)
    clientes: list[Cliente] = []
    for dado in dados:
      cliente = Cliente(
        id_cliente=dado.get("id_cliente"),
        nome=dado.get("nome"),
        email=dado.get("email"),
        telefone=dado.get("telefone"),
        tipo_imovel=dado.get("tipo_imovel"),
        tipo_aquisicao=dado.get("tipo_aquisicao"),
        cidade_desejada=dado.get("cidade_desejado"),
        uf_desejado=dado.get("uf_desejado"),
        orcamento=dado.get("orcamento"),
        pendente=dado.get("pendente"),
        quant_vagas=dado.get("quant_vagas"),
        quant_banheiros=dado.get("quant_banheiros"),
        quant_quartos=dado.get("quant_quartos")
      )
      clientes.append(cliente)
    return clientes

  def adicionar_cliente(self, cliente: Cliente) -> None:
    dados = self.carregar_json(self.path_clientes)
    dados.append(
      {
        "id_cliente": self.gerar_id(dados=dados),
        "nome": cliente.nome.upper(),
        "email": cliente.email.upper(),
        "telefone": cliente.telefone.upper(),
        "tipo_imovel": cliente.tipo_imovel.upper(),
        "tipo_aquisicao": cliente.tipo_aquisicao.upper(),
        "cidade_desejado": cliente.cidade_desejada,
        "uf_desejado": cliente.uf_desejado.upper(),
        "orcamento": cliente.orcamento,
        "pendente": cliente.pendente,
        "quant_vagas": cliente.quant_vagas,
        "quant_banheiros": cliente.quant_banheiros,
        "quant_quartos": cliente.quant_quartos
      }
    )
    self.salvar_json(path=self.path_clientes,dados=dados)
  
  def excluir_cliente(self, id_cliente: int) -> bool:
    clientes: list[Cliente] = self.listar_clientes()
    novos_dados = []
    for cliente in clientes:
      if cliente.id_cliente != id_cliente:
        novos_dados.append({
          "id_cliente": cliente.id_cliente,
          "nome": cliente.nome.upper(),
          "email": cliente.email.upper(),
          "telefone": cliente.telefone.upper(),
          "tipo_imovel": cliente.tipo_imovel.upper(),
          "tipo_aquisicao": cliente.tipo_aquisicao.upper(),
          "cidade_desejado": cliente.cidade_desejada.upper(),
          "uf_desejado": cliente.uf_desejado.upper(),
          "orcamento": cliente.orcamento,
          "pendente": cliente.pendente,
        }
      )
    self.salvar_json(path=self.path_clientes, dados=novos_dados)
  
  def atualizar_cliente(self, cliente: Cliente) -> None:
    clientes: list[Cliente] = self.listar_clientes()
    novos_dados = []
    for c in clientes:
      if c.id_cliente == cliente.id_cliente:
        novos_dados.append({
          "id_cliente": cliente.id_cliente,
          "nome": cliente.nome.upper(),
          "email": cliente.email.upper(),
          "telefone": cliente.telefone.upper(),
          "tipo_imovel": cliente.tipo_imovel.upper(),
          "tipo_aquisicao": cliente.tipo_aquisicao.upper(),
          "cidade_desejado": cliente.cidade_desejada,
          "uf_desejado": cliente.uf_desejado.upper(),
          "orcamento": cliente.orcamento,
          "pendente": cliente.pendente,
          "quant_vagas": cliente.quant_vagas,
          "quant_banheiros": cliente.quant_banheiros,
          "quant_quartos": cliente.quant_quartos
        })
      else:
        novos_dados.append({
          "id_cliente": c.id_cliente,
          "nome": c.nome.upper(),
          "email": c.email.upper(),
          "telefone": c.telefone.upper(),
          "tipo_imovel": c.tipo_imovel.upper(),
          "tipo_aquisicao": c.tipo_aquisicao.upper(),
          "cidade_desejado": c.cidade_desejada,
          "uf_desejado": c.uf_desejado.upper(),
          "orcamento": c.orcamento,
          "pendente": c.pendente,
        })
    self.salvar_json(path=self.path_clientes, dados=novos_dados)
  
  def importar(self, path_new) -> None:
    dados = self.carregar_json(path_new)
    for dado in dados:
      cliente=Cliente(
        id_cliente=None,
        nome=dado.get("nome"),
        email=dado.get("email"),
        telefone=dado.get("telefone"),
        tipo_imovel=dado.get("tipo_imovel"),
        tipo_aquisicao=dado.get("tipo_aquisicao"),
        cidade_desejada=dado.get("cidade_desejada"),
        uf_desejado=dado.get("uf_desejado"),
        orcamento=dado.get("orcamento"),
        pendente=dado.get("pendente")
      )
      self.adicionar_cliente(cliente=cliente)
      if cliente.pendente is False:
        continue
      self.marcar_pendente(id_cliente=cliente.id_cliente, pendente=True)

  def marcar_pendente(self, id_cliente: int, pendente: bool) -> None:
    clientes = self.listar_clientes()
    if pendente:
      for cliente in clientes:
        if cliente.id_cliente == id_cliente:
          cliente.pendente = pendente
          self.atualizar_cliente(cliente=cliente)
          break
      self.jsonPendencia.adicionar_cliente_pendente(id_cliente=id_cliente)
    else:
      for cliente in clientes:
        if cliente.id_cliente == id_cliente:
          cliente.pendente = pendente
          self.atualizar_cliente(cliente=cliente)
          break
      self.jsonPendencia.remover_cliente_pendente(id_cliente=id_cliente)

  def listar_clientes_pendentes(self) -> list[Cliente]:
    clientes = self.listar_clientes()
    pendentes = [cliente for cliente in clientes if cliente.pendente]
    return pendentes

if __name__ == "__main__":
  clienteJson = ClienteJson()
  cliente = Cliente(
    id_cliente=None,
    nome="teste",
    email="email",
    telefone="1212121212",
    tipo_imovel="APARTAMENTO",
    tipo_aquisicao="ALUGUEL",
    cidade_desejada=None,
    uf_desejado="SP",
    orcamento=900,
    pendente=False
    )
  clienteJson.adicionar_cliente(cliente=cliente)
  pass