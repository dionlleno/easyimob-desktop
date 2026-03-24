import os

class LogGerador:
  def __init__(self):
    self.path_log = os.path.join("data", "log.txt")
  
  def criar_log_file(self) -> None:
    try:
      if not os.path.exists(self.path_log):
        with open(self.path_log, 'w', encoding='utf-8') as arquivo:
          arquivo.write("")
    except FileNotFoundError as erro:
      self.salvar_log(titulo="Arquivo nao encontrado", conteudo="Falha ao criar o arquivo de log.", erro=erro)
    except Exception as erro:
      self.salvar_log(titulo="Geral", conteudo="Falha ao criar o arquivo de log.", erro=erro)

  
  def salvar_log(self, titulo: str, conteudo: str, erro: str) -> None:
    try:
      with open(self.path_log, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"\n{titulo}: {conteudo} \n -> {erro}")
    except Exception as erro:
      print("Erro ao salvar log!\n -> {erro}")