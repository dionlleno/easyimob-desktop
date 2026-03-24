import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models.anuncio import Anuncio
from models.cliente import Cliente

class EnviarEmail:
  def __init__(self):
    # Dados do remetente e destinatário
    self.remetente = "dionlleno84@gmail.com"
    self.destinatarios = ["alicevargas.ads@gmail.com","emerson_sj@yahoo.com.br", "diegossandrade2015@gmail.com"]
    self.senha = "ryzn sdxo nftj vhzp "

    # Criando o objeto da mensagem
    self.mensagem = MIMEMultipart()
    self.mensagem['From'] = self.remetente
    self.mensagem['To'] = ", ".join(self.destinatarios)

  def enviar_email_anuncio(self, anuncios: list[Anuncio], cliente: Cliente):
    # Corpo do e-mail
    self.mensagem['Subject'] = f"Novos Anúncios Encontrados para {cliente.nome} - {cliente.id_cliente}"
    anuncios_texto = f"Olá, Alice! Tudo bem? Segue os novos anúncios encontrados: \n{cliente.to_email()}\nAnuncios:\n"
    
    for anuncio in anuncios:
      anuncios_texto = anuncios_texto + anuncio.__str__() + "\n---------------------------------------------\n"
    self.mensagem.attach(MIMEText(anuncios_texto, 'plain'))
    try:
      # Configurando o servidor SMTP do Gmail
      servidor = smtplib.SMTP('smtp.gmail.com', 587)
      servidor.starttls()
      servidor.login(self.remetente, self.senha)

      # Enviando o e-mail
      print(self.mensagem)
      print(anuncios_texto)
      servidor.send_message(self.mensagem)
      print("E-mail enviado com sucesso!")
    except Exception as e: 
      print(f"Erro ao enviar e-mail: {e}")