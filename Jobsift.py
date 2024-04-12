import streamlit as st
import json
import base64 
from functions.fetch_data import fetch_data
from functions.calculate_score import calculate_score


st.set_page_config(page_title="BEPC-Jobsift", page_icon="static/logo.png", layout='wide')

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
      JobSift <span style="font-style: italic; font-size: 17px;">V3.0 for recruiting</span>
    </h2>
  </div>
  """,
  unsafe_allow_html=True,
)

# User Input via Streamlit widgets
job_id = st.text_input('Enter the Job ID') #'23087' for testing
candidate_id = st.text_input('Enter the Candidate ID') # '298853' for testing


if st.button('Evaluate Resume', type = 'primary'):
  if job_id and candidate_id:
    with st.spinner('Evaluating...'):
      # Read Guidelines
      with open('helpers/schema.txt', 'r') as file:
        schema = file.read()
      
      # Fetch Job Description and Candidate Resume
      job_description, candidate_resume = fetch_data(job_id, candidate_id)

      if not job_description:
        st.error("Job description not found, please check the job id and description on Bullhorn.")
      elif not candidate_resume:
        st.error("Candidate's resume not found, please check the candidate id and resume on Bullhorn.")
        
      else:
        # Calculate Score and Summary
        score_summary = calculate_score(job_description, candidate_resume, schema)
        
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