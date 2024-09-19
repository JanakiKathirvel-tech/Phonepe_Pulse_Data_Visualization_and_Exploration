import streamlit as st
from streamlit_option_menu import option_menu

# Streamlit part
st.set_page_config( layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select = option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    pass

elif select == "DATA EXPLORATION":
    tab1,tab2,tab3 =st.tabs(["Aggregated analysis","Map analysis","Top analysis"])

    with tab1:
        agg_method =st.radio("Select the method", ["Insurance Analysis","Transaction Analysis","User Analysis"])
        if agg_method == "Insurance Analysis":
            pass
        elif agg_method == "Transaction Analysis":
            pass
        elif agg_method == "User Analysis":
            pass

    with tab2:
        map_method =st.radio("Select the method", ["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])
        if map_method == "Map Insurance Analysis":
            pass
        elif map_method == "Map Transaction Analysis":
            pass
        elif map_method == "Map User Analysis":
            pass

    with tab3:
        top_method =st.radio("Select the method", ["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])
        if top_method == "Top Insurance Analysis":
            pass
        elif top_method == "Top Transaction Analysis":
            pass
        elif top_method == "Top User Analysis":
            pass

elif select == "TOP CHARTS":
    pass