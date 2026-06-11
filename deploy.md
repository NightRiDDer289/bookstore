# Deploy para Render via GitHub Actions


## Como funciona


O workflow executa dois jobs em sequência a cada push na branch `main`:


1. **test** — instala dependências e roda os testes com SQLite em memória
2. **deploy** — aciona o deploy no Render via API e aguarda a conclusão


## Secrets necessários


Configure os seguintes secrets no repositório do GitHub em **Settings → Secrets and variables → Actions**:


| Secret | Descrição |
|---|---|
| `RENDER_API_KEY` | Chave de API do Render |
| `RENDER_SERVICE_ID` | ID do serviço Web no Render (ex: `srv-xxxxxxxxxxxx`) |
| `SECRET_KEY` | Django `SECRET_KEY` usada nos testes do CI |


## Como obter as credenciais do Render


### API Key
1. Acesse [dashboard.render.com](https://dashboard.render.com)
2. Vá em **Account Settings → API Keys**
3. Clique em **Create API Key** e copie o valor


### Service ID
1. No dashboard do Render, acesse o seu Web Service
2. O ID aparece na URL: `https://dashboard.render.com/web/srv-xxxxxxxxxxxx`
3. Copie o trecho `srv-xxxxxxxxxxxx`


## Configuração do serviço no Render


Ao criar o Web Service no Render, configure:


- **Environment:** Python
- **Build Command:**
  ```
  pip install poetry && poetry install --without dev --no-interaction
  ```
- **Start Command:**
  ```
  poetry run python manage.py migrate --noinput && poetry run gunicorn bookstore.wsgi:application --bind 0.0.0.0:$PORT
  ```
- **Environment Variables:** adicione as mesmas variáveis do `.env.dev` com os valores de produção (`SECRET_KEY`, `DEBUG=0`, `SQL_*`, etc.)
