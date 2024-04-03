from groq import Groq
from dotenv import load_dotenv 


load_dotenv()
client = Groq()

def calculate_score(job_description, candidate_resume, schema):
  response = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    temperature=0,  
    seed= 123455555,
    response_format={"type": "json_object"},
    messages=[
        {"role":"system", "content":"You are an expert recruiter for a \
          staffing company that specializes in engineering solutions and \
          IT project management services to Fortune 500 companies in the Life Science and Technology industries.\
          Your job is to evaluate and rank how well a candidate's resume matches a job description\
          based on the provided job description and candidate's resume, in JSON. \
          Unless the candidate meets or exceeds every requirement in the job description, give them a score less than 5."},
        {"role":"user", "content":f"JSON Schema: {schema}"},
        {"role":"user", "content":f"Job Description: {job_description}"},
        {"role":"user", "content":f"Candidate Resume: {candidate_resume}"},
      ],
  )

  return response.choices[0].message.content