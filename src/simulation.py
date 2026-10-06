from src.financial_ratios import (
    marge_nette,
    roe,
    roa,
    fonds_roulement,
    besoin_fonds_roulement,
    tresorerie_nette,
    dso,
    dpo,
    dio,
    ccc,
    ratio_endettement,
)


def simuler(donnees):
    resultat = {}

    resultat["marge_nette"] = marge_nette(
        donnees["resultat_net"],
        donnees["chiffre_affaires"]
    )

    resultat["roe"] = roe(
        donnees["resultat_net"],
        donnees["capitaux_propres"]
    )

    resultat["roa"] = roa(
        donnees["resultat_net"],
        donnees["total_actif"]
    )

    resultat["fr"] = fonds_roulement(
        donnees["ressources_stables"],
        donnees["emplois_stables"]
    )

    resultat["bfr"] = besoin_fonds_roulement(
        donnees["actif_circulant_exploitation"],
        donnees["passif_circulant_exploitation"]
    )

    resultat["tresorerie_nette"] = tresorerie_nette(
        resultat["fr"],
        resultat["bfr"]
    )

    resultat["dso"] = dso(
        donnees["creances_clients"],
        donnees["chiffre_affaires"]
    )

    resultat["dpo"] = dpo(
        donnees["dettes_fournisseurs"],
        donnees["achats"]
    )

    resultat["dio"] = dio(
        donnees["stock_moyen"],
        donnees["cout_des_ventes"]
    )

    resultat["ccc"] = ccc(
        resultat["dio"],
        resultat["dso"],
        resultat["dpo"]
    )

    resultat["ratio_endettement"] = ratio_endettement(
        donnees["dettes_financieres"],
        donnees["capitaux_propres"]
    )

    return resultat