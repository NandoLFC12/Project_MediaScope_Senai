# 🚀 Media Scope

**Media Scope** é uma plataforma SaaS de Analytics focada em criadores de conteúdo do YouTube. O sistema oferece dashboards interativos, gerenciamento de assinaturas, integração via OAuth2 com Google/YouTube e análise de sentimentos de comentários usando Processamento de Linguagem Natural (NLP).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.11+, Django 5.x
* **Banco de Dados:** PostgreSQL
* **Autenticação:** Django Auth + Social Auth (Google OAuth2)
* **Integrações:** YouTube Data API v3
* **Data Science:** TextBlob (Análise de Sentimentos) (a ser implementado)
* **Frontend:** HTML5, CSS3 (Dark Mode), JavaScript

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
* [Python 3.11+](https://www.python.org/downloads/)
* [PostgreSQL](https://www.postgresql.org/download/) (e pgAdmin para gerenciar)
* [Git](https://git-scm.com/)

---

## 🚀 Guia de Instalação e Execução

Siga os passos abaixo para rodar o projeto localmente.

### 1. Clonar o Repositório
```bash
git clone https://github.com/Fabinhonhou/MediaScope.git
cd MediaScope
git checkout dash
```

### 2. Crie e Ative o ambiente virtual (venv)
```bash
(windows)
python -m venv venv
venv\Scripts\activate

#caso esteja em um sistema operacional diferente, utilizar esses códigos abaixo
#(mac/linux)
#python3 -m venv venv
#source venv/bin/activate
```
### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```
### 4. Configure as Variáveis do Ambiente (.env)
na raiz do projeto, crie um arquivo chamado **.env** e cole os seguintes dados nele 
```
# Configurações do Django
DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui

# Banco de Dados (PostgreSQL)
DB_NAME=MediaScope
DB_USER=postgres
DB_PASSWORD=sua_senha_postgres
DB_HOST=localhost
DB_PORT=5432

# Google OAuth2 / YouTube API
# (Obtenha no Google Cloud Console)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=seu_client_id_do_google
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=seu_client_secret_do_google
```
(será enviado um arquivo .env com os dados já preenchidos para utilização e teste do projeto)

### 5. Configurar o Banco de Dados

Certifique-se de que o PostgreSQL está rodando e que você criou um banco de dados vazio com o nome definido no .env

Em seguida, execute as migrações:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Criar um Superusuário 
```bash
python manage.py createsuperuser
```
### 7. Rodar o Servidor
```bash
python manage.py runserver

# O projeto estará acessível em: http://127.0.0.1:8000/
```
(como é algo sobre análise de redes sociais com a utilização de um canal Youtube, é necessário que a conta utilizada tenha um canal no youtube. Caso a conta não possua um canal, irá aparecer a menssagem que a conta não possui dados para a análise. Nossos testes estão sendo feitos na conta de um amigo que será utilizada na apresentação final do trabalho.)

---

### 🧪 Funcionalidades Principais
1.Autenticação Híbrida: Login via E-mail/Senha ou Google (YouTube).

2.Pipeline de Perfil: Recuperação automática da foto e ID do canal do YouTube após o login.

3.Dashboard: Visão geral de métricas e gráficos.

4.Planos e Assinaturas: Sistema de upgrade de conta (Free/Pro).

5.Configurações de Usuário: Edição de perfil, troca de senha, dark mode e "Danger Zone" (Exclusão de conta).

--- 

### ⚠️ Observações Importantes

O sistema de upload de fotos ignora arquivos locais no Git para manter o repositório leve.