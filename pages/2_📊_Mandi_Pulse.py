import streamlit as st
import pandas as pd
from utils.i18n_helper import t

st.title(f"📊 {t('mandi_pulse_header')}")
st.write(t('mandi_pulse_sub'))
st.write("---")

st.subheader("🌾 Live Market Commodity Prices (Telangana)")
data = {
    "Commodity": ["Paddy (Rice)", "Cotton", "Maize", "Chilli", "Turmeric"],
    "Mandi Price (per Quintal)": ["₹2,320", "₹7,100", "₹2,150", "₹18,500", "₹13,200"],
    "Daily Status": ["📈 +₹20", "📉 -₹50", "📈 +₹10", "📈 +₹300", "📉 -₹120"]
}
df = pd.DataFrame(data)
st.table(df)

st.info("💡 Real-time regional APMC market data integration via open government APIs goes here.")