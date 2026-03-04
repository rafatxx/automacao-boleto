import os
import time
import glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
USUARIO = os.getenv('LOGIN_USUARIO', "")
SENHA = os.getenv('LOGIN_SENHA', "")
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE", "")
SENHA_EMAIL = os.getenv("SENHA_EMAIL", "")
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO", "")

def enviar_email_com_boleto(caminho_do_pdf):
    print(f"\n Preparando para enviar o arquivo")
    
    mensagem = MIMEMultipart()
    mensagem['From'] = EMAIL_REMETENTE
    mensagem['To'] = EMAIL_DESTINO
    mensagem['Subject'] = "Boleto da Faculdade Impacta"
    
    corpo_email = "Opa, tudo bem?\n\nSegue em anexo o boleto da faculdade deste mês gerado e enviado automaticamente."
    mensagem.attach(MIMEText(corpo_email, 'plain'))

    try:
        with open(caminho_do_pdf, "rb") as arquivo:
            anexo = MIMEApplication(arquivo.read(), _subtype="pdf")
            anexo.add_header('Content-Disposition', 'attachment', filename="Boleto_Faculdade_Mes_Atual.pdf")
            mensagem.attach(anexo)
    except Exception as e:
        print(f" Erro ao ler o anexo: {e}")
        return

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(EMAIL_REMETENTE, SENHA_EMAIL)
        
        texto_mensagem = mensagem.as_string()
        servidor.sendmail(EMAIL_REMETENTE, EMAIL_DESTINO, texto_mensagem)
        servidor.quit()
        print(" E-mail enviado com sucesso!")
    except Exception as e:
        print(f" Erro ao enviar e-mail: {e}")

print("Iniciando o navegador...")
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

url_faculdade = "https://account.impacta.edu.br/"
navegador.get(url_faculdade)

try:
    espera = WebDriverWait(navegador, 15)
    
    campo_usuario = espera.until(EC.presence_of_element_located((By.ID, 'deslogin')))
    campo_usuario.send_keys(USUARIO)
    
    campo_senha = navegador.find_element(By.ID, 'dessenhalogin')
    campo_senha.send_keys(SENHA)

    print("\n" + "="*50)
    print(" ATENÇÃO: O navegador está aguardando você resolver o CAPTCHA")
    print("1. Vá para a janela do Chrome que acabou de abrir.")
    print("2. Resolva o CAPTCHA e clique em FAZER LOGIN.")
    print("3. Volte aqui neste terminal e aperte ENTER para continuar.")
    print("="*50 + "\n")

    input("Pressione ENTER quando já estiver logado no portal")
    print("\nBoa! Agora vou la pegar o boleto para você")

    try:
        espera_curta = WebDriverWait(navegador, 5)
        botao_fechar_1 = espera_curta.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fechar')]")))
        botao_fechar_1.click()
        time.sleep(1)
    except:
        pass

    menu_financeiro_online = espera.until(EC.element_to_be_clickable((By.LINK_TEXT, "Financeiro Online")))
    menu_financeiro_online.click()

    submenu_financeiro = espera.until(EC.element_to_be_clickable((By.LINK_TEXT, "Financeiro")))
    submenu_financeiro.click()

    try:
        espera_curta = WebDriverWait(navegador, 5)
        botao_fechar_2 = espera_curta.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Fechar')]")))
        botao_fechar_2.click()
        time.sleep(1)
    except:
        pass

    boletos = espera.until(EC.presence_of_all_elements_located((By.LINK_TEXT, "Imprimir Boleto")))
    boleto_mais_recente = boletos[-1]
    boleto_mais_recente.click()
    
    print(" Download do boleto iniciado. Aguardando 10 segundos para concluir")
    time.sleep(10) 

    pasta_downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    arquivos_pdf = glob.glob(os.path.join(pasta_downloads, '*.pdf'))
    
    if arquivos_pdf:
        boleto_baixado = max(arquivos_pdf, key=os.path.getctime)
        print(f" Arquivo mais recente encontrado: {os.path.basename(boleto_baixado)}")
        
        enviar_email_com_boleto(boleto_baixado)
    else:
        print("Erro: Nenhum arquivo PDF encontrado na pasta de Downloads.")

except Exception as e:
    print(f"\nOcorreu um erro durante a execução: {e}")

finally:
    navegador.quit()
    print("\nNavegador fechado. Processo finalizado com sucesso!")