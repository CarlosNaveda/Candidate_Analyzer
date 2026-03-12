import os
from dotenv import load_dotenv
from notion_client import Client, UnknownHTTPResponseError
import time

from openai_llm_analysis import format_events

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
database_id = os.getenv("NOTION_DATABASE_ID")

def save_data_safe_to_notion(candidate, result,retries,delay):

    parent = notion_get_parent()
    properties = notion_get_properties(candidate,result)

    for i in range(retries):
        try:
            notion.pages.create(parent=parent, properties=properties)
            return
        except UnknownHTTPResponseError as e:
            print(f"Error en Notion, intento {i+1}/{retries}: {e}")
            time.sleep(delay)

    print("No se pudo crear la página después de varios intentos.")


def notion_get_parent():
    parent = {"database_id": database_id}
    return parent

def notion_get_properties(candidate,result):
    # Variables del candidato
    full_name = candidate["full_name"]
    dni = candidate["dni"]
    sex = candidate["sex"]
    apply_position = candidate["apply_position"]
    political_party = candidate["political_party"]
    number = candidate.get("number", "-")  # Uso get porque puede que no todos los candidatos lo traigan.

    # Variable del contexto
    news_formatted = result["news_formatted"]

    # Variables del análisis
    risk_level = result["analysis"]["risk_level"]
    clean = result["analysis"]["clean"]
    legal_issues = result["analysis"]["legal_issues"]
    controversies = result["analysis"]["controversies"]
    events = format_events(result["analysis"]["events"])  # Esta le hago un formateo previo
    summary = result["analysis"]["summary"]
    confidence = result["analysis"]["confidence"]

    # Variable del uso del LLM
    usage = result["usage"]

    # Maps
    risk_level_map = {
        "green": "🟢 Bajo",
        "orange": "🟠 Medio",
        "red": "🔴 Alto"
    }

    apply_position_map = {
        "PRESIDENTE DE LA REPÚBLICA": "PRESIDENTE DE LA REPÚBLICA",
        "PRIMER VICEPRESIDENTE DE LA REPÚBLICA": "1ER VICEPRESIDENTE",
        "SEGUNDO VICEPRESIDENTE DE LA REPÚBLICA": "2DO VICEPRESIDENTE",
        "DIPUTADO": "DIPUTADO",
        "SENADOR": "SENADOR",
        "REPRESENTANTE ANTE EL PARLAMENTO ANDINO": "PARLAMENTO ANDINO"
    }

    sex_map = {
        "MASCULINO": "Masculino",
        "FEMENINO": "Femenino"
    }

    properties = {
        "Nombre candidato": notion_title(full_name),
        "Dni": notion_text(dni),
        "Sexo": {"select": {"name": sex_map.get(sex, "Otro")}},
        "Postula a cargo": {"select": {"name": apply_position_map.get(apply_position, "OTRO")}},
        "Partido político": notion_text(political_party),
        "Número": notion_text(number),
        "Noticias": notion_text(news_formatted),
        "Nivel de riesgo": {"select": {"name": risk_level_map.get(risk_level, "⚪ Desconocido")}},
        "Limpio": {"select": {"name": "SI" if clean else "NO"}},
        "Problemas legales": {"select": {"name": "SI" if legal_issues is True else "NO"}},
        "Controversias": {"select": {"name": "SI" if controversies else "NO"}},
        "Eventos": notion_text(events),
        "Resumen": notion_text(summary),
        "Confianza del análisis %": notion_number(confidence),
        "Uso": notion_text(usage)
    }
    return properties


def notion_title(text):
    return {"title": [{"text": {"content": text}}]}

def notion_text(text):
    return {"rich_text": [{"text": {"content": str(text)}}]}

def notion_number(number):
    return {"number": number}