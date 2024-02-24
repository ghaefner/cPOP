from cPOP.src.etl import read_data, calc_stats
from cPOP.src.tags import make_tag_groups
from cPOP.src.db import write_db

print("Read data.")
df = read_data()

print("Make tag groups.")
df = make_tag_groups(df)

print("Calc stats.")
df = calc_stats(df)


write_db(df)