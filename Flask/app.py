from flask import Flask,request,render_template
import pandas as pd
import pickle


app=Flask(__name__)
model=pickle.load(open("book.pkl",'rb'))

data=pd.read_csv("us_canada_user_rating_pivot1.csv",encoding="ISO-8859-1",index_col="bookTitle")


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/extractor')
def extractor():
    return render_template('extractor.html')

@app.route('/keywords',methods=['POST'])
def keywords():
    typ=request.form['type']
    output=request.form['output']
    print(output)
    distances,indices=model.kneighbors(data.loc[output,:].values.reshape(1,-1),n_neighbors=6)
    keyword=[]
    for i in range(0,len(distances.flatten())):
        if i==0:
            print('Recommendations for {0}:\n'.format(output))
        else:
            keyword.append('{0}: {1}'.format(i,data.index[indices.flatten()[i]]))
            
    return render_template('keywords.html',keyword=keyword)

if __name__=='__main__':
    app.run(debug=False)