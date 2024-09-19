import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import requests
import json

#Dataframe creation

#sql connection
mydb = psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "Kamali@123")

cursor =mydb.cursor()

#agge_insurance_dataframe
cursor.execute("Select * from aggregated_insurance")
mydb.commit()
agge_ins_data = cursor.fetchall()

agg_insurance = pd.DataFrame(agge_ins_data, columns=("States", "Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))

#agge_transaction_dataframe
cursor.execute("Select * from aggregated_transaction")
mydb.commit()
agge_trans_data = cursor.fetchall()

agg_transaction = pd.DataFrame(agge_trans_data, columns=("States", "Years","Quater","Transaction_type","Transaction_count","Transaction_amount"))


#agge_users_dataframe
cursor.execute("Select * from aggregated_users")
mydb.commit()
agge_users_data = cursor.fetchall()

agg_users = pd.DataFrame(agge_users_data, columns=("States", "Years","Quater","Brands","Transaction_count","Percentage"))

#map_insurance_dataframe
cursor.execute("Select * from map_insurance")
mydb.commit()
map_ins_data = cursor.fetchall()

map_insurance = pd.DataFrame(map_ins_data, columns=("States", "Years","Quater","Districts","Transaction_count","Transaction_amount"))


#map_transaction_dataframe
cursor.execute("Select * from map_transaction")
mydb.commit()
map_trans_data = cursor.fetchall()

map_transaction = pd.DataFrame(map_trans_data, columns=("States", "Years","Quater","Districts","Transaction_count","Transaction_amount"))

#map_users_dataframe
cursor.execute("Select * from map_users")
mydb.commit()
map_users_data = cursor.fetchall()

map_users = pd.DataFrame(map_users_data, columns=("States", "Years","Quater","Districts","Registeredusers","Appopens"))


#top_insurance_dataframe
cursor.execute("Select * from top_insurance")
mydb.commit()
top_ins_data = cursor.fetchall()

top_insurance = pd.DataFrame(top_ins_data, columns=("States", "Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#top_transaction_dataframe
cursor.execute("Select * from top_trans")
mydb.commit()
top_trans_data = cursor.fetchall()

top_transaction = pd.DataFrame(top_trans_data, columns=("States", "Years","Quater","Pincodes","Transaction_count","Transaction_amount"))


#top_users_dataframe
cursor.execute("Select * from top_users")
mydb.commit()
top_users_data = cursor.fetchall()

top_users = pd.DataFrame(top_users_data, columns=("States", "Years","Quater","Pincodes","Registeredusers"))

def Transaction_amount_count_y(df, year):
    agg_Trans_amtcount =  df[df["Years"]== year]
    agg_Trans_amtcount.reset_index(drop = True, inplace= True)
    
    agg_Trans_amtcount = agg_Trans_amtcount.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    agg_Trans_amtcount.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(agg_Trans_amtcount, x="States", y="Transaction_amount", title=f"{year} Transaction Amount", height=650, width= 600)
        #fig_amount.show()  # this will show the output in new tab
        st.plotly_chart(fig_amount) # this will show the result chart in same streamlit page

    with col2:
        fig_count = px.bar(agg_Trans_amtcount, x="States", y="Transaction_count", title=f"{year} Transaction Count"  ,height=650, width= 600)
        st.plotly_chart(fig_count) # this will show the result chart in same streamlit page

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    
    states_name =[] 
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    col1, col2 = st.columns(2)

    with col1:
        fig_india_1 = px.choropleth(agg_Trans_amtcount, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="Rainbow", 
                                range_color=(agg_Trans_amtcount["Transaction_amount"].min(),agg_Trans_amtcount["Transaction_amount"].max()),
                                hover_name= "States", title = f"{year} TRANSACTION AMOUNT", fitbounds="locations", height=600, width= 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(agg_Trans_amtcount, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="Rainbow", 
                                range_color=(agg_Trans_amtcount["Transaction_count"].min(),agg_Trans_amtcount["Transaction_count"].max()),
                                hover_name= "States", title = f"{year} TRANSACTION COUNT", fitbounds="locations", height=600, width= 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

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
            col1,col2 = st.columns(2)

            with col1:
                years = st.slider("select the year", agg_insurance["Years"].min(), agg_insurance["Years"].max(), agg_insurance["Years"].min())

            Transaction_amount_count_y(agg_insurance, years)
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