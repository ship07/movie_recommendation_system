from flask import Flask,render_template,request,url_for,redirect
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

app=Flask(__name__)

dataset=pd.read_csv('./clean_dataset/clean_data2.csv')

def create_similarity():
    cv=CountVectorizer()
    count_matrix=cv.fit_transform(dataset['combo'])
    similarity_score=cosine_similarity(count_matrix)
    return similarity_score

def recommendation(movie):
    movie=movie.lower()
    if movie not in dataset['movie_title'].unique():
        return None
    else:
        similarity_score=create_similarity()
        location=dataset.loc[dataset['movie_title']==movie].index[0]
        similar_movie=list(enumerate(similarity_score[location]))
        similar_movie=sorted(similar_movie,key=lambda x:x[1],reverse=True)
        similar_movie=similar_movie[1:11]
        recommended_movies=[]
        for movies in range(len(similar_movie)):
            m=similar_movie[movies][0]
            recommended_movies.append(dataset['movie_title'][m])
        return recommended_movies

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=='POST':
        movie=request.form['movie']
        recommended_movies=recommendation(movie)
        result=True
        if recommended_movies==None:
            result=False
        #print(recommended_movies)
        return render_template("recommendation.html",movies_list=recommended_movies,result=result)
    return render_template("m.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
    
if __name__=="__main__":
    app.run(debug=True)
