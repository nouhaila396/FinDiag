import streamlit as st

st.set_page_config(
    page_title="FinDiag",
    page_icon="📊",
    layout="wide",
)

# ─────────────────────────────────────────────
# En-tête
# ─────────────────────────────────────────────

st.title("📊 FinDiag")
st.subheader("Financial Analysis & Diagnostic")

st.markdown(
    """
    Bienvenue dans **FinDiag**, votre application d'analyse et de
    diagnostic financier.
    """
)

st.divider()

# ─────────────────────────────────────────────
# Navigation
# ─────────────────────────────────────────────

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Choisir une rubrique :",
    [
        "🏠 Accueil",
        "📥 Importation des données",
        "📊 Tableau de bord",
        "💰 Analyse financière",
        "🔎 Diagnostic",
        "📄 Rapport",
    ],
)

# ─────────────────────────────────────────────
# Contenu des pages
# ─────────────────────────────────────────────

if page == "🏠 Accueil":
    st.header("🏠 Accueil")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📁 Données", "Non importées")

    with col2:
        st.metric("📊 Analyse", "En attente")

    with col3:
        st.metric("🔎 Diagnostic", "En attente")

    st.info(
        "Commencez par importer vos données financières "
        "pour lancer l'analyse."
    )


elif page == "📥 Importation des données":
    st.header("📥 Importation des données")

    st.write(
        "Cette section permettra d'importer le fichier Excel "
        "contenant les données financières de l'entreprise."
    )

    uploaded_file = st.file_uploader(
        "Sélectionnez votre fichier Excel",
        type=["xlsx", "xls"],
    )

    if uploaded_file is not None:
        st.success(f"Fichier sélectionné : {uploaded_file.name}")


elif page == "📊 Tableau de bord":
    st.header("📊 Tableau de bord")

    st.info(
        "Le tableau de bord sera disponible après l'importation "
        "des données."
    )


elif page == "💰 Analyse financière":
    st.header("💰 Analyse financière")

    st.info(
        "Les indicateurs financiers seront affichés ici."
    )


elif page == "🔎 Diagnostic":
    st.header("🔎 Diagnostic financier")

    st.info(
        "Le diagnostic financier sera généré ici."
    )


elif page == "📄 Rapport":
    st.header("📄 Rapport")

    st.info(
        "La génération du rapport sera disponible ici."
    )
