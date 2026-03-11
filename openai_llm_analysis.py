from openai import OpenAI
from dotenv import load_dotenv
import os
from google_news import *
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def news_llm_analyzer(candidate):

    #Buscamos las noticias del candidato y formateamos a texto
    news = search_news(candidate)
    news_formatted = format_news(news)

    #Mostramos las noticias que analizará
    print(f"""
Contexto de Noticias
{news_formatted}
"""
         )

    #Armamos el prompt
    prompt = f"""
Eres un analista neutral que evalúa riesgos legales y controversias de candidatos políticos del Perú.
Debes analizar el siguiente candidato utilizando ÚNICAMENTE las noticias proporcionadas en el contexto.

Candidato:
Nombre: "KEIKO SOFIA FUJIMORI HIGUCHI"
DNI: 10001088
Sexo: FEMENINO
Cargo al que postula: PRESIDENTE DE LA REPÚBLICA
Partido político: FUERZA POPULAR

Contexto (titulares de noticias):
{news_formatted}

Tarea:
Analiza si el candidato tiene antecedentes o menciones relacionadas con:

- denuncias
- investigaciones fiscales
- corrupción
- lavado de dinero
- enriquecimiento ilícito
- procesos judiciales
- escándalos políticos relevantes

Reglas importantes:

1. Usa SOLO la información del contexto proporcionado.
2. No inventes información ni agregues datos externos.
3. Si las noticias no son claramente sobre el candidato, ignóralas.
4. Si no hay evidencia clara, marca los campos como null.
5. Sé objetivo y neutral.

Clasificación de riesgo:

- "green" → No se detectan problemas legales ni controversias relevantes.
- "orange" → Existen controversias políticas, denuncias menores o situaciones discutidas públicamente.
- "red" → Existen investigaciones, denuncias graves o procesos judiciales relevantes.

Responde SOLO en JSON con esta estructura exacta:

{{
"risk_level": "green | orange | red",
"clean": true/false/null,
"legal_issues": true/false/null,
"controversies": true/false/null,
"events": [
"Descripción breve del evento + fuente"
],
"summary": "explicación corta y neutral del análisis",
"confidence": 0.0-1.0
}}
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    #Mostramos el costo del uso del LLM
    show_usage(response.usage)

    #Formateamos el resultado a JSON
    try:
        result = json.loads(response.output_text.strip())
    except json.decoder.JSONDecodeError as e:
        print("Error:", e)
        print("Output:", response.output_text)
        return None

    return result


def show_usage(usage):

    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    total_tokens = usage.total_tokens

    # precios gpt-4.1-mini
    input_cost = input_tokens * 0.40 / 1_000_000
    output_cost = output_tokens * 1.60 / 1_000_000
    total_cost = input_cost + output_cost

    print("Input tokens:", input_tokens)
    print("Output tokens:", output_tokens)
    print("Total tokens:", total_tokens)
    print(f"Total Cost: ${total_cost:.6f}")