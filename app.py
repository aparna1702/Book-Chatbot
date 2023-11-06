from flask import Flask, render_template, request, jsonify
import torch
import pickle
import numpy as np
import pandas as pd

popular_df = pd.read_pickle('popular.pkl') #opening popular_df
pt=pd.read_pickle('pt.pkl')
books=pd.read_pickle('books.pkl')
similarity_scores = pd.read_pickle('similarity_scores.pkl')


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
        msg = request.form["msg"]
        input = msg
        return jsonify({"books": recommend(input)})

def recommend(user_input):
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        data.append(item)

    

    return data


if __name__ == '__main__':
    app.run()