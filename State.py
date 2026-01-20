from typing import List, Tuple, Annotated
from typing_extensions import TypedDict
from operator import add

class AgentState(TypedDict):
    question:str ## this will be the question asked by the user
    user_id:int
    next:str ## based on the user question we will find know either this user question belongs to information_node or booking_node\
    information_respond:str ## it will tell to which category the information based question belongs to like by_doctor or by_specialization
    booking_respond:str ## it will tell you to which category the booking based question belongs to that is setting or cancelling or rescheduling
    data:str
    final_response:str

