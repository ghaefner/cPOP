import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import PercentFormatter
import numpy as np
from cPOP.constants import Columns, PATH_TO_PLOT_FOLDER


def set_ax_parameters(ax, percent_formatting = True):
    # Set labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Fraction of Stackoverflow Searches (%)')
    ax.set_title('Popularity of Programming Languages Over the Years')

    # Format y-axis labels as percentage if true
    if percent_formatting:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
    
    # Add grid lines
    ax.grid(True)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

def plot_tag_group_fraction(df):
    # Filter out rows where tag_group is 'other'
    df_filtered = df[df[Columns.TAG_GROUP] != 'other']
    
    # Group by year and tag_group, and calculate the fraction
    grouped_df = df_filtered.groupby([Columns.YEAR, Columns.TAG_GROUP]).apply(lambda x: x[Columns.COUNT].sum() / x[Columns.YEAR_COUNT].iloc[0]).reset_index(name=Columns.FRACTION)

    fig, ax = plt.subplots(figsize=(10, 6))

    for tag_group, group_data in grouped_df.groupby(Columns.TAG_GROUP):
        plt.plot(group_data[Columns.YEAR], group_data[Columns.FRACTION], label=tag_group)
  
    # Set y-axis limits
    max_fraction = grouped_df[Columns.FRACTION].max()
    ax.set_ylim(ymin=0, ymax=1.05*max_fraction)
    set_ax_parameters(ax)

    return fig

def save_fig(fig, output_path="Output.png"):
    print(f"Saving plot to {PATH_TO_PLOT_FOLDER+output_path}.")
    # Save the plot as a .png file
    fig.savefig(PATH_TO_PLOT_FOLDER+output_path, bbox_inches='tight')


def update_timeseries_frame(frame, df):
    # Filter the DataFrame for the current frame
    data = df[df[Columns.YEAR] == frame]

    # Group the data by tag_group
    grouped_data = data.groupby(Columns.TAG_GROUP)

    # Plot a line for each tag_group
    for tag_group, group_data in grouped_data:
        plt.plot(group_data[Columns.YEAR], group_data[Columns.FRACTION], label=tag_group)

    # Set labels and title
    plt.xlabel('Year')
    plt.ylabel('Fraction of Stackoverflow Searches (%)')
    plt.title('Popularity of Programming Languages Over the Years')

    # Set y axis limits
    max_fraction = df[Columns.FRACTION].max()
    plt.ylim(0, 1.05 * max_fraction)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1.0))

    # Add grid lines
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def plot_tag_group_fraction_animated(df, output_path="output.gif"):
    # Filter out rows where tag_group is 'other'
    df_filtered = df[df[Columns.TAG_GROUP] != 'other']
    
    # Group by year and tag_group, and calculate the fraction
    grouped_df = df_filtered.groupby([Columns.YEAR, Columns.TAG_GROUP]).apply(lambda x: x[Columns.COUNT].sum() / x[Columns.YEAR_COUNT].iloc[0]).reset_index(name=Columns.FRACTION)
    
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the animation
    anim = FuncAnimation(fig, update_timeseries_frame, frames=sorted(df[Columns.YEAR].unique()), fargs=(grouped_df,), interval=1000)

    # Save the animation as a GIF
    anim.save(PATH_TO_PLOT_FOLDER + "/" + output_path, writer='imagemagick')
