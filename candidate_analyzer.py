import time
from google_news import search_news
from jne_api import get_candidates
from filter_candidates import filter_candidates
from openai_llm_analysis import news_llm_analyzer

# Variables
president_tag = "PRESIDENTE DE LA REPÚBLICA"
first_vicepresident_tag = "PRIMER VICEPRESIDENTE DE LA REPÚBLICA"
second_vicepresident_tag = "SEGUNDO VICEPRESIDENTE DE LA REPÚBLICA"


def main():

    #Capturamos el tiempo de inicio
    start_time = time.time()

    print(news_llm_analyzer("KEIKO SOFIA FUJIMORI HIGUCHI"))


    # #Obtenemos los candidatos
    # candidates = get_candidates()
    #
    # #Filtramos los candidatos | Solo presidenciales
    # candidates_presidential = filter_candidates(candidates, president_tag)
    #
    # candidates_analyzer_results = []
    #
    # for c in candidates_presidential:
    #
    #     news = search_news(c["full_name"])    # Obtenemos las noticias riesgosas del candidato
    #
    #     candidates_analyzer_results.append({
    #         "full_name": c["full_name"],
    #         "dni" : c['dni'],
    #         "sex": c['sex'],
    #         "apply_position" : c['apply_position'],
    #         "political_party": c['political_party'],
    #         "news": news,
    #     })
    #
    # for a in candidates_analyzer_results:
    #     print(a)

    # Capturamos el tiempo de fin
    end_time = time.time()

    #Mostramos el tiempo de ejecución
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()









