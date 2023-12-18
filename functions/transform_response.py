# this function transforms the output from the response as readable strings for easy coding and formatting
import os
def transform_response(
  requirements_table, 
  desired_elements_table,
  job_type
  ):

  requirements_table_start = '<p><table class="table"><tr><th>Category</th><th>Score</th><th>Explanation</th></tr>'
  requirements_table_middle = ''
  requirements_table_end = '</table></p>'

  desired_table_start = '<p><table class="table"><tr><th>Category</th><th>Score</th><th>Explanation</th></tr>'
  desired_table_middle = ''
  desired_table_end = '</table></p>'

  req_rating = 0
  pref_rating = 0
  additional_counter_req = 0
  additional_counter_pref = 0

  os.system('cls')

  if job_type == 'Light Industrial':
    print('----------------REQUIRED ELEMENTS----------------')
    for req_key, req_value in requirements_table.items(): #this first loop is just for the additional counter
      print(req_key, req_value)
      print('-------------------------------------------------')
      if req_value['measurable'] == True:
        additional_counter_req += 1

    for req_key, req_value in requirements_table.items(): #this is the loop that will calculate the rating and build a table
      if req_value['measurable'] == True:
        req_rating += req_value['score'] / additional_counter_req
        requirements_table_middle += '<tr>'
        new_row = '<td>'+ req_key +'</td><td>' + str(round((req_value['score'] / additional_counter_req), 1)) + '</td><td>' + req_value['explanation'] + '</td>'
        requirements_table_middle += new_row
        requirements_table_middle += '</tr>'   

    print('----------------DESIRED ELEMENTS-----------------')
    for req_key, req_value in desired_elements_table.items(): #this first loop is just for the additional counter
      print(req_key, req_value)
      print('-------------------------------------------------')
      if req_value['measurable'] == True:
        additional_counter_pref += 1

    for req_key, req_value in desired_elements_table.items(): #this is the loop that will calculate the rating and build a table
      if req_value['measurable'] == True:
        pref_rating += req_value['score'] / additional_counter_pref
        desired_table_middle += '<tr>'
        new_row = '<td>'+ req_key +'</td><td>' + str(round((req_value['score'] / additional_counter_pref), 1)) + '</td><td>' + req_value['explanation'] + '</td>'
        desired_table_middle += new_row
        desired_table_middle += '</tr>'
    if additional_counter_pref == 0:
      req_rating = 0
      desired_table_middle += '<tr>'
      new_row = '<td>All</td><td>10</td><td>The job description does not specify any required elements.</td>'
      desired_table_middle += new_row
      desired_table_middle += '</tr>'
      
  if job_type == 'Professional':
    print('----------------REQUIRED ELEMENTS----------------')
    for req_key, req_value in requirements_table.items(): #this first loop is just for the additional counter
      print(req_key, req_value)
      print('-------------------------------------------------')
      if req_value['measurable'] == True:
        additional_counter_req += 1
    
    for req_key, req_value in requirements_table.items(): #this is the loop that will calculate the rating and build a table
      if req_value['measurable'] == True:
        req_rating += req_value['score'] / additional_counter_req
        requirements_table_middle += '<tr>'
        new_row = '<td>'+ req_key +'</td><td>' + str(round((req_value['score'] / additional_counter_req), 1)) + '</td><td>' + req_value['explanation'] + '</td>'
        requirements_table_middle += new_row
        requirements_table_middle += '</tr>'
    
    print('----------------DESIRED ELEMENTS-----------------')
    for req_key, req_value in desired_elements_table.items(): #this first loop is just for the additional counter
      print(req_key, req_value)
      print('-------------------------------------------------')
      if req_value['measurable'] == True:
        additional_counter_pref += 1
    for req_key, req_value in desired_elements_table.items(): #this is the loop that will calculate the rating and build a table
      if req_value['measurable'] == True:
        pref_rating += req_value['score'] / additional_counter_pref
        desired_table_middle += '<tr>'
        new_row = '<td>'+ req_key +'</td><td>' + str(round((req_value['score'] / additional_counter_pref), 1)) + '</td><td>' + req_value['explanation'] + '</td>'
        desired_table_middle += new_row
        desired_table_middle += '</tr>'
    if additional_counter_pref == 0:
      pref_rating = 0
      desired_table_middle += '<tr>'
      new_row = '<td>All</td><td>10</td><td>The job description does not specify any preferred elements.</td>'
      desired_table_middle += new_row
      desired_table_middle += '</tr>'

  requirements_table_full = requirements_table_start + requirements_table_middle + requirements_table_end
  desired_table_full = desired_table_start + desired_table_middle + desired_table_end

  if not(isinstance(req_rating, int)): #this turns the score from float into int if its an integer
    if req_rating.is_integer():
      req_rating = int(req_rating)
    else:
      req_rating = round(req_rating, 1)
  
  if not(isinstance(pref_rating, int)): #this turns the score from float into int if its an integer
    if pref_rating.is_integer():
      pref_rating = int(pref_rating)
    else:
      pref_rating = round(pref_rating, 1)

  transformed_response = dict()
  transformed_response['requirements_table'] = requirements_table_full
  transformed_response['requirements_rating'] = req_rating
  transformed_response['desired_elements_table'] = desired_table_full
  transformed_response['preferences_rating'] = pref_rating
  transformed_response['overall_score'] = round((req_rating * 0.7) + (pref_rating * 0.3) / (0.7 + 0.3), 1)

  return transformed_response