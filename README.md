# Automação de Boleto - Faculdade Impacta

Este é um projeto de automação em Python desenvolvido para acessar o portal do aluno da Faculdade Impacta, realizar o download do boleto mensal de forma autônoma e enviá-lo automaticamente para um endereço de e-mail pré-configurado.

## Funcionalidades

- **Web Scraping & Navegação:** Acesso automatizado ao portal acadêmico utilizando `Selenium WebDriver`.
- **Espera Inteligente:** O script faz uma pausa programada, aguardando a intervenção humana apenas para a resolução do CAPTCHA do Google (medida de segurança do site), e retoma o controle em seguida.
- **Manipulação de Arquivos (OS):** Varredura automática na pasta de *Downloads* do Windows para localizar o PDF mais recente baixado.
- **Disparo de E-mail (SMTP):** Envio silencioso (em background) do boleto em anexo utilizando a biblioteca `smtplib` e uma senha de aplicativo do Gmail.
- **Execução Agendada:** Integração com o Agendador de Tarefas do Windows via script `.bat` para rodar a automação todo mês automaticamente.

## Tecnologias Utilizadas

- **Python 3**
- **Selenium** (Automação Web)
- **Webdriver Manager** (Gerenciamento automático do ChromeDriver)
- **Python-dotenv** (Segurança de credenciais)
- **SMTP Library** (Envio de e-mails)
- **Scripting em Batch (.bat)**

## Como configurar e rodar o projeto

### 1. Pré-requisitos
- Ter o [Python](https://www.python.org/) instalado.
- Ter o navegador Google Chrome instalado.
- Ter uma conta do Google/Gmail com a **Verificação em Duas Etapas** ativada e uma **Senha de Aplicativo** gerada.

### 2. Instalação
Clone este repositório no seu computador:

```bash
git clone [https://github.com/SEU_USUARIO/automacao-boleto.git](https://github.com/SEU_USUARIO/automacao-boleto.git)
cd automacao-boleto
```

Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
```

Instale as bibliotecas necessárias:
```bash
pip install selenium webdriver-manager python-dotenv
```
3. Variáveis de Ambiente
Por segurança, as senhas não ficam no código. Crie um arquivo chamado .env na raiz do projeto e preencha com as suas informações:
```bash
Snippet de código (Assim como está no arquivo .env.example):
LOGIN_USUARIO=seu_ra_aqui
LOGIN_SENHA=sua_senha_da_faculdade_aqui
EMAIL_REMETENTE=seu.email@gmail.com
SENHA_EMAIL=sua_senha_de_aplicativo_do_google_aqui
EMAIL_DESTINO=email.de.destino@gmail.com
```
4. Uso Manual
Para rodar a automação manualmente, basta executar o arquivo principal:
```bash
python main.py
```
Siga as instruções no terminal para resolver o CAPTCHA quando solicitado e pressione ENTER.

5. Execução Automática (Windows)
Edite os caminhos das pastas dentro do arquivo rodar_robo.bat para corresponderem ao local onde você salvou o projeto.

Abra o Agendador de Tarefas do Windows.

Crie uma Tarefa Básica mensal apontando para o arquivo rodar_robo.bat.

Na aba de configurações da tarefa, marque a opção "Executar a tarefa o mais rápido possível após um agendamento ter sido perdido".
