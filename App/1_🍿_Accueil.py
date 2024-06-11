import streamlit as st
from streamlit_card import card
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
import requests
import re
import df_call


# ---------------------------
# Paramètre de la page

# Modifying the page title and icon
st.set_page_config(page_title = "Le Senechal", page_icon = ":clapper:", layout = "wide")

# Afficher le logo du Sénéchal
image = "App/img/senechal_logo-removebg-preview.png"
v1, imga = st.columns([0.37, 0.63])
with imga :
    st.image(image , use_column_width=False)

# On appelle notre DataFrame
movie = df_call.df_final()

st.markdown("<h1 style='text-align: center; color: orange;'>Recherche & recommandation de films</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center'>Bienvenue</h2>", unsafe_allow_html=True)

# ---------------------------
# Thème de la semaine

st.header("Cette semaine", divider = "orange")
st.subheader("Nous mettons à l'honneur les parents du monde entier")

col1, col2 = st.columns([0.4, 0.6])
with col1:
    st.image("https://www.un.org/sites/un2.un.org/files/uni289186.jpg", use_column_width = True)

with col2:
    st.subheader("Le 1er juin est la journée mondiale de la Parentalité")
    st. write("Cette Journée mondiale rend hommage au dévouement des parents, à leur engagement et leur sacrifice pour assurer l'avenir de leurs enfants.")
    st. write("Vous trouverez plus d'information sur le portail de [l'UNICEF](https://www.unicef.org/parenting/fr?utm_source=referral&utm_medium=un-fr&utm_campaign=parenting-month-2024-fr)")

# ---------------------------
# Vote pour la diffusion d'un film

st.header("Votez pour la diffusion de l'un des films suivants", divider = "orange")
st.subheader("Les films proposés cette semaine sont:")

list_film = ["Boyhood (2014)", "Le premier cri (2007)", "Juno (2007)"]
colum1, colum2, colum3 = st.columns(3) 
col_list = [colum1, colum2, colum3]

for ind, colnum in enumerate(col_list):
    with colnum:
        card_M = card(title = movie["title_x"][movie["title_date"] == list_film[ind]].iloc[0],
                        text = movie["genres_x"][movie["title_date"] == list_film[ind]].iloc[0],
                        image = "https://image.tmdb.org/t/p/w500" + movie["poster_path"][movie["title_date"] == list_film[ind]].iloc[0],
                        styles = {"card" :{"width": "280px",
                                            "height": "400px",
                                            "border_radius": "10px"},
                                "text": {"font_family": "Source Sans Pro, sans serif"},
                                "title": {"font_family": "Source Sans Pro"}})
            
            
st.write("Cochez un ou plusieurs films")

with st.form("Vote"):
    film1 = st.checkbox(list_film[0])
    film2 = st.checkbox(list_film[1])
    film3 = st.checkbox(list_film[2])
    
    selection = {list_film[0]: film1,
                 list_film[1]: film2,
                 list_film[2]: film3}
    
    vote = st.form_submit_button("Film à diffuser")
    
    if vote:
        st.balloons()
        for key, val in selection.items():
            if val == 1:
                st.write(f"Vous avez voté pour {key}")

# ---------------------------
# Partie Infos Pratiques

st.header("Infos Pratiques", divider = "orange")

# Web Scrapping du site 
SéanceURL = "https://www.cinema-senechal.com/horaires/"
EventURL = "https://www.cinema-senechal.com/tous-nos-evenements/"

pageSéance = requests.get(SéanceURL)
pageEvent = requests.get(EventURL)
soupSéance = BeautifulSoup(pageSéance.text, "html.parser")
soupEvent = BeautifulSoup(pageEvent.text, "html.parser")

# Donner des informations sur le prochain évènement
st.subheader("Prochain évènement:")
col1, col2 = st.columns([0.4, 0.6])
event_image = soupEvent.find("img", {"class": "css-b5to1a"})
col1.image(event_image["src"])
event = soupEvent.find("div", {"class": "css-194pin2"})
col2.write(event.find("h2", {"class": "css-zkq0cp"}).text)
date = re.findall("(\w+) (\d+) (\w+) (\d+)", event.text)[0]
col2.write("Ce " + date[0] + " " + date[1] + " " + date[2] + " " + date[3])

# Les tarifs du cinéma
st.subheader("Les tarifs")
st.dataframe(pd.DataFrame({"Catégorie": ["- de 14 ans", 
                                         "Jeune (- de 18 ans)",
                                         "Etudiant",
                                         "Demandeur d'emploi - famille nombreuse",
                                         "Senior (+ de 60 ans)",
                                         "Tarif dimanche matin",
                                         "Normal",
                                         "Abonnement 5 places valable 6 mois",
                                         "Abonnement 10 places valable 1 an"],
                           "Prix": ["5,00 €",
                                    "7,30 €",
                                    "7,30 €",
                                    "7,30 €",
                                    "7,30 €",
                                    "6,00 €",
                                    "8,80 €",
                                    "32,50 €",
                                    "65,00 €"]}), hide_index = True)

# Lien vers le site du Sénéchal
st.subheader("Pour plus d'infos ou pour réserver, rendez-vous [ici](https://www.cinema-senechal.com/)")
          