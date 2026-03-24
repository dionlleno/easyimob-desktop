from models.anuncio import Anuncio

class Pendencia:
  def __init__(self, id_cliente: int, anuncios_encontrados: list[Anuncio]):
    self.id_cliente = id_cliente
    self.anuncios_encontrados: list[Anuncio] = anuncios_encontrados

  def to_dict(self):
    return {
      "id_cliente": self.id_cliente,
      "anuncios_encontrados": [anuncio.to_dict() for anuncio in self.anuncios_encontrados]
    }
  
  def __repr__(self):
    return f"Pendencia(id_cliente={self.id_cliente}, anuncios_encontrados={self.anuncios_encontrados})"
  
  def __str__(self):
    return f"Pendencia do cliente #{self.id_cliente} com {len(self.anuncios_encontrados)} anúncios encontrados."