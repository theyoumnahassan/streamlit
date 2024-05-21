import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Data preparation
data = {
    "Horizontal axis data": [0.043485448, 0.002824752, 0.02882878, -0.077079456, -0.01463746, 0.017547201, 0.019324806, 0.001640258, 0.005766812, -0.01816063, -0.06217503, -0.041475734, -0.01152244, 0.020396001, 0.007766971, -0.004771621, -0.015981693, -0.007533428, 0.005917426, -0.00234798, -0.000524319, 0.032717452, -0.012525849, 0.018573417, 0.007843185, -0.004782745, -0.011831706, 0.044249413, -0.008862209, -0.030496258, -0.033258782, 0.036090406, -0.006843892, -0.001213519, 0.020823266],
    "Vertical axis data": [-0.038398944, -0.02803502, 0.077439952, 0.024706829, 0.055153809, 0.070656277, 0.056437845, -0.002586871, -0.048932821, 0.002810928, 0.072836851, 0.006542164, 0.00789216, 0.015991844, 0.056333237, 0.00821867, -0.031295357, -0.047902437, -0.009335493, -0.044064789, -0.041746791, -0.062105616, -0.03518149, -0.02161096, -0.035776384, 0.003629166, -0.039581307, 0.082353699, -0.016517444, 0.033964106, -0.000219319, -0.026489528, -0.058315008, -0.005541743, 0.07254126],
    "Brand": ["Popular and leading", "Professional", "Ethical", "Aggressive", "Youthful", "Unbiased", "Trustworthy/ Credible", "Sensational", "Faster Coverage", "Changes and improves its content regularly", "Follow others", "For intellectuals and highly educated people", "Can go to any extent for popularity", "Reference to the day to day happenings", "Respected", "Elegant / stylish", "Powerful", "Non-stop news coverage", "Has content that interest me", "Has exclusive access to important news", "Covers a wide range of topics", "Strong on-ground coverage of events", "Daring news provider", "Available on multi platforms", "Has the best Anchors and Reporters", "Proper Business news coverage", "Proper International news coverage", "Proper local news coverage", "Best talk shows/ expert interactions", "Asharq News", "Sky News Arabia", "Al Arabiya", "Al Jazeera", "Al Hadath", "Al Ekhbariya"],
}

df = pd.DataFrame(data)

# Streamlit app
st.title('Positioning Map')

# Plotting
fig, ax = plt.subplots()
scatter = ax.scatter(df['Horizontal axis data'], df['Vertical axis data'])

# Annotate each point with the brand name
for i, txt in enumerate(df['Brand']):
    ax.annotate(txt, (df['Horizontal axis data'][i], df['Vertical axis data'][i]))

plt.xlabel('Horizontal axis')
plt.ylabel('Vertical axis')
plt.title('Brand Positioning Map')

st.pyplot(fig)
