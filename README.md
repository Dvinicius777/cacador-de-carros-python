# 🏎️ Caçador de Carros (Web Scraper)

Ferramenta em Python para monitorar anúncios de veículos no Mercado Livre e extrair dados estruturados para análise.

## 🎯 Objetivo
Buscar ofertas de carros específicos, adaptando-se ao layout dinâmico do site e gerando uma saída limpa com:
- Título
- Preço
- Atributos (ano, km e afins)
- Link do anúncio

## 🛠️ Tecnologias Utilizadas
- **Python 3.12+**
- **Requests**: requisições HTTP com timeout, retries e User-Agent
- **BeautifulSoup4**: parsing de HTML e extração de dados

## ⚙️ Funcionalidades
- ✅ Busca por qualquer modelo (ex: Civic, Porsche, Ferrari)
- ✅ Extração inteligente de título, preço e atributos
- ✅ Fallback de seletores para maior robustez contra mudanças de layout
- ✅ Tratamento de erros de conexão e HTTP
- ✅ Execução interativa ou via linha de comando

## 🚀 Como rodar o projeto
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute em modo interativo:
   ```bash
   python cacador_carros.py
   ```
4. Ou passe o modelo diretamente:
   ```bash
   python cacador_carros.py "honda civic"
   ```

## 💡 Opções úteis
- Limitar resultados:
  ```bash
  python cacador_carros.py "corolla" --limite 3
  ```
- Habilitar logs de debug:
  ```bash
  python cacador_carros.py "porsche" --debug
  ```

## ⚠️ Observações
- Como se trata de scraping, mudanças no HTML do site podem exigir ajuste de seletores.
- Em casos de bloqueio temporário, tente novamente após alguns minutos.
