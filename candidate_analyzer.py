import time
from google_news import search_news
from jne_api import *
from filter_candidates import filter_candidates
from notion_api import save_data_safe_to_notion
from openai_llm_analysis import news_llm_analyzer

# Variables
president_tag = "PRESIDENTE DE LA REPÚBLICA"
first_vicepresident_tag = "PRIMER VICEPRESIDENTE DE LA REPÚBLICA"
second_vicepresident_tag = "SEGUNDO VICEPRESIDENTE DE LA REPÚBLICA"


def main():

    #Capturamos el tiempo de inicio
    start_time = time.time()

    #Obtenemos los candidatos presidenciales y vicepresidenciales
    all_candidates_president_vicepresident = get_candidates_president_vicepresident()
    all_candidates_deputies = get_candidates_deputies()

    #Filtramos los candidatos
    candidates_presidential = filter_candidates(all_candidates_president_vicepresident, president_tag)
    candidates_first_vicepresident = filter_candidates(all_candidates_president_vicepresident, first_vicepresident_tag)
    candidates_second_vicepresident = filter_candidates(all_candidates_president_vicepresident, second_vicepresident_tag)

    # Evaluamos los candidatos
    candidate_evaluation(candidates_presidential)
    candidate_evaluation(candidates_first_vicepresident)
    candidate_evaluation(candidates_second_vicepresident)
    candidate_evaluation(all_candidates_deputies)

    # Capturamos el tiempo de fin
    end_time = time.time()

    #Mostramos el tiempo de ejecución
    execution_time = end_time - start_time
    print(f"⏱️ Tiempo de Ejecución: {execution_time:.2f} seconds")


def candidate_evaluation(candidate_group):

    # Evaluamos los candidatos dentro del grupo recibido
    for candidate in candidate_group:
        # Por cada candidato llamamos al analizador LLM
        print("🔎 Analizando candidato: " + candidate["full_name"])
        result = news_llm_analyzer(candidate)

        # Guardamos la información en Notion
        print("📝 Grabando información en notion...")
        save_data_safe_to_notion(candidate, result,3,5)


if __name__ == "__main__":
    main()









