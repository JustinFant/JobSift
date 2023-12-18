import streamlit as st
import base64 
import time
from functions.fetch_data import fetch_data
from functions.calculate_score import calculate_score
from functions.transform_response import transform_response
from functions.get_recommendation import get_recommendation

# Initialize Streamlit and set page configurations
st.set_page_config(page_title="BEPC-JobSift", page_icon="static/logo.png", layout='wide')

# Function to read binary data and convert to base64
def get_image_base64(image_path):
  with open(image_path, 'rb') as img_file:
    return base64.b64encode(img_file.read()).decode('utf-8')

# Convert images to base64 and include in HTML
sr2new = get_image_base64('static/rs2.png')
st.markdown(
  f"""
  <div class="container">
    <h2 class="text-center mt-4">
      <img src="data:image/png;base64,{sr2new}" width="50" height="50" class="d-inline-block align-top" alt="">
      JobSift v2.1 <span style="font-style: italic; font-size: 17px;">for recruiting</span>
    </h2>
  </div>
  """,
  unsafe_allow_html=True,
)

# User Input via Streamlit widgets
job_type = st.selectbox('Select Job Type', ['Light Industrial', 'Professional'])
job_id = st.text_input('Enter the Job ID') #'23087' for testing
candidate_id = st.text_input('Enter the Candidate ID')  # Changed 'candidate' to 'candidate_id' for consistency '298853' for testing
# experience = st.text_input('3.- Enter the Candidate Experience')
# keywords = st.text_input('4.- Enter the Keywords')

# Load scoring examples
with open('helpers/score_examples.txt', 'r') as f:
  score_examples = f.read()

# Evaluate Resume Button
if st.button('Evaluate Resume', type = 'primary'):
  with st.spinner('Evaluating...'):
    start_time = time.time()
    timeout = 10

    # Fetch Job Description and Candidate Resume
    job_description, candidate_resume = fetch_data(job_id, candidate_id)
    
    # Keep trying to fetch data if invalid, stop after 10 seconds
    while (not job_description or not candidate_resume) and time.time() - start_time < timeout:
      job_description, candidate_resume = fetch_data(job_id, candidate_id)
      
    if not job_description or not candidate_resume:
      st.error('Timeout while fetching data, please try again.')
      st.rerun()

    # Calculate Score and Summary
    score_summary = calculate_score(job_description, candidate_resume, job_type, score_examples)

    transformed_response = transform_response( #transform the response arrays into html tables
      score_summary['requirements_table'],
      score_summary['desired_elements_table'],
      job_type
    )
    
    # Display Results
    st.markdown("## Viability Summary:")
    st.markdown(f"**{get_recommendation(transformed_response['overall_score'])}**")
    st.markdown(score_summary['viability_summary'], unsafe_allow_html=True)
    st.header(f"Overall Score: {transformed_response['overall_score']}/10")
    # st.subheader(f"Requirements Rating: {transformed_response['requirements_rating']}") 
    st.text('Required Elements Breakdown:')
    st.markdown(transformed_response['requirements_table'], unsafe_allow_html=True)
    # st.subheader(f"Preferences Rating : {transformed_response['preferences_rating']}")
    st.text('Desired Elements Breakdown:')
    st.markdown(transformed_response['desired_elements_table'], unsafe_allow_html=True)
    # print(transformed_response['overall_score'])

# Footer
st.markdown("""
<footer class="footer mt-auto py-3">
  <div class="container text-center">
    <p class="text-muted">
      Copyright © 2023 | BEPC Incorporated | All Rights Reserved |
      <a href="Privacy_Policy_Link">Privacy Policy</a> |
      <a href="Cybersecurity_Link">Cybersecurity</a> |
      <a href="HIPAA_Link">HIPAA</a>
      |  MSJAMMXXIII
    </p>
  </div>
</footer>
""", unsafe_allow_html=True)