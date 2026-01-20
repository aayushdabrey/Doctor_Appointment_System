import pandas as pd
import numpy as np
from typing_extensions import TypedDict,Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.tools import tool
from pydantic import BaseModel,Field,field_validator
from model import Model
from State import AgentState
from langchain_core.output_parsers import StrOutputParser

from PromptManager import PromptManager
from DateTimeModel import DateModel,DateTimeModel,UniqueIdentificationNumber
from typing import Literal

import pandas as pd
import os
df = pd.read_csv(os.path.join("data", "doctor_availability.csv"))



class question_check(BaseModel):
    response:str = Field(description = "question belongs to information or booking or nothing")

class information_node_class(BaseModel):
    response:str = Field(description="To which category the question belongs to 'by_doctor','by_specialization, 'end'")

class get_doctor_date(BaseModel):
    doctor_name:str = Field(description="doctor name")
    date:str = Field(descriptio= "date ")
class check_specialist_date(BaseModel):
    specialist:str = Field(description="The particular specialist")
    date:str  = Field(description="The Date where particular specialist is available")

class booking_node_class(BaseModel):
    response:str = Field(description="To which category the booking belongs to 'cancel_booking','set_booking', 'reschedule_booking','end' ")

class booking_cancel(BaseModel):
    doctor_name:str = Field(description="doctor name")
    date:str = Field(description= "date ")

class booking_set(BaseModel): 
    doctor_name:str = Field(description="doctor name")
    date:str = Field(description= "date ")

class booking_reschedule(BaseModel): 
    doctor_name:str = Field(description="doctor name")
    new_date:str = Field(description= " new date for appointment with the doctor")
    old_date:str = Field(description = "old date of appointment with the doctor")

    
@tool
def check_availibility_by_doctor(desired_date:DateModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
        "checking the availibilty of doctor based on date and doctor name"
        df["date_slot_time"] = df["date_slot"].apply(lambda x:x.split(' ')[-1])
        
        rows = list(df[(df["date_slot"].apply(lambda x:x.split(' ')[0])==desired_date.date)&(df["doctor_name"]==doctor_name)&(df["is_available"]==True)]["date_slot_time"])

        if len(rows) == 0:
            output = "No available slots"
        else:

            output = f""" for the given date {desired_date.date} and desired doctor {doctor_name} These are the available slots\n
                        {' '.join(rows)}
                        """
            return output
@tool
def check_availibility_by_specialization(desired_date:DateModel,specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
        "This tool will help to extract information from the dateframe on base of desired date and specialization"

        df["date_slot_time"] = df["date_slot"].apply(lambda x:x.split(" ")[1])

        rows = df[(df["date_slot"].apply(lambda x:x.split(" ")[0])==desired_date.date)&(df["specialization"]==specialization)&(df["is_available"]==True)].groupby(["specialization","doctor_name"])["date_slot_time"].apply(list).reset_index(name = "available_slots")

        if len(rows) == 0:
            output = "No available slots"
            return output
        def value_to_am_pm(value):
            ## value = 14:30 ,just example
            hours,minutes = map(int,value.split(":")) ## [14,30]
            if hours>=12:
                period = "PM"
            else:
                period = "AM"
            hours = hours%12 or hours
            return f"{hours}:{minutes:02d} {period}"
        output = ""
        for row in rows.values:
            value = f"The doctor {row[1]} is available at this slots {' '.join([value_to_am_pm(value) for value in row[2]])}\n\n"
            output = output+value
        return output

 
@tool
def cancel_appointment(date:DateTimeModel,id_number:UniqueIdentificationNumber,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
        "This function is just for cancelling the appointment of the doctor"
    
        rows = df[(df["date_slot"] == date.date)&(df["patient_to_attend"]==id_number.id)&(df["doctor_name"]==doctor_name)]
        if len(rows) == 0:
            output = "There are no available bookings"
            return output
        else:
            df.loc[(df["date_slot"]== date.date)&(df["patient_to_attend"]==id_number.id)&(df["doctor_name"]==doctor_name),["is_available","patient_to_attend"]] = [[True,None]]
            df.to_csv(r"D:\Doctor_Appointment_System\data\doctor_availability.csv",index=False)
            return "Successfully cancelled"
    
        
@tool
def set_appointment(desired_date:DateTimeModel,id_number:UniqueIdentificationNumber,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
        "tool for setting the appointment with the doctor"
        value = df[(df["date_slot"]==desired_date.date)&(df["is_available"]==True)&(df["doctor_name"]==doctor_name)]
        if len(value) ==0:
            return "There is no availibility of doctor at this time"
        else:
            df.loc[(df["date_slot"]==desired_date.date)&(df["is_available"]==True)&(df["doctor_name"]==doctor_name),["is_available","patient_to_attend"]] = [[False,id_number.id]]
            df.to_csv(r"D:\Doctor_Appointment_System\data\doctor_availability.csv",index=False)
            return "The appointment set successfully"
    
       
@tool
def reschedule_appointment(old_date:DateTimeModel,new_date:DateTimeModel,id_number:UniqueIdentificationNumber,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    "tool for rescheduling the appointment with the doctor"
    rows = df[(df["date_slot"]==new_date.date)&(df["doctor_name"]==doctor_name)&(df["is_available"]==True)]
    if len(rows) ==0:
        return "there is no availibilty of doctors at this time"
    else:
        cancel_appointment.invoke({"date":old_date,"id_number":id_number,"doctor_name":doctor_name})
        set_appointment.invoke({"desired_date":new_date,"id_number":id_number,"doctor_name":doctor_name})
        return "Successfully rescheduled for the desired time"


class Agent:
    def __init__(self):
        self.model = Model()
        self.llm = self.model.get()
        self.prompts = PromptManager() 
       
   
    

        
    
    def Supervisor(self,State:AgentState):
        prompt = ChatPromptTemplate.from_messages(
            [("system",self.prompts.get_system_prompt_for_supervisor()),
            ("human","{question}")]
        )
        question_checker = prompt | self.llm.with_structured_output(question_check)
        question = State.get("question",None)
        if question == None:
            raise Exception("The question not found in the supervisor")
        if question:
            respond = question_checker.invoke({"question":question}).response
        else:
            raise Exception("User question is not given")
        return {"question":question,"next":respond}
    

    def router(self,state:AgentState):
        next = state.get("next",None)
        if next == None:
            raise Exception("next not found in router!")
        if next == "information":
            return "information"
        elif next == "booking":
            return "booking"
        else:
            return "end"
    
    def information_node(self,state:AgentState):
        question = state.get("question",None)
       
        if question == None:
            raise Exception("question not found in information node")
        
        prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_system_prompt_for_information_node()),
        ("human","{question}")]
        )

        information_checker = prompt | self.llm.with_structured_output(information_node_class)

        respond = information_checker.invoke({"question":question}).response

        return {"question":question,"information_respond":respond}
    
    def router_information(self,state:AgentState):
        information_respond = state.get("information_respond",None)
        if information_respond == None:
            raise Exception("Information respond not found")
        if information_respond == "by_doctor":
            return "by_doctor"
        elif information_respond == "by_specialization":
            return "by_specialization"
        else:
            return "end"
    
    
    def information_node_by_doctor(self,state:AgentState):
        question = state.get("question",None)
        if question == None:
            raise Exception("the question not found in information node by doctor")
     
        
        system_prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_prompt_for_information_node_by_doctor()),
        ("human","{question}")]
        )
        fetcher = system_prompt | self.llm.with_structured_output(get_doctor_date)
        response = fetcher.invoke({"question":question})
        doctor_name = response.doctor_name
        date = response.date

        output = check_availibility_by_doctor.invoke({"desired_date":{"date":date},"doctor_name":doctor_name})
      



        system_prompt_2 = ChatPromptTemplate.from_messages([
        ("system", self.prompts.get_prompt_respond_for_information_node_by_doctor()),
        ("human", "Question: {question}\nData: {data}")
        ] )

        agent = system_prompt_2 | self.llm | StrOutputParser()
        final_response = agent.invoke({"question": question, "data": output})

        return {"data":output,"final_response": final_response}
    

    def information_node_by_specialist(self,state:AgentState):
        question = state.get("question",None)
        if question == None:
            raise Exception("The question not found in information node by specialist")
        
        system_prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_prompt_for_information_node_by_specialist()),
        ("human","{question}")]
        )
        fetcher = system_prompt | self.llm.with_structured_output(check_specialist_date)
        response = fetcher.invoke({"question":question})
        specialist = response.specialist
        date = response.date

        output = check_availibility_by_specialization.invoke({"desired_date":{"date":date},'specialization':specialist})


        system_prompt_2 = ChatPromptTemplate.from_messages([
        ("system", self.prompts.get_prompt_respond_for_information_node_by_specialist()),
        ("human", "Question: {question}\nData: {data}")
        ] )

        agent = system_prompt_2 | self.llm | StrOutputParser()
        final_response = agent.invoke({"question": question, "data": output})

        return {"data":output,"final_response": final_response}
    
    
    def booking_node(self,state:AgentState):
        question = state.get("question",None)
        if question == None:
            raise Exception("The question not found on booking node")

        prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_system_prompt_for_booking_node()),
        ("human","{question}")]
        )

        information_checker = prompt | self.llm.with_structured_output(booking_node_class)

        respond = information_checker.invoke({"question":question}).response

        return {"question":question,"booking_respond":respond}
    
    def router_booking(self,state:AgentState):
        booking_respond = state.get('booking_respond',None)
        if booking_respond == None:
            raise Exception("booking_respond not found in router booking")
        if booking_respond == "set_booking":
            return "set_booking"
        elif booking_respond == "cancel_booking":
            return "cancel_booking"
        elif booking_respond == "reschedule_booking":
            return "reschedule_booking"
        elif booking_respond == "end":
            return "end"
    

    def booking_node_for_cancel(self,state:AgentState):
        question = state.get("question",None)
        if question == None:
            raise Exception("The question not found in booking_node_for_cancel")
        user_id = state.get("user_id",None)
        if user_id == None:
            raise Exception("The user_id not found in booking_node_for_cancel")
        
        
        system_prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_prompt_for_booking_node_for_cancel()),
        ("human","{question}")]
        )
        fetcher = system_prompt | self.llm.with_structured_output(booking_cancel)
        response = fetcher.invoke({"question":question})
        doctor_name = response.doctor_name
        date = response.date
        output = cancel_appointment.invoke({"date":{"date":date},"doctor_name":doctor_name,"id_number":{"id":int(user_id)}})

        system_prompt_2 = ChatPromptTemplate.from_messages([
        ("system", self.prompts.get_prompt_respond_for_booking_node_for_cancel()),
        ("human", "Question: {question}\nData: {data}")
        ] )

        agent = system_prompt_2 | self.llm | StrOutputParser()
        final_response = agent.invoke({"question": question, "data": output})

        return {"data":output,"final_response": final_response}

    def booking_node_for_set(self,state:AgentState):
        question = state.get("question",None)
        if question == None:
            raise Exception("The question not found in booking_node_for_set")
        user_id = state.get("user_id",None)
        if user_id == None:
            raise Exception("The user_id not found in booking_node_for_set")
        
        
        system_prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_prompt_for_booking_node_for_set()),
        ("human","{question}")]
        )
        fetcher = system_prompt | self.llm.with_structured_output(booking_cancel)
        response = fetcher.invoke({"question":question})
        doctor_name = response.doctor_name
        date = response.date
    
        output = set_appointment.invoke({"desired_date":{"date":date},"doctor_name":doctor_name,"id_number":{"id":int(user_id)}})

        system_prompt_2 = ChatPromptTemplate.from_messages([
        ("system", self.prompts.get_prompt_respond_for_booking_node_for_set()),
        ("human", "Question: {question}\nData: {data}")
        ] )

        agent = system_prompt_2 | self.llm | StrOutputParser()
        final_response = agent.invoke({"question": question, "data": output})

        return {"data":output,"final_response": final_response}
    

    def booking_node_for_reschedule(self,state:AgentState):
        question = state.get("question",None)
        if question == None:
            raise Exception("The question not found in booking_node_for_reschedule")
        user_id = state.get("user_id",None)
        if user_id == None:
            raise Exception("The user_id not found in booking_node_for_reschedule")
        
    
        
        system_prompt = ChatPromptTemplate.from_messages(
        [("system",self.prompts.get_prompt_for_booking_node_for_reschedule()),
        ("human","{question}")]
        )
        fetcher = system_prompt | self.llm.with_structured_output(booking_reschedule)
        response = fetcher.invoke({"question":question})
        doctor_name = response.doctor_name
        old_date = response.old_date
        new_date = response.new_date
    
        output = reschedule_appointment.invoke({"old_date":{"date":old_date},"new_date":{"date":new_date},"doctor_name":doctor_name,"id_number":{"id":int(user_id)}})

        system_prompt_2 = ChatPromptTemplate.from_messages([
        ("system", self.prompts.get_prompt_respond_for_booking_node_for_reschedule()),
        ("human", "Question: {question}\nData: {data}")
        ] )

        agent = system_prompt_2 | self.llm | StrOutputParser()
        final_response = agent.invoke({"question": question, "data": output})

        return {"data":output,"final_response": final_response}
            
