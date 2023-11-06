import requests
import openai
from openai import OpenAI
client = OpenAI()

def fetch_data(job_id, candidate_id):
    # Fetch Job Description
    url_job = 'https://bepc.backnetwork.net/JobSiftBeta/assets/php/equalizer.php'
    data_job = {"job": job_id, "get_description": "1"}
    response_job = requests.post(url_job, data=data_job)
    job_description = response_job.text

    # Fetch Resume
    url_resume = 'https://bepc.backnetwork.net/JobSiftBeta/assets/php/job.php'
    data_resume = {"candidate": candidate_id}
    response_resume = requests.post(url_resume, data=data_resume)
    candidate_resume = response_resume.text

    return job_description, candidate_resume

def calculate_score(job_description, candidate_resume, job_type):
    # Read scoring guidelines from text files
    with open('professional.txt', 'r') as f:
        Professional_Scoring_Guidelines = f.read()

    with open('light_industrial.txt', 'r') as f:
        Light_Industrial_Scoring_Guidelines = f.read()

    # Make API call
    score_summary = client.chat.completions.create(
    model= "gpt-4",
    messages=[
        {"role":"user", "content":"You are an expert recruiting AI.\
         Evaluate how a candidate's resume matches a job description\
         based on the following guidelines:"},
        {"role":"user", "content":f"Job Type: {job_type}"},
        {"role":"user", "content":f"If the job type is Professional:\
         - There are 10 points for Requirements and 10 points for Desired elements.\
         - Consider 4 main categories: Experience, Education, Certifications, Skills.\
         - {Professional_Scoring_Guidelines}"},
        {"role":"user", "content":f"If the job type is Light Industrial:\
         - There are 10 points for Requirements and 10 points for Desired elements.\
         - Consider 3 main categories: Experience, Education, Certifications.\
        - {Light_Industrial_Scoring_Guidelines}"},
        {"role":"user", "content":"Provide a score from 0 to 10 representing how well\
         the candidate matches the job description for both Requirements and Desired elements.."},
        {"role":"user", "content":f"Job Description: {job_description}"},
        {"role":"user", "content":f"Candidate Resume: {candidate_resume}"},
        {"role":"user", "content":f"Also, provide a 2-3 paragraph summary of the candidate's\
         viability for the job description. The text should have the following format:\
         Rating: \\n<br><br> Viability Summary: \\n this should be at the begining of the output."},
         {"role":"user", "content":"Create a formated table listing the Required and Desired categories,\
          the score you gave, and the explanation for that score given, these tables should be placed at the bottom."},
    ],
    temperature=0, #The temperature parameter controls the randomness of the generated output.
    )
    # Extract the summary text from the response
    score = score_summary['choices'][0]['message']['content']
    return score
