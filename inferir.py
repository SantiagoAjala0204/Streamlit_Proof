import joblib
# Datos fijos para prueba
features = [[19, 2, 20, 0, 6,
             True, False, False, False, False, False,
             False, False, True, False, False, False,
             False, True, False, False, True, False,
             False, False, False, True, False, False]]
# Cargar el modelo
modelo = joblib.load("modelo_random_forest.pkl")
# Hacer la predicción
prediccion = modelo.predict(features)
print("Predicción:", prediccion[0])