def diagnostic_rentabilite(marge_nette, roe, roa):
    points_forts = []
    points_faibles = []

    if marge_nette > 10:
        points_forts.append("Marge nette satisfaisante")
    elif marge_nette < 0:
        points_faibles.append("Marge nette négative")

    if roe > 10:
        points_forts.append("ROE satisfaisant")
    elif roe < 0:
        points_faibles.append("ROE négatif")

    if roa > 5:
        points_forts.append("ROA satisfaisant")
    elif roa < 0:
        points_faibles.append("ROA négatif")

    return points_forts, points_faibles


def diagnostic_tresorerie(fr, bfr, tresorerie):
    points_forts = []
    points_faibles = []
    risques = []

    if fr > 0:
        points_forts.append("Fonds de roulement positif")
    else:
        points_faibles.append("Fonds de roulement insuffisant")

    if bfr <= 0:
        points_forts.append("BFR maîtrisé")
    else:
        points_faibles.append("BFR positif")
        risques.append("Besoin de financement du cycle d'exploitation")

    if tresorerie > 0:
        points_forts.append("Trésorerie nette positive")
    else:
        points_faibles.append("Trésorerie nette négative")
        risques.append("Risque de tension de trésorerie")

    return points_forts, points_faibles, risques


def diagnostic_delais(dso, dpo, dio, ccc):
    points_forts = []
    points_faibles = []
    risques = []

    if dso <= 60:
        points_forts.append("Délai clients maîtrisé")
    else:
        points_faibles.append("Délai clients élevé")
        risques.append("Risque d'immobilisation des créances clients")

    if dio <= 90:
        points_forts.append("Rotation des stocks satisfaisante")
    else:
        points_faibles.append("Rotation des stocks lente")
        risques.append("Risque d'immobilisation des stocks")

    if ccc <= 60:
        points_forts.append("Cycle de conversion de trésorerie maîtrisé")
    else:
        points_faibles.append("Cycle de conversion de trésorerie élevé")

    return points_forts, points_faibles, risques


def diagnostic_endettement(ratio_endettement):
    points_forts = []
    points_faibles = []
    risques = []

    if ratio_endettement <= 100:
        points_forts.append("Endettement maîtrisé")
    else:
        points_faibles.append("Endettement important")
        risques.append("Risque financier lié à l'endettement")

    return points_forts, points_faibles, risques


def diagnostic_global(marge_nette, roe, roa, fr, bfr, tresorerie,
                      dso, dpo, dio, ccc, ratio_endettement):

    forces = []
    faiblesses = []
    risques = []

    f, fa = diagnostic_rentabilite(marge_nette, roe, roa)
    forces.extend(f)
    faiblesses.extend(fa)

    f, fa, r = diagnostic_tresorerie(fr, bfr, tresorerie)
    forces.extend(f)
    faiblesses.extend(fa)
    risques.extend(r)

    f, fa, r = diagnostic_delais(dso, dpo, dio, ccc)
    forces.extend(f)
    faiblesses.extend(fa)
    risques.extend(r)

    f, fa, r = diagnostic_endettement(ratio_endettement)
    forces.extend(f)
    faiblesses.extend(fa)
    risques.extend(r)

    return {
        "points_forts": forces,
        "points_faibles": faiblesses,
        "risques": risques
    }
