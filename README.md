The movie recommendation system developed as part of the AIML   project successfully provides personalized movie recommendations based on user input. The system leverages collaborative filtering techniques and cosine similarity to suggest movies similar to the ones entered by the user. Users can interact with the system by entering movie names, viewing recommendations, and managing their watchlist.
The user interface provides a user-friendly experience, allowing users to easily navigate the system and interact with movie recommendations. Additionally, the inclusion of a watchlist feature enables users to save their preferred movies for future reference, enhancing user engagement and satisfaction.


About the Dataset:

The dataset used in this movie recommendation system is sourced from the MovieLens website. It consists of two main datasets:
1.	Movies Dataset:
      

      •	This dataset contains information about various movies, including their unique identifiers (movieId), titles (title), and genres (genres).

      •	Each movie is associated with one or more genres, allowing for genre-based analysis and recommendations.

2.	Ratings Dataset:

      •	The ratings dataset contains user ratings for different movies.

      •	It includes details such as the user identifier (userId), movie identifier (movieId), rating given by the user (rating), and timestamp of the rating (timestamp).

      •	This dataset enables the recommendation system to provide personalized movie recommendations based on user preferences and past ratings.




Proposed algorithms

Collaborative Filtering with Cosine Similarity

Working Principle:

•	Collaborative filtering is a commonly used technique in recommendation systems that leverages user-item interaction data to make predictions.

•	In this algorithm, we calculate the similarity between items based on user ratings using the cosine similarity metric.

•	The cosine similarity measures the cosine of the angle between two vectors, representing the ratings given by users to different movies.

•	The higher the cosine similarity between two movies, the more similar they are in terms of user preferences.
 
•	To generate recommendations for a given movie, we identify the most similar movies based on their cosine similarity scores and recommend the top N movies to the user.

 
