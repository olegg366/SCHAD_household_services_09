
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, shapiro, pearsonr, ttest_ind, mannwhitneyu, chi2_contingency
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
def changerecl(x):
    if x <= 1:
        return 'мало'
    if x == 2:
        return 'средне'
    if x > 2:
        return 'много'
    
def changeage(x):
    if x <= 44:
        return 'молодой возраст'
    if 45 <= x <= 59:
        return 'средний возраст'
    if x >= 60:
        return 'пожилой возраст'
def standr_comf_rh(df):
    if 40 <= df['rh'] <= 60:
        return 'OK'
    else:
        return 'not OK'
def corrs(x1, x2):
    ty1 = type(x1[0])
    ty2 = type(x2[0])
    if ty1 == ty2:
        if ty1 == np.float64:
            pass
df = pd.read_csv('corrected_data.csv', delimiter=',') 
df['countmen'] = 1

df['реклам_категория'] = df['количество_рекламаций'].map(changerecl)
df['возрастная_категория'] = df['возраст'].map(changeage)

dfmeanage = df[['пол', 'страна', 'возраст']].groupby(['пол', 'страна']).mean().round().astype(int)

goodtemp = df.loc[df['предпочтительное_изменение_температуры'] == 'Без изменений']

dfcomftemp = goodtemp[['температура_воздуха_в_помещении', 'возрастная_категория']].groupby('возрастная_категория').mean()

df3 =  goodtemp[['страна', 'пол', 'countmen']].groupby(['страна', 'пол']).count()
df3.reset_index(inplace=True)
for i in range(len(df3)):
    df3['countmen'][i] = df3['countmen'][i] / len(df.loc[(df['страна'] == df3['страна'][i]) & (df['пол'] == df3['пол'][i])]) * 100
    
pivot = pd.pivot_table(df, index=['страна', 'пол', 'возрастная_категория'], values=['температура_воздуха_в_помещении', 'температура_воздуха_на_улице', 'rh'], 
                       aggfunc='mean')

df['стандр_комф_вл'] = df.apply(standr_comf_rh, axis=1)
cols = list(df.columns)
cols.remove('Unnamed: 0')
for i in cols:
    for j in cols[cols.index(i) + 1:]:
        nulli = df[i].isnull().any()
        nullj = df[j].isnull().any()
        if not nulli and not nullj:
            shapii = None
            shapij = None
            print(i, j)
            print()
            if type(df[i][0]) is np.float64:
                shapii = shapiro(df[i])[1]
            if type(df[j][0]) is np.float64:
                shapij = shapiro(df[j])[1]
            if (shapii is not None and shapij is None) or (shapii is None and shapij is not None):
                
                if shapii is not None:
                    le1 = le.fit_transform(df[j])
                    if shapii < 0.05:
                        
                        stu = ttest_ind(df[i], le1)
                        print(f'corr: {stu.statistic}')
                        print(f'pvalue: {stu.pvalue}')
                    else:
                        mann = mannwhitneyu(df[i], df[j])
                        print(f'corr: {mann.statistic}')
                        print(f'pvalue: {mann.pvalue}')
                        
                else:
                    le2 = le.fit_transform(df[i])
                    if shapij < 0.05:
                        stu = ttest_ind(le2, df[j])
                        print(f'corr: {stu.statistic}')
                        print(f'pvalue: {stu.pvalue}')
                    else:
                        mann = mannwhitneyu(df[i], df[j])
                        print(f'corr: {mann.statistic}')
                        print(f'pvalue: {mann.pvalue}')
                
                        
            if shapii is not None and shapij is not None:
                if shapii < 0.05 or shapij < 0.05:
                    pear = pearsonr(df[i], df[j])
                    print(f'corr: {pear.statistic}')
                    print(f'pvalue: {pear.pvalue}')
                else:
                    spear = spearmanr(df[i], df[j])
                    print(f'corr: {spear.statistic}')
                    print(f'pvalue: {spear.pvalue}')
            if shapii is None and shapij is None:
                crosschi = pd.crosstab(df[i], df[j])
                chi = chi2_contingency(crosschi)
                print(f'corr: {chi.statistic}')
                print(f'pvalue: {chi.pvalue}')
            print()
            print()            
                
    

df.to_csv('corrected_data_categor_byRost.csv')
