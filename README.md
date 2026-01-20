# 🏎️ Caçador de Carros (Web Scraper)

Ferramenta de automação desenvolvida em Python para monitorar preços de veículos no Mercado Livre em tempo real.

## 🎯 Objetivo
Buscar ofertas de carros específicos, contornando o novo layout dinâmico ("Poly") do Mercado Livre e extraindo dados estruturados para análise.

## 🛠️ Tecnologias Utilizadas
* **Python 3.12+**
* **Requests:** Para requisições HTTP com simulação de User-Agent (Bypass de bloqueios simples).
* **BeautifulSoup4:** Para Data Scraping e parsing de HTML.

## ⚙️ Funcionalidades
* ✅ Busca por qualquer modelo (ex: Civic, Porsche, Ferrari).
* ✅ Extração inteligente de dados: Título, Preço, Ano e Quilometragem.
* ✅ Adaptação automática ao layout moderno do Mercado Livre (Seletores Poly).
* ✅ Tratamento de erros e validação de conexão.

## 🚀 Como rodar o projeto
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt