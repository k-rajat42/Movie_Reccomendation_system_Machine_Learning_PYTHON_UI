import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tkinter import Tk, Label, Button, Entry, StringVar, Checkbutton, IntVar, Frame
from tkinter import messagebox
import csv

# Load the  database
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Merge the databases
data = pd.merge(ratings, movies, on='movieId')

# Create a pivot table
pivot_table = data.pivot_table(index='userId', columns='title', values='rating')

# Fill missing values with 0
pivot_table = pivot_table.fillna(0)

# Calculate similarity matrix
item_similarity = cosine_similarity(pivot_table.T)

# Read watchlist from CSV
def read_watchlist_from_csv():
    try:
        with open('watchlist.csv', 'r') as file:
            reader = csv.reader(file)
            watchlist = list(reader)
            return [movie[0] for movie in watchlist]
    except FileNotFoundError:
        return []

# Write watchlist to CSV
def write_watchlist_to_csv(watchlist):
    with open('watchlist.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for movie in watchlist:
            writer.writerow([movie])

# Make recommendations
def get_recommendations(movie_name, top_n=5):
    movie_idx = pivot_table.columns.get_loc(movie_name)
    similar_scores = list(enumerate(item_similarity[movie_idx]))
    similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)
    top_similar = similar_scores[1:top_n+1]
    top_movies = [pivot_table.columns[i] for i,_ in top_similar]
    return top_movies

class RecommendationSystemUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Movie Recommendation System | AIML GROUP PROJECT ")
        self.window.geometry("800x600")
        self.window.configure(bg='lightblue')

        self.label = Label(window, text="Enter Movie name and year (e.g., Toy Story (1995))", bg='gold', font=('Arial',11))
        self.label.pack()

        self.movie_name = StringVar()
        self.entry = Entry(window, textvariable=self.movie_name, width=35, font=('arial',10))
        self.entry.pack()

        self.button = Button(window, text="Get Recommendations", command=self.get_recommendations_ui, bg='green', fg='white', pady=5)
        self.button.pack(pady=(10, 5))  # Add vertical padding below this button

        self.clear_button = Button(window, text="Clear", command=self.clear_recommendations, bg='red', fg='white', pady=5)
        self.clear_button.pack(pady=5)  # Place the clear button below the Get Recommendations button

        self.recommendations_frame = Frame(window, bg='lightblue')  # Create a dedicated frame for recommendations
        self.recommendations_frame.pack()  # Pack the recommendations frame initially

        self.watchlist_frame = None

        self.watchlist_button = Button(window, text="View Watchlist", command=self.toggle_watchlist, bg='blue', fg='white', pady=5)
        self.watchlist_button.pack(pady=(5, 10))  # Add vertical padding above this button

        self.recommendations = []
        self.watchlist = read_watchlist_from_csv()  # Load watchlist from CSV on initialization
        
        self.group_members_label = Label(window, text="", bg='cyan', fg='black')
        self.group_members_label.place(relx=0.5, rely=1.0, anchor='s')  # Place label at bottom  corner


    def get_recommendations_ui(self):
        movie_name = self.movie_name.get().strip()
        if movie_name:
            self.clear_recommendations()  # Clear previous recommendations
            recommendations = get_recommendations(movie_name)
            for movie in recommendations:
                var = IntVar(value=1 if movie in self.watchlist else 0)
                c = Checkbutton(self.recommendations_frame, text=movie, variable=var, bg='lightblue', command=lambda movie=movie, var=var: self.update_watchlist(movie, var))
                c.pack(anchor='w')  
                self.recommendations.append(c)

    def update_watchlist(self, movie, var):
        if var.get() == 1:
            if movie not in self.watchlist:
                self.watchlist.append(movie)
                write_watchlist_to_csv(self.watchlist)  # Update CSV file with the modified watchlist
        else:
            if movie in self.watchlist:
                self.watchlist.remove(movie)
                write_watchlist_to_csv(self.watchlist)  # Update CSV file with the modified watchlist

    def toggle_watchlist(self):
        if self.watchlist_frame:
            self.watchlist_frame.destroy()  # Destroy the watchlist frame if it exists
            self.watchlist_frame = None
        else:
            self.show_watchlist()  # Show the watchlist frame

    def show_watchlist(self):
        self.watchlist_frame = Frame(self.window, bg='lightblue')  # Create a new watchlist frame
        self.watchlist_frame.pack()

        label = Label(self.watchlist_frame, text="Watchlist", bg='lightblue')
        label.pack()

        for movie in self.watchlist:
            var = IntVar(value=1)
            c = Checkbutton(self.watchlist_frame, text=movie, variable=var, bg='lightblue', command=lambda movie=movie, var=var: self.update_watchlist(movie, var))
            c.pack(anchor='w')  # Pack Checkbuttons to the left (west) side within the watchlist frame

        back_button = Button(self.watchlist_frame, text="Back", command=self.toggle_watchlist, bg='red', fg='white', pady=5)
        back_button.pack(pady=10)

    def clear_recommendations(self):
        for widget in self.recommendations:
            widget.destroy()
        self.recommendations = []  # Clear the recommendations list

root = Tk()
my_gui = RecommendationSystemUI(root)
root.mainloop()