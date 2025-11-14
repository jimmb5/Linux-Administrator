import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Analysis",
    layout="wide"
)

@st.cache_resource
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",
        database="datadb"
    )
    return conn

st.title("Data analyysi kiihtyvyydestä")
st.write("Mitattu puhelimella phyphox sovelluksella")

conn = get_db_connection()

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
        cursor.close()
        conn.close()
