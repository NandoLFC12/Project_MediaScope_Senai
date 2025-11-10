# --- Configurações do Makefile ---
# Define os executáveis DENTRO da venv para não precisar "ativar"

# Padrão Mac/Linux (funciona no Git Bash do Windows!)
PYTHON = venv/bin/python
PIP = venv/bin/pip

# Se você estiver no CMD/PowerShell PURO, comente as 2 linhas acima
# e descomente as 2 abaixo:
# PYTHON = venv/Scripts/python
# PIP = venv/Scripts/pip


# --- Comandos Mágicos ---

.PHONY: setup database run superuser clean

# O comando principal para o primeiro setup
setup:
	@echo ">>> 1. Criando ambiente virtual (venv)..."
	python -m venv venv
	@echo ">>> 2. Instalando todas as dependências do requirements.txt..."
	$(PIP) install -r requirements.txt
	@echo ">>> Setup inicial concluído! Agora rode 'make database'"

# O comando para preparar o banco de dados
database:
	@echo ">>> 1. Aplicando migrações no banco de dados..."
	$(PYTHON) manage.py migrate
	@echo ">>> 2. Criando a tabela de cache..."
	$(PYTHON) manage.py createcachetable
	@echo ">>> Banco de dados pronto! Crie um admin com 'make superuser'"

# O comando para rodar o servidor
run:
	@echo ">>> Iniciando o servidor em http://127.0.0.1:8000/"
	$(PYTHON) manage.py runserver

# Comando separado para o admin (porque é interativo)
superuser:
	@echo ">>> Criando um novo Superusuário (Admin)..."
	$(PYTHON) manage.py createsuperuser

# Limpa os arquivos de cache do Python
clean:
	@echo ">>> Limpando cache do Python (__pycache__)..."
	find . -type d -name "__pycache__" -exec rm -r {} + || del /S /Q __pycache__
	@echo ">>> Limpeza concluída."