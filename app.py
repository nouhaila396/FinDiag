from __future__ import annotations

import html
import io
import math
import re
import unicodedata
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# Configuration and translations
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="FinDiag",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "language": "Language",
        "english": "🇬🇧 English",
        "french": "🇫🇷 Français",
        "arabic": "🇸🇦 العربية",
        "home": "Home",
        "dashboard": "Dashboard",
        "analysis": "Analysis",
        "diagnostic": "Diagnostic",
        "report": "Report",
        "import_data": "Import Data",
        "brand_tagline": "Financial clarity, built on your data",
        "home_title": "Financial Intelligence",
        "home_subtitle": (
            "Transform your financial data into clear analysis, "
            "practical diagnostics, and actionable insights."
        ),
        "start_analysis": "Start Analysis",
        "features_title": "A clearer view of financial performance",
        "feature_performance": "Financial Performance",
        "feature_performance_desc": "Track key figures and performance indicators.",
        "feature_risk": "Risk Analysis",
        "feature_risk_desc": "Review liquidity and capital structure indicators.",
        "feature_diagnostic": "Financial Diagnostic",
        "feature_diagnostic_desc": "Identify strengths and areas that need attention.",
        "feature_reports": "Reports",
        "feature_reports_desc": "Prepare a structured summary of your analysis.",
        "home_import_hint": "Start by importing an Excel workbook to explore your data.",
        "import_title": "Import financial data",
        "import_intro": "Upload an Excel workbook, choose a worksheet, and review its contents.",
        "upload_label": "Excel workbook",
        "upload_help": "Supported formats: .xlsx and .xls",
        "no_file": "Choose an Excel file to begin.",
        "file_ready": "Workbook loaded: {filename}",
        "worksheets": "Available worksheets",
        "select_sheet": "Select a worksheet",
        "load_sheet": "Load worksheet",
        "sheet_loaded": "Worksheet loaded successfully.",
        "import_error": "The workbook could not be read: {error}",
        "no_sheets": "No worksheets were found in this workbook.",
        "rows": "Rows",
        "columns": "Columns",
        "numeric_columns": "Numeric columns",
        "preview": "Data preview",
        "validation": "Data validation",
        "validation_ok": "No major data-quality issues were detected.",
        "empty_data": "The selected worksheet is empty.",
        "missing_headers": "One or more column names are missing or blank.",
        "duplicate_headers": "Duplicate column names were detected.",
        "missing_values": "{count} missing cell(s) were found.",
        "empty_rows": "{count} completely empty row(s) were found.",
        "empty_columns": "{count} completely empty column(s) were found.",
        "invalid_numeric": (
            "{count} value(s) in financial columns could not be interpreted as numbers."
        ),
        "no_columns": "The worksheet has no columns.",
        "continue_dashboard": "Continue to Dashboard",
        "current_data": "Currently loaded data",
        "change_sheet_note": "Load another worksheet to replace the currently loaded data.",
        "dashboard_title": "Financial dashboard",
        "dashboard_intro": "A high-level view of the available financial data.",
        "empty_state_title": "Your dashboard is ready when your data is",
        "empty_state_body": "Import an Excel worksheet to see available KPIs, charts, and data-quality information.",
        "go_import": "Go to Import Data",
        "key_indicators": "Key indicators",
        "not_available": "Not available",
        "revenue": "Revenue",
        "gross_profit": "Gross profit",
        "gross_margin": "Gross margin",
        "operating_margin": "Operating margin",
        "net_income": "Net income",
        "net_margin": "Net margin",
        "roa": "Return on assets (ROA)",
        "roe": "Return on equity (ROE)",
        "current_ratio": "Current ratio",
        "quick_ratio": "Quick ratio",
        "cash_ratio": "Cash ratio",
        "debt_ratio": "Debt ratio",
        "debt_to_equity": "Debt-to-equity",
        "equity_ratio": "Equity ratio",
        "financial_leverage": "Financial leverage",
        "asset_turnover": "Asset turnover",
        "inventory_turnover": "Inventory turnover",
        "receivables_turnover": "Receivables turnover",
        "cash": "Cash",
        "total_assets": "Total assets",
        "total_liabilities": "Total liabilities",
        "equity": "Equity",
        "current_assets": "Current assets",
        "current_liabilities": "Current liabilities",
        "revenue_trend": "Revenue and net income",
        "data_quality": "Missing values by column",
        "row_number": "Row",
        "financial_analysis_title": "Financial analysis",
        "analysis_intro": "Indicators are calculated only when the required data is available.",
        "profitability": "Profitability",
        "liquidity": "Liquidity",
        "solvency": "Solvency and capital structure",
        "efficiency": "Efficiency",
        "indicator": "Indicator",
        "value": "Value",
        "interpretation": "Calculation",
        "formula_gross_margin": "Gross profit ÷ revenue",
        "formula_operating_margin": "Operating income ÷ revenue",
        "formula_net_margin": "Net income ÷ revenue",
        "formula_roa": "Net income ÷ total assets",
        "formula_roe": "Net income ÷ equity",
        "formula_current_ratio": "Current assets ÷ current liabilities",
        "formula_quick_ratio": "(Current assets − inventory) ÷ current liabilities",
        "formula_cash_ratio": "Cash ÷ current liabilities",
        "formula_debt_ratio": "Total liabilities (or debt) ÷ total assets",
        "formula_debt_to_equity": "Debt (or total liabilities) ÷ equity",
        "formula_equity_ratio": "Equity ÷ total assets",
        "formula_financial_leverage": "Total assets ÷ equity",
        "formula_asset_turnover": "Revenue ÷ total assets",
        "formula_inventory_turnover": "Cost of goods sold ÷ inventory",
        "formula_receivables_turnover": "Revenue ÷ receivables",
        "formula_not_available": "Required source columns were not detected.",
        "diagnostic_title": "Financial diagnostic",
        "diagnostic_intro": "Observations below are based on transparent rules and detected data only.",
        "strengths": "Financial strengths",
        "attention": "Areas requiring attention",
        "risks": "Potential risks",
        "observations": "Key observations",
        "no_strengths": "No strengths can be confirmed from the available indicators yet.",
        "no_attention": "No threshold-based warning was triggered by the available indicators.",
        "insufficient_data": "Some conclusions are limited because required information is missing.",
        "missing_info": "Missing information affecting indicators: {items}.",
        "liquidity_pressure": "Potential liquidity pressure: the current ratio is below 1.",
        "healthy_liquidity": "Positive liquidity signal: the current ratio is at least 1.5.",
        "high_debt": "Potential risk: the debt ratio is above 70%.",
        "moderate_debt": "Positive capital-structure signal: the debt ratio is 50% or lower.",
        "negative_margin": "Potential profitability risk: the net margin is negative.",
        "positive_margin": "Positive profitability signal: the net margin is above 10%.",
        "strong_equity": "Positive capital signal: equity represents more than half of total assets.",
        "improving_margin": "Positive trend: net margin has improved across the available rows.",
        "declining_margin": "Attention: net margin has declined across the available rows.",
        "improving_revenue": "Positive trend: revenue has increased across the available rows.",
        "declining_revenue": "Attention: revenue has decreased across the available rows.",
        "no_rule_triggered": "No critical threshold was triggered by the indicators that could be calculated.",
        "report_title": "Financial report",
        "report_intro": "Review the summary below and download a shareable HTML report.",
        "company_overview": "Data overview",
        "report_summary": "Main indicators",
        "report_profitability": "Profitability",
        "report_liquidity": "Liquidity",
        "report_solvency": "Solvency",
        "report_efficiency": "Efficiency",
        "download_report": "Download HTML report",
        "report_generated": "The report reflects the currently loaded worksheet.",
        "source_file": "Source file",
        "source_sheet": "Worksheet",
        "no_report_data": "Import data before generating a report.",
        "report_download_name": "findiag_financial_report.html",
        "records": "records",
        "fields": "fields",
        "missing": "Missing",
        "column": "Column",
        "financial_dataset": "Financial dataset",
        "no_financial_columns": "No recognized financial columns were detected. Review the worksheet headers.",
        "validation_details": "Validation details",
        "load_first": "Load a worksheet to view its preview and validation results.",
    },
    "fr": {
        "language": "Langue",
        "english": "🇬🇧 English",
        "french": "🇫🇷 Français",
        "arabic": "🇸🇦 العربية",
        "home": "Accueil",
        "dashboard": "Tableau de bord",
        "analysis": "Analyse",
        "diagnostic": "Diagnostic",
        "report": "Rapport",
        "import_data": "Importer les données",
        "brand_tagline": "La clarté financière, fondée sur vos données",
        "home_title": "Intelligence Financière",
        "home_subtitle": (
            "Transformez vos données financières en analyses claires, "
            "diagnostics pratiques et informations exploitables."
        ),
        "start_analysis": "Commencer l'analyse",
        "features_title": "Une vision plus claire de la performance financière",
        "feature_performance": "Performance financière",
        "feature_performance_desc": "Suivez les chiffres clés et les indicateurs de performance.",
        "feature_risk": "Analyse des risques",
        "feature_risk_desc": "Examinez la liquidité et la structure du capital.",
        "feature_diagnostic": "Diagnostic financier",
        "feature_diagnostic_desc": "Identifiez les points forts et les éléments à surveiller.",
        "feature_reports": "Rapports",
        "feature_reports_desc": "Préparez une synthèse structurée de votre analyse.",
        "home_import_hint": "Commencez par importer un classeur Excel pour explorer vos données.",
        "import_title": "Importer des données financières",
        "import_intro": "Importez un classeur Excel, choisissez une feuille et examinez son contenu.",
        "upload_label": "Classeur Excel",
        "upload_help": "Formats pris en charge : .xlsx et .xls",
        "no_file": "Choisissez un fichier Excel pour commencer.",
        "file_ready": "Classeur chargé : {filename}",
        "worksheets": "Feuilles disponibles",
        "select_sheet": "Sélectionner une feuille",
        "load_sheet": "Charger la feuille",
        "sheet_loaded": "La feuille a été chargée avec succès.",
        "import_error": "Impossible de lire le classeur : {error}",
        "no_sheets": "Aucune feuille n'a été trouvée dans ce classeur.",
        "rows": "Lignes",
        "columns": "Colonnes",
        "numeric_columns": "Colonnes numériques",
        "preview": "Aperçu des données",
        "validation": "Validation des données",
        "validation_ok": "Aucun problème majeur de qualité des données n'a été détecté.",
        "empty_data": "La feuille sélectionnée est vide.",
        "missing_headers": "Un ou plusieurs noms de colonnes sont manquants ou vides.",
        "duplicate_headers": "Des noms de colonnes en double ont été détectés.",
        "missing_values": "{count} cellule(s) manquante(s) détectée(s).",
        "empty_rows": "{count} ligne(s) entièrement vide(s) détectée(s).",
        "empty_columns": "{count} colonne(s) entièrement vide(s) détectée(s).",
        "invalid_numeric": (
            "{count} valeur(s) de colonnes financières n'ont pas pu être interprétées comme des nombres."
        ),
        "no_columns": "La feuille ne contient aucune colonne.",
        "continue_dashboard": "Continuer vers le tableau de bord",
        "current_data": "Données actuellement chargées",
        "change_sheet_note": "Chargez une autre feuille pour remplacer les données actuellement chargées.",
        "dashboard_title": "Tableau de bord financier",
        "dashboard_intro": "Vue d'ensemble des données financières disponibles.",
        "empty_state_title": "Votre tableau de bord est prêt dès que vos données le sont",
        "empty_state_body": "Importez une feuille Excel pour afficher les indicateurs, graphiques et informations sur la qualité des données.",
        "go_import": "Importer les données",
        "key_indicators": "Indicateurs clés",
        "not_available": "Non disponible",
        "revenue": "Chiffre d'affaires",
        "gross_profit": "Marge brute",
        "gross_margin": "Taux de marge brute",
        "operating_margin": "Marge opérationnelle",
        "net_income": "Résultat net",
        "net_margin": "Marge nette",
        "roa": "Rentabilité des actifs (ROA)",
        "roe": "Rentabilité des capitaux propres (ROE)",
        "current_ratio": "Ratio de liquidité générale",
        "quick_ratio": "Ratio de liquidité réduite",
        "cash_ratio": "Ratio de liquidité immédiate",
        "debt_ratio": "Ratio d'endettement",
        "debt_to_equity": "Endettement / capitaux propres",
        "equity_ratio": "Ratio de fonds propres",
        "financial_leverage": "Levier financier",
        "asset_turnover": "Rotation des actifs",
        "inventory_turnover": "Rotation des stocks",
        "receivables_turnover": "Rotation des créances",
        "cash": "Trésorerie",
        "total_assets": "Total de l'actif",
        "total_liabilities": "Total des passifs",
        "equity": "Capitaux propres",
        "current_assets": "Actif circulant",
        "current_liabilities": "Passif circulant",
        "revenue_trend": "Chiffre d'affaires et résultat net",
        "data_quality": "Valeurs manquantes par colonne",
        "row_number": "Ligne",
        "financial_analysis_title": "Analyse financière",
        "analysis_intro": "Les indicateurs sont calculés uniquement lorsque les données requises sont disponibles.",
        "profitability": "Rentabilité",
        "liquidity": "Liquidité",
        "solvency": "Solvabilité et structure du capital",
        "efficiency": "Efficacité",
        "indicator": "Indicateur",
        "value": "Valeur",
        "interpretation": "Calcul",
        "formula_gross_margin": "Marge brute ÷ chiffre d'affaires",
        "formula_operating_margin": "Résultat opérationnel ÷ chiffre d'affaires",
        "formula_net_margin": "Résultat net ÷ chiffre d'affaires",
        "formula_roa": "Résultat net ÷ total de l'actif",
        "formula_roe": "Résultat net ÷ capitaux propres",
        "formula_current_ratio": "Actif circulant ÷ passif circulant",
        "formula_quick_ratio": "(Actif circulant − stocks) ÷ passif circulant",
        "formula_cash_ratio": "Trésorerie ÷ passif circulant",
        "formula_debt_ratio": "Passifs totaux (ou dettes) ÷ total de l'actif",
        "formula_debt_to_equity": "Dettes (ou passifs totaux) ÷ capitaux propres",
        "formula_equity_ratio": "Capitaux propres ÷ total de l'actif",
        "formula_financial_leverage": "Total de l'actif ÷ capitaux propres",
        "formula_asset_turnover": "Chiffre d'affaires ÷ total de l'actif",
        "formula_inventory_turnover": "Coût des ventes ÷ stocks",
        "formula_receivables_turnover": "Chiffre d'affaires ÷ créances",
        "formula_not_available": "Les colonnes sources requises n'ont pas été détectées.",
        "diagnostic_title": "Diagnostic financier",
        "diagnostic_intro": "Les observations reposent sur des règles transparentes et les données détectées.",
        "strengths": "Points forts financiers",
        "attention": "Points à surveiller",
        "risks": "Risques potentiels",
        "observations": "Observations principales",
        "no_strengths": "Les indicateurs disponibles ne permettent pas encore de confirmer de point fort.",
        "no_attention": "Aucune alerte fondée sur les seuils n'a été déclenchée par les indicateurs disponibles.",
        "insufficient_data": "Certaines conclusions sont limitées, car des informations requises sont manquantes.",
        "missing_info": "Informations manquantes affectant les indicateurs : {items}.",
        "liquidity_pressure": "Pression potentielle sur la liquidité : le ratio de liquidité générale est inférieur à 1.",
        "healthy_liquidity": "Signal positif de liquidité : le ratio de liquidité générale est au moins égal à 1,5.",
        "high_debt": "Risque potentiel : le ratio d'endettement dépasse 70 %.",
        "moderate_debt": "Signal positif de structure du capital : le ratio d'endettement est inférieur ou égal à 50 %.",
        "negative_margin": "Risque potentiel de rentabilité : la marge nette est négative.",
        "positive_margin": "Signal positif de rentabilité : la marge nette dépasse 10 %.",
        "strong_equity": "Signal positif de capital : les capitaux propres représentent plus de la moitié de l'actif.",
        "improving_margin": "Tendance positive : la marge nette s'est améliorée sur les lignes disponibles.",
        "declining_margin": "À surveiller : la marge nette a diminué sur les lignes disponibles.",
        "improving_revenue": "Tendance positive : le chiffre d'affaires a augmenté sur les lignes disponibles.",
        "declining_revenue": "À surveiller : le chiffre d'affaires a diminué sur les lignes disponibles.",
        "no_rule_triggered": "Aucun seuil critique n'a été déclenché par les indicateurs calculables.",
        "report_title": "Rapport financier",
        "report_intro": "Consultez la synthèse ci-dessous et téléchargez un rapport HTML partageable.",
        "company_overview": "Aperçu des données",
        "report_summary": "Indicateurs principaux",
        "report_profitability": "Rentabilité",
        "report_liquidity": "Liquidité",
        "report_solvency": "Solvabilité",
        "report_efficiency": "Efficacité",
        "download_report": "Télécharger le rapport HTML",
        "report_generated": "Le rapport correspond à la feuille actuellement chargée.",
        "source_file": "Fichier source",
        "source_sheet": "Feuille",
        "no_report_data": "Importez des données avant de générer un rapport.",
        "report_download_name": "rapport_financier_findiag.html",
        "records": "enregistrements",
        "fields": "champs",
        "missing": "Manquant",
        "column": "Colonne",
        "financial_dataset": "Jeu de données financier",
        "no_financial_columns": "Aucune colonne financière reconnue. Vérifiez les en-têtes de la feuille.",
        "validation_details": "Détails de validation",
        "load_first": "Chargez une feuille pour afficher son aperçu et les résultats de validation.",
    },
    "ar": {
        "language": "اللغة",
        "english": "🇬🇧 English",
        "french": "🇫🇷 Français",
        "arabic": "🇸🇦 العربية",
        "home": "الرئيسية",
        "dashboard": "لوحة المعلومات",
        "analysis": "التحليل",
        "diagnostic": "التشخيص",
        "report": "التقرير",
        "import_data": "استيراد البيانات",
        "brand_tagline": "وضوح مالي يستند إلى بياناتك",
        "home_title": "الذكاء المالي",
        "home_subtitle": "حوّل بياناتك المالية إلى تحليل واضح وتشخيص عملي ورؤى قابلة للتنفيذ.",
        "start_analysis": "بدء التحليل",
        "features_title": "رؤية أوضح للأداء المالي",
        "feature_performance": "الأداء المالي",
        "feature_performance_desc": "تابع الأرقام الرئيسية ومؤشرات الأداء.",
        "feature_risk": "تحليل المخاطر",
        "feature_risk_desc": "راجع مؤشرات السيولة وهيكل رأس المال.",
        "feature_diagnostic": "التشخيص المالي",
        "feature_diagnostic_desc": "حدّد نقاط القوة والمجالات التي تتطلب الانتباه.",
        "feature_reports": "التقارير",
        "feature_reports_desc": "أعد ملخصاً منظماً للتحليل.",
        "home_import_hint": "ابدأ باستيراد مصنف Excel لاستكشاف بياناتك.",
        "import_title": "استيراد البيانات المالية",
        "import_intro": "ارفع مصنف Excel، واختر ورقة عمل، ثم راجع محتواها.",
        "upload_label": "مصنف Excel",
        "upload_help": "الصيغ المدعومة: .xlsx و .xls",
        "no_file": "اختر ملف Excel للبدء.",
        "file_ready": "تم تحميل المصنف: {filename}",
        "worksheets": "أوراق العمل المتاحة",
        "select_sheet": "اختر ورقة عمل",
        "load_sheet": "تحميل ورقة العمل",
        "sheet_loaded": "تم تحميل ورقة العمل بنجاح.",
        "import_error": "تعذرت قراءة المصنف: {error}",
        "no_sheets": "لم يتم العثور على أوراق عمل في هذا المصنف.",
        "rows": "الصفوف",
        "columns": "الأعمدة",
        "numeric_columns": "الأعمدة الرقمية",
        "preview": "معاينة البيانات",
        "validation": "التحقق من البيانات",
        "validation_ok": "لم يتم اكتشاف مشكلات كبيرة في جودة البيانات.",
        "empty_data": "ورقة العمل المحددة فارغة.",
        "missing_headers": "اسم عمود واحد أو أكثر مفقود أو فارغ.",
        "duplicate_headers": "تم اكتشاف أسماء أعمدة مكررة.",
        "missing_values": "تم العثور على {count} خلية مفقودة.",
        "empty_rows": "تم العثور على {count} صف فارغ بالكامل.",
        "empty_columns": "تم العثور على {count} عمود فارغ بالكامل.",
        "invalid_numeric": "تعذر تفسير {count} قيمة في الأعمدة المالية كأرقام.",
        "no_columns": "لا تحتوي ورقة العمل على أعمدة.",
        "continue_dashboard": "المتابعة إلى لوحة المعلومات",
        "current_data": "البيانات المحمّلة حالياً",
        "change_sheet_note": "حمّل ورقة أخرى لاستبدال البيانات المحمّلة حالياً.",
        "dashboard_title": "لوحة المعلومات المالية",
        "dashboard_intro": "نظرة عامة على البيانات المالية المتاحة.",
        "empty_state_title": "ستكون لوحة المعلومات جاهزة عند توفر بياناتك",
        "empty_state_body": "استورد ورقة Excel لعرض المؤشرات والرسوم البيانية ومعلومات جودة البيانات.",
        "go_import": "الانتقال إلى استيراد البيانات",
        "key_indicators": "المؤشرات الرئيسية",
        "not_available": "غير متاح",
        "revenue": "الإيرادات",
        "gross_profit": "الربح الإجمالي",
        "gross_margin": "هامش الربح الإجمالي",
        "operating_margin": "هامش التشغيل",
        "net_income": "صافي الدخل",
        "net_margin": "هامش صافي الربح",
        "roa": "العائد على الأصول",
        "roe": "العائد على حقوق الملكية",
        "current_ratio": "نسبة التداول",
        "quick_ratio": "نسبة السيولة السريعة",
        "cash_ratio": "نسبة النقدية",
        "debt_ratio": "نسبة الدين",
        "debt_to_equity": "الدين إلى حقوق الملكية",
        "equity_ratio": "نسبة حقوق الملكية",
        "financial_leverage": "الرافعة المالية",
        "asset_turnover": "معدل دوران الأصول",
        "inventory_turnover": "معدل دوران المخزون",
        "receivables_turnover": "معدل دوران الذمم المدينة",
        "cash": "النقدية",
        "total_assets": "إجمالي الأصول",
        "total_liabilities": "إجمالي الالتزامات",
        "equity": "حقوق الملكية",
        "current_assets": "الأصول المتداولة",
        "current_liabilities": "الالتزامات المتداولة",
        "revenue_trend": "الإيرادات وصافي الدخل",
        "data_quality": "القيم المفقودة حسب العمود",
        "row_number": "الصف",
        "financial_analysis_title": "التحليل المالي",
        "analysis_intro": "تُحسب المؤشرات فقط عند توفر البيانات المطلوبة.",
        "profitability": "الربحية",
        "liquidity": "السيولة",
        "solvency": "الملاءة وهيكل رأس المال",
        "efficiency": "الكفاءة",
        "indicator": "المؤشر",
        "value": "القيمة",
        "interpretation": "طريقة الحساب",
        "formula_gross_margin": "الربح الإجمالي ÷ الإيرادات",
        "formula_operating_margin": "الدخل التشغيلي ÷ الإيرادات",
        "formula_net_margin": "صافي الدخل ÷ الإيرادات",
        "formula_roa": "صافي الدخل ÷ إجمالي الأصول",
        "formula_roe": "صافي الدخل ÷ حقوق الملكية",
        "formula_current_ratio": "الأصول المتداولة ÷ الالتزامات المتداولة",
        "formula_quick_ratio": "(الأصول المتداولة − المخزون) ÷ الالتزامات المتداولة",
        "formula_cash_ratio": "النقدية ÷ الالتزامات المتداولة",
        "formula_debt_ratio": "إجمالي الالتزامات (أو الدين) ÷ إجمالي الأصول",
        "formula_debt_to_equity": "الدين (أو إجمالي الالتزامات) ÷ حقوق الملكية",
        "formula_equity_ratio": "حقوق الملكية ÷ إجمالي الأصول",
        "formula_financial_leverage": "إجمالي الأصول ÷ حقوق الملكية",
        "formula_asset_turnover": "الإيرادات ÷ إجمالي الأصول",
        "formula_inventory_turnover": "تكلفة البضاعة المباعة ÷ المخزون",
        "formula_receivables_turnover": "الإيرادات ÷ الذمم المدينة",
        "formula_not_available": "لم يتم التعرف على الأعمدة المصدر المطلوبة.",
        "diagnostic_title": "التشخيص المالي",
        "diagnostic_intro": "تستند الملاحظات إلى قواعد واضحة والبيانات التي تم التعرف عليها فقط.",
        "strengths": "نقاط القوة المالية",
        "attention": "مجالات تتطلب الانتباه",
        "risks": "مخاطر محتملة",
        "observations": "ملاحظات رئيسية",
        "no_strengths": "لا تكفي المؤشرات المتاحة لتأكيد نقاط قوة حالياً.",
        "no_attention": "لم تُفعّل المؤشرات المتاحة أي تنبيه قائم على الحدود المحددة.",
        "insufficient_data": "بعض الاستنتاجات محدودة بسبب نقص المعلومات المطلوبة.",
        "missing_info": "المعلومات الناقصة التي تؤثر في المؤشرات: {items}.",
        "liquidity_pressure": "ضغط محتمل على السيولة: نسبة التداول أقل من 1.",
        "healthy_liquidity": "إشارة إيجابية للسيولة: نسبة التداول لا تقل عن 1.5.",
        "high_debt": "مخاطر محتملة: نسبة الدين تتجاوز 70٪.",
        "moderate_debt": "إشارة إيجابية لهيكل رأس المال: نسبة الدين لا تتجاوز 50٪.",
        "negative_margin": "مخاطر محتملة على الربحية: هامش صافي الربح سلبي.",
        "positive_margin": "إشارة إيجابية للربحية: هامش صافي الربح يتجاوز 10٪.",
        "strong_equity": "إشارة إيجابية لرأس المال: تمثل حقوق الملكية أكثر من نصف الأصول.",
        "improving_margin": "اتجاه إيجابي: تحسن هامش صافي الربح عبر الصفوف المتاحة.",
        "declining_margin": "يتطلب الانتباه: تراجع هامش صافي الربح عبر الصفوف المتاحة.",
        "improving_revenue": "اتجاه إيجابي: ارتفعت الإيرادات عبر الصفوف المتاحة.",
        "declining_revenue": "يتطلب الانتباه: انخفضت الإيرادات عبر الصفوف المتاحة.",
        "no_rule_triggered": "لم يتم تجاوز أي حد حرج في المؤشرات التي أمكن حسابها.",
        "report_title": "التقرير المالي",
        "report_intro": "راجع الملخص أدناه ونزّل تقرير HTML قابل للمشاركة.",
        "company_overview": "نظرة عامة على البيانات",
        "report_summary": "المؤشرات الرئيسية",
        "report_profitability": "الربحية",
        "report_liquidity": "السيولة",
        "report_solvency": "الملاءة",
        "report_efficiency": "الكفاءة",
        "download_report": "تنزيل تقرير HTML",
        "report_generated": "يعكس التقرير ورقة العمل المحمّلة حالياً.",
        "source_file": "الملف المصدر",
        "source_sheet": "ورقة العمل",
        "no_report_data": "استورد البيانات قبل إنشاء التقرير.",
        "report_download_name": "تقرير_مالي_findiag.html",
        "records": "سجل",
        "fields": "حقل",
        "missing": "مفقود",
        "column": "العمود",
        "financial_dataset": "مجموعة بيانات مالية",
        "no_financial_columns": "لم يتم التعرف على أعمدة مالية. راجع عناوين ورقة العمل.",
        "validation_details": "تفاصيل التحقق",
        "load_first": "حمّل ورقة عمل لعرض المعاينة ونتائج التحقق.",
    },
}


def get_translation(key: str, **kwargs: Any) -> str:
    """Return the active translation, with English as a defensive fallback."""
    language = st.session_state.get("language", "en")
    template = TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(
        key, TRANSLATIONS["en"].get(key, key)
    )
    try:
        return template.format(**kwargs)
    except (KeyError, ValueError):
        return template


def t(key: str, **kwargs: Any) -> str:
    return get_translation(key, **kwargs)


def _language_changed() -> None:
    st.session_state.language = st.session_state.language_widget


def _navigate(page: str) -> None:
    st.session_state.page = page


def initialize_state() -> None:
    defaults = {
        "page": "home",
        "language": "en",
        "language_widget": "en",
        "uploaded_file": None,
        "uploaded_filename": None,
        "file_signature": None,
        "sheet_names": [],
        "selected_sheet": None,
        "data": None,
        "analysis_results": None,
        "diagnostic_results": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_state()


# ---------------------------------------------------------------------------
# Styling and generated geometric wordmark
# ---------------------------------------------------------------------------

def inject_styles() -> None:
    is_rtl = st.session_state.language == "ar"
    direction = "rtl" if is_rtl else "ltr"
    alignment = "right" if is_rtl else "left"

    # This block contains CSS only; all visible page content uses Streamlit widgets.
    st.markdown(
        f"""
        <style>
        .st-key-findiag_header [data-testid="stHorizontalBlock"] {{
            direction: ltr;
        }}
                .st-key-findiag_navigation [data-testid="stHorizontalBlock"] {{
            direction: ltr;
            flex-direction: {"row-reverse" if is_rtl else "row"} !important;
        }}
        .st-key-findiag_header [data-testid="stSelectbox"] {{
            direction: {direction};
        }}
        .stApp {{
            background: #F7FAFF;
            color: #172033;
            direction: {direction};
        }}
        [data-testid="stAppViewContainer"] {{
            direction: {direction};
        }}
        [data-testid="stMain"] {{
            direction: {direction};
        }}
        [data-testid="stMarkdownContainer"] {{
            text-align: {alignment};
        }}
        [data-testid="stHeader"] {{
            background: rgba(247, 250, 255, 0.94);
        }}
        [data-testid="stMain"] .block-container {{
            max-width: 1320px;
            padding-top: 5rem !important;
            padding-bottom: 3rem;
        }}
        h1, h2, h3 {{
            color: #172033;
            letter-spacing: -0.02em;
        }}
        [data-testid="stMetric"] {{
            background: #FFFFFF;
            border: 1px solid #E4E9F1;
            border-radius: 14px;
            padding: 16px 18px;
        }}
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: #E4E9F1 !important;
            border-radius: 14px !important;
            background: #FFFFFF;
        }}
        .stButton > button {{
            border-radius: 10px;
            font-weight: 600;
            min-height: 2.6rem;
        }}
        [data-testid="stFileUploader"] {{
            border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_logo_svg() -> str:
    """Create a spacious, geometric FINDIAG wordmark with a dark A accent."""
    glyphs = [
        # F
        '<path d="M5 5 H44 M5 5 V57 M5 30 H35"/>',
        # I
        '<path d="M12 5 H38 M25 5 V57 M12 57 H38"/>',
        # N
        '<path d="M5 57 V5 L45 57 V5"/>',
        # D
        '<path d="M5 5 V57 H23 C52 57 52 5 23 5 Z"/>',
        # I
        '<path d="M12 5 H38 M25 5 V57 M12 57 H38"/>',
        # A: dark crossbar is the small brand accent.
        '<path d="M5 57 L25 5 L45 57"/>',
        # G
        '<path d="M45 15 C40 7 33 4 24 4 C8 4 4 17 4 31 C4 48 12 58 26 58 C35 58 42 54 45 49 V33 H27"/>',
    ]

    elements: list[str] = []
    for index, path in enumerate(glyphs):
        x = 8 + index * 63
        elements.append(
            f'<g transform="translate({x}, 0)" fill="none" stroke="#4183C4" '
            f'stroke-width="7" stroke-linecap="square" stroke-linejoin="miter">{path}</g>'
        )
        if index == 5:
            elements.append(
                f'<path d="M{8 + index * 63 + 16} 38 H{8 + index * 63 + 34}" '
                'fill="none" stroke="#1F2324" stroke-width="7" stroke-linecap="square"/>'
            )

    return (
       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 68" '
       'width="450" height="68" role="img" aria-label="FINDIAG">'
        '<rect width="450" height="68" fill="transparent"/>'
        + "".join(elements)
        + "</svg>"
    )


def render_header() -> None:
    assets = Path("assets")
    assets.mkdir(parents=True, exist_ok=True)
    logo_path = assets / "findiag_logo.svg"
    logo_svg = create_logo_svg()
    if not logo_path.exists() or logo_path.read_text(encoding="utf-8") != logo_svg:
        logo_path.write_text(logo_svg, encoding="utf-8")

    language_options = ["en", "fr", "ar"]
    display_names = {
        "en": t("english"),
        "fr": t("french"),
        "ar": t("arabic"),
    }

    with st.container(key="findiag_header"):
        logo_col, language_col = st.columns([5.2, 1.8])

        with logo_col:
            st.image(logo_svg, width=190)
            st.caption(t("brand_tagline"))

        with language_col:
            selected = st.selectbox(
                t("language"),
                language_options,
                format_func=lambda value: display_names[value],
                key="language_widget",
                on_change=_language_changed,
                label_visibility="collapsed",
            )

    # Keep the selected language in the durable application state.
    st.session_state.language = selected
    st.divider()


def render_navigation() -> None:
    pages = [
        ("home", "home"),
        ("dashboard", "dashboard"),
        ("analysis", "analysis"),
        ("simulation", "simulation"),
        ("diagnostic", "diagnostic"),
        ("report", "report"),
        ("import", "import_data"),
    ]

    # Do not reverse this list. The CSS reverses the visual column order
    # for Arabic, putting Home at the right and Import Data at the left.
    with st.container(key="findiag_navigation"):
        columns = st.columns(len(pages))
        for column, (page_id, label_key) in zip(columns, pages):
            with column:
                st.button(
                    t(label_key),
                    key=f"nav_{page_id}",
                    type="primary" if st.session_state.page == page_id else "secondary",
                    use_container_width=True,
                    on_click=_navigate,
                    args=(page_id,),
                )

    st.write("")


# ---------------------------------------------------------------------------
# Data validation, normalization, and financial column detection
# ---------------------------------------------------------------------------

ALIASES: dict[str, list[str]] = {
    "revenue": [
        "revenue", "sales", "net sales", "turnover", "chiffre d'affaires",
        "chiffre affaires", "ca", "ventes", "produits", "الإيرادات", "المبيعات",
    ],
    "cost_of_goods_sold": [
        "cost of goods sold", "cogs", "cost of sales", "cost of revenue",
        "cout des ventes", "coût des ventes", "achats consommés", "coût d'achat",
    ],
    "gross_profit": [
        "gross profit", "gross income", "profit brut", "marge brute",
        "الربح الإجمالي",
    ],
    "operating_income": [
        "operating income", "operating profit", "ebit", "résultat opérationnel",
        "resultat operationnel", "résultat d'exploitation", "resultat exploitation",
    ],
    "net_income": [
        "net income", "net profit", "profit after tax", "net earnings",
        "résultat net", "resultat net", "bénéfice net", "benefice net",
        "صافي الدخل", "صافي الربح",
    ],
    "total_assets": [
        "total assets", "assets total", "total asset", "total actif",
        "total de l'actif", "actif total", "إجمالي الأصول",
    ],
    "current_assets": [
        "current assets", "circulating assets", "actif circulant",
        "actifs circulants", "الأصول المتداولة",
    ],
    "inventory": [
        "inventory", "inventories", "stock", "stocks", "inventaire", "المخزون",
    ],
    "cash": [
        "cash", "cash and cash equivalents", "cash equivalents", "trésorerie",
        "tresorerie", "disponibilités", "disponibilites", "نقدية", "النقدية",
    ],
    "receivables": [
        "receivables", "accounts receivable", "trade receivables",
        "créances clients", "creances clients", "clients", "الذمم المدينة",
    ],
    "current_liabilities": [
        "current liabilities", "short term liabilities", "current debt",
        "passif circulant", "dettes à court terme", "dettes court terme",
        "الالتزامات المتداولة",
    ],
    "total_liabilities": [
        "total liabilities", "liabilities total", "total liabilities and debt",
        "total passif", "total des passifs", "total dettes", "إجمالي الالتزامات",
    ],
    "debt": [
        "debt", "total debt", "financial debt", "borrowings", "dettes",
        "emprunts", "الدين", "الديون",
    ],
    "equity": [
        "equity", "shareholders equity", "total equity", "shareholder funds",
        "capitaux propres", "fonds propres", "حقوق الملكية",
    ],
}


def normalize_text(value: Any) -> str:
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("’", "'")
    text = re.sub(r"[_\-./]+", " ", text)
    text = re.sub(r"[^\w\s']", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def parse_number(value: Any) -> float:
    """Parse common numeric strings, including decimal-comma formats."""
    if pd.isna(value):
        return float("nan")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    text = str(value).strip().replace("\u00a0", "").replace(" ", "")
    if not text:
        return float("nan")

    # Keep digits, decimal marks, signs and scientific notation.
    text = re.sub(r"[^0-9,.\-+eE]", "", text)
    if not text:
        return float("nan")

    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        pieces = text.split(",")
        if len(pieces) == 2 and len(pieces[-1]) in (1, 2):
            text = text.replace(",", ".")
        else:
            text = text.replace(",", "")

    try:
        return float(text)
    except ValueError:
        return float("nan")


def numeric_series(series: pd.Series) -> pd.Series:
    direct = pd.to_numeric(series, errors="coerce")
    if direct.notna().sum() >= series.notna().sum() * 0.8:
        return direct.astype(float)
    return series.map(parse_number).astype(float)


def detect_financial_columns(df: pd.DataFrame) -> dict[str, int]:
    """Map recognized financial concepts to their column positions."""
    detected: dict[str, int] = {}
    if df is None or df.empty:
        return detected

    normalized_columns = [normalize_text(column) for column in df.columns]
    normalized_aliases = {
        concept: [normalize_text(alias) for alias in aliases]
        for concept, aliases in ALIASES.items()
    }

    for concept, aliases in normalized_aliases.items():
        # Prefer exact matches to avoid loose matches such as "debt" in a long label.
        for index, column_name in enumerate(normalized_columns):
            if column_name and column_name in aliases:
                detected[concept] = index
                break

        if concept in detected:
            continue

        for index, column_name in enumerate(normalized_columns):
            if not column_name:
                continue
            if any(
                len(alias) >= 5 and (alias in column_name or column_name in alias)
                for alias in aliases
            ):
                detected[concept] = index
                break

    return detected


def validate_data(df: pd.DataFrame) -> tuple[list[tuple[str, dict[str, Any]]], dict[str, int]]:
    """Return translated-message keys and summary counts for a worksheet."""
    messages: list[tuple[str, dict[str, Any]]] = []
    counts = {
        "rows": 0 if df is None else len(df),
        "columns": 0 if df is None else len(df.columns),
        "numeric_columns": 0,
        "missing_values": 0,
    }

    if df is None or df.empty:
        messages.append(("empty_data", {}))
        return messages, counts

    counts["missing_values"] = int(df.isna().sum().sum())
    counts["numeric_columns"] = sum(
        1 for index in range(df.shape[1])
        if numeric_series(df.iloc[:, index]).notna().any()
    )

    if len(df.columns) == 0:
        messages.append(("no_columns", {}))
    if any(
        column is None
        or not str(column).strip()
        or str(column).strip().lower().startswith("unnamed:")
        for column in df.columns
    ):
        messages.append(("missing_headers", {}))
    if pd.Index(df.columns).duplicated().any():
        messages.append(("duplicate_headers", {}))

    empty_rows = int(df.isna().all(axis=1).sum())
    empty_columns = int(df.isna().all(axis=0).sum())
    if empty_rows:
        messages.append(("empty_rows", {"count": empty_rows}))
    if empty_columns:
        messages.append(("empty_columns", {"count": empty_columns}))
    if counts["missing_values"]:
        messages.append(("missing_values", {"count": counts["missing_values"]}))

    detected = detect_financial_columns(df)
    invalid_count = 0
    for index in set(detected.values()):
        source = df.iloc[:, index]
        parsed = numeric_series(source)
        invalid_count += int((source.notna() & parsed.isna()).sum())
    if invalid_count:
        messages.append(("invalid_numeric", {"count": invalid_count}))

    return messages, counts


def _column_values(df: pd.DataFrame, detected: dict[str, int], concept: str) -> pd.Series | None:
    index = detected.get(concept)
    if index is None or index >= df.shape[1]:
        return None
    return numeric_series(df.iloc[:, index])


def _last_value(series: pd.Series | None) -> float | None:
    if series is None:
        return None
    values = series.dropna()
    if values.empty:
        return None
    result = float(values.iloc[-1])
    return result if math.isfinite(result) else None


def safe_divide(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    result = numerator / denominator
    return result if math.isfinite(result) else None


def calculate_financial_metrics(df: pd.DataFrame) -> dict[str, Any]:
    """Calculate available metrics from the last non-empty observation."""
    detected = detect_financial_columns(df)
    series = {
        key: _column_values(df, detected, key)
        for key in ALIASES
    }
    last = {key: _last_value(value) for key, value in series.items()}

    revenue = last["revenue"]
    gross_profit = last["gross_profit"]
    if gross_profit is None and revenue is not None and last["cost_of_goods_sold"] is not None:
        gross_profit = revenue - last["cost_of_goods_sold"]

    liabilities = last["total_liabilities"]
    debt = last["debt"]
    ratio_liabilities = liabilities if liabilities is not None else debt
    debt_for_equity = debt if debt is not None else liabilities

    metrics: dict[str, float | None] = {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "gross_margin": safe_divide(gross_profit, revenue),
        "operating_margin": safe_divide(last["operating_income"], revenue),
        "net_income": last["net_income"],
        "net_margin": safe_divide(last["net_income"], revenue),
        "roa": safe_divide(last["net_income"], last["total_assets"]),
        "roe": safe_divide(last["net_income"], last["equity"]),
        "current_ratio": safe_divide(last["current_assets"], last["current_liabilities"]),
        "quick_ratio": safe_divide(
            None if last["current_assets"] is None else
            last["current_assets"] - (last["inventory"] or 0.0),
            last["current_liabilities"],
        ),
        "cash_ratio": safe_divide(last["cash"], last["current_liabilities"]),
        "debt_ratio": safe_divide(ratio_liabilities, last["total_assets"]),
        "debt_to_equity": safe_divide(debt_for_equity, last["equity"]),
        "equity_ratio": safe_divide(last["equity"], last["total_assets"]),
        "financial_leverage": safe_divide(last["total_assets"], last["equity"]),
        "asset_turnover": safe_divide(revenue, last["total_assets"]),
        "inventory_turnover": safe_divide(last["cost_of_goods_sold"], last["inventory"]),
        "receivables_turnover": safe_divide(revenue, last["receivables"]),
        "cash": last["cash"],
        "total_assets": last["total_assets"],
        "total_liabilities": liabilities,
        "equity": last["equity"],
        "current_assets": last["current_assets"],
        "current_liabilities": last["current_liabilities"],
    }

    st.session_state.analysis_results = metrics
    return metrics


def get_trend(df: pd.DataFrame, metric: str) -> int | None:
    """Return 1 for increasing, -1 for decreasing, 0 for unchanged, None if unavailable."""
    detected = detect_financial_columns(df)
    revenue = _column_values(df, detected, "revenue")
    if metric == "revenue":
        values = revenue
    elif metric == "net_margin":
        net_income = _column_values(df, detected, "net_income")
        if revenue is None or net_income is None:
            return None
        values = net_income / revenue.replace(0, float("nan"))
    else:
        return None

    if values is None:
        return None
    values = values.dropna()
    if len(values) < 2:
        return None
    first, last = float(values.iloc[0]), float(values.iloc[-1])
    if math.isclose(first, last, rel_tol=1e-9, abs_tol=1e-9):
        return 0
    return 1 if last > first else -1


# ---------------------------------------------------------------------------
# Formatting and reusable page helpers
# ---------------------------------------------------------------------------

PERCENT_METRICS = {
    "gross_margin", "operating_margin", "net_margin", "roa", "roe",
    "debt_ratio", "equity_ratio",
}
RATIO_METRICS = {
    "current_ratio", "quick_ratio", "cash_ratio", "debt_to_equity",
    "financial_leverage", "asset_turnover", "inventory_turnover",
    "receivables_turnover",
}
MONEY_METRICS = {
    "revenue", "gross_profit", "net_income", "cash", "total_assets",
    "total_liabilities", "equity", "current_assets", "current_liabilities",
}


def format_metric(key: str, value: float | None) -> str:
    if value is None or not math.isfinite(value):
        return t("not_available")
    if key in PERCENT_METRICS:
        return f"{value * 100:,.2f}%"
    if key in RATIO_METRICS:
        return f"{value:,.2f}×"
    return f"{value:,.2f}"


def show_empty_state() -> None:
    with st.container(border=True):
        st.subheader(t("empty_state_title"))
        st.write(t("empty_state_body"))
        st.button(
            t("go_import"),
            type="primary",
            on_click=_navigate,
            args=("import",),
            key="empty_import_button",
        )


def metric_card(label_key: str, metric_key: str, metrics: dict[str, Any]) -> None:
    with st.container(border=True):
        st.metric(t(label_key), format_metric(metric_key, metrics.get(metric_key)))


def get_financial_frame() -> pd.DataFrame | None:
    data = st.session_state.get("data")
    return data if isinstance(data, pd.DataFrame) else None


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def render_home() -> None:
    st.write("")
    st.title(t("home_title"))
    st.subheader(t("home_subtitle"))
    st.write("")
    st.button(
        t("start_analysis"),
        type="primary",
        on_click=_navigate,
        args=("import",),
        key="home_start_button",
    )

    st.write("")
    st.write("")
    st.header(t("features_title"))

    features = [
        ("feature_performance", "feature_performance_desc"),
        ("feature_risk", "feature_risk_desc"),
        ("feature_diagnostic", "feature_diagnostic_desc"),
        ("feature_reports", "feature_reports_desc"),
    ]
    for start in (0, 2):
        columns = st.columns(2)
        for column, (title_key, desc_key) in zip(columns, features[start:start + 2]):
            with column:
                with st.container(border=True):
                    st.subheader(t(title_key))
                    st.write(t(desc_key))

    st.info(t("home_import_hint"))


def render_import_page() -> None:
    st.title(t("import_title"))
    st.write(t("import_intro"))

    uploaded = st.file_uploader(
        t("upload_label"),
        type=["xlsx", "xls"],
        help=t("upload_help"),
        key="upload_widget",
    )

    if uploaded is not None:
        raw_bytes = uploaded.getvalue()
        signature = (uploaded.name, len(raw_bytes))
        if signature != st.session_state.file_signature:
            st.session_state.uploaded_file = raw_bytes
            st.session_state.uploaded_filename = uploaded.name
            st.session_state.file_signature = signature
            st.session_state.sheet_names = []
            st.session_state.selected_sheet = None
            st.session_state.data = None
            st.session_state.analysis_results = None
            st.session_state.diagnostic_results = None

    file_bytes = st.session_state.get("uploaded_file")
    filename = st.session_state.get("uploaded_filename")

    if not file_bytes or not filename:
        st.info(t("no_file"))
        if get_financial_frame() is not None:
            st.subheader(t("current_data"))
            st.caption(t("change_sheet_note"))
            render_loaded_data()
        return

    st.success(t("file_ready", filename=filename))

    try:
        extension = Path(filename).suffix.lower()
        engine = "xlrd" if extension == ".xls" else "openpyxl"
        workbook = pd.ExcelFile(io.BytesIO(file_bytes), engine=engine)
        sheet_names = workbook.sheet_names
        st.session_state.sheet_names = sheet_names
    except Exception as exc:
        st.error(t("import_error", error=str(exc)))
        return

    if not sheet_names:
        st.warning(t("no_sheets"))
        return

    current_sheet = st.session_state.get("selected_sheet")
    if current_sheet not in sheet_names:
        current_sheet = sheet_names[0]
        st.session_state.selected_sheet = current_sheet

    if st.session_state.get("sheet_widget") not in sheet_names:
        st.session_state.sheet_widget = current_sheet

    selected_sheet = st.selectbox(
        t("select_sheet"),
        sheet_names,
        key="sheet_widget",
    )
    st.session_state.selected_sheet = selected_sheet

    st.button(
        t("load_sheet"),
        type="primary",
        key="load_sheet_button",
    )

    # The button's state is read after the widget declaration on each rerun.
    if st.session_state.get("load_sheet_button"):
        try:
            df = pd.read_excel(
                io.BytesIO(file_bytes),
                sheet_name=selected_sheet,
                engine=engine,
            )
            st.session_state.data = df
            st.session_state.analysis_results = None
            st.session_state.diagnostic_results = None
            st.session_state.loaded_filename = filename
            st.session_state.loaded_sheet = selected_sheet
            st.success(t("sheet_loaded"))
        except Exception as exc:
            st.error(t("import_error", error=str(exc)))
            return

    if get_financial_frame() is not None:
        st.write("")
        st.subheader(t("current_data"))
        st.caption(t("change_sheet_note"))
        render_loaded_data()
        st.button(
            t("continue_dashboard"),
            type="primary",
            key="continue_dashboard_button",
            on_click=_navigate,
            args=("dashboard",),
        )
    else:
        st.info(t("load_first"))


def render_loaded_data() -> None:
    df = get_financial_frame()
    if df is None:
        return

    messages, counts = validate_data(df)
    numeric_count = counts["numeric_columns"]

    cols = st.columns(3)
    cols[0].metric(t("rows"), counts["rows"])
    cols[1].metric(t("columns"), counts["columns"])
    cols[2].metric(t("numeric_columns"), numeric_count)

    st.subheader(t("preview"))
    st.dataframe(df.head(100), use_container_width=True, hide_index=True)

    st.subheader(t("validation"))
    if not messages:
        st.success(t("validation_ok"))
    else:
        for key, params in messages:
            if key in {"empty_data", "missing_headers", "duplicate_headers", "invalid_numeric"}:
                st.warning(t(key, **params))
            else:
                st.info(t(key, **params))


def render_dashboard() -> None:
    st.title(t("dashboard_title"))
    st.write(t("dashboard_intro"))
    df = get_financial_frame()
    if df is None:
        show_empty_state()
        return

    metrics = calculate_financial_metrics(df)
    st.subheader(t("key_indicators"))

    kpis = [
        ("revenue", "revenue"),
        ("net_income", "net_income"),
        ("net_margin", "net_margin"),
        ("current_ratio", "current_ratio"),
        ("debt_ratio", "debt_ratio"),
        ("cash", "cash"),
        ("total_assets", "total_assets"),
        ("total_liabilities", "total_liabilities"),
    ]
    for start in range(0, len(kpis), 4):
        columns = st.columns(4)
        for column, (label_key, metric_key) in zip(columns, kpis[start:start + 4]):
            with column:
                metric_card(label_key, metric_key, metrics)

    st.write("")
    detected = detect_financial_columns(df)
    revenue_series = _column_values(df, detected, "revenue")
    net_income_series = _column_values(df, detected, "net_income")
    if (revenue_series is not None and revenue_series.notna().any()) or (
        net_income_series is not None and net_income_series.notna().any()
    ):
        chart_data = pd.DataFrame(index=range(len(df)))
        if revenue_series is not None:
            chart_data[t("revenue")] = revenue_series.reset_index(drop=True)
        if net_income_series is not None:
            chart_data[t("net_income")] = net_income_series.reset_index(drop=True)

        date_index = None
        for index, column in enumerate(df.columns):
            normalized = normalize_text(column)
            if normalized in {"date", "year", "period", "annee", "année", "période"}:
                date_index = index
                break
        if date_index is not None:
            chart_data.insert(
                0,
                t("row_number"),
                df.iloc[:, date_index].astype(str).reset_index(drop=True),
            )
            x_axis = t("row_number")
        else:
            chart_data.insert(0, t("row_number"), range(1, len(df) + 1))
            x_axis = t("row_number")

        with st.container(border=True):
            st.subheader(t("revenue_trend"))
            fig = px.line(chart_data, x=x_axis, y=list(chart_data.columns[1:]), markers=True)
            fig.update_layout(
                template="plotly_white",
                margin=dict(l=15, r=15, t=15, b=15),
                legend_title_text="",
                xaxis_title="",
                yaxis_title="",
            )
            st.plotly_chart(fig, use_container_width=True)

    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    with st.container(border=True):
        st.subheader(t("data_quality"))
        if missing.empty:
            st.success(t("validation_ok"))
        else:
            missing_frame = pd.DataFrame({
                t("column"): missing.index.astype(str),
                t("missing"): missing.values,
            })
            fig = px.bar(
                missing_frame,
                x=t("column"),
                y=t("missing"),
                color_discrete_sequence=["#4183C4"],
            )
            fig.update_layout(
                template="plotly_white",
                margin=dict(l=15, r=15, t=15, b=15),
                xaxis_title="",
                yaxis_title="",
            )
            st.plotly_chart(fig, use_container_width=True)


ANALYSIS_GROUPS = {
    "profitability": [
        ("gross_margin", "formula_gross_margin"),
        ("operating_margin", "formula_operating_margin"),
        ("net_margin", "formula_net_margin"),
        ("roa", "formula_roa"),
        ("roe", "formula_roe"),
    ],
    "liquidity": [
        ("current_ratio", "formula_current_ratio"),
        ("quick_ratio", "formula_quick_ratio"),
        ("cash_ratio", "formula_cash_ratio"),
    ],
    "solvency": [
        ("debt_ratio", "formula_debt_ratio"),
        ("debt_to_equity", "formula_debt_to_equity"),
        ("equity_ratio", "formula_equity_ratio"),
        ("financial_leverage", "formula_financial_leverage"),
    ],
    "efficiency": [
        ("asset_turnover", "formula_asset_turnover"),
        ("inventory_turnover", "formula_inventory_turnover"),
        ("receivables_turnover", "formula_receivables_turnover"),
    ],
}


def render_analysis() -> None:
    st.title(t("financial_analysis_title"))
    st.write(t("analysis_intro"))
    df = get_financial_frame()
    if df is None:
        show_empty_state()
        return

    metrics = calculate_financial_metrics(df)
    if not detect_financial_columns(df):
        st.warning(t("no_financial_columns"))

    for group_key, indicators in ANALYSIS_GROUPS.items():
        st.subheader(t(group_key))
        rows = []
        for metric_key, formula_key in indicators:
            value = metrics.get(metric_key)
            rows.append({
                t("indicator"): t(metric_key),
                t("value"): format_metric(metric_key, value),
                t("interpretation"): (
                    t(formula_key) if value is not None else t("formula_not_available")
                ),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def build_diagnostic(df: pd.DataFrame, metrics: dict[str, Any]) -> dict[str, list[str]]:
    strengths: list[str] = []
    attention: list[str] = []
    observations: list[str] = []

    current_ratio = metrics.get("current_ratio")
    debt_ratio = metrics.get("debt_ratio")
    net_margin = metrics.get("net_margin")
    equity_ratio = metrics.get("equity_ratio")

    if current_ratio is not None:
        if current_ratio < 1:
            attention.append("liquidity_pressure")
        elif current_ratio >= 1.5:
            strengths.append("healthy_liquidity")

    if debt_ratio is not None:
        if debt_ratio > 0.70:
            attention.append("high_debt")
        elif debt_ratio <= 0.50:
            strengths.append("moderate_debt")

    if net_margin is not None:
        if net_margin < 0:
            attention.append("negative_margin")
        elif net_margin > 0.10:
            strengths.append("positive_margin")

    if equity_ratio is not None and equity_ratio > 0.50:
        strengths.append("strong_equity")

    margin_trend = get_trend(df, "net_margin")
    revenue_trend = get_trend(df, "revenue")
    if margin_trend == 1:
        strengths.append("improving_margin")
    elif margin_trend == -1:
        attention.append("declining_margin")
    if revenue_trend == 1:
        observations.append("improving_revenue")
    elif revenue_trend == -1:
        attention.append("declining_revenue")

    # Report only the source fields that are absent and affect common indicators.
    detected = detect_financial_columns(df)
    missing_concepts: set[str] = set()
    requirements = {
        "current_ratio": {"current_assets", "current_liabilities"},
        "net_margin": {"net_income", "revenue"},
        "debt_ratio": {"total_assets", "total_liabilities"},
        "equity_ratio": {"equity", "total_assets"},
    }
    for metric_name, concepts in requirements.items():
        if metrics.get(metric_name) is None:
            for concept in concepts:
                if concept not in detected:
                    missing_concepts.add(concept)

    missing_labels = [t(concept) for concept in sorted(missing_concepts)]
    if missing_labels:
        observations.append("insufficient_data")
        observations.append("missing_info:" + ", ".join(missing_labels))

    if not strengths and not attention and not observations:
        observations.append("no_rule_triggered")

    result = {
        "strengths": strengths,
        "attention": attention,
        "observations": observations,
    }
    st.session_state.diagnostic_results = result
    return result

def render_simulation() -> None:
    st.title("Simulation financière")
    st.info("Module de simulation financière en préparation.")
def render_diagnostic() -> None:
    st.title(t("diagnostic_title"))
    st.write(t("diagnostic_intro"))
    df = get_financial_frame()
    if df is None:
        show_empty_state()
        return

    metrics = calculate_financial_metrics(df)
    result = build_diagnostic(df, metrics)

    st.subheader(t("strengths"))
    if result["strengths"]:
        for key in result["strengths"]:
            st.success(t(key))
    else:
        st.info(t("no_strengths"))

    st.subheader(t("attention"))
    if result["attention"]:
        for key in result["attention"]:
            st.warning(t(key))
    else:
        st.success(t("no_attention"))

    st.subheader(t("observations"))
    if result["observations"]:
        for item in result["observations"]:
            if item.startswith("missing_info:"):
                st.info(t("missing_info", items=item.split(":", 1)[1]))
            elif item == "insufficient_data":
                st.info(t(item))
            else:
                st.info(t(item))
    else:
        st.info(t("no_rule_triggered"))


def build_html_report(
    df: pd.DataFrame,
    metrics: dict[str, Any],
    diagnostic: dict[str, list[str]],
) -> str:
    """Create a standalone, downloadable report without rendering HTML in the app."""
    language = st.session_state.language
    direction = "rtl" if language == "ar" else "ltr"
    alignment = "right" if language == "ar" else "left"

    source_file = html.escape(str(st.session_state.get("loaded_filename", "")))
    source_sheet = html.escape(str(st.session_state.get("loaded_sheet", "")))

    metric_keys = [
        "revenue", "net_income", "net_margin", "current_ratio",
        "debt_ratio", "cash", "total_assets", "total_liabilities",
    ]
    metric_rows = "".join(
        "<tr><th>{}</th><td>{}</td></tr>".format(
            html.escape(t(key)),
            html.escape(format_metric(key, metrics.get(key))),
        )
        for key in metric_keys
    )

    strengths = "".join(
        f"<li>{html.escape(t(key))}</li>" for key in diagnostic["strengths"]
    ) or f"<li>{html.escape(t('no_strengths'))}</li>"
    attention = "".join(
        f"<li>{html.escape(t(key))}</li>" for key in diagnostic["attention"]
    ) or f"<li>{html.escape(t('no_attention'))}</li>"

    return f"""<!doctype html>
<html lang="{language}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t("report_title"))} — FinDiag</title>
<style>
body {{ margin: 0; padding: 36px; background: #F7FAFF; color: #172033;
       font: 15px/1.6 Arial, sans-serif; direction: {direction}; text-align: {alignment}; }}
main {{ max-width: 900px; margin: auto; padding: 32px; background: #fff;
        border: 1px solid #E4E9F1; border-radius: 16px; }}
h1, h2 {{ color: #172033; }}
h1 {{ border-bottom: 3px solid #4183C4; padding-bottom: 12px; }}
table {{ width: 100%; border-collapse: collapse; margin: 18px 0 28px; }}
th, td {{ padding: 11px 12px; border-bottom: 1px solid #E4E9F1; text-align: {alignment}; }}
th {{ color: #687386; width: 48%; }}
.brand {{ color: #4183C4; font-weight: 700; letter-spacing: .14em; }}
small {{ color: #687386; }}
</style>
</head>
<body>
<main>
<p class="brand">FINDIAG</p>
<h1>{html.escape(t("report_title"))}</h1>
<p>{html.escape(t("report_intro"))}</p>
<h2>{html.escape(t("company_overview"))}</h2>
<p><strong>{html.escape(t("source_file"))}:</strong> {source_file}<br>
<strong>{html.escape(t("source_sheet"))}:</strong> {source_sheet}<br>
<strong>{html.escape(t("rows"))}:</strong> {len(df)} &nbsp; | &nbsp;
<strong>{html.escape(t("columns"))}:</strong> {len(df.columns)}</p>
<h2>{html.escape(t("report_summary"))}</h2>
<table>{metric_rows}</table>
<h2>{html.escape(t("strengths"))}</h2><ul>{strengths}</ul>
<h2>{html.escape(t("attention"))}</h2><ul>{attention}</ul>
<p><small>FinDiag</small></p>
</main>
</body>
</html>"""


def render_report() -> None:
    st.title(t("report_title"))
    st.write(t("report_intro"))
    df = get_financial_frame()
    if df is None:
        st.info(t("no_report_data"))
        return

    metrics = calculate_financial_metrics(df)
    diagnostic = build_diagnostic(df, metrics)

    st.subheader(t("company_overview"))
    source_file = st.session_state.get("loaded_filename", st.session_state.uploaded_filename)
    source_sheet = st.session_state.get("loaded_sheet", st.session_state.selected_sheet)
    st.write(
        f"**{t('source_file')}:** {source_file or t('not_available')}  \n"
        f"**{t('source_sheet')}:** {source_sheet or t('not_available')}  \n"
        f"**{t('rows')}:** {len(df)} · **{t('columns')}:** {len(df.columns)}"
    )

    st.subheader(t("report_summary"))
    report_metrics = [
        ("revenue", "revenue"),
        ("net_income", "net_income"),
        ("net_margin", "net_margin"),
        ("current_ratio", "current_ratio"),
        ("debt_ratio", "debt_ratio"),
        ("total_assets", "total_assets"),
    ]
    for start in range(0, len(report_metrics), 3):
        columns = st.columns(3)
        for column, (label_key, metric_key) in zip(columns, report_metrics[start:start + 3]):
            with column:
                metric_card(label_key, metric_key, metrics)

    st.subheader(t("strengths"))
    if diagnostic["strengths"]:
        for key in diagnostic["strengths"]:
            st.success(t(key))
    else:
        st.info(t("no_strengths"))

    st.subheader(t("attention"))
    if diagnostic["attention"]:
        for key in diagnostic["attention"]:
            st.warning(t(key))
    else:
        st.info(t("no_attention"))

    report = build_html_report(df, metrics, diagnostic)
    st.download_button(
        t("download_report"),
        data=report.encode("utf-8"),
        file_name=t("report_download_name"),
        mime="text/html",
        type="primary",
    )
    st.caption(t("report_generated"))


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

def main() -> None:
    inject_styles()
    render_header()
    render_navigation()

    page = st.session_state.get("page", "home")
    renderers = {
        "home": render_home,
        "dashboard": render_dashboard,
        "analysis": render_analysis,
        "diagnostic": render_diagnostic,
        "report": render_report,
        "import": render_import_page,
    }
    renderers.get(page, render_home)()


if __name__ == "__main__":
    main()
    