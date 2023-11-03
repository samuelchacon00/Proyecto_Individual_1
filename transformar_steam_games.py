import pandas as pd

def isfloat(valor):
    try:
        float(valor)
        return True
    except:
        return False

def es_gratis(valor:str):
    try:
        return "Free" in valor
    except:
        return False

def funcion_year(string):
    string=str(string)
    lista=string.split("-")    

    if len(lista)>1 and string!="-1":
        return int(lista[0])
    else:
        return -1

nombre="datasets/steam_games.csv"

df=pd.read_csv(nombre,sep=";")

columnas_indeseadas=["publisher","specs","early_access"]

df.drop(columns=columnas_indeseadas,inplace=True)

# con esta mascara podemos ver que en el campo price, los unicos que no son valores numericos y tampoco
# tiene incluido la palabra "Free" son 5 elementos de los cuales 3 se pueden considerar gratis,
# los demos son versiones de prueba, y siempre son gratis

# aqui se puede apreciar aplicando la mascaras y viendo lo que hay en el campos genres (generos) y
# el campo tags (etiquetas) si hay alguna indicacion de que dicho juego sea gratis

mask=~(df["price"].apply(lambda x:isfloat(x))) & ~(df["price"].apply(lambda x:es_gratis(x)))
#print(df[["price","tags"]][mask])

indices=df[mask].index
for i in df[mask].index:
    for n in [df.at[i,"price"],df.at[i,"tags"],df.at[i,"genres"]]:
        if "Free" in n or "Demo" in n:
            df.at[i,"price"]="0"

#acualizamos la mascara y solo queda un valor que dice "play now" que no explica el precio
mask=~(df["price"].apply(lambda x:isfloat(x))) & ~(df["price"].apply(lambda x:es_gratis(x)))
#print(df[mask]["price"])

#quedando de esta forma un -1 para hacer mas facil las normalizacion y la transformacion
df.at[df[mask].index[0],"price"]=-1

# y finalmente estableciendo 0 como precio a los que dicen Free

mask=~(df["price"].isna()) & ~(df["price"].apply(lambda x:isfloat(x))) & (df["price"].apply(lambda x:es_gratis(x)))

for i in df[mask].index:
    df.at[i,"price"]="0"

#print(df[df["price"].apply(lambda x:isfloat(x))].sum())

# no hay registros duplicados
#print(df.duplicated().sum())

df = df.rename(columns={'id': 'item_id'})
#print(df)

mask=~df["release_date"].apply(lambda x:"-" in x)

for i in df[mask].index:
    df.at[i,"release_date"]="-1"

#recordatorio: agregar la columna year con el anio de release_date para poder hacer la funcion de la api 

#df["year"]=df["release_date"].apply(lambda x:funcion_year(x))

#print(df.isna().sum())
#print(df.info())

df["price"]=df["price"].apply(lambda x:float(x))
#df["year"]=df["year"].apply(lambda x:int(x))

df["release_date"].fillna("Unknow",inplace=True)
#df["year"].fillna("-1",inplace=True)

df.drop(columns=["Unnamed: 0"],inplace=True)

mask=(df["genres"].apply(lambda x:"Free to Play" in x)) | (df["tags"].apply(lambda x:"Free to Play" in x)) & ( df["price"]>0)
df[mask]["price"]=df[mask]["price"].apply(lambda x:0)

### -------------- Esta parte se hace para el modelo de aprendizaje automatico--------------------------------###


# borrando el duplicado del campo item_id porque si se llega a preguntar por ese va devolver el primero y hay que ver si son iguales
print("ahora hay: "+str(df[["item_id"]].duplicated().sum())+" duplicados")
# da uno por lo tanto si hay un duplicado

#vemos cual es ese duplicado
mask=df[["item_id"]].duplicated()
repetido=df[mask]["item_id"].values[0]

mask=df["item_id"]==repetido

temporal=df[mask].reset_index()

#una vez que tenemos los indices del duplicado vemos si los registros de todos los campos coinciden para luego ya eliminarlo 

i=0
for n in df.columns:
    if temporal[n].values[0]==temporal[n].values[0]:
        i+=1

print(i==df.shape[1])
# es tru significa que son completamente iguales

df.drop([df[mask].index[0]],inplace=True)

print("y ahora hay: "+str(df[["item_id"]].duplicated().sum()))

#print(df[["genres","price"]])
#print(df.isna().sum())
#exit()
#print(df.info())
#print(df.isna().sum())

df.to_csv(nombre,sep=";",index=False)