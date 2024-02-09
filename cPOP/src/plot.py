import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from cPOP.constants import Columns, PATH_TO_PLOT_FOLDER

def set_ax_parameters(ax, percent_formatting = True):
    # Set labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Fraction of Stackoverflow Searches (%)')
    ax.set_title('Popularity of Programming Languages Over the Years')

    # Set y axis limits
    ax.set_ylim(0, 1.1)

    # Format y-axis labels as percentage if true
    if percent_formatting:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1%}'))
    
    # Add grid lines
    ax.grid(True)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))


def plot_tag_group_fraction(df, output_path="output.png"):
    # Filter out rows where tag_group is 'other'
    df_filtered = df[df[Columns.TAG_GROUP] != 'other']
    
    # Group by year and tag_group, and calculate the fraction
    grouped_df = df_filtered.groupby([Columns.YEAR, Columns.TAG_GROUP]).apply(lambda x: x[Columns.COUNT].sum() / x[Columns.YEAR_COUNT].iloc[0]).reset_index(name=Columns.FRACTION)
    
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    for tag_group, group_data in grouped_df.groupby(Columns.TAG_GROUP):
        plt.plot(group_data[Columns.YEAR], group_data[Columns.FRACTION], label=tag_group)

     # Set y axis limits
    max_fraction = grouped_df['fraction'].max()
    ax.set_ylim(0, 1.1 * max_fraction)

    set_ax_parameters(ax=ax, percent_formatting=True)

    # Save the plot as a .png file
    plt.savefig(PATH_TO_PLOT_FOLDER+"/"+output_path, bbox_inches='tight')


def plot_animation(df, output_path):
    # Filter out rows where tag_group is 'other'
    df_filtered = df[df[Columns.TAG_GROUP] != 'other']
    
    # Group by year and tag_group, and calculate the fraction
    grouped_df = df_filtered.groupby([Columns.YEAR, Columns.TAG_GROUP]).apply(lambda x: x[Columns.COUNT].sum() / x[Columns.YEAR_COUNT].iloc[0]).reset_index(name=Columns.FRACTION)
    
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_title(f'Programming Language Popularity Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage')
    ax.set_ylim(0, 1.1)
    ax.grid(True)

    # Create an empty dictionary to store line objects for each tag_group
    lines = {}

    def update(frame):
        # Filter data for the current frame (year)
        df_frame = grouped_df[grouped_df[Columns.YEAR] <= frame]
        
        # Clear the previous plot
        ax.clear()

        # Plot the data for each tag_group
        for tag_group, data in df_frame.groupby(Columns.TAG_GROUP):
            if tag_group not in lines:
                # If line does not exist for tag_group, create a new line and store it in the dictionary
                lines[tag_group], = ax.plot(data[Columns.YEAR], data[Columns.FRACTION], label=tag_group)
            else:
                # If line already exists, update the data
                lines[tag_group].set_data(data[Columns.YEAR], data[Columns.FRACTION])

        # Add legend
        ax.legend()

    # Create the animation
    anim = FuncAnimation(fig, update, frames=sorted(df[Columns.YEAR].unique()), interval=1000, repeat=False)

    # Save the animation as a GIF
    anim.save(PATH_TO_PLOT_FOLDER+"/"+output_path, writer='imagemagick')


def plot_tag_group_fraction_animated(df, output_path="output.gif"):
    # Filter out rows where tag_group is 'other'
    df_filtered = df[df[Columns.TAG_GROUP] != 'other']
    
    # Group by year and tag_group, and calculate the fraction
    grouped_df = df_filtered.groupby([Columns.YEAR, Columns.TAG_GROUP]).apply(lambda x: x[Columns.COUNT].sum() / x[Columns.YEAR_COUNT].iloc[0]).reset_index(name=Columns.FRACTION)
    
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    lines = []

    # Set y axis limits
    max_fraction = grouped_df[Columns.FRACTION].max()
    ax.set_ylim(0, 0.3)

    set_ax_parameters(ax=ax, percent_formatting=True)

    def update(frame):
        ax.clear()
        for tag_group, group_data in grouped_df.groupby(Columns.TAG_GROUP):
            data = group_data[group_data[Columns.YEAR] <= frame]
            line, = plt.plot(data[Columns.YEAR], data[Columns.FRACTION], label=tag_group)
            lines.append(line)
        
        

    # Create the animation
    anim = FuncAnimation(fig, update, frames=sorted(df[Columns.YEAR].unique()), interval=1000, repeat=False)

    # Save the animation as a GIF
    anim.save(PATH_TO_PLOT_FOLDER+"/"+output_path, writer='imagemagick')
