import streamlit as st
import datetime

col1, col2 = st.columns(2)

with col1:
    data = st.date_input("Data", value=datetime.date.today())
    
with col2:
    st.write("Data formatada:")
    st.write(data.strftime("%d/%m/%Y"))
