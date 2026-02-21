import streamlit as st
import pandas as pd
from src.db import DBConnector

def get_db():
    return DBConnector()

def load_zones():
    db = get_db()
    try:
        df = db.query_to_df("SELECT LocationID, Zone, Borough FROM taxi_zones ORDER BY Zone")
    except Exception as e:
        st.error(f"Error loading zones: {e}")
        df = pd.DataFrame()
    finally:
        db.close()
    return df

def run_app():
    st.set_page_config(page_title="NYC Taxi Demand", page_icon="🚖", layout="wide")
    st.title("🚖 NYC Taxi Demand Prediction")
    st.markdown("Forecast taxi demand across New York City based on historical trends.")
    
    st.sidebar.header("Prediction Settings")
    st.sidebar.write("Select parameters to forecast demand.")
    
    zones_df = load_zones()
    if not zones_df.empty:
        # Create a display string for the dropdown
        zones_df['Display'] = zones_df['Zone'] + " (" + zones_df['Borough'] + ")"
        zone_dict = dict(zip(zones_df['Display'], zones_df['LocationID']))
        
        selected_zone_display = st.sidebar.selectbox("Select Pickup Zone", options=list(zone_dict.keys()))
        selected_location_id = zone_dict[selected_zone_display]
        st.sidebar.write(f"**Location ID:** {selected_location_id}")
        
        st.sidebar.markdown("---")
        hour_val = st.sidebar.slider("Hour of Day (0-23)", min_value=0, max_value=23, value=17)
        dow_val = st.sidebar.selectbox(
            "Day of Week",
            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            index=1 # Default Tuesday
        )
        
        # Mapping dow string to int for model
        dow_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        dow_int = dow_mapping[dow_val]
        
        if st.sidebar.button("Predict Demand", type="primary"):
            from src.inference import get_latest_model, load_model, predict_demand
            try:
                model_path = get_latest_model()
                model = load_model(model_path)
                
                prediction = predict_demand(model, selected_location_id, hour_val, dow_int)
                
                st.success(f"### Predicted Demand: {int(prediction)} rides")
                st.info(f"📍 **{selected_zone_display}** | 🕒 **{hour_val}:00** | 📅 **{dow_val}**")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                
    else:
        st.sidebar.error("Could not load taxi zones. Please ensure the ingestion step has been run.")

if __name__ == "__main__":
    run_app()
