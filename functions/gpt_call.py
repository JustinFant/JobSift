from openai import OpenAI
from dotenv import load_dotenv 


load_dotenv()
client = OpenAI()

def gpt_call(job_data, candidate_resume, schema):
  response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0,  
    seed= 123455555,
    response_format={"type": "json_object"},
    messages=[
        {"role":"system", "content":"You are an expert recruiter for a \
          staffing company that specializes in engineering solutions and \
          IT project management services to Fortune 500 companies in the Life Science and Technology industries.\
          Your job is to evaluate and rank how well a candidate's resume matches a job description \
          based on the provided job description and candidate's resume, in JSON. \
          Unless the candidate meets or exceeds every requirement in the job description, give them a score less than 5. \
          Do not recommend candidates that have things like gaps in work history, short tenures, and other similar issues."},
        {"role":"user", "content":f"JSON Schema: {schema}"},
        {"role":"user", "content":f"Job Description: {job_data}"},
        {"role":"user", "content":f"Candidate Resume: {candidate_resume}"},
      ],
  )
  # print(response.choices[0].message.content)
  return response.choices[0].message.content