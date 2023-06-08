import numpy as np
import pandas as pd
import joblib
import pickle
from flask import Flask, request , render_template

app= Flask(__name__)

model = pickle.load(open('models/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


# Add the recommendations route



if __name__ == "__main__":
    app.run(debug=True)