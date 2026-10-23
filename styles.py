import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    .stApp {
        background: radial-gradient(ellipse at 80% 0%, #24163a 0%, #0b0a12 48%);
        color: #f7f4ff;
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.035em;
    }

    [data-testid="stSidebar"] {
        background: #100e19;
        border-right: 1px solid #2b243a;
    }

    /* Hide default automatic Streamlit multi-page list */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1c182a, #13111d);
        padding: 18px;
        border: 1px solid #302842;
        border-radius: 18px;
    }

    div[data-testid="stMetricLabel"] {
        color: #aaa4bc;
    }

    div[data-testid="stMetricValue"] {
        color: #f7f4ff;
        font-family: 'Space Grotesk', sans-serif;
    }

    .stButton > button {
        border-radius: 12px;
        border: 1px solid #45365e;
        background: linear-gradient(135deg, #9b7cf5, #7653d6);
        color: white;
        font-weight: 650;
        min-height: 42px;
    }

    .stButton > button:hover {
        border-color: #d9c9ff;
        color: white;
        box-shadow: 0 0 22px #9b7cf533;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: #171421 !important;
        color: white !important;
        border: 1px solid #393047 !important;
        border-radius: 12px !important;
    }

    .fp-card {
        background: linear-gradient(145deg, #201b2f, #13111d);
        border: 1px solid #332a45;
        border-radius: 20px;
        padding: 20px 22px;
        margin-bottom: 12px;
    }

    .fp-eyebrow {
        color: #b9a7f9;
        text-transform: uppercase;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
    }

    .fp-muted {
        color: #aaa4bc;
        font-size: 0.92rem;
    }

    .fp-big {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
    }

    hr {
        border-color: #302842;
    }
    </style>
    """, unsafe_allow_html=True)
