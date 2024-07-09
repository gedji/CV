import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText
import os
import time

# Set your local directory here
local_directory = 'C:/Users/djime/Downloads'  # Replace with your actual directory

# Email setup
EMAIL_ADDRESS = os.getenv('email')
EMAIL_PASSWORD = os.getenv('password')
NOTIFICATION_EMAIL = os.getenv('receiver')

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = NOTIFICATION_EMAIL

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def list_local_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def process_files(files):
    # Simulate processing
    for file in files:
        st.write(f"Processing {file}...")
        time.sleep(1)  # Simulate some processing time

    return True  # Simulate successful processing

# Streamlit UI with enhanced design
st.set_page_config(
    page_title="Dynamic Data Processing Pipeline",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0; /* Light gray background */
    }
    .streamlit-btn {
        background-color: #3498db !important; /* Blue button */
        color: white !important;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 20px;
        margin-top: 10px;
    }
    .streamlit-btn:hover {
        background-color: #2980b9 !important; /* Darker blue on hover */
    }
    .output-banner {
        padding: 10px;
        background-color: #2ecc71; /* Green banner */
        color: white;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
        border-radius: 5px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .block {
        display: inline-block;
        padding: 10px;
        margin: 10px;
        background-color: lightblue;
        border: 1px solid #000;
        border-radius: 5px;
        transition: transform 1s;
    }
    .moving-block {
        animation: moveBlock 2s forwards;
    }
    @keyframes moveBlock {
        from { transform: translateX(0); }
        to { transform: translateX(100px); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Streamlit app
def main():
    success = None  # Initialize success variable
    
    st.title("Dynamic Data Processing Pipeline")
    st.header("Step 1: Random Selection Block")

    file_count = st.number_input("Number of files to select:", min_value=1, value=5)

    if st.button("Start Pipeline", key="start_button"):
        uploaded_files = list_local_files(local_directory)
        
        if len(uploaded_files) < file_count:
            st.error(f"Not enough files in the directory. Only {len(uploaded_files)} files available.")
        else:
            with st.spinner("Selecting files..."):
                selected_files = random.sample(uploaded_files, file_count)
                st.write("""
                    <div class="block moving-block">Random Selection</div>
                """, unsafe_allow_html=True)
                time.sleep(2)  # Simulate the selection animation
                st.success("Files selected successfully!")
                st.write("<h3>Selected Files:</h3>", unsafe_allow_html=True)
                st.write("<ul>", unsafe_allow_html=True)
                for file in selected_files:
                    st.write(f"<li>{file}</li>", unsafe_allow_html=True)
                st.write("</ul>", unsafe_allow_html=True)
            
            with st.spinner("Processing selected files..."):
                st.write("""
                    <div class="block moving-block">Processing</div>
                """, unsafe_allow_html=True)
                success = process_files(selected_files)
                time.sleep(2)  # Simulate the processing animation
            
            if success:
                st.success("All processes completed successfully.")
                send_email("Pipeline Success", "All processes completed successfully!")
                st.balloons()  # Display balloons on success
            else:
                st.error("An error occurred during processing.")
                send_email("Pipeline Error", "An error occurred during processing.")

    # Output display in a styled banner
    if success:
        st.markdown('<div class="output-banner">All processes completed successfully!</div>', unsafe_allow_html=True)
    elif success is False:
        st.markdown('<div class="output-banner">An error occurred during processing.</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()



