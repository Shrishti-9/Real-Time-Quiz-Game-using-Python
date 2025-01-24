import requests
import html

parameters = {
    'amount' : 10,
    'type': 'boolean'
}

# Making a GET request to Open Trivia Database to get 10 random questions of type True and False i.e. Boolean
response = requests.get('https://opentdb.com/api.php', params=parameters)
response.raise_for_status() # Checking if an error as occurred
data = response.json() # To fetch data from the API
question_data = data['results'] #Storing required data to question_data
#print(question_data)

question_bank = [] # Empty list

# To append required data ('question' & 'correct_answer') in a list
for i in range(10):
    question_text = html.unescape(question_data[i]['question']) # convert the ascii string into html script by replacing ascii characters with special characters by using html
    #print(question_text)
    question_answer = question_data[i]['correct_answer']
    #print(question_answer)
    question_bank.append({'Question':question_text, 'Answer':question_answer})
    
#print(question_bank)
#print(question_bank[0]['question'])
print(len(question_bank))
