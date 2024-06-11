import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_card import card
import df_call

# ---------------------------
# Paramètre de la page

# Modifying the page title and icon
st.set_page_config(
    page_title="Le Senechal - Movies",
    page_icon="🎥",
    layout = "wide"
)

# Afficher le logo du Sénéchal
image = "App/img/senechal_logo-removebg-preview.png"
v1, imga = st.columns([0.37, 0.63])
with imga :
    st.image(image , use_column_width=False)

# -----------------------------------------------------------------------------------
# NE PAS UTILISER TENTATIVE DE CSS POUR FORMATER LES COLONNES

# CSS code to make the width of columns match with lenght of text
# st.markdown("""
#             <style>
#                 div[data-testid="column"] {
#                     width: fit-content !important;
#                     flex: unset;
#                 }
#                 div[data-testid="column"] * {
#                     width: fit-content !important;
#                 }
#                 div[data-testid="column"] {
#                     margin-right: 1px;
#                     margin-left: 1px;
#                     padding: 10px;
#                 }
#                 div[class="css-5spcrp"] {
#                     padding: 10px !important;
#                 }
#                 [data-testid="stSidebarNav"]::before {
#                 content: " ";
#                 margin-left: 20px;
#                 margin-top: 20px;
#                 font-size: 30px;
#                 position: relative;
#                 color: orange;
#                 font-family: Source Sans Pro, sans_serif;
#                 top: 100px;
#                 }
#             </style>
#             """, unsafe_allow_html=True)

# add_logo("C:/Users/User/OneDrive/Documents/Wild Code School/Project 2/Ressources/senechal_logo-removebg-preview.png")
# --------------------------------------------------------------------------------------------------

# On appelle le df
movie = df_call.df_final()

# -------------------------------
# Titre de la section
st.markdown("<h1 style='text-align: center; color: orange;'>Rechercher par titre</h1>", unsafe_allow_html=True)

st.header("Vous pouvez effectuer votre recherche ci-dessous", divider = "orange")

# Recherche de l'utilisateur
movie_search = st.text_input("Nom du film:", value="")

# Filter the dataframe using masks (search on french title or original title)
try:
    m1 = movie["title_x"].str.contains(movie_search, case = False)
    m2 = movie["originalTitle"].str.contains(movie_search, case = False)
    search = movie[m1 | m2].sort_values("popularity", ascending = False)
except:
    st.error("Nous n'avons malheureusement trouvé aucun film correspondant à votre recherche")

# Show the results, if you have a text_search
if movie_search:
    if search.empty:
        st.error("Nous n'avons malheureusement trouvé aucun film correspondant à votre recherche")

# Boucles imbriquées pour remplir 5 lignes dans les 3 colonnes
    col1, col2, col3 = st.columns(3)
    col = [col1, col2, col3]
    
    for adding in [0, 3, 6, 9, 12]:
        for ind, numCol in enumerate(col):
            try:
                with numCol:
                    cardNum = "card"+str(ind + adding)
                    cardNum = card(title = search['title_x'][search['title_x'] == search['title_x'].iloc[ind + adding]].iloc[0],
                                    text = search['genres_x'][search['title_x'] == search['title_x'].iloc[ind + adding]].iloc[0],
                                    image = 'https://image.tmdb.org/t/p/w500' + search['poster_path'][search['title_x'] == search['title_x'].iloc[ind + adding]].iloc[0],
                                    styles = {'card' :{'width': '280px',
                                                        'height': '400px',
                                                        'border_radius': '10px',
                                                        'padding': '10px'},
                                            'text': {'font_family': 'Source Sans Pro'},
                                            'title': {'font_family': 'Source Sans Pro'}}
                                    # on_click = lambda: st.switch_page('Pages/5_Vos_Recherches.py'), # tentative d'associer une action au clique -> ne fonctionne pas dans une boucle
                                    )

            except:
                with numCol:
                    st.write("")

