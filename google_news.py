import requests
import urllib.parse
import xml.etree.ElementTree as ET



def search_news(name_candidate):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
    }


    #Parseamos el nombre del candidato para colocarlo en URL
    name_candidate_quotes = urllib.parse.quote(f'"{name_candidate}"')
    search = urllib.parse.quote("Perú (denuncia OR corrupción OR investigación OR fiscalía OR lavado OR soborno OR caso)")
    url_google_news = f"https://news.google.com/rss/search?q={name_candidate_quotes}+{search}+Peru&hl=es-419&gl=PE&ceid=PE:es-419"

    print(url_google_news)
    response = requests.get(url_google_news,headers=headers)
    response.raise_for_status()

    # Pasamos de XML a XML Tree
    response_xml_tree = ET.fromstring(response.content)

    source_news = []

    for noticia in response_xml_tree.findall(".//item")[:5]:

        title = noticia.find("title").text
        news_url = noticia.find("link").text
        publish_date = noticia.find("pubDate").text
        source = noticia.find("source").text


        #En caso no exista estos elementos, sigamos a la siguiente iteración
        if title is None or news_url is None: continue

        source_news.append({
            "title": title,
            "news_url": news_url,
            "publish_date": publish_date,
            "source": source,
        })


    return source_news


def format_news(source_news):
    formatted = []
    #No considero el url ya que consume muchos tokens en el input
    for i, news in enumerate(source_news,1):
        formatted.append(
f"""
number_news: {i}
title: {news["title"]}
publish_date: {news["publish_date"]}
source: {news["source"]}                        
"""
        )
    return "\n".join(formatted)

