# from firebase import firebase
import pyrebase
import tweepy

# firebase_admin = firebase.FirebaseApplication("https://bigdata-83675-default-rtdb.firebaseio.com",None)

config = {
  "apiKey": "",
  "authDomain": "BigData.firebaseapp.com",
  "databaseURL": "https://bigdata-83675-default-rtdb.firebaseio.com",
  "storageBucket": ""
}

firebase1 = pyrebase.initialize_app(config)

# read configs
user_key = 'X8c8cya1e1aPD2XQsIRJn3HGC'
user_secret = 'Lvm3HETlbg2fMvPLGHAp2FeWnP4D4HKog2JGkfT9gFiJrrqBj8'
access_token = '1535360072880115713-uiSbSiJiOBNCHhRrYlRwUm1OMsTGiY'
secret_access_token = 'XPHmAHktJHr1F4TZSxltc20SV0waKk8hnWH9jpkZ6kb91'


authentication = tweepy.OAuthHandler(user_key, user_secret)

#remaining code
api = tweepy.API(authentication)
userID = 'EnelClientesCL'
db = firebase1.database()
def validar_tweet_db(id):
    tweet_por_id = db.child("/corte_de_luz/datos_corte_de_luz").order_by_child("id").equal_to(id).get()
    if tweet_por_id.val() == []:
        return False
    else:
        return True
        
user = api.get_user(screen_name=userID)
total_tweet = user.statuses_count 
   
while True:
    user = api.get_user(screen_name=userID)
    nuevos_tweet = int(user.statuses_count) - total_tweet
    total_tweet = total_tweet + nuevos_tweet
    print(nuevos_tweet)
    print(total_tweet)
    
    if nuevos_tweet == 0:
        tweets = api.user_timeline(screen_name=userID,
                                count=200,
                                include_rts = False,
                                tweet_mode = 'extended'
                                )
      
        for info in tweets[:200]:
            print(validar_tweet_db(info.id))
            if validar_tweet_db(info.id) == False:
                hashtags = info.entities['hashtags']
                print(hashtags)
                for hashtag in hashtags:
                    if hashtag['text'] == 'CorteDeEnergía':
                        
                        data_corte_de_luz = {
                            'id': info.id,
                            'fecha': str(info.created_at),
                            'mensaje': info.full_text,
                            'categoria':  hashtag['text'] 
                        }
                        # resultado = firebase_admin.post('/corte_de_luz/datos_corte_de_luz', data_corte_de_luz)
                        resultado = db.child("/corte_de_luz/datos_corte_de_luz").push(data_corte_de_luz)
                        
            


            