import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_card import card
import df_call

# ---------------------------
# Paramètre de la page

# Modifying the page title and icon
st.set_page_config(page_title = "Le Senechal - People", page_icon = "👯‍♂️", layout = "wide")

# Add the logo
image = "App/img/senechal_logo-removebg-preview.png"
v1, imga = st.columns([0.37, 0.63])
with imga :
    st.image(image , use_column_width=False)

# ------------------------------
# Titre de la section + appel des df
st.markdown("<h1 style='text-align: center; color: orange;'>Rechercher par scénariste ou acteur</h1>", unsafe_allow_html=True)
movie = df_call.df_final()
name = df_call.name_df()

st.header("Vous pouvez effectuer votre recherche ci-dessous", divider = "orange")

# Barre de recherche + stockage du résultat dans une liste pour gérer les homonymes
name_search = st.text_input("Nom de l'acteur ou du scénariste:", value="")
name_list = name["nconst"][name["primaryName"].str.contains(name_search, na = False, case = False)]

# Filter the dataframe using masks
try:
    m1 = movie["actor1"].isin(name_list)
    m2 = movie["actor2"].isin(name_list)
    m3 = movie["actor3"].isin(name_list)
    m4 = movie["director1"].isin(name_list)
    m5 = movie["writer1"].isin(name_list)
    search = movie[m1 | m2 | m3 | m4 | m5].sort_values("popularity", ascending = False)
except:
    st.error("Nous n'avons malheureusement trouvé aucun film correspondant à votre recherche")

# Show the results, if you have a text_search
if name_search:
    if search.empty:
        st.error("Nous n'avons malheureusement trouvé aucun film correspondant à votre recherche")

# Boucles imbriquées pour remplir 5 lignes dans les 3 colonnes
    col1, col2, col3 = st.columns(3)
    col = [col1, col2, col3]

    for adding in [0, 3, 6, 9, 12, 15]:    
        for ind, numCol in enumerate(col):
            try:
                with numCol:
                    card_one = card(title = search["title_x"][search["title_x"] == search["title_x"].iloc[ind + adding]].iloc[0],
                                    text = search["genres_x"][search["title_x"] == search["title_x"].iloc[ind + adding]].iloc[0],
                                    image = "https://image.tmdb.org/t/p/w500" + search["poster_path"][search["title_x"] == search["title_x"].iloc[ind + adding]].iloc[0],
                                    styles = {"card" :{"width": "280px",
                                                        "height": "400px",
                                                        "border_radius": "10px"},
                                            "text": {"font_family": "Source Sans Pro, sans serif"},
                                            "title": {"font_family": "Source Sans Pro"}})
            except:
                with numCol:
                    st.write("")
