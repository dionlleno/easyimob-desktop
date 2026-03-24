import json
import os

from models.anuncio import Anuncio
from models.pesquisa import Pesquisa
from utils.extrator_anuncios import ExtratorAnuncios

class PendenciaJson:
  def __init__(self):
    self.path_anuncios = os.path.join("data", "anuncios_pendentes.json")
  
  def carregar_json(self, path) -> dict:
    if not os.path.exists(path):
      return []
    try:
      with open(path, 'r', encoding='utf-8') as arquivo:
        return json.load(arquivo)
    except FileNotFoundError as erro:
      print(f"Arquivo nao encontrado -> {path}")
      print(f"Erro: {erro}")
    except json.JSONDecodeError as erro:
      print(f"Erro ao decodificar JSON do arquivo -> {path}")
      print(f"Erro: {erro}")
      return []
  
  def salvar_json(self, path, dados) -> None:
    try:
      with open(path, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    except Exception as erro:
      print(f"Erro ao salvar o arquivo -> {path}")
      print(f"Erro: {erro}") 
  
  def listar_anuncios_pendentes(self, id_cliente) -> list[Anuncio]:
    dados = self.carregar_json(self.path_anuncios)
    anuncios: list[Anuncio] = []
    for dado in dados:
      if dado.get("id_cliente") == id_cliente:
        a = dado.get("anuncios_encontrados", {})
        for anuncio in a:
          anuncios.append(Anuncio(
            id_anuncio=int(anuncio.get("id_anuncio")),
            titulo=anuncio.get("titulo"),
            link_anuncio=anuncio.get("link_anuncio"),
            link_imagens=anuncio.get("link_imagens", []),
            valor_imovel=anuncio.get("valor_imovel"),
            valor_condominio=anuncio.get("valor_condominio"),
            valor_iptu=anuncio.get("valor_iptu"),
            area=anuncio.get("area"),
            tipo_imovel=anuncio.get("tipo_imovel"),
            tipo_aquisicao=anuncio.get("tipo_aquisicao"),
            cidade=anuncio.get("cidade"),
            bairro=anuncio.get("bairro"),
            ddd=anuncio.get("ddd"),
            uf=anuncio.get("uf"),
            quartos=anuncio.get("quartos"),
            banheiros=anuncio.get("banheiros"),
            vaga_garagem=anuncio.get("vaga_garagem"),
            detalhes_imovel=anuncio.get("detalhes_imovel"),
            detalhes_condominio=anuncio.get("detalhes_condominio"),
          ))
        return anuncios
    return []

  def adicionar_cliente_pendente(self, id_cliente: int) -> None:
    dados = self.carregar_json(self.path_anuncios)
    for dado in dados:
      if dado.get("id_cliente") == id_cliente:
        return
    dados.append({
      "id_cliente": id_cliente,
      "anuncios_encontrados": []
    })
    self.salvar_json(path=self.path_anuncios, dados=dados)
  
  def remover_cliente_pendente(self, id_cliente: int) -> None:
    dados = self.carregar_json(self.path_anuncios)
    dados_filtrados = []
    for dado in dados:
      if dado.get("id_cliente") != id_cliente:
        dados_filtrados.append(dado)
    self.salvar_json(path=self.path_anuncios, dados=dados_filtrados)

  def adicionar_anuncio_pendente(self, id_cliente: int, anuncios: list[Anuncio]) -> None:
    dados = self.carregar_json(self.path_anuncios)
    for dado in dados:
      if id_cliente == dado.get("id_cliente"):
        novos_anuncios = dado.get("anuncios_encontrados", [])
        for anuncio in anuncios:
          if any(a.get("titulo") == anuncio.titulo for a in novos_anuncios):
            print("Anuncio ja existe na lista de pendentes.")
            continue
          novos_anuncios.append({
            "id_anuncio": anuncio.id_anuncio,
            "titulo": anuncio.titulo,
            "link_anuncio": anuncio.link_anuncio,
            "link_imagens": anuncio.link_imagens,
            "valor_imovel": anuncio.valor_imovel,
            "valor_condominio": anuncio.valor_condominio,
            "valor_iptu": anuncio.valor_iptu,
            "area": anuncio.area,
            "tipo_imovel": anuncio.tipo_imovel,
            "tipo_aquisicao": anuncio.tipo_aquisicao,
            "cidade": anuncio.cidade,
            "bairro": anuncio.bairro,
            "ddd": anuncio.ddd,
            "uf": anuncio.uf,
            "quartos": anuncio.quartos,
            "banheiros": anuncio.banheiros,
            "vaga_garagem": anuncio.vaga_garagem,
            "detalhes_imovel": anuncio.detalhes_imovel,
            "detalhes_condominio": anuncio.detalhes_condominio,
          })
        dado["anuncios_encontrados"] = novos_anuncios
        break
    self.salvar_json(path=self.path_anuncios, dados=dados)

  def remover_anuncios_pendentes(self, id_cliente: int) -> None:
    dados = self.carregar_json(self.path_anuncios)
    dados_filtrados = []
    for dado in dados:
      if dado.get("id_cliente") != id_cliente:
        dados_filtrados.append(dado)
    self.salvar_json(path=self.path_anuncios, dados=dados_filtrados)

if __name__ == "__main__":
  """
  jsonPendencia = PendenciaJson()
  anuncios = jsonPendencia.listar_anuncios_pendentes(id_cliente=1)
  for anuncio in anuncios:
  pendencia = PendenciaJson()
  pendencia.remover_anuncios_pendentes(id_cliente=1)
  """
  anuncio_json = PendenciaJson()
  anuncios = anuncio_json.listar_anuncios_pendentes(id_cliente=1)
  extrator = ExtratorAnuncios()
  pesquisa = Pesquisa(
    tipo_busca="aluguel",
    quant_paginas=1,
    uf="SP",
    orcamento_max=None,
    quant_vagas=None,
    quant_quartos=None,
    quant_banheiros=None)
  anuncios = extrator.extrair_anuncios(pesquisa=pesquisa)
  for anuncio in anuncios:
    anuncio_json.adicionar_anuncio_pendente(id_cliente=1, anuncio=anuncio)