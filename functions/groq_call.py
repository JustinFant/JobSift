from groq import Groq
from dotenv import load_dotenv 


load_dotenv()
client = Groq()

def groq_call(job_data, candidate_resume, schema):
  response = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    temperature=0,  
    seed=123455555,
    response_format={"type": "json_object"},
     messages=[
      {"role":"system", "content":"You are an expert recruiter tasked with analyzing and evaluating candidates for job viability. \
        You will be provided with a job description outlining the key responsibilities, required skills, and qualifications for a role, \
        a candidate's resume detailing their professional background, skills and achievements, and a JSON schema specifying the evaluation criteria. \
        You will evaluate the candidate and provide a score from 1-10 for the candidate's overall viability for the position focusing on hard skills rather than soft or implied skills, \
        a brief 3-4 sentence summary of the candidate's qualifications, you will also specify any gaps in job history, \
        and key highlights of the candidate's experience and skills that align with the job description. You will also provide the job title and candidate's name. \
        Score candidates based on the following criteria: \
        1-4: The candidate does not meet the minimum requirements and you do not recommend them for the position. Place candidates with a poor job history with several gaps or 'job hopping' behavior in this range. \
        5-7: The candidate meets the minimum requirements but is not an ideal fit. \
        8-10: The candidate exceeds the minimum requirements and meets or exceeds the prefered qualifications, experience, skills, education, etc. \
        Prioritize scoring based on experience, education and qualifications, and avoid scoring based on soft skills."},
      {"role":"user", "content":f"JSON Schema: {schema}"},
      {"role":"user", "content":f"Job Description: {job_data}"},
      {"role":"user", "content":f"Candidate Resume: {candidate_resume}"},
    ],
  )
  # print(response.choices[0].message.content)
  return response.choices[0].message.content