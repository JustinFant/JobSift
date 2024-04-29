import os
import json
from supabase import create_client, Client

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


def save_response(save, schema, job_description, resume, response):
  if save:
    response_data = {
      "messages": [
        {"role": "system", "content": "Marv is an expert recruiter for a staffing company."},
        {"role": "user", "content": f"Evaluate and rank how well a candidate's resume matches a job description, based on the provided job description and candidate's resume, in JSON. JSON schema: {schema}, Job Description: {job_description}, Candidate's Resume: {resume}."},
        {"role": "assistant", "content": f"{response}"},
      ]
    }

    response_data = json.dumps(response_data)

    data = supabase.table("fine_tuning").insert({
      "response": response_data
    }).execute()

    current_responses = supabase.table('data').select('positive_responses').execute()
    
    responses = supabase.table('data').update({
      'positive_responses': current_responses.data[0]['positive_responses'] + 1
    }).eq('id', 1).execute()

    if data and responses:
      return 'Response saved successfully, thank you for your feedback!'
    else:
      return 'Failed to save response, please try again later.'
  else:
    current_responses = supabase.table('data').select('negative_responses').execute()
    
    data = supabase.table('data').update({
      'negative_responses': current_responses.data[0]['negative_responses'] + 1
    }).eq('id', 1).execute()

    if data:
      return 'Thank you for your feedback!'
    else:
      return 'Failed to save response, please try again later.'
