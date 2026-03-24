class Localidade:
  def __init__(self, estado: str, uf: str, cidades: list[str] = []):
    self.estado = estado
    self.uf = uf
    self.cidades = cidades
  
  def to_dict(self) -> dict:
    return {
      "estado": self.estado,
      "uf": self.uf,
      "cidades": self.cidades
    }
  
  def __str__(self):
    return f"Localidade(estado={self.estado}, uf={self.uf}, cidades={self.cidades})"