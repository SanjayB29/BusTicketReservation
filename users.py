import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
import tempfile

def user_page():
    st.title('Bus Ticket Reservation System - User Page')

    # Initialize session states for form inputs and actions
    if 'from_location' not in st.session_state:
        st.session_state['from_location'] = ''
    if 'to_location' not in st.session_state:
        st.session_state['to_location'] = ''
    if 'selected_bus' not in st.session_state:
        st.session_state['selected_bus'] = None  # Use None to simplify logic
    if 'seats_to_book' not in st.session_state:
        st.session_state['seats_to_book'] = 1
    if 'book_clicked' not in st.session_state:  # We only need this state
        st.session_state['book_clicked'] = False

    from_location = st.text_input('From', key='from_location', on_change=_reset_book_state)
    to_location = st.text_input('To', key='to_location', on_change=_reset_book_state)

    excel_file = 'bus_details.xlsx'

    if from_location and to_location:
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
            available_buses = df[(df['From'].str.lower() == from_location.lower()) & (df['To'].str.lower() == to_location.lower())]
            if not available_buses.empty:
                bus_names = available_buses['Bus Name'].tolist()
                selected_bus = st.selectbox("Available Buses", bus_names, key='selected_bus', on_change=_reset_book_state)
                seats_to_book = st.number_input('Number of Seats to Book', min_value=1, format='%d', key='seats_to_book', on_change=_reset_book_state)
                book_button = st.button('Book Ticket')

                if book_button or st.session_state['book_clicked']:
                    if selected_bus and _book_ticket(selected_bus, seats_to_book):
                        st.session_state['book_clicked'] = True
                        _download_ticket(selected_bus, seats_to_book)
                    else:
                        st.error('Not enough seats available or bus not found.')
            else:
                st.error('No buses available for the selected route.')

def _reset_book_state():
    """Reset the book state to handle form changes properly."""
    st.session_state['book_clicked'] = False

def _book_ticket(selected_bus, seats_to_book):
    """Book a ticket by updating the number of available seats."""
    excel_file = 'bus_details.xlsx'
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        bus_row = df.loc[df['Bus Name'] == selected_bus]
        if not bus_row.empty:
            current_seats = bus_row['Number of Seats'].values[0]
            if current_seats >= seats_to_book:
                df.loc[df['Bus Name'] == selected_bus, 'Number of Seats'] = current_seats - seats_to_book
                df.to_excel(excel_file, index=False)
                return True
    return False

def _generate_ticket(selected_bus, seats_to_book):
    """Generate a PDF ticket and return its path."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Bus Ticket for {selected_bus}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Number of Seats: {seats_to_book}", ln=True, align='C')

    # Save the PDF to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

def _download_ticket(selected_bus, seats_to_book):
    """Provide a download button for the generated ticket PDF."""
    ticket_file = _generate_ticket(selected_bus, seats_to_book)
    with open(ticket_file, "rb") as file:
        st.download_button(
            label="Download Ticket",
            data=file,
            file_name="bus_ticket.pdf",
            mime="application/pdf"
        )

