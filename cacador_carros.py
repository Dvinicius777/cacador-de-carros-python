import requests
from bs4 import BeautifulSoup

def buscar_carro_final():
    modelo = input("\n🏎️  Qual carro você quer pesquisar? (Ex: Civic, Corolla, Porsche): ")
    print(f"\n🔍 Acessando Mercado Livre para buscar '{modelo}'...")
    print("-" * 60)

    url = f"https://lista.mercadolivre.com.br/veiculos/{modelo.replace(' ', '-')}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        anuncios = soup.find_all('div', class_='ui-search-result__wrapper')

        if not anuncios:
            print("❌ Não encontrei nenhum carro. O site pode ter bloqueado ou o termo está errado.")
            return

        print(f"✅ Encontrei {len(anuncios)} carros! Listando os top 5:\n")

        count = 0
        for item in anuncios:
            if count >= 5:
                break
            
            try:
                titulo_tag = item.find('a', class_='poly-component__title')
                if not titulo_tag: continue
                titulo = titulo_tag.text.strip()
                link = titulo_tag['href']

                preco_tag = item.find('span', class_='andes-money-amount__fraction')
                preco = preco_tag.text if preco_tag else "Preço não informado"

                detalhes = item.find_all('li', class_='poly-attributes_list__item')
                info_extra = " | ".join([d.text.strip() for d in detalhes]) if detalhes else ""

                print(f"🚘 {titulo}")
                print(f"💰 R$ {preco}")
                print(f"📅 {info_extra}")
                print(f"🔗 Link: {link}")
                print("-" * 60)
                
                count += 1

            except Exception as e:
                continue

    except Exception as e:
        print(f"Erro de conexão: {e}")

if __name__ == "__main__":
    buscar_carro_final()
