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

def plot_tag_timeseries(df):
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
    df_frame = df[df[Columns.YEAR] == frame]
    fig = plot_tag_timeseries(df_frame)
    return fig


def plot_animation(df, output_path="animation.gif"):
   # Create a new figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define the animation function
    def animate(frame):
        ax.clear()  # Clear the previous frame
        
        # Filter the DataFrame for the current frame
        df_frame = df[df[Columns.YEAR] == frame]
        
        # Plot the data for the current frame using plot_tag_fraction
        plot_tag_timeseries(df_frame)
        
    # Create the animation
    anim = FuncAnimation(fig, animate, frames=sorted(df[Columns.YEAR].unique()), interval=1000)

    # Save the animation as a GIF
    anim.save(PATH_TO_PLOT_FOLDER+output_path, writer='pillow')


def plot_top_tag_groups(df, year):
    # Filter and sort dataframe
    df = df[(df[Columns.YEAR] == year) & (df[Columns.TAG_GROUP] != "other")].sort_values(by=Columns.FRACTION, ascending=True)

    # Take top 10 tag groups
    top_tag_groups = df.tail(10)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_tag_groups[Columns.TAG_GROUP], top_tag_groups[Columns.FRACTION], color='skyblue')
    ax.set_xlabel('% of Stackoverflow Searches')
    ax.set_ylabel('Programming Language')
    ax.set_title(f'Top 10 Programming Languages in {year}')
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:.1%}'.format(x)))

    return fig


def plot_top_animation(df):

    unique_years = df[Columns.YEAR].unique()

    fig, ax = plt.subplots(figsize=(10, 6))

    anim = FuncAnimation(fig, lambda year: plot_top_tag_groups(df, year), frames=unique_years, repeat=False)

    return anim