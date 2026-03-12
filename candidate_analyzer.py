import time
from google_news import search_news
from jne_api import get_candidates
from filter_candidates import filter_candidates
from notion_api import save_data_to_notion
from openai_llm_analysis import news_llm_analyzer

# Variables
president_tag = "PRESIDENTE DE LA REPÚBLICA"
first_vicepresident_tag = "PRIMER VICEPRESIDENTE DE LA REPÚBLICA"
second_vicepresident_tag = "SEGUNDO VICEPRESIDENTE DE LA REPÚBLICA"


def main():

    #Capturamos el tiempo de inicio
    start_time = time.time()

    #Obtenemos los candidatos
    all_candidates = get_candidates()

    #Filtramos los candidatos | Solo presidenciales
    candidates_presidential = filter_candidates(all_candidates, president_tag)
    candidates_first_vicepresident = filter_candidates(all_candidates, first_vicepresident_tag)
    candidates_second_vicepresident = filter_candidates(all_candidates, second_vicepresident_tag)

    # Evaluamos los candidatos a Presidentes
    candidate_evaluation(candidates_presidential)

    # Evaluamos los candidatos a Primer Vicepresidente
    candidate_evaluation(candidates_first_vicepresident)

    # Evaluamos los candidatos a Segundo Vicepresidente
    candidate_evaluation(candidates_second_vicepresident)

    # Capturamos el tiempo de fin
    end_time = time.time()

    #Mostramos el tiempo de ejecución
    execution_time = end_time - start_time
    print(f"⏱️ Tiempo de Ejecución: {execution_time:.2f} seconds")


def candidate_evaluation(candidate_group):

    # Evaluamos los candidatos dentro del grupo recibido
    for candidate in candidate_group[:1]:
        # Por cada candidato llamamos al analizador LLM
        print("🔎 Analizando candidato: " + candidate["full_name"])
        result = news_llm_analyzer(candidate)

        # Guardamos la información en Notion
        print("📝 Grabando información en notion...")
        save_data_to_notion(candidate, result)


if __name__ == "__main__":
    main()









