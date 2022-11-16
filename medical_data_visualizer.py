import seaborn as sb
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


df = pd.read_csv('medical_examination.csv')

BMI_cal = df['weight'] / (df['height'] / 100) ** 2
BMI_condition = [(BMI_cal >25),(BMI_cal <=25)]
BMI_value = [0,1]
df['overweight'] = np.select(BMI_condition,BMI_value)

df['cholesterol'] = np.where(df['cholesterol'] == 1,0,1)
df['gluc'] = np.where(df['gluc'] == 1,0,1)

def cat_plot():
    df_plot = df.melt(id_vars='cardio',value_vars=['active','alco','cholesterol','gluc','overweight','smoke'])
    df_plot = df_plot.groupby(['cardio', 'variable', 'value']).size().reset_index()
    df_plot = df_plot.rename(columns={0 : 'total'})
    
    plot_graph = sb.catplot(data=df_plot,x='variable',y='total',hue='value',col='cardio',kind='bar')
    fig = plot_graph.fig
    fig.savefig('catplot.png')
    return fig

def heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
        ]
    
    corr_data = df_heat.corr()
    mask = np.triu(np.ones_like(corr_data, dtype=bool))
    fig , ax = plt.subplots(figsize=(16,9))
    sb.heatmap(corr_data, mask=mask, square=True, annot=True,fmt='.1f', linewidths=0.5)
    fig.savefig('heatmap.png')
    return fig

