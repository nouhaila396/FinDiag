def marge_nette(resultat_net, chiffre_affaires):
    if chiffre_affaires == 0:
        return 0
    return (resultat_net / chiffre_affaires) * 100


def roe(resultat_net, capitaux_propres):
    if capitaux_propres == 0:
        return 0
    return (resultat_net / capitaux_propres) * 100


def roa(resultat_net, total_actif):
    if total_actif == 0:
        return 0
    return (resultat_net / total_actif) * 100


def fonds_roulement(ressources_stables, emplois_stables):
    return ressources_stables - emplois_stables


def besoin_fonds_roulement(actif_circulant_exploitation,
                           passif_circulant_exploitation):
    return actif_circulant_exploitation - passif_circulant_exploitation


def tresorerie_nette(fr, bfr):
    return fr - bfr


def dso(creances_clients, chiffre_affaires):
    if chiffre_affaires == 0:
        return 0
    return (creances_clients / chiffre_affaires) * 365


def dpo(dettes_fournisseurs, achats):
    if achats == 0:
        return 0
    return (dettes_fournisseurs / achats) * 365


def dio(stock_moyen, cout_des_ventes):
    if cout_des_ventes == 0:
        return 0
    return (stock_moyen / cout_des_ventes) * 365


def ccc(dio_value, dso_value, dpo_value):
    return dio_value + dso_value - dpo_value


def ratio_endettement(dettes_financieres, capitaux_propres):
    if capitaux_propres == 0:
        return 0
    return (dettes_financieres / capitaux_propres) * 100