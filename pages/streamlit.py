import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

# Define data
data = {
    "Brand": ["Popular and leading", "Professional", "Ethical", "Aggressive", "Youthful", "Unbiased", 
              "Trustworthy/ Credible", "Sensational", "Faster Coverage", "Changes and improves its content regularly", 
              "Follow others", "For intellectuals and highly educated people", "Can go to any extent for popularity", 
              "Reference to the day to day happenings", "Respected", "Elegant / stylish", "Powerful", "Non-stop news coverage", 
              "Has content that interest me", "Has exclusive access to important news", "Covers a wide range of topics", 
              "Strong on-ground coverage of events", "Daring news provider", "Available on multi platforms", 
              "Has the best Anchors and Reporters", "Proper Business news coverage", "Proper International news coverage", 
              "Proper local news coverage", "Best talk shows/ expert interactions", "Asharq News", "Sky News Arabia", 
              "Al Arabiya", "Al Jazeera", "Al Hadath", "Al Ekhbariya"],
    "X": [0.043485448, 0.002824752, 0.02882878, -0.077079456, -0.01463746, 0.017547201, 0.019324806, 
          0.001640258, 0.005766812, -0.01816063, -0.06217503, -0.041475734, -0.01152244, 0.020396001, 
          0.007766971, -0.004771621, -0.015981693, -0.007533428, 0.005917426, -0.00234798, -0.000524319, 
          0.032717452, -0.012525849, 0.018573417, 0.007843185, -0.004782745, -0.011831706, 0.044249413, 
          -0.008862209, -0.030496258, -0.033258782, 0.036090406, -0.006843892, -0.001213519, 0.020823266],
    "Y": [-0.038398944, -0.02803502, 0.077439952, 0.024706829, 0.055153809, 0.070656277, 0.056437845, 
          -0.002586871, -0.048932821, 0.002810928, 0.072836851, 0.006542164, 0.00789216, 0.015991844, 
          0.056333237, 0.00821867, -0.031295357, -0.047902437, -0.009335493, -0.044064789, -0.041746791, 
          -0.062105616, -0.03518149, -0.02161096, -0.035776384, 0.003629166, -0.039581307, 0.082353699, 
          -0.016517444, 0.033964106, -0.000219319, -0.026489528, -0.058315008, -0.005541743, 0.07254126]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Streamlit App
st.set_page_config(layout="wide", page_title="Perceptual Map")

# Apply Streamlit settings for background color
st.markdown(
    """
    <style>
    .css-1lcbmhc {
        background-color: black;
    }
    .css-17eq0hr {
        background-color: black;
    }
    .css-12ttj6m {
        background-color: black;
    }
    .css-1h2cbd9 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Perceptual Map of News Channels")

# Channel Picker
news_channels = ["Asharq News", "Sky News Arabia", "Al Arabiya", "Al Jazeera", "Al Hadath", "Al Ekhbariya"]
channel = st.selectbox("Choose a channel to focus on:", news_channels)

# Highlight specific news channels and relevant topics
df['color'] = df['Brand'].apply(lambda x: 'red' if x == 'Asharq News' else ('blue' if x not in news_channels else 'green'))
df['size'] = df['Brand'].apply(lambda x: 12 if x in news_channels else 8)

# Create Perceptual Map
fig = px.scatter(df, x='X', y='Y', color='color', size='size', hover_data=['Brand'])

# Add large shadows around news channels and relevant topics
highlighted_areas = news_channels + ["Popular and leading", "Professional", "Ethical", "Aggressive", "Youthful"]
for area in highlighted_areas:
    area_data = df[df['Brand'] == area]
    fig.add_trace(go.Scatter(
        x=[area_data['X'].values[0]] * 20,
        y=[area_data['Y'].values[0]] * 20,
        mode='markers',
        marker=dict(
            size=[20 + i * 5 for i in range(20)],
            color='rgba(0, 255, 0, 0.1)' if area in news_channels else 'rgba(0, 0, 255, 0.1)',
            opacity=0.3
        ),
        showlegend=False
    ))

# Layout
fig.update_layout(
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False)
)

# Display the map
st.plotly_chart(fig, use_container_width=True)

# Calculate distances for insights
df['distance'] = ((df['X'] - df[df['Brand'] == channel]['X'].values[0])**2 + 
                  (df['Y'] - df[df['Brand'] == channel]['Y'].values[0])**2)**0.5

# Filter out other channels and get closest attributes
attributes = df[~df['Brand'].isin(news_channels)]
closest_attributes = attributes.sort_values(by='distance').head(10)

# Highlight the selected channel and its closest attributes
highlighted = pd.concat([closest_attributes, df[df['Brand'] == channel]])

for index, row in highlighted.iterrows():
    fig.add_trace(go.Scatter(
        x=[row['X']],
        y=[row['Y']],
        mode='markers+text',
        marker=dict(
            size=20,
            color='white',
            opacity=1
        ),
        text=[row['Brand']],
        textposition='top center',
        showlegend=False
    ))

# Draw ellipses around channels to include closest attributes
for news_channel in news_channels:
    channel_data = df[df['Brand'] == news_channel]
    closest = attributes[attributes['distance'] <= attributes[attributes['Brand'] == news_channel]['distance'].quantile(0.25)]
    closest = pd.concat([closest, channel_data])
    
    if news_channel == 'Asharq News':
        color = 'red'
    elif news_channel == 'Sky News Arabia':
        color = 'green'
    elif news_channel == 'Al Arabiya':
        color = 'blue'
    elif news_channel == 'Al Jazeera':
        color = 'yellow'
    elif news_channel == 'Al Hadath':
        color = 'orange'
    elif news_channel == 'Al Ekhbariya':
        color = 'purple'
    
    fig.add_trace(go.Scatter(
        x=np.append(closest['X'].values, closest['X'].values[0]),
        y=np.append(closest['Y'].values, closest['Y'].values[0]),
        mode='lines',
        line=dict(color=color, width=2, dash='dash'),
        fill='toself',
        fillcolor=f'rgba{tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}',
        showlegend=False
    ))

# Display the map with ellipses
st.plotly_chart(fig, use_container_width=True)

# Display data for the selected channel
st.write(f"Details for {channel}:")

st.write(f"{channel} is known for the following attributes:")
st.write(", ".join(closest_attributes['Brand'].tolist()))

# Display DataFrame for the selected channel
st.dataframe(df[df['Brand'] == channel])
