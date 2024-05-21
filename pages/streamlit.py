import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

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

# Title
st.title("Perceptual Map of News Channels")

# Channel Picker
channel = st.selectbox("Choose a channel to focus on:", df["Brand"])

# Highlight specific news channels
news_channels = ["Asharq News", "Sky News Arabia", "Al Arabiya", "Al Jazeera", "Al Hadath", "Al Ekhbariya"]
df['color'] = df['Brand'].apply(lambda x: 'green' if x in news_channels else 'blue')
df['size'] = df['Brand'].apply(lambda x: 12 if x in news_channels else 8)

# Create Perceptual Map
fig = px.scatter(df, x='X', y='Y', color='color', size='size', hover_data=['Brand'])

# Add shadows around news channels
for channel in news_channels:
    channel_data = df[df['Brand'] == channel]
    fig.add_trace(go.Scatter(
        x=[channel_data['X'].values[0]] * 10,
        y=[channel_data['Y'].values[0]] * 10,
        mode='markers',
        marker=dict(
            size=[10 + i for i in range(10)],
            color='rgba(0, 255, 0, 0.1)',
            opacity=0.4
        ),
        showlegend=False
    ))

# Add labels for highlighted focus areas
focus_areas = ['Popular and leading', 'Professional', 'Ethical', 'Aggressive', 'Youthful']
for area in focus_areas:
    fig.add_trace(go.Scatter(
        x=df[df['Brand'] == area]['X'], 
        y=df[df['Brand'] == area]['Y'], 
        text=area, 
        mode='markers+text', 
        textposition='top center'
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

# Display data for the selected channel
st.write(f"Details for {channel}:")
st.dataframe(df[df['Brand'] == channel])
