
# 🤖 LinkedIn Crawler - Feed to PostsFeed (Render Ready)

Este projeto roda automaticamente todo dia às 09h, coleta os posts recentes da sua rede no LinkedIn e preenche a aba `PostsFeed` da sua planilha no Google Sheets.

## ✅ Como usar

1. Suba este repositório para o GitHub
2. Crie um novo serviço na [Render.com](https://render.com) como "Cron Job"
3. Adicione uma variável de ambiente:
   - `LI_AT` com o valor do seu cookie LinkedIn (`li_at`)
4. O job será executado automaticamente todos os dias

## Arquivos incluídos

- `main.py` → script principal com scraping e upload
- `requirements.txt` → dependências
- `.render-config.yaml` → configuração automática para Render
