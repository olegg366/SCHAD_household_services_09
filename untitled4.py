import pandas as pd
def change(x):
    if x <= 1:
        return 'мало'
    if x == 2:
        return 'средне'
    if x > 2:
        return 'много'
df = pd.read_csv('data.csv', delimiter=';') 
df['reclam_cat'] = df['количество_рекламаций'].map(change)