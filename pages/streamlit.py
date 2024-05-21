import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data
data = {
    'Topic': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3],
    'Attribute': [
        'Respected news provider', 'Has exclusive access to important news', 'Has contents that interest me', 
        'Strong on-ground coverage of events', 'Powerful', 'Available on multi-platforms', 
        'Proper International Coverage', 'Covers a wide range of topics', 'Non-stop News Coverage', 
        'Has Best Anchors & Reporters', 'Daring news provider', 'Has proper local news coverage', 
        'Elegant / Stylish new provider', 'Proper Business News Coverage', 'Has Best talk shows / expert interactions', 
        'Ethical', 'Trustworthy/ Credible', 'Unbiased news provider', 'Professional', 'Faster Coverage', 
        'Sensational news provider', 'Popular & leading news provider', 'Changes & Improves Content Regularly', 
        'Reference for day today happenings', 'Youthful', 'For Intellectuals and highly Educated', 
        'Can go any extent for popularity', 'Aggressive', 'Boring', 'Follow others'
    ],
    'Asharq News': [1, 0, 0, -0.7568, -1.5135, 0.7027, 0, 0.7027, -1.3514, 0.6757, 0, 0.6486, 0.6216, 1.1892, 0.5946, 
                    0.9459, -1.7297, 2.3514, -0.7838, 0, -0.5946, -1.7027, 0, -0.4865, -0.2162, 0.5676, -0.1622, -0.0541, 0, 0],
    'Skynews Arabia': [2, -1.5676, 2.3514, -1.5135, -1.5135, -0.7027, 0.7027, 0.7027, 1.3514, -1.3514, -0.6757, -1.2973, 
                       1.2432, -0.5946, 1.1892, -3.7838, 1.7297, 3.9189, -0.7838, 0, 1.1892, 0, -0.5405, -1.4595, 1.2973, 
                       0.1892, 0, -0.1081, 0, 0],
    'Alarabiya': [0, 0.7838, 0.7838, 1.5135, -0.7568, 0.7027, 2.1081, -0.7027, 2.0270, -2.0270, 0, -1.2973, -1.2432, 0.5946, 
                  1.7838, -0.9459, 0, 2.3514, 0.7838, -1.3514, 2.3784, 1.7027, 0.5405, 1.9459, -0.4324, -0.9459, -0.3243, -0.0541, 0, 0],
    'Aljazeera': [-1, -0.7838, 0, 2.2703, 2.2703, 0, 0, 2.1081, -0.6757, 3.3784, 1.3514, -0.6486, -1.8649, -0.5946, 0.5946, 
                  -4.7297, -0.8649, -4.7027, 2.3514, 1.3514, 0, 1.7027, 0.5405, 2.4324, -0.2162, 0, -0.3243, 0, 0, 0],
    'Alhadath': [-4, 3.1351, -3.1351, 1.5135, 3.0270, 1.4054, 1.4054, 0.7027, -2.0270, 2.0270, 0.6757, -1.9459, -0.6216, 
                 1.1892, -1.1892, 3.7838, -0.8649, -2.3514, -2.3514, 2.0270, -1.1892, 0, -1.0811, -1.4595, -0.2162, -0.1892, 
                 0.8108, 0.1081, 0, 0],
    'Alekhbariya': [-3, -1.5676, 0.7838, -1.5135, -0.7568, -2.1081, -2.8108, -2.1081, -1.3514, -1.3514, -0.6757, 4.5405, 
                    1.8649, -1.1892, -2.3784, 5.6757, 1.7297, -0.7838, 0, -2.0270, -2.3784, -1.7027, 0.5405, -0.4865, 0, 
                    0.3784, 0, 0.1081, 0, 0]
}

df = pd.DataFrame(data)

# Streamlit app
st.set_page_config(page_title="Perceptual Map", page_icon=":bar_chart:", layout="wide", theme="dark")

st.title("Perceptual Map of News Channels")

# Date picker
st.date_input("Select a date:")

# Topic selector
topics = df['Topic'].unique()
selected_topic = st.selectbox("Select a Topic:", topics)

# Filter data based on selected topic
filtered_df = df[df['Topic'] == selected_topic]

# Perceptual Map
fig = px.scatter(filtered_df, x="Attribute", y="Asharq News", color=filtered_df['Topic'].apply(lambda x: "red" if x == 1 else "green" if x == 2 else "blue"), 
                 hover_data=['Skynews Arabia', 'Alarabiya', 'Aljazeera', 'Alhadath', 'Alekhbariya'], 
                 title="Perceptual Map", labels={"x": "Attributes", "y": "Importance"})

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Attributes",
    yaxis_title="Normalized Importance"
)

st.plotly_chart(fig, use_container_width=True)
