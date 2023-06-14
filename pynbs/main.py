# %%
import numpy as np
import pandas as pd
import joblib

# %%
new_ds=pd.read_csv("new_ds.csv")
svd=joblib.load('../models/svd_model.pkl')
ratings=pd.read_csv(r"../dataset/ratings.csv")
try:
    ratings1=pd.read_csv(r"F:\movie_recommendor\ratings1.csv")
except FileNotFoundError:
    print("")

# %%
def merge(ratings1,ratings):
    ratings=ratings.append(ratings1,ignore_index=True)
    return ratings

# %%
def recommendonmovie(movie):
    similarity=np.load('similaritybwmovies.npy')
    movie_index=new_ds[new_ds["title1"]==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    for i in movies_list:
        print(new_ds.iloc[i[0]].title1)
    

# %%
def del_variable(variable1):
    del variable1
del_variable(svd)

# %%
def get_best_movies(obj,id,obj1):
    movieid=obj1['id'].unique()
    l=[]
    b=[]
    for movie in movieid:
        result=svd.predict(id,movie)
        estimation=result[3]
        b.append((movie,estimation))
    return b

# %%
def get_recommendations(userid):
    predictions=get_best_movies(ratings,userid,new_ds)
    lis=[]
    sorted_predictions=sorted(predictions,key=lambda x:x[1],reverse=True)
    sorted_predictions=sorted_predictions[0:10]
    
    for i in sorted_predictions:
        specific_row =new_ds[new_ds["id"]==i[0]]['title1'].values[0]
        print(specific_row)
        

# %%
get_recommendations(7800)

# %%
recommendonmovie('The 39 Steps')

# %%
moviesnew=pd.read_csv(r"moviesnew.csv")

# %% [markdown]
# 

# %%
moviesnew['tag']=moviesnew['tag'].apply(lambda x:x.replace(" ",''))
moviesnew['tag']=moviesnew['tag'].apply(lambda x:x.lower())

# %%
def search(keywords):
    import re
    keywords=keywords.lower()
    keywords=keywords.split()
  
    # Filter the DataFrame based on the keywords
    filtered_rows = []
    for index, row in moviesnew.iterrows():
        text = row['tag']
        
        if all(re.search(keyword, text) for keyword in keywords):
            filtered_rows.append(row)
        
        

    filtered_df = pd.DataFrame(filtered_rows)
    try:

        filtered_df=filtered_df.sort_values(by='vote_average',ascending=False)
    # Print the filtered DataFrame
        print("not found exact results")
        print(filtered_df["title1"].head(25))
    except KeyError:
        filtered_rows = []
        for index, row in moviesnew.iterrows():
            text = row['tag']
            
            if any(re.search(keyword, text) for keyword in keywords):
                filtered_rows.append(row)
        filtered_df = pd.DataFrame(filtered_rows)
        filtered_df=filtered_df.sort_values(by='vote_average',ascending=False)
        print(filtered_df['title1'].head(25))


# %%
search("horror comedy")


# %%
def create_userid():
    a=ratings['userId']
    userid=a.max()+1
    return userid


# %%

def giverating(userid,movieid,rating):
    import time
    timestamp=int(time.time())
    

    ratings1=pd.DataFrame({'userId':[userid],'movieId':[movieid],'rating':[rating],'timestamp':[int(timestamp)]})
   
    ratings1.to_csv(r"F:\movie_recommendor\ratings1.csv",index=False)

# %%
giverating(270896,110,5)
ratings=merge(ratings1,ratings)


# %%
from random import randint
def main(userid):
    if ratings[ratings["userId"]==userid].size==0:
          
          for i in range(25):
            print(new_ds.iloc[randint(0,45538)]["title1"])
          
    else:
         a=get_recommendations(userid)
         recommendonmovie(a)
         print('rated')
main(270895)

# %%
import streamlit as st
import pickle
movies_all = pd.read_csv("../pynbs/moviesall.csv").values

st.title("Movie Recommender System")
option = st.selectbox("ABC",movies_all)



# %%



