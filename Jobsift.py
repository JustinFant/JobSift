import streamlit as st
import json
import time
import base64 
from functions.fetch_data import fetch_data
from functions.groq_call import groq_call
from functions.gpt_call import gpt_call
from functions.save_response import save_response


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
with open('helpers/schema.txt', 'r') as file:
  schema = file.read()

@st.experimental_fragment
def save():
  st.markdown("""
    <style>
        div[data-testid="column"] {
            width: fit-content !important;
            flex: unset;
        }
        div[data-testid="column"] * {
            width: fit-content !important;
        }
    </style>
  """, unsafe_allow_html=True)

  col1, col2 = st.columns([1, 1])
  with col1:
    if st.button('Save Response'):
      save = True
      response = save_response(save, schema, job_description, candidate_resume, score_summary)
      if not 'Failed' in response:
        st.success(response)
      else:
        st.error(response)
  with col2:
    if st.button(':red[Discard Response]'):
      save = False
      response = save_response(save, schema, job_description, candidate_resume, score_summary)
      if not 'Failed' in response:
        st.success(response)
      else:
        st.error(response)

if st.button('Evaluate Resume', type = 'primary'):
  if job_id and candidate_id:
    with st.spinner('Evaluating...'):
      if DEBUG_TIMER:
        # Start timer before fetch_data
        start_time = time.time()
      
      job_description, candidate_resume = fetch_data(job_id, candidate_id)
      # job_description, candidate_resume = 'Job Description', 'Candidate Resume'
      
      if DEBUG_TIMER:
        # Print time spent in fetch_data
        print(f"Time in fetch data: {time.time() - start_time} seconds")

      if not job_description:
        st.error("Job description not found, please check the job id and description on Bullhorn.")
      elif not candidate_resume:
        st.error("Candidate's resume not found, please check the candidate id and resume on Bullhorn.")
      else:
        if model == 'Groq':
          if DEBUG_TIMER:
            # Start timer before groq call
            start_time = time.time()
          
          score_summary = groq_call(job_description, candidate_resume, schema)
          
          if DEBUG_TIMER:
            # Print time spent in groq call
            print(f"Time in groq call: {time.time() - start_time} seconds")
        else:
          if DEBUG_TIMER:
            # Start timer before gpt call
            start_time = time.time()
          
          score_summary = gpt_call(job_description, candidate_resume, schema)

          if DEBUG_TIMER:
            # Print time spent in gpt call
            print(f"Time in gpt call: {time.time() - start_time} seconds")

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
        
        save()
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

# score_summary = """
#   {
#     "analysis": {
#       "score": 8,
#       "candidate_name": "Cesar Chavez",
#       "job_title": "Quality Engineer",
#       "experience": "Cesar Chavez has over 20 years of experience in Quality and Manufacturing, including roles such as Quality Assurance Engineer at Cardinal Health and Quality Engineer at PGSTech. He has extensive experience in ISO certifications, quality system audits, and supplier quality management.",
#       "skills": "Cesar is a Six Sigma Black Belt, skilled in Lean Manufacturing, APQP, CAPA, and FMEA. He has strong technical skills in quality assurance, process improvement, and project management, with certifications in Internal Auditing for ISO 9000:2015 and TS 16949.",
#       "summary": "Cesar Chavez is a highly experienced candidate with over two decades in quality and manufacturing roles, directly aligning with the requirements for the Quality Engineer position at BEPC Inc. His extensive experience in managing quality assurance across multiple plants, implementing ISO standards, and leading significant quality improvement initiatives makes him a strong candidate. He meets the educational and experience requirements, possesses relevant certifications, and has a proven track record of success in similar roles. No noticeable gaps in employment or short tenures were observed in his resume. His skills and experience highly match the job description, making him a recommended candidate for this position."
#     }
#   }
# """