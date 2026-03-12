import os
from dotenv import load_dotenv
from notion_client import Client

from openai_llm_analysis import format_events

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")

def save_data_to_notion(candidate, result):

    #Dummy data
    candidate = {
        "full_name": "KEIKO SOFIA FUJIMORI HIGUCHIAAA",
        "dni": "10001088",
        "sex": "FEMENINO",
        "apply_position": "PRESIDENTE DE LA REPÚBLICA",
        "partido": "FUERZA POPULAR",
        "political_party": "Titulares separados por |"
    }

    #Variables del candidato
    full_name = candidate["full_name"]
    dni = candidate["dni"]
    sex = candidate["sex"]
    apply_position = candidate["apply_position"]
    political_party = candidate["political_party"]

    #Variable del contexto
    news_formatted = result["news_formatted"]

    #Variables del análisis
    risk_level = result["analysis"]["risk_level"]
    clean = result["analysis"]["clean"]
    legal_issues = result["analysis"]["legal_issues"]
    controversies = result["analysis"]["controversies"]
    events = format_events(result["analysis"]["events"]) #Esta le hago un formateo previo
    summary = result["analysis"]["summary"]
    confidence = result["analysis"]["confidence"]

    # Variable del uso del LLM
    usage = result["usage"]


    print("Saving data to Notion...")
    print(candidate)

    notion.pages.create(
        parent={"database_id": database_id},
        properties={
            "Nombre candidato": {"title": [{"text": {"content": full_name}}]},
            "Dni": {"rich_text": [{"text": {"content": dni}}]},
            "Sexo": {"select": {"name": "Femenino" if sex=="FEMENINO" else "Masculino"}},
            "Postula a cargo": {"rich_text": [{"text": {"content": apply_position}}]},
            "Partido político": {"rich_text": [{"text": {"content": political_party}}]},
            "Noticias": {"rich_text": [{"text": {"content": news_formatted}}]},
            "Nivel de riesgo": {
                "select": {
                    "name": {"green": "🟢 Bajo", "orange": "🟠 Medio", "red": "🔴 Alto"}[risk_level]
                }
            },
            "Limpio": {"select": {"name": "SI" if clean else "NO"}},
            "Problemas legales": {"select": {"name": "SI" if legal_issues is True else "NO"}},
            "Controversias": {"select": {"name": "SI" if controversies else "NO"}},
            "Eventos": {"rich_text": [{"text": {"content": events}}]},
            "Resumen": {"rich_text": [{"text": {"content": summary}}]},
            "Confianza del análisis %": {"number": confidence},
            "Uso": {"rich_text": [{"text": {"content": usage}}]}
        }
    )
