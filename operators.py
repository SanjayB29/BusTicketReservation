import streamlit as st
import pandas as pd
import os

def operator_page():
    st.title('Bus Ticket Reservation System - Operator Page')

    # Create form to enter bus details
    with st.form("bus_form", clear_on_submit=True):
        bus_name = st.text_input('Bus Name')
        from_location = st.text_input('From')
        to_location = st.text_input('To')
        number_of_seats = st.number_input('Number of Seats', min_value=1, format='%d')
        time_of_departure = st.time_input('Time of Departure')
        submit_button = st.form_submit_button('Add Bus')

    excel_file = 'bus_details.xlsx'

    # Function to save bus details to an Excel sheet
    def save_to_excel(bus_name, from_location, to_location, number_of_seats, time_of_departure):
        data = {
            'Bus Name': [bus_name],
            'From': [from_location],
            'To': [to_location],
            'Number of Seats': [number_of_seats],
            'Time of Departure': [time_of_departure.strftime("%H:%M")]
        }

        df = pd.DataFrame(data)

        if os.path.exists(excel_file):
            with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
        else:
            df.to_excel(excel_file, index=False)

    # If the user clicks the 'Add Bus' button, save the bus details to an Excel file
    if submit_button:
        save_to_excel(bus_name, from_location, to_location, number_of_seats, time_of_departure)
        st.success('Bus added successfully!')
