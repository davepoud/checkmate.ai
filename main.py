from dotenv import load_dotenv
from openai import OpenAI, WebSocketQueueFullError
import json
from datetime import datetime, date, timezone
from pydantic import BaseModel
    

def write_to(input_file, data):
    with open(input_file, mode = 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def read_from(input_file):
    with open(input_file, mode = 'r', encoding = "utf-8") as file:
        file_data = json.load(file)
        return file_data


def current_date():
    datetd = date.today()
    return datetd

today = current_date()


dev_prompt = [
        {"role": "system",
         "content":(
             f"You are a data analyst that is storing information into a to do list, todays date is {today}, you need to return a dictionary with 3 values: that strictly follow this format: what:the task, when: month day, year and time (optionally) and where:location if you are missing date or location or time that is completely fine, ignore those values. Only ask for clarification if the task itself is missing")}
         ]

message_history = []


class Reminder(BaseModel):
    what: str
    when: str
    where: str
      

print("define your reminder, at any point let me know if you want to exit")
while True: 
    user_input = input()
        
    if user_input.strip().lower() in ["exit", "quit", "done"]:
        print("Ending chat and saving reminder...")
        break

    message_history.append({"role":"user", "content":user_input})
# Loads variables from .env into the environment
    load_dotenv()

# Automatically uses os.environ.get("OPENAI_API_KEY")
    client = OpenAI()

    response = client.responses.parse(
        model="gpt-6-luna", 
        input = dev_prompt + message_history,
        text_format = Reminder,

        )
    
    reminder_obj = response.output_parsed

    raw_data_list = read_from("to_do.json")
    raw_data_list.append(reminder_obj.model_dump())
    write_to("to_do.json", raw_data_list)

for val in raw_data_list:
    print(f"{val["what"]} {val["where"]} {val["when"]}") 
 
