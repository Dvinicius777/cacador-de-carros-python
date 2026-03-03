from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://lista.mercadolivre.com.br/veiculos/{}"
DEFAULT_TIMEOUT = 15
MAX_RESULTADOS_PADRAO = 5

LOGGER = logging.getLogger(__name__)


@dataclass
class AnuncioCarro:
    titulo: str
    preco: str
    atributos: str
    link: str


def criar_sessao() -> requests.Session:
    """Cria sessão HTTP com headers e política de retry."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    retry = Retry(
        total=3,
        backoff_factor=0.7,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
    )

    sessao = requests.Session()
    sessao.headers.update(headers)
    sessao.mount("https://", HTTPAdapter(max_retries=retry))
    sessao.mount("http://", HTTPAdapter(max_retries=retry))
    return sessao


def montar_url(modelo: str) -> str:
    termo = quote_plus(modelo.strip().replace(" ", "-"))
    return BASE_URL.format(termo)


def obter_html(sessao: requests.Session, url: str) -> str:
    resposta = sessao.get(url, timeout=DEFAULT_TIMEOUT)
    resposta.raise_for_status()
    return resposta.text


def _extrair_titulo_e_link(anuncio) -> tuple[str, str] | None:
    seletores_titulo = [
        "a.poly-component__title",
        "a.ui-search-item__group__element",
        "h2.ui-search-item__title a",
    ]
    for seletor in seletores_titulo:
        tag = anuncio.select_one(seletor)
        if tag and tag.get_text(strip=True) and tag.get("href"):
            return tag.get_text(strip=True), tag["href"]
    return None


def _extrair_preco(anuncio) -> str:
    seletores_preco = [
        "span.andes-money-amount__fraction",
        "span.price-tag-fraction",
    ]
    for seletor in seletores_preco:
        tag = anuncio.select_one(seletor)
        if tag and tag.get_text(strip=True):
            return tag.get_text(strip=True)
    return "Preço não informado"


def _extrair_atributos(anuncio) -> str:
    seletores_atributos = [
        "li.poly-attributes_list__item",
        "ul.ui-search-card-attributes li",
    ]
    for seletor in seletores_atributos:
        itens = anuncio.select(seletor)
        if itens:
            return " | ".join(item.get_text(strip=True) for item in itens)
    return "Sem detalhes extras"


def extrair_anuncios(html: str, limite: int = MAX_RESULTADOS_PADRAO) -> list[AnuncioCarro]:
    soup = BeautifulSoup(html, "html.parser")
    seletores_card = [
        "div.ui-search-result__wrapper",
        "li.ui-search-layout__item",
    ]

    cards: Iterable = []
    for seletor in seletores_card:
        cards = soup.select(seletor)
        if cards:
            break

    anuncios: list[AnuncioCarro] = []
    for card in cards:
        titulo_link = _extrair_titulo_e_link(card)
        if not titulo_link:
            continue
        titulo, link = titulo_link
        anuncio = AnuncioCarro(
            titulo=titulo,
            preco=_extrair_preco(card),
            atributos=_extrair_atributos(card),
            link=link,
        )
        anuncios.append(anuncio)
        if len(anuncios) >= limite:
            break

    return anuncios


def buscar_carros(modelo: str, limite: int = MAX_RESULTADOS_PADRAO) -> list[AnuncioCarro]:
    sessao = criar_sessao()
    url = montar_url(modelo)
    LOGGER.info("Buscando modelo '%s' em %s", modelo, url)
    html = obter_html(sessao, url)
    return extrair_anuncios(html, limite=limite)


def imprimir_anuncios(anuncios: list[AnuncioCarro]) -> None:
    if not anuncios:
        print("❌ Não encontrei nenhum carro. O site pode ter bloqueado ou o termo está errado.")
        return

    print(f"✅ Encontrei {len(anuncios)} carros! Listando resultados:\n")
    for anuncio in anuncios:
        print(f"🚘 {anuncio.titulo}")
        print(f"💰 R$ {anuncio.preco}")
        print(f"📅 {anuncio.atributos}")
        print(f"🔗 Link: {anuncio.link}")
        print("-" * 60)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Busca carros no Mercado Livre.")
    parser.add_argument("modelo", nargs="?", help="Modelo desejado (ex: Civic, Corolla)")
    parser.add_argument("--limite", type=int, default=MAX_RESULTADOS_PADRAO, help="Limite de resultados")
    parser.add_argument("--debug", action="store_true", help="Ativa logs de depuração")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(levelname)s: %(message)s")

    modelo = args.modelo or input("\n🏎️  Qual carro você quer pesquisar? (Ex: Civic, Corolla, Porsche): ").strip()
    if not modelo:
        print("❌ Você precisa informar um modelo válido.")
        return

    print(f"\n🔍 Acessando Mercado Livre para buscar '{modelo}'...")
    print("-" * 60)

    try:
        anuncios = buscar_carros(modelo=modelo, limite=max(args.limite, 1))
    except requests.RequestException as exc:
        print(f"Erro de conexão ao acessar o Mercado Livre: {exc}")
        return

    imprimir_anuncios(anuncios)


if __name__ == "__main__":
    main()
