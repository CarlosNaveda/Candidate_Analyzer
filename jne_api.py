import requests

#Variables
api_url_candidatos = "https://web.jne.gob.pe/serviciovotoinformado/api/votoinf/listarCanditatos"

def get_candidates():
    api_url_candidatos_payload = {
        "idProcesoElectoral": 124,
        "strUbiDepartamento": '',
        "idTipoEleccion": 1
    }

    api_url_candidatos_headers = {
        "Content-Type": "application/json"
    }

    # Enviamos la petición POST
    response = requests.post(
        url=api_url_candidatos,
        json=api_url_candidatos_payload,
        headers=api_url_candidatos_headers
    )

    response.raise_for_status()

    # Guardamos en variable el response
    data = response.json()
    data_candidatos = data['data']

    candidatos = []

    # Recorremos toda la data
    for candidato in data_candidatos:

        full_name = f"{candidato['strNombres']} {candidato['strApellidoPaterno']} {candidato['strApellidoMaterno']}"

        candidatos.append({
            "full_name": full_name,
            "dni" : candidato['strDocumentoIdentidad'],
            "sex": candidato['strSexo'],
            "apply_position" : candidato['strCargo'],
            "political_party": candidato['strOrganizacionPolitica']
        })

    return candidatos