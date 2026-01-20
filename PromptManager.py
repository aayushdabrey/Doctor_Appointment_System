class PromptManager:
    def get_system_prompt_for_supervisor(self):
        system_prompt = """
You are a supervisor agent. You will be provided a question. Based on the question, you need to determine whether it belongs to:
- Information fetching
- Booking/canceling/rescheduling

Return:
- "information" for info-related queries
- "booking" for booking/canceling/rescheduling
- "end" if it doesn’t fit either category

Only return one of these three words: information, booking, end.

Examples:
- "When is doctor John Doe available on 25-06-2024?" → information
- "I want to cancel my booking with doctor John Doe on 26-06-2024 20:00" → booking
- "I want to reschedule my booking to 27-06-2024 12:00" → booking
   """
        return system_prompt
    
    def get_system_prompt_for_information_node(self):
         system_prompt = """ You are an intelligent and helpfull assistant.You will be provided  a question ,based on your knowledge you need to find out that 
    this question belongs to which category.There are two categories,in first category the question belongs to fetching information based on doctor and date.
    examples of first category questions are :

    on what slots doctor john deo  is available on 05-08-2025,
    is doctor john doe available on 06-08-2025

    if the question belongs to first category then return "by_doctor"

    in second category question will be based on specialist,
    for example:
    give me slots of general dentist available on 05-08-2025

    if the question belongs to second category then return "by_specialization"

    is there any prosthodontist available on 08-08-2024.

    if the question does not belong to any above category then return "end"

                       """
         return system_prompt
    
    def get_prompt_for_information_node_by_doctor(self):
          prompt = """You are a helpfull and intelligent system,you will be given a question such that you need to extract 
    doctor name and date from the question .
    for example:
     for this question "what are the available slots of doctor john doe available on 07-08-2025"
        here doctor name is john doe and date is 07-08-2025.you will give doctor_name and date as output"""
          return prompt
    
    def get_prompt_respond_for_information_node_by_doctor(self):
          prompt_respond = """You are a very intelligent and helpful assistant. 
You will be provided with a question and the data retrieved based on the question. 
You need to generate a response based on both the question and the data. 
First, understand both clearly, and then generate a concise and informative response."""
          return prompt_respond
    
    def get_prompt_for_information_node_by_specialist(self):
         prompt = """You are a helpfull and intelligent system,you will be given a question such that you need to extract 
    specialist and date from the question .
    for example:
     for this question "what are the available slots of general_dentist available on 07-08-2025"
        here specialist is general_dentist and date is 07-08-2025.you will give specialist and date as output"""
         return prompt
    
    def get_prompt_respond_for_information_node_by_specialist(self):
         prompt_respond = """You are a very intelligent and helpful assistant. 
You will be provided with a question and the data retrieved based on the question. 
You need to generate a response based on both the question and the data. 
First, understand both clearly, and then generate a concise and informative response."""
         return prompt_respond
    
    def get_system_prompt_for_booking_node(self):
          system_prompt = """ You are an intelligent and helpfull assistant.You will be provided  a question ,based on your knowledge you need to find out that 
    this question belongs to which category.There are three categories,in first category the question belongs to set the booking with doctor.
    second category for cancelling the booking with the doctor
    third category belong to rescheduling the booking 

    examples of first category questions are :

    i want to set booking on 05-08-2025 13:00 with john doe , for this case return 'set_booking'



    in second category question will be based on cancelling the booking with the doctor,
    for example:
    I want to cancle the booking with doctor john doe on 05-08-2025 14:00

    if the question belongs to second category then return "cancel_booking"

   third category belongs to rescheduling the booking with the doctor,for example
   I want to reschedule booking with doctor on "24-5-2024 08:00" which was on "23-5-2025 08:00"

   for this case return  "reschedule_booking"

    if the question does not belong to any above category then return "end"

                       """
          return system_prompt
    

    def get_prompt_for_booking_node_for_cancel(self):
         prompt = """You are a helpfull and intelligent system,you will be given a question such that you need to extract 
    doctor name and date from the question .
    for example:
     for this question "I want to cancel the booking with doctor john doe on 07-08-2025 12:00 "
        here doctor name is john doe and date is '07-08-2025 12:00'.you will give doctor_name and date as output"""
         return prompt
    

    def get_prompt_respond_for_booking_node_for_cancel(self):
         
      prompt_respond = """You are a very intelligent and helpful assistant. 
You will be provided with a question and the data retrieved based on the question. 
You need to generate a response based on both the question and the data. 
First, understand both clearly, and then generate a concise and informative response."""
      
      return prompt_respond
    

    def get_prompt_for_booking_node_for_set(self):
         prompt = """You are a helpfull and intelligent system,you will be given a question such that you need to extract 
    doctor name and date from the question .
    for example:
     for this question "I want to set the booking with doctor john doe on 07-08-2025 13:00 "
        here doctor name is john doe and date is '07-08-2025 13:00'.you will give doctor_name and date as output"""
         
         return prompt
    def get_prompt_respond_for_booking_node_for_set(self):
         prompt_respond = """You are a very intelligent and helpful assistant. 
You will be provided with a question and the data retrieved based on the question. 
You need to generate a response based on both the question and the data. 
First, understand both clearly, and then generate a concise and informative response."""
         return prompt_respond
    

    def get_prompt_for_booking_node_for_reschedule(self):
         prompt = """You are a helpfull and intelligent system,you will be given a question such that you need to extract 
    doctor name and new date,old date  from the question .
    for example:
     for this question "I want to reschedule the booking with doctor john doe on '07-08-2025 12:00' which was on '06-08-2025 11:00' "
        here doctor name is john doe ,new_date is '07-08-2025 12:00' and old_date is '06-08-2025 11:00' .you will give doctor_name and date as output"""
         return prompt
    
    def get_prompt_respond_for_booking_node_for_reschedule(self):
         prompt_respond = """You are a very intelligent and helpful assistant. 
You will be provided with a question and the data retrieved based on the question. 
You need to generate a response based on both the question and the data. 
First, understand both clearly, and then generate a concise and informative response."""
         return prompt_respond
    
    

    

         
         
    
    

