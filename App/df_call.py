import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# --------------------------------------------------------------------------

# Data Frame pour les films
def df_final():
    link = "https://raw.githubusercontent.com/githubmhd/movie_recommendations/main/App/movie_final_ML.csv"
    df_movie = pd.read_csv(link, low_memory = False, index_col = "Unnamed: 0")
    
    # Création d'une nouvelle colonne avec la release date pour gérer les homonymes
    df_movie["title_date"] = df_movie["title_x"] + " (" + df_movie["release_date"].astype(str) + ")"
    
    return df_movie


# --------------------------------------------------------------------------

# Data Frame pour les scénaristes et acteurs
def name_df():
    link = "https://raw.githubusercontent.com/githubmhd/movie_recommendations/main/App/name_list.csv"
    df_name = pd.read_csv(link, low_memory = False, index_col = "Unnamed: 0")
    
    # Création d'une nouvelle ligne pour gérer les films qui n'ont pas 3 acteurs de renseigné
    new = {"nconst" : "non renseigné",
              "primaryName": "", 
              "birthYear" : "", 
              "deathYear" : "", 
              "primaryProfession" : "", 
              "knownForTitles" : ""}

    df_name.loc[1] = new
    
    return df_name

# --------------------------------------------------------------------------

# Machine Learning
def ML_Reco(tconst):
    # Get the df
    movie = df_final()
    
    # Define X
    X = movie.drop(columns=['tconst', 'originalTitle', 'title_x', 
                            'backdrop_path', 'id', 'imdb_id', 'overview', 'poster_path', "title_date"])
    
    # Name columns types
    numeric_cols = ["runtimeMinutes", "averageRating", "numVotes","popularity", "release_date"]

    category_cols = ["isAdult", "original_language", "director1", "writer1", "actor1", "actor2", "actor3"]

    pass_cols = ['Drama', 'Adventure', 'Fantasy',
        'Biography', 'Romance', 'History', 'Comedy', 'Crime', 'Mystery',
        'Horror', 'Western', 'Action', 'Family', 'War', 'Sci-Fi', 'Thriller',
        'Sport', 'Documentary', 'Music', 'Animation', 'Film-Noir', 'News']
    
    # Define the preprocessor
    num_preprocessor = StandardScaler()
    cat_preprocessor = OneHotEncoder()

    # Create the model with pipeline
    model_nearest = (make_pipeline(
                                    ColumnTransformer([('OneHotEncoder', cat_preprocessor, category_cols),
                                                    ('StandardScaler', num_preprocessor, numeric_cols),
                                                    ( 'already_factorized','passthrough', pass_cols)]),
                                    NearestNeighbors(n_neighbors = 7)  ))
    
    # Fit the model 
    model_nearest.fit(X)
    
    # Create a new X that fits with the pipeline
    X_transformed = model_nearest.named_steps['columntransformer'].fit_transform(X) 
    
    # Get the index of the search
    ind = movie[movie['tconst'] == tconst].index
    
    # Get the index of the nearest neighbors
    kneighbors_ind = model_nearest.named_steps['nearestneighbors'].kneighbors(X_transformed[ind], n_neighbors = 7)[1]
    
    # I put in a list the names of nearest movies
    result = [movie["title_x"].iloc[ele] for ele in kneighbors_ind[0]]
    # I remove the closest from my list (the movie searched itself)
    result.remove(movie["title_x"][movie["tconst"] == tconst].iloc[0])
    
    return result
    