class Anuncio:
    def __init__(self, id_anuncio: int, titulo: str, link_anuncio: str, link_imagens: list[str], valor_imovel: float, valor_iptu: float, valor_condominio: float, tipo_imovel: str, tipo_aquisicao: str, cidade: str, bairro: str, area: str, quartos: int, banheiros: int, vaga_garagem: int, detalhes_imovel: str, detalhes_condominio: str, ddd: str, uf: str):
        self.id_anuncio = id_anuncio
        self.titulo = titulo
        self.link_anuncio = link_anuncio
        self.link_imagens = link_imagens
        self.valor_imovel = valor_imovel
        self.valor_iptu = valor_iptu
        self.valor_condominio = valor_condominio
        self.tipo_imovel = tipo_imovel
        self.tipo_aquisicao = tipo_aquisicao
        self.cidade = cidade
        self.bairro = bairro
        self.area = area
        self.ddd = ddd
        self.uf = uf
        self.quartos = quartos
        self.banheiros = banheiros
        self.vaga_garagem = vaga_garagem
        self.detalhes_imovel = detalhes_imovel
        self.detalhes_condominio = detalhes_condominio

    def to_dict(self):
        return {
            "id_anuncio": self.id_anuncio,
            "titulo": self.titulo,
            "link_anuncio": self.link_anuncio,
            "link_imagens": self.link_imagens,
            "valor_imovel": self.valor_imovel,
            "valor_iptu": self.valor_iptu,
            "valor_condominio": self.valor_condominio,
            "tipo_imovel": self.tipo_imovel,
            "tipo_aquisicao": self.tipo_aquisicao,
            "cidade": self.cidade,
            "bairro": self.bairro,
            "area": self.area,
            "ddd": self.ddd,
            "uf": self.uf,
            "quartos": self.quartos,
            "banheiros": self.banheiros,
            "vaga_garagem": self.vaga_garagem,
            "detalhes_imovel" : self.detalhes_imovel,
            "detalhes_condominio" : self.detalhes_condominio,
        }

    def __repr__(self):
        return f"Anuncio(id_anuncio={self.id_anuncio}, titulo={self.titulo}, link_anuncio={self.link_anuncio}, link_imagens={self.link_imagens}, valor_imovel={self.valor_imovel}, valor_iptu={self.valor_iptu}, valor_condominio={self.valor_condominio}, tipo_imovel={self.tipo_imovel}, tipo_aquisicao={self.tipo_aquisicao}, cidade={self.cidade}, bairro={self.bairro}, ddd={self.ddd}, uf={self.uf}, area={self.area}, quartos={self.quartos}, banheiros={self.banheiros}, vaga_garagem={self.vaga_garagem}, detalhes_imovel={self.detalhes_imovel}, detalhes_condominio= {self.detalhes_condominio})"
    
    def __str__(self):
        return (
            f"🏠 Anúncio #{self.id_anuncio}\n"
            f"Título: {self.titulo}\n"
            f"Link: {self.link_anuncio}\n"
            f"\n💰 Valores:\n"
            f"  - Aluguel/Venda: R$ {self.valor_imovel}\n"
            f"  - IPTU: R$ {self.valor_iptu or 'Não informado'}\n"
            f"  - Condomínio: R$ {self.valor_condominio or 'Não informado'}\n"
            f"\n📌 Tipo de imóvel: {self.tipo_imovel}\n"
            f"🏷️ Tipo de aquisição: {self.tipo_aquisicao}\n"
            f"\n📍 Localização:\n"
            f"  - Cidade: {self.cidade} - {self.uf}\n"
            f"  - Bairro (DDD {self.ddd}): {self.bairro}\n"
            f"\n📐 Detalhes:\n"
            f"  - Área: {self.area} m² - Quartos: {self.quartos} - Banheiros: {self.banheiros} - Vagas na garagem: {self.vaga_garagem}\n"
            f"\n🧾 Detalhes do imóvel:\n  {self.detalhes_imovel or '  - Nenhum'}\n"
            f"\n🏢 Detalhes do condomínio:\n  {self.detalhes_condominio or '  - Nenhum'}"
            f"\n\nImagens: {', '.join(self.link_imagens) if self.link_imagens else '  - Nenhuma'}\n"
        )
    
    def to_email(self) -> str:
        return (
            f"🏠 Anúncio #{self.id_anuncio}\n"
            f"Título: {self.titulo}\n"
            f"Link: {self.link_anuncio}\n"
            f"\n💰 Valores:\n"
            f"  - Aluguel/Venda: R$ {self.valor_imovel:,.2f}\n"
            f"  - IPTU: R$ {self.valor_iptu:,.2f}" if self.valor_iptu else "Não informado" + "\n"
            f"  - Condomínio: R$ {self.valor_condominio:,.2f}" if self.valor_condominio else "Não informado" + "\n"
            f"\n📌 Tipo de imóvel: {self.tipo_imovel}\n"
            f"🏷️ Tipo de aquisição: {self.tipo_aquisicao}\n"
            f"\n📍 Localização:\n"
            f"  - Cidade: {self.cidade} - {self.uf}\n"
            f"  - Bairro (DDD {self.ddd}): {self.bairro}\n"
            f"\n📐 Detalhes:\n"
            f"  Área: {self.area} m² - Quartos: {self.quartos} - Banheiros: {self.banheiros} - Vagas na garagem: {self.vaga_garagem}\n"
            f"\n🧾 Detalhes do imóvel:\n  {self.detalhes_imovel or 'Nenhum'}\n"
            f"\n🏢 Detalhes do condomínio:\n  {self.detalhes_condominio or 'Nenhum'}\n"
        )
