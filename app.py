import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ==========================
# LOAD FILES
# ==========================
model = pickle.load(open("model.pkl", "rb"))
companies = pickle.load(open("company.pkl", "rb"))
car_dict = pickle.load(open("name.pkl", "rb"))
cars = pd.read_csv("quikr_car.csv")

# ==========================
# CUSTOM CSS
# ==========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}



/* Title */
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: 800;
    color: white;
    margin-top: 10px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 25px;
}

/* Cards */
.card {
    background: #1e293b;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #334155;
}

.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #334155;
}

.metric-card h2 {
    color: #22c55e;
}

.metric-card h3 {
    color: white;
}

/* Prediction Box */
.prediction-box {
    background: linear-gradient(
        135deg,
        #16a34a,
        #15803d
    );
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 40px;
    font-weight: bold;
    margin-top: 20px;
}

/* Labels */
label {
    color: white !important;
    font-weight: 600 !important;
}

/* Input text */
.stNumberInput input,
.stTextInput input {
    color: white !important;
    background-color: #334155 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #1e293b !important;
    border-radius: 15px;
    border: 1px solid #475569;
    padding: 6px;
    color: white !important;
    transition: all 0.3s ease;
}

.stSelectbox div[data-baseweb="select"]:hover {
    border: 1px solid #3b82f6;
    box-shadow: 0 0 15px rgba(59,130,246,0.4);
}

/* Button */
.stButton button {
    padding: 15px;
    border-radius: 200px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
    color: white;
    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );
}

}

</style>
""", unsafe_allow_html=True)

#main  display part

st.markdown(
    "<h1 class='main-title'>🚗 Car Price Predictor</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>AI Powered Used Car Price Estimation</p>",
    unsafe_allow_html=True
)

st.markdown("---")


left, right = st.columns([2,1])

with left:


    company = st.selectbox(
        "🏢 Select Company",
        sorted(companies)
    )

    car_name = st.selectbox(
        "🚘 Select Car Model",
        sorted(car_dict[company])
    )

    fuel_type = st.selectbox(
        "⛽ Fuel Type",
        sorted(cars["fuel_type"].dropna().unique())
    )

    purchase_year = st.slider(
        "📅 Purchase Year",
        min_value=1990,
        max_value=datetime.now().year,
        value=2016
    )

    kms_driven = st.number_input(
        "🛣️ Kilometers Driven",
        min_value=0,
        value=50000,
        step=100
    )



age = datetime.now().year - purchase_year

with right:

    st.markdown(
        f"""
        <div class='metric-card'>
            <h3>🚘 Car Age</h3>
            <h2>{age} Years</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='metric-card'>
            <h3>🛣️ Distance Travelled</h3>
            <h2>{kms_driven:,} km</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("💰 Predict Car Price"):

    input_df = pd.DataFrame({
        "name": [car_name],
        "company": [company],
        "age": [age],
        "kms_driven": [kms_driven],
        "fuel_type": [fuel_type]
    })


    prediction = float(model.predict(input_df)[0])

    st.markdown(
            f"""
            <div class='prediction-box'>
                Estimated Market Value<br><br>
                ₹ {prediction:,.0f}
            </div>
            """,
            unsafe_allow_html=True
    )




st.markdown("---")
st.markdown(
    "<center style='color:#94a3b8'>Built with ❤️ using Streamlit & Scikit-Learn</center>",
    unsafe_allow_html=True
)