import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

def user_page():
    st.title('Bus Ticket Reservation System - User Page')

    if 'booking_successful' not in st.session_state:
        st.session_state['booking_successful'] = False

    if 'ticket_details' not in st.session_state:
        st.session_state['ticket_details'] = {}

    excel_file = 'bus_details.xlsx'

    def check_file_exists(file_path):
        return os.path.exists(file_path)

    def read_buses(from_location, to_location):
        if check_file_exists(excel_file):
            df = pd.read_excel(excel_file)
            filtered_df = df[(df['From'].str.lower() == from_location.lower()) &
                             (df['To'].str.lower() == to_location.lower())]
            return filtered_df
        else:
            return pd.DataFrame()

    def update_seats(bus_name, departure_time, seats_to_book):
        if check_file_exists(excel_file):
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                if row['Bus Name'] == bus_name and row['Time of Departure'] == departure_time:
                    if row['Number of Seats'] >= seats_to_book:
                        df.at[index, 'Number of Seats'] -= seats_to_book
                        df.to_excel(excel_file, index=False)
                        return True
                    else:
                        st.error('Not enough seats available.')
                        return False
        return False

    def generate_ticket(details):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for key, value in details.items():
            pdf.cell(0, 10, f'{key}: {value}', ln=True)
        ticket_file = "ticket.pdf"
        pdf.output(ticket_file)
        return ticket_file

    def book_ticket():
        departure_time = st.session_state.available_buses[st.session_state.available_buses['Bus Name'] == st.session_state.selected_bus]['Time of Departure'].iloc[0]
        if update_seats(st.session_state.selected_bus, departure_time, st.session_state.selected_seats):
            st.session_state['ticket_details'] = {
                'Bus Name': st.session_state.selected_bus,
                'From': st.session_state.from_location,
                'To': st.session_state.to_location,
                'Departure Time': departure_time,
                'Seats Booked': st.session_state.selected_seats
            }
            st.session_state['booking_successful'] = True
        else:
            st.session_state['booking_successful'] = False
            st.error('Failed to book ticket. Please try again.')

    with st.form(key='search_form'):
        from_location = st.text_input('From', key='from_location')
        to_location = st.text_input('To', key='to_location')
        search_buses = st.form_submit_button('Search Buses')

    if search_buses:
        st.session_state['available_buses'] = read_buses(from_location, to_location)

    if 'available_buses' in st.session_state and not st.session_state['available_buses'].empty:
        st.write('Available Buses:', st.session_state['available_buses'][['Bus Name', 'From', 'To', 'Number of Seats', 'Time of Departure']])
        
        bus_options = st.session_state['available_buses']['Bus Name'].tolist()
        selected_bus = st.selectbox('Select a Bus to Book', options=bus_options, key='selected_bus')
        
        seats_options = list(range(1, 11))
        selected_seats = st.selectbox('Select Number of Seats to Book', options=seats_options, key='selected_seats')
        
        if st.button('Book Ticket'):
            book_ticket()
        
        if 'booking_successful' in st.session_state and st.session_state['booking_successful']:
            ticket_file = generate_ticket(st.session_state['ticket_details'])
            st.success(f"Ticket(s) booked successfully! {st.session_state['ticket_details']['Seats Booked']} seat(s) have been booked.")
            with open(ticket_file, "rb") as file:
                st.download_button(label="Download Ticket", data=file, file_name="ticket.pdf", mime="application/pdf")
    elif 'available_buses' in st.session_state:
        st.write("No available buses for the selected route.")
