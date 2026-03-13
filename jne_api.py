import requests

#Variables
api_url_candidatos = "https://web.jne.gob.pe/serviciovotoinformado/api/votoinf/listarCanditatos"

def get_candidates_president_vicepresident():

    api_url_candidatos_payload = create_payload_president_vicepresident()
    api_url_candidatos_headers = create_header()
    response = create_request_post(api_url_candidatos_payload, api_url_candidatos_headers)

    response.raise_for_status()

    # Guardamos en variable el response
    data = response.json()
    data_candidates = data['data']
    candidates = save_data(data_candidates)

    return candidates

def get_candidates_deputies():
    api_url_candidatos_payload = create_payload_deputies()
    api_url_candidatos_headers = create_header()
    response = create_request_post(api_url_candidatos_payload, api_url_candidatos_headers)

    response.raise_for_status()

    # Guardamos en variable el response
    data = response.json()
    data_candidates = data['data']
    candidates = save_data_with_number(data_candidates)

    return candidates

def get_candidates_senators():
    api_url_candidatos_payload = create_payload_senator()
    api_url_candidatos_headers = create_header()
    response = create_request_post(api_url_candidatos_payload, api_url_candidatos_headers)

    response.raise_for_status()

    # Guardamos en variable el response
    data = response.json()
    data_candidates = data['data']
    candidates = save_data_with_number(data_candidates)

    return candidates

def get_candidates_andean_parliament():
    api_url_candidatos_payload = create_payload_andean_parliament()
    api_url_candidatos_headers = create_header()
    response = create_request_post(api_url_candidatos_payload, api_url_candidatos_headers)

    response.raise_for_status()

    # Guardamos en variable el response
    data = response.json()
    data_candidates = data['data']
    candidates = save_data_with_number(data_candidates)

    return candidates

def create_payload_president_vicepresident():
     api_url_candidatos_payload = {
        "idProcesoElectoral": 124,
        "strUbiDepartamento": '',
        "idTipoEleccion": 1
    }

     return api_url_candidatos_payload

def create_payload_deputies():
    api_url_candidatos_payload = {
        "idProcesoElectoral": 124,
        "strUbiDepartamento": '140100',
        "idTipoEleccion": 15
    }

    return api_url_candidatos_payload

def create_payload_senator():
    api_url_candidatos_payload = {
        "idProcesoElectoral": 124,
        "strUbiDepartamento": '',
        "idTipoEleccion": 20
    }

    return api_url_candidatos_payload

def create_payload_andean_parliament():
    api_url_candidatos_payload = {
        "idProcesoElectoral": 124,
        "strUbiDepartamento": '',
        "idTipoEleccion": 3
    }

    return api_url_candidatos_payload

def create_header():
    api_url_candidatos_headers = {
        "Content-Type": "application/json"
    }
    return api_url_candidatos_headers

def create_request_post(payload,headers):
    response = requests.post(
        url=api_url_candidatos,
        json=payload,
        headers=headers
    )

    return response

def save_data(data_candidatos):

    candidatos = []

    # Recorremos toda la data
    for candidato in data_candidatos:
        full_name = f"{candidato['strNombres']} {candidato['strApellidoPaterno']} {candidato['strApellidoMaterno']}"

        candidatos.append({
            "full_name": full_name,
            "dni": candidato['strDocumentoIdentidad'],
            "sex": candidato['strSexo'],
            "apply_position": candidato['strCargo'],
            "political_party": candidato['strOrganizacionPolitica'],
            "state": candidato['strEstadoCandidato']
        })

    return candidatos

def save_data_with_number(data_candidatos):

    candidatos = []

    # Recorremos toda la data
    for candidato in data_candidatos:
        full_name = f"{candidato['strNombres']} {candidato['strApellidoPaterno']} {candidato['strApellidoMaterno']}"

        candidatos.append({
            "full_name": full_name,
            "dni": candidato['strDocumentoIdentidad'],
            "sex": candidato['strSexo'],
            "apply_position": candidato['strCargo'],
            "political_party": candidato['strOrganizacionPolitica'],
            "number": candidato['intPosicion'],
            "state": candidato['strEstadoCandidato']
        })

    return candidatos

