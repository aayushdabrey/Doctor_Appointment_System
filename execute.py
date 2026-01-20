from Workflow import Workflow
import warnings
warnings.filterwarnings("ignore")

workflow = Workflow()


##question = "I want to reschedule  session with doctor john doe on  09-08-2024 13:00 which was held on 08-08-2024 12:30"
question = "I want to cancel session with doctor john doe on 09-08-2024 13:00"
question = "I want to set session with doctor john doe on 09-08-2024 13:00"
inputs = {"question":question,"user_id":1000041.0}
inputs = {"question":"I want to set session with doctor john doe on 09-08-2024 13:00","user_id":1000041.0}
response= workflow.execute(inputs)
print(response.get("final_response"))