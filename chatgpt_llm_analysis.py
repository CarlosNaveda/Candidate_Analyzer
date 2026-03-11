from openai import OpenAI

from google_news import *

client = OpenAI()

def news_llm_analyzer(candidate):

    #Buscamos las noticias del candidato y formateamos a texto
    news = search_news(candidate)
    news_formatted = format_news(news)

    #Armamos el prompt
    prompt = f"""
Eres un analista neutral que evalúa riesgos legales y controversias de candidatos políticos del Perú.
Debes analizar el siguiente candidato utilizando ÚNICAMENTE las noticias proporcionadas en el contexto.

Candidato:
Nombre: {candidate["full_name"]}
DNI: {candidate["dni"]}
Sexo: {candidate["sex"]}
Cargo al que postula: {candidate["apply_position"]}
Partido político: {candidate["political_party"]}

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

{
"risk_level": "green | orange | red",
"clean": true/false/null,
"legal_issues": true/false/null,
"controversies": true/false/null,
"events": [
"Descripción breve del evento + fuente"
],
"summary": "explicación corta y neutral del análisis",
"confidence": 0.0-1.0
}
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text