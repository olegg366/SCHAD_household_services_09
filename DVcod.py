import pandas as pd
df = pd.read_csv('Отредактированные данные.csv', encoding='utf-8', sep=';', skipinitialspace=True)

def check_data(data_df):
    print('\033[1m' + 'Изучим исходные данные' + '\033[0m')
    print(data_df.info())
    print(data_df.shape) #(строки, столбцы)

    missed_cells = data_df.isnull().sum().sum() / (data_df.shape[0] * (data_df.shape[1] - 1)) #ячейки
    missed_rows = sum(data_df.isnull().sum(axis = 1) > 0) / data_df.shape[0]
    print('\033[1m' + '\nПроверка пропусков' + '\033[0m')
    print('Количество пропусков: {:.0f}'.format(data_df.isnull().sum().sum()))
    print('Доля пропусков: {:.1%}'.format(missed_cells) + '\033[0m')
    print("Доля строк, содержащих пропуски: {:.1%}".format(missed_rows))

    #Проверка дубликатов
    print('\033[1m' + '\nПроверка на дубликаты' + '\033[0m')
    print('Количество полных дубликатов: ', data_df.duplicated().sum())

    print('\033[1m' + '\nОписание количественных строк' + '\033[0m')
    print(data_df.describe().T)

    print('\033[1m' + '\nОписание категориальных строк' + '\033[0m')
    print(data_df.describe(include='object').T)

    print('\033[1m' + '\nВывод уникальных значений по каждому категориальному признаку' + '\033[0m')
    df_object = data_df.select_dtypes(include='object').columns

    for i in df_object:
        print('\033[1m' + '_' + str(i) + '\033[0m')
        print(data_df[i].value_counts())

df['режим_при_смешанном_типе_охлаждения'] = df['режим_при_смешанном_типе_охлаждения'].fillna('нет')
df['способ_обогрева'] = df['способ_обогрева'].fillna('нет')

#gr1 = df.groupby(['климат'])['возраст']
#for key, item in gr1:
 #   print(key)
 #   print(gr1.get_group(key).value_counts(), "\n\n")

gr2 = df.groupby([['климат'],['способ_охлаждения'],['способ_обогрева']])['оценка_комфорта']
md = gr2.median()

#check_data(df)
