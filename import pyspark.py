from firebase import firebase
import random
import pyrebase
import pandas as pd

config = {
  "apiKey": "",
  "authDomain": "BigData.firebaseapp.com",
  "databaseURL": "https://bigdata-83675-default-rtdb.firebaseio.com",
  "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
all_user_ids = db.child("/corte_de_luz/datos_corte_de_luz").get()
comunas = ['ALHUÉ','BUIN','CALERA DE TANGO','CERRILLOS','CERRO NAVIA','COLINA','CONCHALÍ','CURACAVÍ','EL BOSQUE','EL MONTE','ESTACIÓN CENTRAL','HUECHURABA','INDEPENDENCIA','ISLA DE MAIPO','LA CISTERNA','LA FLORIDA','LA GRANJA','LAMPA','LA PINTANA','LA REINA','LAS CONDES','LO BARNECHEA','LO ESPEJO','LO PRADO'
          'MACUL','MAIPÚ','MARÍA PINTO','MELIPILLA','ÑUÑOA','PADRE HURTADO','PAINE','PEDRO AGUIRRE CERDA','PEÑAFLOR','PEÑALOLÉN','PIRQUE','PROVIDENCIA','PUDAHUEL','PUENTE ALTO','QUILICURA','QUINTA NORMAL','RECOLETA','RENCA','SAN BERNARDO','SAN JOAQUÍN','SAN JOSÉ DE MAIPO','SAN MIGUEL','SAN PEDRO','SAN RAMÓN'
          'SANTIAGO','TALAGANTE','TILTIL','VITACURA']
lista = []

for corte in all_user_ids.each():
  text = corte.val()
  list_text = text['mensaje'].split()
  valida_comuna = False;
  for palabra in list_text:
    palabra = palabra.replace(",","")
    palabra = palabra.replace(".","")
    if palabra.upper() in comunas:
      text['comuna'] = palabra.upper()
      valida_comuna = True
  if valida_comuna == False:
    text['comuna'] = 'Sin Comuna';
    
  lista.append(text)
  
df = pd.DataFrame(lista)  
df['fecha'] = pd.to_datetime(df['fecha'])
df['Year'] = df['fecha'].dt.year
df['Month'] = df['fecha'].dt.month
df['Day'] = df['fecha'].dt.day

df.to_csv('data_csv.csv', index=False)