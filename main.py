import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
import warnings

warnings.filterwarnings('ignore')

# -------------------------------
# LOAD DATA
# -------------------------------
column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('file.tsv', sep='\t', names=column_names)

movie_titles = pd.read_csv('Movie_Id_Titles.csv')

data = pd.merge(df, movie_titles, on='item_id')

ratings = pd.DataFrame(data.groupby('title')['rating'].mean())
ratings['num of ratings'] = data.groupby('title')['rating'].count()

moviemat = data.pivot_table(index='user_id',
                            columns='title',
                            values='rating')

# -------------------------------
# RECOMMEND FUNCTION
# -------------------------------
def recommend():
    movie_name = entry.get()
    result_box.delete('1.0', tk.END)

    if movie_name not in moviemat.columns:
        result_box.insert(tk.END, "❌ Movie not found. Try another name.\n")
        return

    movie_user_ratings = moviemat[movie_name]
    similar_to_movie = moviemat.corrwith(movie_user_ratings)

    corr_movie = pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie.dropna(inplace=True)

    corr_movie = corr_movie.join(ratings['num of ratings'])

    recommendations = corr_movie[corr_movie['num of ratings'] > 100] \
        .sort_values('Correlation', ascending=False) \
        .head(10)

    result_box.insert(tk.END, f"🎯 Recommendations for:\n{movie_name}\n\n")

    for i, (title, row) in enumerate(recommendations.iterrows(), 1):
        result_box.insert(tk.END,
            f"{i}. {title}\n   ⭐ {row['Correlation']:.2f}   👥 {int(row['num of ratings'])}\n\n"
        )

# -------------------------------
# UI DESIGN (MODERN DARK)
# -------------------------------
root = tk.Tk()
root.title("Movie Recommender")
root.geometry("720x600")
root.configure(bg="#121212")

# Header
header = tk.Label(root,
                  text="🎬 Movie Recommender",
                  font=("Segoe UI", 20, "bold"),
                  bg="#121212",
                  fg="#00FFD1")
header.pack(pady=15)

# Input frame
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)

entry = tk.Entry(frame,
                 width=40,
                 font=("Segoe UI", 12),
                 bg="#1f1f1f",
                 fg="white",
                 insertbackground="white",
                 bd=0)
entry.grid(row=0, column=0, padx=10, ipady=6)

# Button hover
def on_enter(e):
    btn['bg'] = '#00c2a8'

def on_leave(e):
    btn['bg'] = '#00FFD1'

# Button
btn = tk.Button(frame,
                text="Search",
                command=recommend,
                bg="#00FFD1",
                fg="black",
                font=("Segoe UI", 10, "bold"),
                bd=0,
                padx=15,
                pady=5)
btn.grid(row=0, column=1)

btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

# Result box (scrollable)
result_box = scrolledtext.ScrolledText(root,
                                       height=22,
                                       width=85,
                                       font=("Consolas", 10),
                                       bg="#1f1f1f",
                                       fg="#e6e6e6",
                                       insertbackground="white",
                                       bd=0)
result_box.pack(pady=20)

root.mainloop()