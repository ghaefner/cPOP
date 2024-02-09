import matplotlib.pyplot as plt
from cPOP.constants import Columns, PATH_TO_PLOT_FOLDER

def plot_tag_group_fraction(df, output_path="output.png"):
    # Filter out rows where tag_group is 'other'
    df_filtered = df[df[Columns.TAG_GROUP] != 'other']
    
    # Group by year and tag_group, and calculate the fraction
    grouped_df = df_filtered.groupby([Columns.YEAR, Columns.TAG_GROUP]).apply(lambda x: x[Columns.COUNT].sum() / x[Columns.YEAR_COUNT].iloc[0]).reset_index(name=Columns.FRACTION)

    
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    for tag_group, group_data in grouped_df.groupby(Columns.TAG_GROUP):
        plt.plot(group_data[Columns.YEAR], group_data[Columns.FRACTION], label=tag_group)

    # Set labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Fraction of Stackoverflow Searches (%)')
    ax.set_title('Popularity of Programming Languages Over the Years')

    # Set y axis limits
    max_fraction = grouped_df['fraction'].max()
    ax.set_ylim(0, 1.1 * max_fraction)

    # Format y-axis labels as percentage
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))

    # Add grid lines
    ax.grid(True)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Save the plot as a .png file
    plt.savefig(PATH_TO_PLOT_FOLDER+"/"+output_path, bbox_inches='tight')