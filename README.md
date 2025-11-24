# MediaScope — Plataforma de Análise de Dados do YouTube

**Resumo**
MediaScope é uma plataforma para coletar, processar e visualizar métricas de canais e vídeos do YouTube, construída em Python utilizando a biblioteca oficial do Google para acesso à YouTube Data API. Esta versão foi entregue como um repositório com scripts de coleta, serviços e uma interface/ou scripts para análise.

---

## Índice
- [Resumo](#resumo)
- [Funcionalidades](#funcionalidades)
- [Stack e Dependências](#stack-e-dependências)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Instalação](#instalação)
- [Configuração (API Keys e .env)](#configuração-api-keys-e-env)
- [Como rodar](#como-rodar)
- [Scripts úteis](#scripts-úteis)
- [Como a YouTube Data API é utilizada](#como-a-youtube-data-api-é-utilizada)
- [Banco de dados](#banco-de-dados)
- [Testes](#testes)
- [Melhorias futuras](#melhorias-futuras)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## Funcionalidades
- Coleta de estatísticas de vídeos e canais (views, likes, comentários, inscritos, metadata).
- Agendamento de coleta periódica (cron / scheduler).
- Exportação de dados para CSV/Excel.
- Dashboards / visualizações (pode incluir scripts para gerar gráficos com Plotly/Matplotlib).
- Relatórios automatizados (opcional).

---

## Stack e Dependências
- Python 3.10+
- google-api-python-client (YouTube Data API)
- requests
- pandas (provável)
- Dependências listadas em `requirements.txt` (verificado no repositório).

> Verifique `requirements.txt` para a lista completa de pacotes e versões.

---

## Estrutura sugerida do repositório (detectado)
A análise inicial identificou os seguintes arquivos/estruturas (amostra):

```
/mnt/data/Project_MediaScope_Senai-dash
```

Arquivos detectados: 64 (amostra incluída no rascunho de documentação entregue).

Pastas e arquivos importantes:
- `scripts/` — scripts de coleta e atualização (ex.: `collect_data.py`, `update_metrics.py`)
- `app/` ou `src/` — código principal da aplicação (se existir)
- `requirements.txt` — dependências Python
- `README.md` original (presente no repositório)
- `.env.example` ou similar (se existir) — variáveis de ambiente exemplo

> Observação: se alguma das pastas acima não existir no seu repositório, adapte conforme a estrutura real.

---

## Instalação

1. Clone o repositório:
```bash
git clone /mnt/data/Project_MediaScope_Senai-dash.zip media_scope
cd media_scope
```

2. Crie e ative um virtualenv (recomendado):
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate    # Windows (PowerShell)
```

3. Instale dependências:
```bash
pip install -r requirements.txt
```

---

## Configuração (API Keys e .env)

Crie um arquivo `.env` na raiz do projeto (ou copie `.env.example`) com as variáveis mínimas:

```
YOUTUBE_API_KEY=your_api_key_here
DATABASE_URL=...
# Outras variáveis possíveis:
# DJANGO_SECRET_KEY (se aplicável)
# FLASK_APP (se aplicável)
# SMTP_* (se houver envio de e-mail)
```

Como obter a API Key do YouTube:
1. Acesse o console do Google Cloud (https://console.cloud.google.com/).
2. Crie um novo projeto (ou use um existente).
3. Habilite a API "YouTube Data API v3".
4. Vá em "Credenciais" e crie uma API Key.
5. Cole a chave em `YOUTUBE_API_KEY` no seu `.env`.

---

## Como rodar

### Executar scripts de coleta manualmente
```bash
python scripts/collect_data.py
```

### Rodar a aplicação (se houver FastAPI/Flask)
Exemplos possíveis — adapte conforme o framework usado:

**FastAPI**
```bash
uvicorn app.main:app --reload
```

**Flask**
```bash
export FLASK_APP=app
flask run
```

Se a aplicação não expuser uma API, confira os scripts em `scripts/` para entender como os dados são coletados e onde são salvos.

---

## Scripts úteis (exemplos)
- `scripts/collect_data.py` — coleta dados da YouTube Data API e grava no banco.
- `scripts/update_metrics.py` — atualiza métricas históricas.
- `scripts/export_csv.py` — exporta dados em CSV/Excel.
- `scripts/run_scheduler.py` — roda um agendador (APScheduler / cron wrapper).

> Consulte os scripts reais no diretório `scripts/` para confirmações de nomes e parâmetros.

---

## Como a YouTube Data API é utilizada
O repositório traz detecções de uso da biblioteca `googleapiclient` / chamadas à YouTube API. Exemplo de uso típico:

```python
from googleapiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

request = youtube.videos().list(part="snippet,statistics,contentDetails", id=VIDEO_ID)
response = request.execute()
```

A documentação do Google (YouTube Data API v3) é a referência para parâmetros e quotas. Lembre-se de tratar quotas e implementar retries/backoff para chamadas em lote.

---

## Banco de dados
A análise inicial não detectou com certeza qual banco foi usado. Possíveis opções:
- MongoDB (pymongo / mongoengine)
- PostgreSQL / MySQL (psycopg2 / SQLAlchemy)

Se informar qual foi utilizado, posso gerar o diagrama de esquema (collections/tables e campos) automaticamente.

---

## Testes
- Testes unitários: `pytest` (se existirem testes).
- Rodar testes:
```bash
pytest
```

---

## Boas práticas e observações
- Nunca versionar o `.env` com chaves reais.
- Use variáveis de ambiente para credenciais.
- Trate e registre erros de chamadas à API (logs).
- Implemente paginação e controle de rate-limits.
- Centralize chamadas à API em um módulo/service para facilitar testes e mocking.

---

## Melhorias futuras
- Implementar análise de sentimento dos comentários (NLP).
- Dashboard web completo (React/Vue/Plotly Dash).
- Agendamento robusto (Celery/RabbitMQ ou APScheduler com supervisão).
- Monitor de quota da API e alertas.
- Históricos detalhados e projeções de crescimento.

---

## Contribuição
Sinta-se à vontade para abrir issues e pull requests. Use o padrão de commits e inclua testes para novas funcionalidades.

---

## Licença
Adicione aqui a licença do projeto (por exemplo, MIT). Se não houver, recomendo `MIT` para projetos open-source.

---

## Contato
Para dúvidas sobre a documentação gerada, ou para que eu gere o README finalizado com exemplos extraídos automaticamente do código (endpoints, amostras de payloads, esquema do BD), responda com **"Gerar automático com extração de endpoints e modelos"**.

