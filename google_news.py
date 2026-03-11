import requests
import urllib.parse
import xml.etree.ElementTree as ET



def search_news(name_candidate):

    #Parseamos el nombre del candidato para colocarlo en URL
    name_candidate_quotes = urllib.parse.quote(f'"{name_candidate}"')
    search = urllib.parse.quote("Perú (denuncia OR corrupción OR investigación OR fiscalía OR lavado OR soborno OR caso)")
    url_google_news = f"https://news.google.com/rss/search?q={name_candidate_quotes}+{search}+Peru&hl=es-419&gl=PE&ceid=PE:es-419"

    response = requests.get(url_google_news)
    response.raise_for_status()

    # Pasamos de XML a XML Tree
    response_xml_tree = ET.fromstring(response.content)

    source_news = []

    for noticia in response_xml_tree.findall(".//item")[:10]:

        title = noticia.find("title").text
        news_url = noticia.find("link").text

        #En caso no exista estos elementos, sigamos a la siguiente iteración
        if title is None or news_url is None: continue

        source_news.append({
            "title": noticia.find("title").text,
            "news_url": noticia.find("link").text,
            "publish_date": noticia.find("pubDate").text,
            "source": noticia.find("source").text
        })


    return source_news


def format_news(source_news):
    formatted = []
    for i, news in enumerate(source_news,1):
        formatted.append(
f"""
number_news: {i}
title: {news["title"]}
news_url: {news["news_url"]}
publish_date: {news["publish_date"]}
source: {news["source"]}                        
"""
        )
    return "\n".join(formatted)

