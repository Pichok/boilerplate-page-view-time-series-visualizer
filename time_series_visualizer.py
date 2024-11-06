#%%
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from matplotlib.ticker import FuncFormatter

#%%
# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')

df['date'] = pd.to_datetime(
    df['date'],
    format='%Y-%m-%d', 
    errors='coerce'
)

df = df[
    (df['value'] <= df['value'].quantile(0.975)) &
    (df['value'] >= df['value'].quantile(0.025)) 
]

#%%
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(df['date'],df['value'],color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
   
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

#%%
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    dff_bar = df
    dff_bar['month'] = dff_bar['date'].dt.strftime('%B')
    dff_bar['year'] = dff_bar['date'].dt.strftime('%Y').astype(int)

    def thousands_formatter(x, pos):
        return f'{int(x / 1000)}K' if x >= 1000 else str(int(x))

    order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    plt.figure(figsize=(10,5))
    sns.barplot(
        x='year',
        y='value',
        hue='month',
        data=dff_bar,
        errorbar=None,
        hue_order=order
    )

    plt.title('Daily freeCodeCamp Forum Average Page Views 5/2016-12/2019')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months',frameon=False,ncol=6)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    #plt.xticks(rotation=45)
    plt.tight_layout() 

    # Save image and return fig (don't change this part)
    plt.savefig('bar_plot.png')
    return plt

#%%
def thousands_formatter(x, pos):
    return f'{int(x / 1000)}K' if x >= 1000 else str(int(x))

#%%
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2, figsize=(24,8))

    ax1 = sns.boxplot(
        y='value', 
        x='year', 
        data=df_box, 
        orient='v', 
        ax=axes[0],
        palette="hls"
    )
    ax1.set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax2 = sns.boxplot(
        y='value', 
        x='month', 
        data=df_box, 
        orient='v', 
        ax=axes[1],
        palette="hls",
        order=order
    )
    ax2.set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    for ax in axes.flat:
        ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

# %%
draw_box_plot()
# %%
