import streamlit as st
import pickle
import pandas as pd
import numpy as np

movies_list = pd.read_csv("./pynbs/moviesall.csv")
ratings=pd.read_csv("./dataset/ratings.csv")
new_ds=pd.read_csv("./pynbs/new_ds.csv")
movies_list = movies_list["title"].values


# This model is not opening, Because of suprise module
svd = pickle.load(open("./pynbs/svd_model.pkl","rb"))

def get_recommendations_by_rating(userid):
        predictions=get_best_movies(ratings,userid,new_ds)
        lis=[]
        sorted_predictions=sorted(predictions,key=lambda x:x[1],reverse=True)
        sorted_predictions=sorted_predictions[0:10]
        
        for i in sorted_predictions:
            specific_row =new_ds[new_ds["id"]==i[0]]['title1'].values[0]
            print(specific_row)

def get_best_movies(obj,id,obj1):
    movieid=obj1['id'].unique()
    l=[]
    b=[]
    for movie in movieid:
        result=svd.predict(id,movie)
        estimation=result[3]
        b.append((movie,estimation))
    return b

def recommendonmovie(movie):
    similarity=np.load('similaritybwmovies.npy')
    movie_index=new_ds[new_ds["title1"]==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    for i in movies_list:
        print(new_ds.iloc[i[0]].title1)


st.title("Movie Recommender System")
option = st.selectbox("Choose A Movie To Recommend!",movies_list)

if st.button("Recommend"):
    st.write(option)

    #We need to take this option and send it to our recommend movie function