import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c9cb5ec336fa36659fbba0ba516298dc&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
    full_path =  "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_name = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)

    return recommended_movie_name, recommended_movie_posters

movies_dict = pickle.load(open('movie_dict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
"How would you like to be contacted?",
movies['title'].values)

if st.button("Show Recommendation"):
    name,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])
    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])
    with col4:
        st.text(name[3])
        st.image(posters[3])
    with col5:
        st.text(name[4])
        st.image(posters[4])