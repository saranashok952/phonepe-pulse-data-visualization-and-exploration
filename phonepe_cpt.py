import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu

#streamlit page configuration
st.set_page_config(page_title="Phonepe Pulse Data Visualization and Exploration",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# Phonepe pulse data visualization and exploration"""})


# establishing sql connection
config = {
    'user': 'saran',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'phonepetest',
    'raise_on_warnings': True,
}
mydb = sql.connect(**config)
mycursor = mydb.cursor(buffered=True)

# streamlit code
st.header(":blue[Phonepe Pulse ]")

# Creating option menu at the top
selected = option_menu("INFO", ["Home", "Charts", "Exploration"],
                       icons=["house", "graph-up-arrow", "bar-chart-line", "exclamation-circle"],
                       menu_icon="menu-button-wide",
                       default_index=0,
                       styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                            "--hover-color": "#6F36AD"},
                               "nav-link-selected": {"background-color": "#6F36AD"}})

# INFO 1 - HOME
if selected == "Home":
    st.markdown("# :blue[Phonepe Pulse Data Visualization and Exploration]")
    col1 = st.columns(1)
    column_1 = col1[0]
    with column_1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :blue[Overview :] A User-Friendly Tool for Data Visualization and Exploration Using Streamlit andPlotly is a multi-page application created to gather data and insights that may be presented in an understandable way.")
        st.markdown("### :blue[Steps :] Utilizing scripting, extract and clone data from the Phonepe pulse Github project. Convert the data into an appropriate format and carry out any required pre-processing and cleaning. To ensure effective storage and retrieval, insert the converted data into a MySQL database. To present the data in an engaging and aesthetically pleasing way, use Python's Streamlit and Plotly to create a live geovisualization dashboard. To display the data in the dashboard, retrieve it from the MySQL database.")


# INFO 2 - CHARTS
if selected == "Charts":
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    
    col1 = st.columns(1)
    
    with col1[0]:
        Year = st.radio("**Year**", list(range(2018, 2024)))
        Quarter = st.radio("Quarter", [1, 2, 3, 4])


    #Charts - TRANSACTIONS
    if Type == "Transactions":
        st.markdown("### :blue[Transaction amount and count of all state]")
        mycursor.execute(
            f"select states, sum(transaction_count) as total_transactions, sum(transaction_amount) as total_amount from aggregated_transaction where years = {Year} and quarters = {Quarter} group by states order by total_amount desc limit 20")
        df = pd.DataFrame(mycursor.fetchall(), columns=['states', 'transactions_count', 'total_amount'])
        fig = px.pie(df, values='total_amount',
                    names='states',
                    title='  States',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['transactions_count'],
                    labels={'transactions_count': 'transactions_count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### :blue[Transaction amount and count of all district]")
        mycursor.execute(
            f"select district , sum(transaction_count) as total_count, sum(transaction_amount) as total_amount from map_transaction where years = {Year} and quarters = {Quarter} group by district order by total_amount desc limit 20")
        df = pd.DataFrame(mycursor.fetchall(), columns=['district', 'transactions_count', 'total_amount'])

        fig = px.pie(df, values='total_amount',
                    names='district',
                    title='  Districts',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['transactions_count'],
                    labels={'transactions_count': 'transactions_count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### :blue[Transaction amount and count of all pincode]")
        mycursor.execute(
            f"select pincode, sum(transaction_count) as total_count, sum(transaction_amount) as total_amount from top_transaction where years = {Year} and quarters = {Quarter} group by pincode order by total_amount desc limit 20")
        df = pd.DataFrame(mycursor.fetchall(), columns=['pincode', 'transactions_count', 'total_amount'])
        fig = px.pie(df, values='total_amount',
                    names='pincode',
                    title='  Pincodes',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['transactions_count'],
                    labels={'transactions_count': 'transactions_count'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Charts - USERS
    if Type == "Users":
        st.markdown("### :blue[Brands]")
        mycursor.execute(
            f"SELECT brand, SUM(count) AS total_count, AVG(percentage)*100 AS average_percentage FROM aggregated_user WHERE years = {Year} AND quarters = {Quarter} GROUP BY brand ORDER BY total_count DESC limit 20")
        df = pd.DataFrame(mycursor.fetchall(), columns=['brand', 'total_users', 'average_percentage'])
        fig = px.bar(df,
                    title='  Brands',
                    x="total_users",  
                    y="brand",
                    orientation='h',
                    color='average_percentage',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### :blue[Total users by districts]")
        mycursor.execute(
            f"SELECT district, SUM(users) AS total_users, SUM(app_opens) AS total_app_opens FROM map_user WHERE years = {Year} AND quarters = {Quarter} GROUP BY district ORDER BY total_users DESC limit 20")
        df = pd.DataFrame(mycursor.fetchall(),
                        columns=['district', 'total_users', 'total_app_opens'])
        fig = px.bar(df,
                    title='  Districts',
                    x="total_users",
                    y="district",
                    orientation='h',
                    color='total_users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### :blue[Total users by pincode]")
        mycursor.execute(
            f"SELECT pincode, SUM(registeredUsers) AS total_users FROM top_user WHERE years = {Year} AND quarters = {Quarter} GROUP BY pincode ORDER BY total_users DESC limit 20")
        df = pd.DataFrame(mycursor.fetchall(), columns=['pincode', 'total_users'])
        fig = px.pie(df,
                    values='total_users',
                    names='pincode',
                    title='  Pincodes',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['total_users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### :blue[States]")
        mycursor.execute(
            f"SELECT states, SUM(users) AS total_users, SUM(app_opens) AS total_app_opens FROM map_user WHERE years = {Year} AND quarters = {Quarter} GROUP BY states ORDER BY total_users DESC limit 20")
        df = pd.DataFrame(mycursor.fetchall(),
                        columns=['states', 'total_users', 'total_app_opens'])
        fig = px.pie(df,
                    values='total_users',
                    names='states',
                    title='  States',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['total_app_opens'],
                    labels={'total_app_opens': 'Total App Opens'})

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

# INFO 3 - EXPLORATION
if selected == "Exploration":
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    
    col1 = st.columns(1)
    
    with col1[0]:
        Year = st.radio("**Year**", list(range(2018, 2024)))
        Quarter = st.radio("Quarter", [1, 2, 3, 4])

    # EXPLORATION - TRANSACTIONS
    if Type == "Transactions":

        st.markdown("## :blue[Transactions Amount]")
        mycursor.execute(
            f"select states, sum(transaction_count) as total_transactions, sum(transaction_amount) as total_amount from map_transaction where years = {Year} and quarters = {Quarter} group by states order by states")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['states', 'total_transactions', 'total_amount'])
        df2 = pd.read_csv("C:/Users/dell/Downloads/Data Science/Untitled Folder/Statenames.csv")
        df1.states = df2

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='states',
                            color='total_amount',
                            color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## :blue[Transactions Count]")
        mycursor.execute(
            f"select states, sum(transaction_count) as total_transactions, sum(transaction_amount) as total_amount from map_transaction where years = {Year} and quarters = {Quarter} group by states order by states")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['states', 'total_transactions', 'total_amount'])
        df2 = pd.read_csv("C:/Users/dell/Downloads/Data Science/Untitled Folder/Statenames.csv")
        df1.total_transactions = df1.total_transactions.astype(int)
        df1.states = df2

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='states',
                            color='total_transactions',
                            color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## :blue[Transaction Type]")
        mycursor.execute(
            f"select transaction_name, sum(transaction_count) as total_transactions, sum(transaction_amount) as total_amount from aggregated_transaction where years= {Year} and quarters = {Quarter} group by transaction_name order by transaction_name")
        df = pd.DataFrame(mycursor.fetchall(),
                         columns=['transaction_name', 'total_transactions', 'total_amount'])

        fig = px.bar(df,
                     title='Transaction Types and total transaction',
                     x="transaction_name",
                     y="total_transactions",
                     orientation='v',
                     color='total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=False)

    # EXPLORATION - USERS
    if Type == "Users":

        st.markdown("## :blue[App opens]")
        mycursor.execute(
            f"SELECT states, SUM(registeredUsers) AS total_users FROM top_user WHERE years = {Year} AND quarters = {Quarter} GROUP BY states ORDER BY states")
        df1 = pd.DataFrame(mycursor.fetchall(),
                        columns=['states', 'total_users'])
        df2 = pd.read_csv("C:/Users/dell/Downloads/Data Science/Untitled Folder/Statenames.csv")
        df1.states = df2

        fig1 = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='states',
                            color='states',
                            hover_data={'states': False, 'total_users': True},
                            color_continuous_scale='sunset',
                            labels={'total_users': 'Total Count'},
                            title='App opens of all states')
        fig1.update_geos(fitbounds="locations", visible=False)
        fig1.update_layout(legend_title='States')
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("## :blue[Brands with total count]")
        mycursor.execute(
            f"SELECT brand, SUM(count) AS total_count, AVG(percentage)*100 AS average_percentage FROM aggregated_user WHERE years = {Year} AND quarters = {Quarter} GROUP BY brand ORDER BY total_count")
        df = pd.DataFrame(mycursor.fetchall(),
                        columns=['brand', 'total_count', 'average_percentage'])

        fig = px.bar(df,
                    title='Brand vs Total_Count',
                    x="brand",
                    y="total_count",
                    orientation='v',
                    color='total_count',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=False)

        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                    ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                    'bihar',
                                    'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                    'goa', 'gujarat', 'haryana',
                                    'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                    'ladakh', 'lakshadweep',
                                    'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                    'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                    'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                    'west-bengal'), index=30)

        if selected_state:
            mycursor.execute(
                f"select states, district,years,quarters, sum(users) as total_users, sum(app_opens) as total_appopens from map_user where years = {Year} and quarters = {Quarter} and states = '{selected_state}' group by states, district,years,quarters order by states,district")

            df1 = pd.DataFrame(mycursor.fetchall(), columns=['states', 'district', 'years', 'quarters',
                                                            'total_users', 'total_appopens'])

            fig = px.line(df1,
                        title=selected_state,
                        x="district",
                        y="total_users")
            st.plotly_chart(fig, use_container_width=True)