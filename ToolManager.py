## loading the dataset
import pandas as pd
df = pd.read_csv(r"D:\Doctor_Appointment_System\data\doctor_availability.csv")

from typing import Literal
from langchain_core.tools import tool
from DateTimeModel import DateModel,DateTimeModel,UniqueIdentificationNumber

class ToolManager:
    def __init__(self):
        pass

    @tool
    def check_availibility_by_doctor(self,desired_date:DateModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
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
    def check_availibility_by_specialization(self,desired_date:DateModel,specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
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
    def cancel_appointment(self,date:DateTimeModel,id_number:UniqueIdentificationNumber,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
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
    def set_appointment(self,desired_date:DateTimeModel,id_number:UniqueIdentificationNumber,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
        "tool for setting the appointment with the doctor"
        value = df[(df["date_slot"]==desired_date.date)&(df["is_available"]==True)&(df["doctor_name"]==doctor_name)]
        if len(value) ==0:
            return "There is no availibility of doctor at this time"
        else:
            df.loc[(df["date_slot"]==desired_date.date)&(df["is_available"]==True)&(df["doctor_name"]==doctor_name),["is_available","patient_to_attend"]] = [[False,id_number.id]]
            df.to_csv(r"D:\Doctor_Appointment_System\data\doctor_availability.csv",index=False)
            return "The appointment set successfully"
        
    @tool
    def reschedule_appointment(self,old_date:DateTimeModel,new_date:DateTimeModel,id_number:UniqueIdentificationNumber,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
        "tool for rescheduling the appointment with the doctor"
        rows = df[(df["date_slot"]==new_date.date)&(df["doctor_name"]==doctor_name)&(df["is_available"]==True)]
        if len(rows) ==0:
            return "there is no availibilty of doctors at this time"
        else:
            self.cancel_appointment.invoke({"date":old_date,"id_number":id_number,"doctor_name":doctor_name})
            self.set_appointment.invoke({"desired_date":new_date,"id_number":id_number,"doctor_name":doctor_name})
            return "Successfully rescheduled for the desired time"



    