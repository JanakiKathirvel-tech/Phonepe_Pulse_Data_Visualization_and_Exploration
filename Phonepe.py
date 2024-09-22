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
    agg_Trans_amtcount_Y =  df[df["Years"]== year]
    agg_Trans_amtcount_Y.reset_index(drop = True, inplace= True)
    
    agg_Trans_amtcount = agg_Trans_amtcount_Y.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
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
    
    return agg_Trans_amtcount_Y


def Transaction_amount_count_Q(df, quater):

    agg_Trans_amtcount_Q =  df[df["Quater"]== quater]
    agg_Trans_amtcount_Q.reset_index(drop = True, inplace= True)
    agg_Trans_amtcount = agg_Trans_amtcount_Q.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    agg_Trans_amtcount.reset_index(inplace=True)
    fig_amount = px.bar(agg_Trans_amtcount, x="States", y="Transaction_amount", title=f"{quater} Transaction Amount", height=650, width= 600
                        )
    st.plotly_chart(fig_amount)

    fig_count = px.bar(agg_Trans_amtcount, x="States", y="Transaction_count", title=f"{quater} Transaction Count", height=650, width= 600
                        )
    st.plotly_chart(fig_count)

    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    
    states_name =[] 
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    fig_india_3 = px.choropleth(agg_Trans_amtcount, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow", 
                               range_color=(agg_Trans_amtcount["Transaction_amount"].min(),agg_Trans_amtcount["Transaction_amount"].max()),
                               hover_name= "States", title = f"{quater} TRANSACTION AMOUNT", fitbounds="locations", height=600, width= 600)
    fig_india_3.update_geos(visible = False)
    st.plotly_chart(fig_india_3)

    fig_india_4 = px.choropleth(agg_Trans_amtcount, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow", 
                               range_color=(agg_Trans_amtcount["Transaction_count"].min(),agg_Trans_amtcount["Transaction_count"].max()),
                               hover_name= "States", title = f"{quater} TRANSACTION COUNT", fitbounds="locations", height=600, width= 600)
    fig_india_4.update_geos(visible = False)
    st.plotly_chart(fig_india_4)
    return agg_Trans_amtcount_Q

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)


def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quater"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)


def Map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["Registeredusers", "Appopens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["Registeredusers","Appopens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def Map_user_plot_2(df, quarter):
    muyq= df[df["Quater"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["Registeredusers", "Appopens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["Registeredusers","Appopens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def Map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["Registeredusers", "Appopens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "Registeredusers",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "Appopens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} Appopens",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)


def Top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quater"])["Registeredusers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "Registeredusers", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def Top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quater")["Registeredusers"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quater", y= "Registeredusers",barmode= "group",
                           width=1000, height= 800,color= "Registeredusers",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)


def top_states_agg():
    lt= agg_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "TOP 10 TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

# Streamlit part
st.set_page_config( layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select = option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
       # st.video("C:\\Users\\KJ\\Desktop\\CAPSTONE Projects\\phone pe\\Phone Pe Ad(720P_HD).mp4")
       pass

    col3,col4= st.columns(2)
    
    with col3:
       # st.video("C:\\Users\\KJ\\Desktop\\CAPSTONE Projects\\phone pe\\PhonePe Motion Graphics(720P_HD).mp4")
       pass

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        #st.video("C:\\Users\\KJ\\Desktop\\CAPSTONE Projects\\phone pe\\PhonePe Motion Graphics(720P_HD)_2.mp4")
        pass

elif select == "DATA EXPLORATION":
    tab1,tab2,tab3 =st.tabs(["Aggregated analysis","Map analysis","Top analysis"])

    with tab1:
        
        agg_method =st.radio("Select the method", ["Insurance Analysis","Transaction Analysis","User Analysis"])

        if agg_method == "Insurance Analysis":
            col1,col2 = st.columns(2)

            with col1:
                years = st.slider("select the year", agg_insurance["Years"].min(), agg_insurance["Years"].max(), agg_insurance["Years"].min())
                

            insurance_agg_Y = Transaction_amount_count_y(agg_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                quaters = st.slider("select the year", insurance_agg_Y["Quater"].min(), insurance_agg_Y["Quater"].max(), insurance_agg_Y["Quater"].min())

            Transaction_amount_count_Q(insurance_agg_Y, quaters )

        elif agg_method == "Transaction Analysis":
            col1,col2 = st.columns(2)

            with col1:
                years = st.slider("select the year", agg_transaction["Years"].min(), agg_transaction["Years"].max(), agg_transaction["Years"].min())                

            trans_agg_Y = Transaction_amount_count_y(agg_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", trans_agg_Y["Quater"].min(), trans_agg_Y["Quater"].max(),trans_agg_Y["Quater"].min())

            df_agg_tran_Y_Q= Transaction_amount_count_Q(trans_agg_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)

        elif agg_method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",agg_users["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(agg_users,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quater"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        map_method =st.radio("Select the method", ["Map Insurance Analysis","Map Transaction Analysis","Map User Analysis"])
        if map_method == "Map Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("select the year", map_insurance["Years"].min(), map_insurance["Years"].max(), map_insurance["Years"].min())
               
            insurance_map_Y = Transaction_amount_count_y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                 quaters = st.slider("select the Quater", insurance_map_Y["Quater"].min(), insurance_map_Y["Quater"].max(), insurance_map_Y["Quater"].min())
            Transaction_amount_count_Q(insurance_map_Y, quaters )


        elif map_method == "Map Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("select the year", map_transaction["Years"].min(), map_transaction["Years"].max(), map_transaction["Years"].min())            

            trans_map_Y = Transaction_amount_count_y(map_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", trans_map_Y["Quater"].min(), trans_map_Y["Quater"].max(),trans_map_Y["Quater"].min())

            df_map_tran_Y_Q= Transaction_amount_count_Q(trans_map_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_map_tran_Y_Q["States"].unique())

        elif map_method == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",map_users["Years"].unique())
                map_user_Y= Map_user_plot_1(map_users, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quater"].unique())
                map_user_Y_Q= Map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
                Map_user_plot_3(map_user_Y_Q, state_mu1)
    with tab3:
        top_method =st.radio("Select the method", ["Top Insurance Analysis","Top Transaction Analysis","Top User Analysis"])
        if top_method == "Top Insurance Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("select the year", top_insurance["Years"].min(), top_insurance["Years"].max(), top_insurance["Years"].min())
               
            insurance_top_Y = Transaction_amount_count_y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                 quaters = st.slider("select the year", insurance_top_Y["Quater"].min(), insurance_top_Y["Quater"].max(), insurance_top_Y["Quater"].min())
            Transaction_amount_count_Q(insurance_top_Y, quaters )
        elif top_method == "Top Transaction Analysis":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("select the year", top_transaction["Years"].min(), top_transaction["Years"].max(), top_transaction["Years"].min())            

            trans_top_Y = Transaction_amount_count_y(top_transaction, years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", trans_top_Y["Quater"].min(), trans_top_Y["Quater"].max(),trans_top_Y["Quater"].min())

            df_map_tran_Y_Q= Transaction_amount_count_Q(trans_top_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_map_tran_Y_Q["States"].unique())
        elif top_method == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",top_users["Years"].unique())
                top_user_Y= Map_user_plot_1(top_users, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",top_user_Y["Quater"].unique())
                top_user_Y_Q= Map_user_plot_2(top_user_Y,quarter_mu1)

elif select == "TOP CHARTS":
    # ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
    #                               'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
    #                               'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
    #                              'States With Highest Trasaction Count','States With Highest Trasaction Amount',
    #                              'Top 50 Districts With Lowest Transaction Amount'))
    
    ques = st.selectbox("***Select the Question***",
                        ('Top 10 States having more agg_transaction_amount'))

    if ques=="Top 10 States having more agg_transaction_amount":
        top_states_agg()

   