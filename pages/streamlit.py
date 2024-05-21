import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.spatial.distance import cdist
from scipy.spatial import ConvexHull
import numpy as np
from scipy.interpolate import splprep, splev

# Set page layout to wide
st.set_page_config(layout="wide")

# Data for the perceptual chart
data = {
    "Item": [0.043485448, 0.002824752, 0.02882878, -0.077079456, -0.01463746, 0.017547201,
             0.019324806, 0.001640258, -0.050469967, 0.005766812, -0.01816063, -0.06217503,
             -0.041475734, -0.01152244, 0.020396001, 0.007766971, -0.004771621, -0.015981693,
             -0.007533428, 0.005917426, -0.00234798, -0.000524319, 0.032717452, -0.012525849,
             0.018573417, 0.007843185, -0.004782745, -0.011831706, 0.044249413, -0.008862209,
             -0.030496258, -0.033258782, 0.036090406, -0.006843892, -0.001213519, 0.020823266],
    "Brand": [-0.038398944, -0.02803502, 0.077439952, 0.024706829, 0.055153809, 0.070656277,
              0.056437845, -0.002586871, 0.035968879, -0.048932821, 0.002810928, 0.072836851,
              0.006542164, 0.00789216, 0.015991844, 0.056333237, 0.00821867, -0.031295357,
              -0.047902437, -0.009335493, -0.044064789, -0.041746791, -0.062105616, -0.03518149,
              -0.02161096, -0.035776384, 0.003629166, -0.039581307, 0.082353699, -0.016517444,
              0.033964106, -0.000219319, -0.026489528, -0.058315008, -0.005541743, 0.07254126],
    "Colonne1": ["Popular and leading", "Professional", "Ethical", "Aggressive", "Youthful",
                 "Unbiased", "Trustworthy/ Credible", "Sensational", "Boring", "Faster Coverage",
                 "Changes and improves its content regularly", "Follow others",
                 "For intellectuals and highly educated people", "Can go to any extent for popularity",
                 "Reference to the day to day happenings", "Respected", "Elegant / stylish", "Powerful",
                 "Non-stop news coverage", "Has content that interest me", "Has exclusive access to important news",
                 "Covers a wide range of topics", "Strong on-ground coverage of events", "Daring news provider",
                 "Available on multi platforms", "Has the best Anchors and Reporters", "Proper Business news coverage",
                 "Proper International news coverage", "Proper local news coverage", "Best talk shows/ expert interactions",
                 "Asharq News", "Sky News Arabia", "Al Arabiya", "Al Jazeera", "Al Hadath", "Al Ekhbariya"]
}

df = pd.DataFrame(data)

# Define colors for each channel
colors = {
    "Asharq News": "red",
    "Sky News Arabia": "orange",
    "Al Arabiya": "blue",
    "Al Jazeera": "yellow",
    "Al Hadath": "purple",
    "Al Ekhbariya": "green"
}

# Assign colors to the dataframe
df['color'] = df['Colonne1'].map(colors).fillna('black')

# Function to find the closest topics
def find_closest_topics(channel_name, df, min_topics=10):
    channel_point = df[df['Colonne1'] == channel_name][['Item', 'Brand']].values
    other_points = df[df['Colonne1'] != channel_name][['Item', 'Brand']]
    distances = cdist(channel_point, other_points)[0]
    
    closest_indices = np.argsort(distances)[:min_topics].tolist()
    min_distance = distances[closest_indices[-1]]
    additional_indices = np.where(distances == min_distance)[0]
    
    closest_indices.extend(additional_indices.tolist())
    closest_indices = list(set(closest_indices))[:min_topics]

    closest_topics = df.iloc[closest_indices]
    return closest_topics

# Function to generate a smoothed shape
def smooth_shape(points, resolution=100):
    points = np.array(points)
    t = np.linspace(0, 1, len(points))
    tck, u = splprep([points[:, 0], points[:, 1]], s=0, per=True)
    x_new, y_new = splev(np.linspace(0, 1, resolution), tck)
    return x_new, y_new

# Channel picker
selected_channel = st.selectbox("Select a channel to view details", options=colors.keys())

# Plotting the perceptual chart using Plotly
fig = px.scatter(
    df,
    x='Item',
    y='Brand',
    text='Colonne1',
    color='Colonne1',
    color_discrete_map=colors,
    title=f'Perceptual Chart for {selected_channel}',
    labels={'Item': 'Item', 'Brand': 'Brand'}
)

# Highlight the selected channel
fig.update_traces(marker=dict(size=12, opacity=0.8, color='black'), textposition='top center')
fig.add_scatter(
    x=df[df['Colonne1'] == selected_channel]['Item'],
    y=df[df['Colonne1'] == selected_channel]['Brand'],
    mode='markers+text',
    marker=dict(size=15, color=colors[selected_channel], symbol='star', line=dict(width=2, color='black')),
    text=df[df['Colonne1'] == selected_channel]['Colonne1'],
    textposition='top center',
    showlegend=False
)

# Show only the six channels in the legend
fig.for_each_trace(lambda trace: trace.update(showlegend=True) if trace.name in colors.keys() else trace.update(showlegend=False))

# Add smooth shape connecting the selected channel to its closest topics
closest_topics = find_closest_topics(selected_channel, df)
points = pd.concat([df[df['Colonne1'] == selected_channel], closest_topics])[['Item', 'Brand']].values
hull = ConvexHull(points)
hull_points = points[hull.vertices]
hull_points = np.vstack([hull_points, hull_points[0]])  # Close the polygon

# Calculate smooth shape points
x_vals, y_vals = smooth_shape(hull_points)

fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    fill='toself',
    fillcolor=colors[selected_channel],
    opacity=0.1,
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False
))

fig.update_layout(
    width=1200,
    height=800,
    title=dict(x=0.5),
    font=dict(size=14),
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

st.plotly_chart(fig)

# Display insights for the selected channel
st.subheader(f"Insights for {selected_channel}")
st.markdown(f"**{selected_channel}** tends to be known for:")
st.write(", ".join(closest_topics['Colonne1'].values))

# Run the app with: streamlit run perceptual_chart.py
