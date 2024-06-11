import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_card import card
import df_call

# ---------------------------
# Paramètre de la page

# Modifying the page title and icon
st.set_page_config(page_title = "Le Senechal - MR", page_icon = "🔮", layout = "wide")

# Add the logo of the Senechal
image = "App/img/senechal_logo-removebg-preview.png"
v1, imga = st.columns([0.37, 0.63])
with imga :
    st.image(image , use_column_width=False)

st.markdown("<h1 style='text-align: center; color: orange;'>Rechercher par titre</h1>", unsafe_allow_html=True)

# call the dfs
movie = df_call.df_final()
name = df_call.name_df()

st.header("Vous pouvez effectuer votre recherche ci-dessous", divider = "orange")

# --------------------
# Recherche
selection = st.selectbox("Choisissez votre film", movie["title_date"], index = None)

# Condition s'il y a une recherche et mettre une valeur pour chaque acteur
if selection != None:
    director = movie["director1"][movie["title_date"] == selection].iloc[0]
    actor1 = movie["actor1"][movie["title_date"] == selection].iloc[0]
    actor2 = movie["actor2"][movie["title_date"] == selection].iloc[0]
    actor3 = movie["actor3"][movie["title_date"] == selection].iloc[0]

# On affiche le détail de la recherche
    col1, col2 = st.columns([0.3, 0.7])
    # Première colonne avec l'image
    try:
        with col1:
            card_one = card(title = movie["title_x"][movie["title_date"] == selection].iloc[0],
                            text = movie["genres_x"][movie["title_date"] == selection].iloc[0],
                            image = "https://image.tmdb.org/t/p/w500" + movie["poster_path"][movie["title_date"] == selection].iloc[0],
                            styles = {"card" :{"width": "290px",
                                                "height": "460px",
                                                "border_radius": "10px"},
                                    "text": {"font_family": "Source Sans Pro, sans serif"},
                                    "title": {"font_family": "Source Sans Pro"}})   
    except:
        if selection != None:
            with col1:
                st.markdown("<h1 style='text-align: center; color: orange;'> <br> </h1>", unsafe_allow_html=True)
                st.subheader(movie["title_x"][movie["title_date"] == selection].iloc[0])
                
    # 2e colonne avec les infos
    try:        
        with col2:
            st.markdown("<h1 style='text-align: center; color: orange;'> <br> </h1>", unsafe_allow_html=True)
            st.subheader("Infos:")
            st.write("**Durée:** " + str(movie["runtimeMinutes"][movie["title_date"] == selection].iloc[0]) + " min")
            st.write("**Note:** " + str(movie["averageRating"][movie["title_date"] == selection].iloc[0]) + "/10")
            st.write("**Date de sortie** : " + str(movie["release_date"][movie["title_date"] == selection].iloc[0]))
            st.write("**Directeur:** " + name["primaryName"][name["nconst"] == director].iloc[0])
            st.write("**Acteurs:** " + name["primaryName"][name["nconst"] == actor1].iloc[0] + ", " + name["primaryName"][name["nconst"] == actor2].iloc[0] + ", " + name["primaryName"][name["nconst"] == actor3].iloc[0])
            st.subheader("Synopsis:")
            st.markdown(f"<div style='word-wrap: break-word;'>{movie['overview'][movie['title_date'] == selection].iloc[0]}</div>", unsafe_allow_html=True)
            
    except:
        st.write("")

# ------------------------------------------------------------------------------------------------

# Système de reco
if selection != None:
    st.header("Vous aimerez également:", divider = "orange")
        
    # On appelle la fonction du machine learning pour la recherche
    reco = df_call.ML_Reco(movie["tconst"][movie["title_date"] == selection].iloc[0])

    # On affiche les 6 films les plus proches
    col1, col2, col3 = st.columns(3)
    col = [col1, col2, col3, col1, col2, col3]

    for ind, movie_name in enumerate(reco):
        try:
            with col[ind]:
                cardNum = card(title = movie['title_x'][movie['title_x'] == movie_name].iloc[0],
                                text = movie['genres_x'][movie['title_x'] == movie_name].iloc[0],
                                image = 'https://image.tmdb.org/t/p/w500' + movie['poster_path'][movie['title_x'] == movie_name].iloc[0],
                                styles = {'card' :{'width': '280px',
                                                    'height': '400px',
                                                    'border_radius': '10px',
                                                    'padding': '10px'},
                                        'text': {'font_family': 'Source Sans Pro'},
                                        'title': {'font_family': 'Source Sans Pro'}})

        except:
            with col[ind]:
                st.write(movie['title_x'][movie['title_x'] == movie_name].iloc[0])
                st.write(movie['genres_x'][movie['title_x'] == movie_name].iloc[0])

