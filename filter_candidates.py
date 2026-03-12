
def filter_candidates(candidatos, tag):

    candidates_filtered = []

    # Recorremos los candidatos
    for candidato in candidatos:
        # filtramos
        if candidato["apply_position"] == tag:
            candidates_filtered.append(candidato)

    return candidates_filtered