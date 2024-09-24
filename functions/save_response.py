import os
import json
from supabase import create_client, Client

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def save_response(save, schema, job_description, resume, response):
  if save:
    response_data = {
      "messages": [
        {"role": "system", "content": "You are an expert recruiter for a staffing company that specializes in engineering solutions and IT project management services to Fortune 500 companies in the Life Science and Technology industries."},
        {"role": "user", "content": f"Evaluate and rank how well a candidate's resume matches a job description, based on the provided job description and candidate's resume, in JSON. JSON schema: {schema}, Job Description: {job_description}, Candidate's Resume: {resume}."},
        {"role": "assistant", "content": f"{response}"},
      ]
    }

    response_data = json.dumps(response_data)

    all_responses = supabase.table('fine_tuning').select('response').execute()

    existing_responses = [response['response'] for response in all_responses.data]

    if response_data not in existing_responses:
      data = supabase.table("fine_tuning").insert({
        "response": response_data
      }).execute()

      if data:
        return 'Response saved successfully, thank you for your feedback!'
      else:
        return 'Failed to save response, please try again later.'
    else:
      return 'Failed to save, response already exists.'
  else:
    return 'Thank you for your feedback!'