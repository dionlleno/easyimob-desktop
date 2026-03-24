import json, os, cloudscraper
from parsel import Selector
from models.anuncio import Anuncio
from models.pesquisa import Pesquisa
 
class ExtratorAnuncios:
  def __init__(self):
    self.scraper = cloudscraper.create_scraper()
    self.headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0"
    }
    self.base_url = "https://www.olx.com.br/imoveis"
    self.path_filtro_estado_cidade = os.path.join("data", "estados_cidades.json")

  def carregar_json(self, path):
    if not os.path.exists(path):
      return {}
    with open(path, 'r', encoding='utf-8') as arquivo:
      return json.load(arquivo)

  def gerar_urls(self, pesquisa: Pesquisa) -> list[str]:
    if pesquisa.uf == "TODOS" : link_uf = ""
    else:                       link_uf = f"estado-{pesquisa.uf}"

    if pesquisa.orcamento_max == None:
      link_orcamento = ""
    else:
      link_orcamento = f"&pe={str(pesquisa.orcamento_max)}" 

    if pesquisa.quant_vagas == None:
      link_vagas = ""
    else:
      link_vagas = f"&gsp={str(pesquisa.quant_vagas)}"

    if pesquisa.quant_quartos == None:
      link_quartos   = ""
    else:
      link_quartos = f"&ros={str(pesquisa.quant_quartos)}"

    if pesquisa.quant_banheiros == None:
      link_banheiros = ""
    else:
      link_banheiros = f"&bas={str(pesquisa.quant_banheiros)}"

    link = f"{self.base_url}/{pesquisa.tipo_busca}/{link_uf}?{link_orcamento}{link_vagas}{link_quartos}{link_banheiros}"
    urls = [f"{link}&o={i}" for i in range(1, pesquisa.quant_paginas + 1)]
    return urls

  def listar_cidades(self, anuncios: list[Anuncio], uf) -> list[str]:
    cidades = []
    for anuncio in anuncios:
      if anuncio.uf == uf:
        if anuncio.cidade not in cidades:
          cidades.append(anuncio.cidade)
    return sorted(list(set(cidades)))
  
  def listar_estados(self, anuncios: list[Anuncio]) -> list[str]:
    ufs = []
    for anuncio in anuncios:
      if anuncio.uf not in ufs:
        ufs.append(anuncio.uf)
    limpa = list(set(ufs))
    return sorted(limpa)

  def extrair_anuncios(self, pesquisa: Pesquisa) -> list[Anuncio]:
    anuncios: list[Anuncio] = []
    indice = 1
    for url in self.gerar_urls(pesquisa):
      print(url)
      resposta = self.scraper.get(url=url, headers=self.headers).text
      seletor = Selector(text=resposta)
      resultado = seletor.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
      json_data = json.loads(resultado)
      resultados = json_data.get("props", {}).get("pageProps", {}).get("ads", [])
      for item in resultados:
        # Filtrando PROPAGANDAS
        if "advertisingId" in item:
          continue
        # Extraindo IMAGENS
        imagens: list[str] = []
        for imagem in item.get("images", []):
          imagens.append(imagem.get("original"))

        # Extraindo ENDERECO
        endereco = item.get("locationDetails")
        cidade = endereco.get("neighbourhood", "Não informado")
        uf = endereco.get("uf", "Não informado")
        bairro = endereco.get("municipality", "Não informado")
        ddd = endereco.get("ddd")

        # Extraindo DETALHES DO IMÓVEL
        tipo_imovel = "Não informado"
        tipo_aquisicao = "Não informado"
        area = '0'
        quartos = 0
        banheiros = 0
        vaga_garagem = 0
        valor_condominio = 0.0
        valor_iptu = 0.0
        detalhes_imovel = "Não informado"
        detalhes_condominio = "Não informado"


        for prop in item.get("properties", []):
            match prop.get("name"):
                case "category":
                    tipo_imovel = prop.get("value")
                    continue
                case "real_estate_type":
                    tipo_aquisicao = prop.get("value")
                    continue
                case "size":
                    area = prop.get("value")
                    continue
                case "rooms":
                    try:
                        quartos = int(prop.get("value"))
                    except (ValueError, TypeError):
                        quartos = 0
                    continue
                case "bathrooms":
                    try:
                        banheiros = int(prop.get("value"))
                    except (ValueError, TypeError):
                        banheiros = 0
                    continue
                case "garage_spaces":
                    try:
                        vaga_garagem = int(prop.get("value"))
                    except (ValueError, TypeError):
                        vaga_garagem = 0
                    continue
                case "re_features":
                    detalhes_imovel = prop.get("value", "Não informado")
                    continue
                case "re_complex_features":
                    detalhes_condominio = prop.get("value", "Não informado")
                    continue
                case "condominio":
                    try:
                        valor_condominio = float(prop.get("value").replace("R$ ", "").replace(".", "").replace(",", "."))
                    except (ValueError, AttributeError):
                        valor_condominio = 0.0
                    continue
                case "iptu":
                    try:
                        valor_iptu = float(prop.get("value").replace("R$ ", "").replace(".", "").replace(",", "."))
                    except (ValueError, AttributeError):
                        valor_iptu = 0.0
                    continue

        anuncio = Anuncio(
          id_anuncio=indice,
          titulo = item.get("subject").strip() if item.get("subject") else "Sem título",
          link_anuncio = item.get("friendlyUrl").strip() if item.get("friendlyUrl") else "Sem link",
          link_imagens = imagens,
          valor_imovel = float(item.get("priceValue").replace("R$ ", "").replace(".", "").replace(",", ".")) if item.get("priceValue") else 0.0,
          valor_iptu = valor_iptu,
          valor_condominio = valor_condominio,
          tipo_imovel = tipo_imovel,
          tipo_aquisicao = tipo_aquisicao,
          ddd = ddd,
          cidade = cidade,
          bairro = bairro,
          uf = uf,
          area = area,
          quartos = quartos,
          banheiros = banheiros,
          vaga_garagem = vaga_garagem,
          detalhes_imovel = detalhes_imovel,
          detalhes_condominio = detalhes_condominio,
        )
        anuncios.append(anuncio)
        #print(f"Anúncio extraído: {anuncio}")
        indice += 1
    return anuncios
  
  def atualizar_filtros(self):
    aluguel = Pesquisa(
      tipo_busca="aluguel",
      quant_paginas=5,
      uf=None,
      orcamento_max=None,
      quant_vagas=None,
      quant_quartos=None,
      quant_banheiros=None)
    venda = Pesquisa(
      tipo_busca="venda",
      quant_paginas=5,
      uf=None,
      orcamento_max=None,
      quant_vagas=None,
      quant_quartos=None,
      quant_banheiros=None)
    anuncios_aluguel = self.extrair_anuncios(aluguel)
    anuncios_venda = self.extrair_anuncios(venda)
    anuncios = anuncios_aluguel + anuncios_venda
    ufs = self.listar_estados(anuncios=anuncios)
    dados = self.carregar_json(self.path_filtro_estado_cidade) 
    print(ufs)
    for uf in ufs:
      novas_cidades = self.listar_cidades(anuncios=anuncios, uf=uf)
      break

if __name__ == "__main__":
  """
  filtros = Extrator()
  filtros.atualizar_filtros()
  """
  pesquisa = Pesquisa(
    tipo_busca="aluguel",
    quant_paginas=5,
    uf="df",
    orcamento_max=None,
    quant_vagas=None,
    quant_quartos=None,
    quant_banheiros=None
  )
  extrator = ExtratorAnuncios()
  anuncios = extrator.extrair_anuncios(pesquisa=pesquisa)
  for anuncio in anuncios:
    print(anuncio.cidade)
    if "Recanto das Emas" in anuncio.cidade:
      print(anuncio)