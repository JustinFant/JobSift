from openai import OpenAI
import json
from dotenv import load_dotenv 
from functions.functions_light_industrial import prompt_li_function
from functions.functions_professional import prompt_p_function

load_dotenv()
client = OpenAI()

def calculate_score(job_description, candidate_resume, job_type, score_examples): # api call function to chatgpt
  prompt_guidelines = '' # variable to store the rules of the prompt
  prompt_function = []
  if job_type == 'Light Industrial':  # switch to handle the rules of the prompt
    with open('helpers/light_industrial.txt', 'r') as f:
      prompt_guidelines = f.read()
      prompt_function = prompt_li_function
  elif job_type == 'Professional':
    with open('helpers/professional.txt', 'r') as f:
      prompt_guidelines = f.read()
      prompt_function = prompt_p_function

  score_summary = client.chat.completions.create( # Make API call
    model = "gpt-4-1106-preview", # gpt-3.5-turbo-1106
    seed= 123455555,
    messages = [
      {"role":"system", "content":"You are an expert recruiter for a \
        staffing company that specializes in engineering solutions and \
        IT project management services to Fortune 500 companies in the Life Science and Technology industries.\
        Your job is to evaluate and rank how well a candidate's resume matches a job description\
        based on the guidelines delimited by the triple backticks:"},
      {"role":"user", "content":f"```Job Type: {job_type}"},
      {"role":"user", "content":f"Job Description: {job_description}"},
      {"role":"user", "content":f"Candidate Resume: {candidate_resume}"},
      {"role":"user", "content":f"Scoring Guidelines: {prompt_guidelines}"},
      {"role":"user", "content":f"Scoring Examples: {score_examples}```"},
      {"role":"user", "content":f"Provide a 3-4 sentence summary of the candidate. Include all experience, education \
        certifications and skills listed in their resume. Explain what experience, education, certifications and skills \
        the candidate either posses or does not posses. Explain your reasoning behind the score you gave. Do not mention \
        BEPC in your summary. Refer to the candidate only as candidate, not by their name. Be strict with your scoring. \
        and recommendations, we want the best candidates to be presented to our clients."},
      # {"role":"user", "content":"Create a list of the required categories, specify if the category is required,\
      #   the score you gave, and the explanation for that score given"},
      # {"role":"user", "content":"Create a list of the desired categories, specify if the category is required,\
      #   the score you gave, and the explanation for that score given"},
    ],
    temperature = 0, # The temperature parameter controls the randomness of the generated output.
    functions = prompt_function,
    function_call = {
      "name": "json_answer"
    }
  )

  return json.loads(score_summary.choices[0].message.function_call.arguments) # Extract the summary text from the response