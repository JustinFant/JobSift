import requests
import json

def fetch_data(job_id, candidate_id): # Fetch Job Description and resume

  url = 'https://bepc.backnetwork.net/AutomatedScripts/beats_connection.php'
  data = { "get_beats_job": job_id, "get_beats_candidate": candidate_id }
  response = requests.post(url, data=data)

  # Split the response text into two parts and strip the brackets
  parts = response.text.split('][')
  parts[0] = parts[0] + ']'  
  parts[1] = '[' + parts[1]  

  # Load each part as a separate JSON object
  job = json.loads(parts[0])
  candidate = json.loads(parts[1])

  job_data = {
    "job_title": job[0]['job_title'],
    "job_description": job[0]['job_description']
  }

  candidate_resume = candidate[0]['resume']

  return job_data, candidate_resume