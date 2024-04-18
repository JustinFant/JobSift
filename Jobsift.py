import streamlit as st
import json
import time
import base64 
from functions.fetch_data import fetch_data
from functions.groq_call import groq_call
from functions.gpt_call import gpt_call


st.set_page_config(page_title="BEPC-Jobsift", page_icon="static/logo.png", layout='wide')

# Timer to track seconds spent in each function, set to True to enable
DEBUG_TIMER = False

# Function to read binary data and convert to base64
def get_image_base64(image_path):
  with open(image_path, 'rb') as img_file:
    return base64.b64encode(img_file.read()).decode('utf-8')

# Convert images to base64 and include in HTML
sr2new = get_image_base64('static/JS_3.png')
st.markdown(
  f"""
  <div class="container">
      <h2 class="text-center mt-4">
          <img src="data:image/png;base64,{sr2new}" width="125" height="125" class="d-inline-block align-top" alt="">
          Jobsift <span style="font-style: italic; font-size: 17px;">for recruiting V3.0</span>
      </h2>
  </div>
  """,
  unsafe_allow_html=True,
)

# User Input via Streamlit widgets
model = st.selectbox('Select Model', ['Groq', 'Chat GPT'])
job_id = st.text_input('Enter the Job ID') #'23087' for testing
candidate_id = st.text_input('Enter the Candidate ID') # '298853' for testing


if st.button('Evaluate Resume', type = 'primary'):
  if job_id and candidate_id:
    with st.spinner('Evaluating...'):
      # Read Guidelines
      with open('helpers/schema.txt', 'r') as file:
        schema = file.read()

      if DEBUG_TIMER:
        # Start timer before fetch_data
        start_time = time.time()
      
      # Fetch Job Description and Candidate Resume
      job_description, candidate_resume = fetch_data(job_id, candidate_id)
      
      if DEBUG_TIMER:
        # Print time spent in fetch_data
        print(f"Time to fetch data: {time.time() - start_time} seconds")

      if not job_description:
        st.error("Job description not found, please check the job id and description on Bullhorn.")
      elif not candidate_resume:
        st.error("Candidate's resume not found, please check the candidate id and resume on Bullhorn.")
      else:
        
        if DEBUG_TIMER:
          # Start timer before calculate_score
          start_time = time.time()
        
        if model == 'Groq':
          # Call Groq
          score_summary = groq_call(job_description, candidate_resume, schema)
        else:
          # Call Chat GPT
          score_summary = gpt_call(job_description, candidate_resume, schema)
        
        if DEBUG_TIMER:
          # Print time spent in calculate_score
          print(f"Time to calculate score: {time.time() - start_time} seconds")

        # Convert to JSON
        score_summary = json.loads(score_summary)

        # Display Results
        st.header(f"Sourcing Summary: {score_summary['analysis']['score']}/10")
          
        st.subheader(f"Candidate: _{score_summary['analysis']['candidate_name']} #{candidate_id}_")
          
        st.subheader(f"Applied For: _{score_summary['analysis']['job_title']} #{job_id}_")

        st.subheader("Experience:")
        st.write(f"{score_summary['analysis']['experience']}")
          
        st.subheader("Skills:")
        st.write(f"{score_summary['analysis']['skills']}")

        st.subheader("Summary:")
        st.write(score_summary['analysis']['summary'])
  else:
    st.error('Please enter the Job ID and Candidate ID to evaluate.')

# Footer
st.markdown("""
<footer class="footer mt-auto py-3">
  <div class="container text-center">
    <p class="text-muted">
      Copyright © 2023 | BEPC Incorporated | All Rights Reserved |
      <a href="Privacy_Policy_Link">Privacy Policy</a> |
      <a href="Cybersecurity_Link">Cybersecurity</a> |
      <a href="HIPAA_Link">HIPAA</a>
      |  MSJAJFMMXXIII
    </p>
  </div>
</footer>
""", unsafe_allow_html=True)