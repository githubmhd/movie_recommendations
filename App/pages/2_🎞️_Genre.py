import streamlit as st
from streamlit_tags import st_tags
import pandas as pd
import plotly.express as px
from streamlit_card import card
import df_call
import random

# ---------------------------
# Paramètre de la page

# Modifying the page title and icon
st.set_page_config(page_title = "Le Senechal - Genre", page_icon = ":tv:", layout = "wide")

# Afficher le logo du Sénéchal
image = "App/img/senechal_logo-removebg-preview.png"
v1, imga = st.columns([0.37, 0.63])
with imga :
    st.image(image , use_column_width=False)

# On appelle le df
movie = df_call.df_final()

# ---------------------------
# Titre
st.markdown("<h1 style='text-align: center; color: orange;'>Rechercher par genre</h1>", unsafe_allow_html=True)
st.header("Vous pouvez effectuer votre recherche ci-dessous", divider = "orange")

# Barre de recherche du genre avec des tags (auto completion)
genre_search = st_tags(label ='Entrez votre genre:',
                       text ='Appuyer sur "Entrée" pour ajouter le genre',
                       value = None,
                       suggestions = ['Drama', 'Adventure', 'Fantasy', 'Biography', 'Romance', 
                                     'History', 'Comedy', 'Crime', 'Mystery', 'Horror', 
                                     'Western', 'Action','Family', 'War', 'Sci-Fi', 
                                     'Thriller', 'Sport', 'Documentary', 'Music', 'Animation', 
                                     'Musical', 'Film-Noir', 'News', 'ScienceFiction'],
                        maxtags = 4)

# On check s'il y a eu une recherche
if genre_search:
    genre_list = []
    for ind in range(len(genre_search)):
        genre_list.append(genre_search[ind])
        
# Filter the dataframe using masks
# Multiples conditions en fonction de l'existance d'un acteur 1, 2 ou 3 sans bloquer le reste

    try:
        if len(genre_list) == 1:
            m1 = movie["genres_x"].str.contains(genre_search[0], case = False)
            search = movie[m1].sort_values("popularity", ascending = False)
        elif len(genre_list) == 2:
            m1 = movie["genres_x"].str.contains(genre_search[0], case = False)
            m2 = movie["genres_x"].str.contains(genre_search[1], case = False)
            search = movie[m1 & m2].sort_values("popularity", ascending = False)
        elif len(genre_list) == 2:
            m1 = movie["genres_x"].str.contains(genre_search[0], case = False)
            m2 = movie["genres_x"].str.contains(genre_search[1], case = False)
            m3 = movie["genres_x"].str.contains(genre_search[2], case = False)
            search = movie[m1 & m2 & m3].sort_values("popularity", ascending = False)
        else:
            m1 = movie["genres_x"].str.contains(genre_search[0], case = False)
            m2 = movie["genres_x"].str.contains(genre_search[1], case = False)
            m3 = movie["genres_x"].str.contains(genre_search[2], case = False)
            m4 = movie["genres_x"].str.contains(genre_search[3], case = False)
            search = movie[m1 & m2 & m3 & m4].sort_values("popularity", ascending = False)

    except:
        st.error("Nous n'avons malheureusement trouvé aucun film correspondant à votre recherche")

    indexNum = search.index

# Boucles imbriquées pour mettre 5 lignes dans les 3 colonnes
    col1, col2, col3 = st.columns(3)
    col = [col1, col2, col3]

    for line in range(5):
        for numCol in col:
            try:
                with numCol:
                    # On vient prendre aléatoirement un indice pour l'afficher
                    aleas = int(random.choice(indexNum))
                    card_one = card(title = search["title_x"].loc[aleas],
                                    text = search["genres_x"].loc[aleas],
                                    image = "https://image.tmdb.org/t/p/w500" + search["poster_path"].loc[aleas],
                                    styles = {"card" :{"width": "280px",
                                                        "height": "400px",
                                                        "border_radius": "10px",
                                                        'padding': '10px'},
                                            "text": {"font_family": "Source Sans Pro"},
                                            "title": {"font_family": "Source Sans Pro"}})
            except:
                with numCol:
                    st.write("")
