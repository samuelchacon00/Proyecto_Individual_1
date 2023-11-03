import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data_dir="datasets/"

games=pd.read_csv(data_dir+"steam_games.csv",sep=";")
reviews=pd.read_csv(data_dir+"user_reviews.csv",sep=";")
items=pd.read_parquet(data_dir+"users_items.parquet")

#print(games.describe(include="all"))

plt.subplot(1, 2, 1)  # Primera visualización
sns.boxplot(x='price', data=games)

plt.subplot(1, 2, 2)  # Segunda visualización
sns.violinplot(x='price', data=games, inner='quartile')

plt.tight_layout() 

plt.show()