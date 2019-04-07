import pandas as pd
import numpy as np
import json
import flask

# Cargo modelo y catalogo de paises
data_neighbours = pd.read_csv('data_neighbours.csv', index_col=0)
data_matrix = pd.read_csv('data_matrix.csv', index_col=0)
catalog = pd.read_json('catalog.json', encoding ='utf-8')
catalog['code'] = catalog['code'].astype(str)
catalog['code'] = 't_' + catalog['code']

# initialize our Flask application and some variables
app = flask.Flask(__name__)

@app.route("/destinations")

# Muestro destinos posibles en la recomendacion
def show_destinations():
    destinations = catalog.to_json(orient='records')
    resp = flask.Response(destinations, status=200, mimetype='application/json')
    return resp

# Recomiendo un destino, en base a los que ingresa el usuario
@app.route("/recommend")
def recommend_cities():
    
    # Armo lista con las ciudades que busco el usuario, y las uso para recomendar
    cities = flask.request.args.getlist('city')
    code = catalog[catalog['name'].isin(cities)]['code'].tolist()

    # Recomiendo segun la ciudad que eligio
    most_similar_to_likes = data_neighbours.loc[code]
    similar_list = most_similar_to_likes.values.tolist()
    similar_list = list(set([item for sublist in similar_list for item in sublist]))
    neighbourhood = data_matrix[similar_list].loc[similar_list]

    # Vector que contiene lo que esl usuario busco + vecinos cercanos de ese destino
    user_vector = pd.DataFrame(index=data_neighbours.index,columns=range(0,1))
    for i in range(0,len(user_vector)):
        if user_vector.index[i] in code:
            user_vector.iloc[i,0] = 1.0
        else:
            user_vector.iloc[i,0] = 0.0

    user_vector.iloc[:,0] = user_vector.iloc[:,0].astype(float)
    user_vector = user_vector.loc[similar_list]

    # Calculo score de recomendacion del destino
    score = neighbourhood.dot(user_vector.iloc[:,0]).div(neighbourhood.sum(axis=1))

    # Elimino los destinos que el usuario ya busco
    score = score.drop(code)
    
    # Decodeo la respuesta, poninedo el nombre del destino
    recomendacion = pd.DataFrame()
    recomendacion['code'] = score.nlargest(20).index
    recomendacion['score'] = np.array(score.nlargest(20))

    recomendacion = recomendacion.merge(catalog, on='code')
    recomendacion = recomendacion[['name','country','score']]

    json_recomendacion = recomendacion.to_json(orient='records')
    resp = flask.Response(json_recomendacion, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(debug=True)

# Ejemplos local
# Recomendacion: http://127.0.0.1:5000/recommend?city=Barcelona&city=Bangkok
# Destinos: http://127.0.0.1:5000/destinations

# Ejemplos produccion
# Recomendacion: https://recommend-destination.herokuapp.com/recommend?city=Barcelona&city=Bangkok
# Destinos: https://recommend-destination.herokuapp.com/destinations

