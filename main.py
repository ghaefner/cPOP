from cPOP.src.etl import read_data, calc_stats
from cPOP.src.tags import make_tag_groups
from cPOP.src.plot import plot_animation, save_fig, plot_tag_fraction
from cPOP.constants import Columns
from cPOP.src.db import write_db

print("Read data.")
df = read_data()
print("Make tag groups.")
df = make_tag_groups(df)
print("Calc stats.")
df = calc_stats(df)
print("Plot.")
#plot_tag_group_fraction_animated(df,output_path="Output_Animation.gif")
#save_fig(fig=plot_tag_fraction(df))
#plot_animation(df,output_path="Output_Animation.gif")

write_db(df)