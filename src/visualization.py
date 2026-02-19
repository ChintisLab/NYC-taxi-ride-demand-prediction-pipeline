import streamlit as st
import pandas as pd
from src.db import DBConnector

def load_data(query):
    db = DBConnector()
    df = db.query_to_df(query)
    db.close()
    return df

def run_app():
    st.title("NYC Taxi Demand Prediction")
    st.write("Welcome to the Taxi Demand Dashboard.")

if __name__ == "__main__":
    run_app()
