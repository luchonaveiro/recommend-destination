# Recommend Destination

Este sistema de recomendacion se realizo usando 1.700.000 busquedas de un sitio de e-travel.
Se utilizo el modelo de filtros colaborativos (item-item).
El input del modelo es 1 o más ciudades del mundo, y el modelo devuelve 10 otras recomendaciones de ciudades que usuarios parecidos buscaron.

Se construyo una API al rededor del modelo, la cual se puede consultar con un POST:

https://recommend-destination.herokuapp.com/recommend

body:

{
    "cities":
        ["City 1","City 2",...,"City N]
}

El modelo considera solo 380 ciudades del mundo. Estas se pueden consultar en:

https://recommend-destination.herokuapp.com/destinations





