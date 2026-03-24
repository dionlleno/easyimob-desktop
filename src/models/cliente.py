from models.pesquisa import Pesquisa


class Cliente:
  def __init__(self, nome: str, email: str, telefone: str, tipo_imovel: str, tipo_aquisicao: str, cidade_desejada: str, uf_desejado: str, orcamento: float, pendente: bool = False, id_cliente: int = None, quant_vagas: int = None, quant_banheiros: int = None, quant_quartos: int = None):
    self.id_cliente = id_cliente
    self.nome = nome
    self.email = email
    self.telefone = telefone
    self.tipo_imovel = tipo_imovel
    self.tipo_aquisicao = tipo_aquisicao
    self.cidade_desejada = cidade_desejada
    self.uf_desejado = uf_desejado
    self.quant_vagas = quant_vagas
    self.quant_banheiros = quant_banheiros
    self.quant_quartos = quant_quartos
    self.orcamento = orcamento
    self.pendente = pendente
  
  def gerar_pesquisa(self) -> Pesquisa:
    return Pesquisa(
      tipo_busca = self.tipo_aquisicao.lower(),
      quant_paginas=1,
      uf=self.uf_desejado.lower(),
      orcamento_max=self.orcamento,
      quant_vagas=self.quant_vagas,
      quant_banheiros=self.quant_banheiros,
      quant_quartos=self.quant_quartos  
    )
  
  def to_dict(self):
    return {
      "id_cliente": self.id_cliente,
      "nome": self.nome,
      "email": self.email,
      "telefone": self.telefone,
      "tipo_imovel": self.tipo_imovel,
      "tipo_aquisicao": self.tipo_aquisicao,
      "cidade_desejada": self.cidade_desejada,
      "uf_desejado": self.uf_desejado,
      "qunt_vagas": self.quant_vagas,
      "quant_banheiros": self.quant_banheiros,
      "quant_quartos": self.quant_quartos,
      "orcamento": self.orcamento,
      "pendente": self.pendente
    }
  
  def __str__(self):
    return f"Cliente(id_cliente={self.id_cliente}, nome={self.nome}, email={self.email}, telefone={self.telefone}, tipo_imovel={self.tipo_imovel}, tipo_aquisicao={self.tipo_aquisicao}, cidade_desejada={self.cidade_desejada}, uf_desejado={self.uf_desejado}, quant_vagas={self.quant_vagas}, quant_quartos={self.quant_quartos}, quant_banheiros={self.quant_banheiros} ,orcamento={self.orcamento}, pendente={self.pendente})"
  
  def to_email(self):
    return f"👤 Cliente #{self.id_cliente}\nNome: {self.nome}\nEmail: {self.email}\nTelefone: {self.telefone}\nTipo de Imóvel: {self.tipo_imovel}\nTipo de Aquisição: {self.tipo_aquisicao}\nCidade Desejada: {self.cidade_desejada}\nUF Desejado: {self.uf_desejado}\nQuantidade de Vagas: {self.quant_vagas or 'Não informado'}\nQuantidade de Quartos: {self.quant_quartos or 'Não informado'}\nQuantidade de Banheiros: {self.quant_banheiros or 'Não informado'}\nOrçamento Máximo: R$ {self.orcamento}\n"