from flask import Flask,render_template,request
import mysql.connector

#MRS import
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import process

app=Flask(__name__)

#storing file
movies='movies.csv'
ratings='ratings.csv'

#Extracting file data
df_movies=pd.read_csv(movies, usecols=['movieId','title'], dtype={'movieId':'int32','title':'str'})
df_ratings=pd.read_csv(ratings, usecols=['userId','movieId','rating'],dtype={'userId':'int32','movieId':'int32','rating':'float32'})

#Creating spare Matrix
movies_users=df_ratings.pivot(index='movieId', columns='userId',values='rating').fillna(0)
mat_movies_users=csr_matrix(movies_users.values)



# Cosine Similarity
model_knn= NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
model_knn.fit(mat_movies_users)



# List of Movies recommended

def recommender(movie_name, data, model, n_recommendations):
    model.fit(data)
    idx = process.extractOne(movie_name, df_movies['title'])[2]
    print('Movie Selected: ', df_movies['title'][idx], 'Index: ', idx)
    print('Searching for recommendations.....')
    distances, indices = model.kneighbors(data[idx], n_neighbors=n_recommendations)

    for i in indices:
        final_movies_matrix = df_movies['title'][i].where(i != idx)
    df = pd.DataFrame(final_movies_matrix)

    #making final list from pandas column
    final_data = df['title'].tolist()
    return final_data


#movie_name=str(input("Enter Movie Name : "))
#recommender(movie_name, mat_movies_users, model_knn, 20)



@app.route("/",methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        # Then get the data from the form
        movie_name = request.form['search_field']

    #movie_name = str(input("Enter Movie Name : "))
        movie_list=recommender(movie_name, mat_movies_users, model_knn, 20)
        return render_template('websites/index.html',movie_list=movie_list)
    else:
        return render_template('websites/index.html')

@app.route("/result",methods=['POST','GET'])
def result():
    db=mysql.connector.connect(
        host="localhost",
        user="root",
        password='123',
        database="flask_test"
    )
    mycursor=db.cursor()
    if(request.method=='POST'):
        result=request.form
        name=result['Name']
        mycursor.execute("Select name,Physics,Chemistry,Total from details where name='"+name+"'",)
        r=mycursor.fetchone()
        db.commit()
        mycursor.close()
        return render_template("index.html",r=r)

    if(request.method=='POST'):
        result=request.form
        print(result)
        name=result['Name']
        py=int(result['py'])
        ch=int(result['chem'])
        r=str(py+ch)
        mycursor.execute("Insert into details (name,Physics,Chemistry,Total) values (%s,%s,%s,%s)",(name,py,ch,r))
        db.commit()
        mycursor.close()

        return render_template('test.html',result=result,r=r)
    return render_template("index.html")


@app.route("/Auth")
def Auth():
    return "Auth Page"

app.run(debug=True)