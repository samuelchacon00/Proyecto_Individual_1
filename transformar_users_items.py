import pandas as pd

nombre="datasets/users_items.parquet"
df=pd.read_parquet(nombre)

# no hay nuloes
#print(df.isna().sum())

# no hay duplicados
#print(df.duplicated().sum())

columnas_indeseadas=["playtime_2weeks","items_count"]
df.drop(columns=columnas_indeseadas,inplace=True)

df = df.rename(columns={'old_name': 'new_name'})

df.to_parquet(nombre,index=False)