import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Charger les fichiers CSV
# Charger les fichiers CSV
url1 = "https://raw.githubusercontent.com/JhpAb/data354_Hiring_Challenge/main/DATABASE/cyber_security_ai_tools.csv"
url2 = "https://raw.githubusercontent.com/JhpAb/data354_Hiring_Challenge/main/DATABASE/top_10_authors_df_sorted.csv"

# Add error handling for reading CSV files
try:
    df = pd.read_csv(url1)  # Tableau des publications
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier CSV principal: {e}")
    df = pd.DataFrame()  # Create empty dataframe to prevent errors

try:
    top_10_authors_df_sorted = pd.read_csv(url2)  # Tableau des auteurs
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier des auteurs: {e}")
    top_10_authors_df_sorted = pd.DataFrame(columns=['Author', 'Likes', 'Shares', 'Keywords', 'Content'])

# Titre du dashboard
st.title("📊 LinkedIn Post Analysis Dashboard")

# Sidebar de navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à", ["📈 Statistiques générales", "🏆 Analyse des auteurs", "🔍 Analyse des mots-clés"])

if page == "📈 Statistiques générales":
    st.header("📊 Statistiques générales")

    # Affichage du tableau cyber_security_ai_tools.csv
    st.subheader("Tableau des données : cyber_security_ai_tools.csv")
    st.dataframe(df)

    # Nombre total de publications
    st.metric(label="Total des publications", value=len(df))

    # Nombre d'auteurs uniques
    st.metric(label="Nombre d'auteurs uniques", value=df['Author'].nunique())

    # Graphique des auteurs uniques
    st.subheader("Nombre de publications par auteur")
    author_counts = df['Author'].value_counts().head(30)  # Limiter à 30 pour lisibilité
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=author_counts.index, y=author_counts.values, palette="coolwarm", ax=ax)
    plt.xticks(rotation=90)
    plt.xlabel("Auteurs")
    plt.ylabel("Nombre de publications")
    plt.title("Top 30 des auteurs par nombre de publications")
    st.pyplot(fig)

elif page == "🏆 Analyse des auteurs":
    st.header("🏆 Top 10 Auteurs")

    # Affichage du tableau top_10_authors_df_sorted.csv
    st.subheader("Tableau des données : top_10_authors_df_sorted.csv")
    st.dataframe(top_10_authors_df_sorted)

    # Top 10 auteurs
    st.subheader("Auteurs avec le plus de publications")
    author_counts = top_10_authors_df_sorted['Author'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=author_counts.index, y=author_counts.values, palette="Blues_r", ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Auteurs")
    plt.ylabel("Nombre de publications")
    st.pyplot(fig)

    # Analyse des Likes et Shares
    st.subheader("Likes et Shares des Top 10 Auteurs")
    col1, col2 = st.columns(2)
    with col1:
     fig, ax = plt.subplots(figsize=(8, 5))
     sns.barplot(x='Author', y='Likes', data=top_10_authors_df_sorted, palette='viridis', ax=ax)
     plt.xticks(rotation=45)
     plt.xlabel("Auteur")
     plt.ylabel("Likes")
     st.pyplot(fig)
    with col2:
     fig, ax = plt.subplots(figsize=(8, 5))
     sns.barplot(x='Author', y='Shares', data=top_10_authors_df_sorted, palette='magma', ax=ax)
     plt.xticks(rotation=45)
     plt.xlabel("Auteur")
     plt.ylabel("Shares")
     st.pyplot(fig)

    # Corrélation entre Likes et Shares
    st.subheader("📊 Corrélation entre Likes et Shares")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(x='Likes', y='Shares', data=top_10_authors_df_sorted, color='purple', ax=ax)
    plt.xlabel("Likes")
    plt.ylabel("Shares")
    st.pyplot(fig)
    correlation = top_10_authors_df_sorted['Likes'].corr(top_10_authors_df_sorted['Shares'])
    st.write(f"Coefficient de corrélation : **{correlation:.2f}**")

elif page == "🔍 Analyse des mots-clés":
    st.header("🔍 Analyse des mots-clés")

    # Affichage du tableau top_10_authors_df_sorted.csv (car il contient les mots-clés)
    st.subheader("Tableau des données : top_10_authors_df_sorted.csv")
    st.dataframe(top_10_authors_df_sorted)

    # Nuage de mots des mots-clés
    st.subheader("WordCloud des mots-clés")
    if not top_10_authors_df_sorted.empty and 'Keywords' in top_10_authors_df_sorted.columns:
        text = " ".join(top_10_authors_df_sorted['Keywords'].dropna().astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("La colonne 'Keywords' n'est pas présente dans le dataframe.")

    # Nuage de mots du contenu des posts
    st.subheader("WordCloud du contenu des publications")
    if not top_10_authors_df_sorted.empty and 'Content' in top_10_authors_df_sorted.columns:
        text_content = " ".join(top_10_authors_df_sorted['Content'].dropna().astype(str))
        wordcloud_content = WordCloud(width=800, height=400, background_color='white').generate(text_content)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud_content, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("La colonne 'Content' n'est pas présente dans le dataframe.")

st.sidebar.info("👈 Sélectionnez une section pour explorer les données !")