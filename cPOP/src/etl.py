from pandas import read_csv, merge
from cPOP.constants import PATH_TO_DATA, Columns

def read_data(path=PATH_TO_DATA):
    df = read_csv(path)
    df.dropna(inplace=True)

    # Convert all string/character columns to lower case
    df[df.select_dtypes(include='object').columns] = df.select_dtypes(include='object').apply(lambda x: x.str.lower())

    return df

def calc_stats(df, column=Columns.TAG_GROUP):
    # Calculate the total per tag
    df_tag = df.groupby(column)[Columns.COUNT].sum().reset_index()
    df_tag.columns = [column, Columns.TAG_COUNT]
    
    # Calculate fraction
    df[Columns.FRACTION] = df.apply(lambda row: row[Columns.COUNT] / row[Columns.YEAR_COUNT] if row[Columns.YEAR_COUNT] != 0 else 0, axis=1)
    
    return merge(df, df_tag, on=column, how='left')