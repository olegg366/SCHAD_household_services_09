import pandas as pd
df = pd.read_csv('corrected_data.csv', encoding='utf-8', sep=',', skipinitialspace=True)

df["возраст"] = df['возраст'].astype(int)
gb1 = df.groupby(['возраст'])['рост']
df['рост'] = df['рост'].replace('5.23', '')
df['рост'] = df['рост'].replace('5.74', '')
for key, item in gb1:
    key_mean = gb1.get_group(key).mean()
    df["рост"] = df["рост"].fillna(key_mean)

    print(key)
    print("Количество пропусков: ",gb1.get_group(key).isnull().sum().sum())
    print(gb1.get_group(key).value_counts(),'\n\n')

gb2 = df.groupby(['возраст'])['вес']
for key, item in gb2:
    key_mean = gb2.get_group(key).mean()
    df["вес"] = df["вес"].fillna(key_mean)

    print(key)
    print("Количество пропусков: ",gb2.get_group(key).isnull().sum().sum())
    print(gb2.get_group(key).value_counts(),'\n\n')


df['ощущение_движения_воздуха_(bool)'] = pd.array(df['ощущение_движения_воздуха_(bool)'], dtype=pd.Int64Dtype())
df['занавески'] = pd.array(df['занавески'], dtype=pd.Int64Dtype())
df['вентилятор'] = pd.array(df['вентилятор'], dtype=pd.Int64Dtype())
df['окно'] = pd.array(df['окно'], dtype=pd.Int64Dtype())
df['двери'] = pd.array(df['двери'], dtype=pd.Int64Dtype())
df['отопление'] = pd.array(df['отопление'], dtype=pd.Int64Dtype())
