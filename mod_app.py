import streamlit as st
import pickle
import pandas as pd
import requests
import base64


# Function to fetch the poster from TMDb API
def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c9cb5ec336fa36659fbba0ba516298dc&language=en-US'.format(
        movie_id)
    response = requests.get(url)
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path


# Function to fetch the YouTube trailer from TMDb API
def fetch_trailer(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}/videos?api_key=c9cb5ec336fa36659fbba0ba516298dc&language=en-US'.format(
        movie_id)
    response = requests.get(url)
    data = response.json()

    # Filter only YouTube trailers
    trailers = [video for video in data['results'] if video['site'] == 'YouTube' and video['type'] == 'Trailer']

    # Return the first trailer if available
    if trailers:
        youtube_key = trailers[0]['key']
        youtube_url = f"https://www.youtube.com/watch?v={youtube_key}"
        return youtube_url
    else:
        return None


# Function to get movie recommendations and their posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []

    for i in distances[1:6]:
        # Get movie id and title
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)

        # Fetch the movie poster
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids


# Load the saved movie data
movies_dict = pickle.load(open('movie_dict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load the similarity model
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Set up the background image for the app
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("netflix_1.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://user-images.githubusercontent.com/33485020/108069438-5ee79d80-7089-11eb-8264-08fdda7e0d11.jpg");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stAppViewContainer"] > .main::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Main app title
st.markdown(f'<h1 style="color:#FFFFFF;">Movie Recommendation System</h1>', unsafe_allow_html=True)

# Dropdown for user to select a movie
selected_movie_name = st.selectbox("Enter the Movie You Are Interested In:", movies['title'].values)

# When the user clicks "Show Recommendation"
if st.button("Show Recommendation"):
    recommended_names, recommended_posters, recommended_movie_ids = recommend(selected_movie_name)

    # Display recommended movies in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display first recommendation
    with col1:
        st.text(recommended_names[0])
        st.image(recommended_posters[0])
        trailer_url = fetch_trailer(recommended_movie_ids[0])
        if trailer_url:
            st.video(trailer_url)

    # Display second recommendation
    with col2:
        st.text(recommended_names[1])
        st.image(recommended_posters[1])
        trailer_url = fetch_trailer(recommended_movie_ids[1])
        if trailer_url:
            st.video(trailer_url)

    # Display third recommendation
    with col3:
        st.text(recommended_names[2])
        st.image(recommended_posters[2])
        trailer_url = fetch_trailer(recommended_movie_ids[2])
        if trailer_url:
            st.video(trailer_url)

    # Display fourth recommendation
    with col4:
        st.text(recommended_names[3])
        st.image(recommended_posters[3])
        trailer_url = fetch_trailer(recommended_movie_ids[3])
        if trailer_url:
            st.video(trailer_url)

    # Display fifth recommendation
    with col5:
        st.text(recommended_names[4])
        st.image(recommended_posters[4])
        trailer_url = fetch_trailer(recommended_movie_ids[4])
        if trailer_url:
            st.video(trailer_url)
