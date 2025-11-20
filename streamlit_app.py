import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Analysis",
    layout="wide"
)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",
        database="datadb"
    )
    return conn


def get_weather_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",
        database="weather_db"
    )
    return conn

st.title("Data analyysi kiihtyvyydestä")
st.write("Mitattu puhelimella phyphox sovelluksella")

conn = get_db_connection()
cursor = None

if conn:
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT time_s, acc_x, acc_y, acc_z, abs_acc FROM accelerations ORDER BY time_s")
        data = cursor.fetchall()
        
        if data:
            df = pd.DataFrame(data, columns=['time_s', 'acc_x', 'acc_y', 'acc_z', 'abs_acc'])
            
            fig_x = px.line(df, x='time_s', y='acc_x', 
                           title='Kiihtyvyys X-akselilla',
                           labels={'time_s': 'Aika (s)', 'acc_x': 'Kiihtyvyys (m/s²)'})
            st.plotly_chart(fig_x, use_container_width=True)
            
            fig_y = px.line(df, x='time_s', y='acc_y',
                           title='Kiihtyvyys Y-akselilla',
                           labels={'time_s': 'Aika (s)', 'acc_y': 'Kiihtyvyys (m/s²)'})
            st.plotly_chart(fig_y, use_container_width=True)
            
            fig_z = px.line(df, x='time_s', y='acc_z',
                           title='Kiihtyvyys Z-akselilla',
                           labels={'time_s': 'Aika (s)', 'acc_z': 'Kiihtyvyys (m/s²)'})
            st.plotly_chart(fig_z, use_container_width=True)
            
            fig_abs = px.line(df, x='time_s', y='abs_acc',
                             title='Absoluuttinen kiihtyvyys',
                             labels={'time_s': 'Aika (s)', 'abs_acc': 'Kiihtyvyys (m/s²)'})
            st.plotly_chart(fig_abs, use_container_width=True)
            
    except mysql.connector.Error as e:
        pass
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

st.divider()
st.header("Säädataa")

weather_conn = None

try:
    weather_conn = get_weather_connection()
    weather_df = pd.read_sql(
        "SELECT city, temperature, description, timestamp FROM weather_data ORDER BY timestamp DESC LIMIT 50",
        weather_conn
    )

    if not weather_df.empty:
        st.dataframe(weather_df)

        fig_temp = px.line(
            weather_df.sort_values("timestamp"),
            x="timestamp",
            y="temperature",
            color="city",
            markers=True,
            title="Lämpötilan kehitys"
        )
        fig_temp.update_layout(xaxis_title="Aika", yaxis_title="Lämpötila")
        st.plotly_chart(fig_temp, use_container_width=True)
    else:
        st.info("Säädataa ei löytynyt tietokannasta.")
except mysql.connector.Error:
    st.error("Yhteys säädataan epäonnistui.")
finally:
    if weather_conn:
        weather_conn.close()

st.divider()
st.header("Sähkön hinta c/kWh")

electric_conn = None

try:
    electric_conn = get_weather_connection()
    electric_df = pd.read_sql(
        "SELECT price_cents, start_time FROM electric_prices ORDER BY start_time DESC LIMIT 48",
        electric_conn
    )

    if not electric_df.empty:
        chart_df = electric_df.sort_values("start_time")
        fig_price = px.line(
            chart_df,
            x="start_time",
            y="price_cents",
            markers=True,
            title="Viimeisimmät pörssisähkön hinnat"
        )
        fig_price.update_layout(xaxis_title="Aika", yaxis_title="Snt/kWh")
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.info("Sähkön hintadataa ei löytynyt tietokannasta.")
except mysql.connector.Error:
    st.error("Yhteys sähkön hintadataan epäonnistui.")
finally:
    if electric_conn:
        electric_conn.close()
