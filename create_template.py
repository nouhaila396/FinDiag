from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from pathlib import Path

# Emplacement du fichier Excel
output_path = Path("data/templates/FinDiag_template.xlsx")

# Création du classeur
wb = Workbook()

# Supprimer la feuille par défaut
ws = wb.active
ws.title = "Informations"

# Couleurs
header_fill = PatternFill("solid", fgColor="1F4E78")
header_font = Font(color="FFFFFF", bold=True)

# -------------------------
# Feuille Informations
# -------------------------
ws["A1"] = "FinDiag - Informations générales"
ws["A1"].font = Font(bold=True, size=14)

informations = [
    ("Nom de l'entreprise", ""),
    ("Secteur d'activité", ""),
    ("Devise", "MAD"),
    ("Unité", "MAD"),
    ("Exercice de départ", ""),
    ("Nombre d'exercices", 5),
]

for row, (label, value) in enumerate(informations, start=3):
    ws.cell(row=row, column=1, value=label)
    ws.cell(row=row, column=2, value=value)

# -------------------------
# Compte de résultat
# -------------------------
ws = wb.create_sheet("Compte_Resultat")

headers = ["Poste", "2022", "2023", "2024", "2025", "2026"]
for col, value in enumerate(headers, start=1):
    cell = ws.cell(row=1, column=col, value=value)
    cell.fill = header_fill
    cell.font = header_font

compte_resultat = [
    "Chiffre d'affaires",
    "Achats",
    "Charges externes",
    "Charges de personnel",
    "EBITDA",
    "Résultat d'exploitation",
    "Résultat financier",
    "Résultat net",
]

for row, poste in enumerate(compte_resultat, start=2):
    ws.cell(row=row, column=1, value=poste)

# -------------------------
# Bilan
# -------------------------
ws = wb.create_sheet("Bilan")

for col, value in enumerate(headers, start=1):
    cell = ws.cell(row=1, column=col, value=value)
    cell.fill = header_fill
    cell.font = header_font

bilan = [
    "Immobilisations",
    "Stocks",
    "Créances clients",
    "Autres créances",
    "Disponibilités",
    "Capitaux propres",
    "Dettes financières",
    "Dettes fournisseurs",
    "Dettes fiscales et sociales",
    "Autres dettes",
]

for row, poste in enumerate(bilan, start=2):
    ws.cell(row=row, column=1, value=poste)

# -------------------------
# Données d'exploitation
# -------------------------
ws = wb.create_sheet("Donnees_Exploitation")

for col, value in enumerate(headers, start=1):
    cell = ws.cell(row=1, column=col, value=value)
    cell.fill = header_fill
    cell.font = header_font

exploitation = [
    "Créances clients",
    "Dettes fournisseurs",
    "Stocks",
    "Chiffre d'affaires",
    "Achats",
    "Coût des ventes",
]

for row, poste in enumerate(exploitation, start=2):
    ws.cell(row=row, column=1, value=poste)

# -------------------------
# Mise en forme
# -------------------------
for ws in wb.worksheets:
    ws.column_dimensions["A"].width = 32

    for column in ["B", "C", "D", "E", "F"]:
        ws.column_dimensions[column].width = 16

    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(vertical="center")

# Création du dossier si nécessaire
output_path.parent.mkdir(parents=True, exist_ok=True)

# Sauvegarde
wb.save(output_path)

print(f"Template créé : {output_path}")