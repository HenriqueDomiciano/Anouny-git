from app import app,db
from app import templates
from app.models.forms import Formulario
from app.models.Usuario import  Message
from flask import render_template,redirect,url_for
from datetime import datetime,timedelta 
import re
import pickle
import tweepy
import nltk
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import os
auth = tweepy.OAuthHandler(os.environ['API_KEY'],os.environ['SECRET_API_KEY'])
auth.set_access_token(os.environ['ACESS_TOKEN'],os.environ['ACESS_TOKEN_SECRET'])

api = tweepy.API(auth)
model = pickle.load(open(r'/app/app/controllers/model.pkl','rb'))
cv = pickle.load(open(r'/app/app/controllers/countvect.pkl','rb'))
names = pickle.load(open(r'/app/app/controllers/names.pkl','rb'))

def arrume(review):
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
    review = ' '.join(review)
    return review

@app.route('/',methods=['GET',"POST"])
def index():    
    hate = False
    form = Formulario()
    try:
        time_sent = db.session.query(Message.time).all()[-3:]
        time_sent = [i[0].strftime("%m/%d/%Y, %H:%M:%S") for i in time_sent]
        send = db.session.query(Message.text).all()[-3:]
        send = [i[0] for i in send]
        send = send[::-1]
        time_sent = time_sent[::-1]
    except Exception as e:
        print(e)
        time_sent = []
        send = []

    
    if form.validate_on_submit():
        cut_off = datetime.now()-timedelta(days=1)
        mensagem = form.text.data
        img = form.image.data
        msg = form.text.data
        timeline = tweepy.Cursor(api.user_timeline).items()
        for tweet in timeline:
            if tweet.created_at<=cut_off:
                    api.destroy_status(tweet.id)
            else:
                break
        transform = cv.fit_transform(names+[arrume(msg)]).toarray()
        if model.predict(transform[-1].reshape(1,-1))==1:
            hate = True
        else:
            
            hate = False
            mensagem = Message(mensagem,datetime.now())
            db.session.add(mensagem)
            db.session.commit()

            if img!=None:
                print('E para enviar imagem')
                api.update_with_media(filename ='',status = msg,file = img)
            else:
                print('Não enviei a imagem')
                api.update_status(msg)
            return redirect(url_for('index'))
    
    return render_template('index.html',form=form,data=send, length = len(send), time_sent = time_sent,hate =hate)
