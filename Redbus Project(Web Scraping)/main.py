import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_option_menu import option_menu


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'bus details' 
}

def clean_price(price_str):
    clean_price = float(price_str.replace('INR', '').strip())
    return clean_price


conn = mysql.connector.connect(**db_config)
with st.sidebar:
    selection = option_menu(
        menu_title=None,  
        options=["Home", "About Us"],  
        icons=["house", "info-circle"], 
    )

if selection == "Home":

    tables = ['ksrtc', 'ctu', 'hrtc', 'pepsu', 'rsrtc', 'sbstc',
            'tsrtc', 'upsrtc', 'wbstc', 'wbtc']


    st.title('RideWise')

    selected_table = st.selectbox('Select State', tables)

    query = f"SELECT * FROM {selected_table}"
    df = pd.read_sql(query, conn)

    df['Price'] = df['Price'].apply(clean_price)
        
    
    conn.close()

    if not df.empty:
            
        st.subheader('Filter the Bus that you like')

        
        filter1, filter2 = st.columns([2, 1])  

        with filter1:
            route_names = df['Route Name'].unique()
            selected_route = st.selectbox('Select Route', ['All'] + list(route_names))


        with filter2:
            bus_types = df['Bus Type'].unique()
            selected_bus_type = st.selectbox('Select Bus Type', ['All'] + list(bus_types))


        filter3, filter4 = st.columns([2, 1])


        with filter3:

            min_price, max_price = st.slider(
                'Select Price Range',
                float(df['Price'].min()),
                float(df['Price'].max()),
                (float(df['Price'].min()), float(df['Price'].max())))
            

        with filter4:
            min_rating, max_rating = st.slider(
                'Select Star Rating Range',
                0.0,
                5.0,
                (0.0, 5.0))


        filtered_df = df.copy()

        if selected_route != 'All':
            filtered_df = filtered_df[filtered_df['Route Name'] == selected_route]

        if selected_bus_type != 'All':
            filtered_df = filtered_df[filtered_df['Bus Type'] == selected_bus_type]

        filtered_df = filtered_df[
            (filtered_df['Price'] >= min_price) &
            (filtered_df['Price'] <= max_price) &
            (filtered_df['Star Rating'] >= min_rating) &
            (filtered_df['Star Rating'] <= max_rating)
            ]


        if 'Route Link' in filtered_df.columns:
            filtered_df = filtered_df.drop(columns=['Route Link'])


        st.subheader('Filtered Bus Data')
        if not filtered_df.empty:
                st.dataframe(filtered_df)  
        else:
                st.write("No buses match the selected filters.")
    else:
        st.write("No data available from the selected table.")

elif selection == "About Us":
    st.title('About Us')
    st.write("""
        Welcome to RideWise.

Wait wait wait! We know you are struggling to get your perfect schedule for your bus travel.

Do not take tension. We are here to help you.

Our application provides you the best bus routes, timing schedule, best available seats, Quality Services.

Why to wait? Start venturing!
        """)