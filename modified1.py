import streamlit as st
import pickle
import pandas as pd
import requests
import base64

# TMDb API key
API_KEY = 'c9cb5ec336fa36659fbba0ba516298dc'


# Function to fetch the poster from TMDb API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    data = response.json()
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path


# Function to fetch the YouTube trailer from TMDb API
def fetch_trailer(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    data = response.json()

    trailers = [video for video in data['results'] if video['site'] == 'YouTube' and video['type'] == 'Trailer']

    if trailers:
        youtube_key = trailers[0]['key']
        return youtube_key  # Return the YouTube key for embedding
    else:
        return None


# Function to fetch movie details (director, cast, reviews)
def fetch_movie_details(movie_id):
    url_credits = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US'
    response_credits = requests.get(url_credits)
    credits_data = response_credits.json()

    url_reviews = f'https://api.themoviedb.org/3/movie/{movie_id}/reviews?api_key={API_KEY}&language=en-US'
    response_reviews = requests.get(url_reviews)
    reviews_data = response_reviews.json()

    director = next((crew_member['name'] for crew_member in credits_data['crew'] if crew_member['job'] == 'Director'),
                    None)
    cast_list = [cast_member['name'] for cast_member in credits_data['cast'][:5]]
    reviews = [review['content'] for review in reviews_data['results'][:3]]

    return director, cast_list, reviews


# Function to get movie recommendations and their posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids


# Fetch popular movies
def fetch_popular_movies():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    return response.json()['results']


# Fetch trending movies
def fetch_trending_movies():
    url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}'
    response = requests.get(url)
    return response.json()['results']


# Fetch upcoming movies
def fetch_upcoming_movies():
    url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    return response.json()['results']


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
background-size: cover;
background-position: center;
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
st.markdown(f'<h1 style="color:#FFFFFF;text-align:center;">Movie Recommendation System</h1>', unsafe_allow_html=True)

# Tabs for interactive sections
tab1, tab2, tab3, tab4 = st.tabs(["Recommendations", "Popular", "Trending", "Upcoming"])

# Recommendations Tab
with tab1:
    selected_movie_name = st.selectbox("Choose a Movie You Like:", movies['title'].values)

    if st.button("Get Recommendations"):
        recommended_names, recommended_posters, recommended_movie_ids = recommend(selected_movie_name)

        # Enhanced layout for recommendations
        st.markdown('<h2 style="color:#FFFFFF;">Recommended Movies</h2>', unsafe_allow_html=True)

        # Create a list to store the boxes for the recommended movies
        for i in range(len(recommended_names)):
            # Create a box for each recommendation with a border
            with st.container():
                st.markdown(
                    "<div style='border: 2px solid #FF5733; border-radius: 10px; padding: 10px; margin-bottom: 20px;'>",
                    unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(recommended_posters[i], width=150, use_column_width='auto')
                with col2:
                    st.markdown(f"<h3 style='color: #FFFFFF;'>{recommended_names[i]}</h3>", unsafe_allow_html=True)

                    # Embed the YouTube trailer directly
                    youtube_key = fetch_trailer(recommended_movie_ids[i])
                    if youtube_key:
                        st.markdown(
                            f'<iframe width="80%" height="180" src="https://www.youtube.com/embed/{youtube_key}" frameborder="0" allowfullscreen></iframe>',
                            unsafe_allow_html=True)

                    # Display director and cast
                    director, cast, reviews = fetch_movie_details(recommended_movie_ids[i])
                    st.markdown(
                        f"<div style='padding: 5px;'><strong>Director:</strong> <span style='color: #FFFFFF;'>{director}</span></div>",
                        unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='padding: 5px;'><strong>Cast:</strong> <span style='color: #FFFFFF;'>{', '.join(cast)}</span></div>",
                        unsafe_allow_html=True)

                    # Display user reviews
                    if reviews:
                        st.markdown(f"<div style='padding: 5px;'><strong>User Reviews:</strong></div>",
                                    unsafe_allow_html=True)

                        for review in reviews:
                            st.markdown(
                                f"<div style='padding: 5px; background-color: rgba(255, 255, 255, 0.1);'>{review}</div>",
                                unsafe_allow_html=True)
                    else:
                        st.write("<div style='padding: 10px; color: #FFFFFF;'>No user reviews available.</div>",
                                 unsafe_allow_html=True)

                # Close the recommendation box
                st.markdown("</div>", unsafe_allow_html=True)

# Popular Movies Tab
with tab2:
    if st.button("Show Popular Movies"):
        popular_movies = fetch_popular_movies()
        for movie in popular_movies[:10]:
            with st.expander(movie['title']):
                poster_url = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
                st.image(poster_url, width=150)
                st.write(movie['overview'])

# Trending Movies Tab
with tab3:
    if st.button("Show Trending Movies"):
        trending_movies = fetch_trending_movies()
        for movie in trending_movies[:10]:
            with st.expander(movie['title']):
                poster_url = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
                st.image(poster_url, width=150)
                st.write(movie['overview'])

# Upcoming Movies Tab
with tab4:
    if st.button("Show Upcoming Movies"):
        upcoming_movies = fetch_upcoming_movies()
        for movie in upcoming_movies[:10]:
            with st.expander(movie['title']):
                poster_url = f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}"
                st.image(poster_url, width=150)
                st.write(movie['overview'])
