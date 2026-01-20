from langgraph.graph import StateGraph,START,END
from typing import List
from typing_extensions import TypedDict
from Agents import Agent
from State import AgentState

class Workflow:
    def __init__(self):
        self.agent = Agent()
    def graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("Supervisor",self.agent.Supervisor)
        workflow.add_node("information_node",self.agent.information_node)
        workflow.add_node("booking_node",self.agent.booking_node)
        workflow.add_node("information_node_by_doctor",self.agent.information_node_by_doctor)
        workflow.add_node("information_node_by_specialist",self.agent.information_node_by_specialist)
        workflow.add_node("booking_node_for_cancel",self.agent.booking_node_for_cancel)
        workflow.add_node("booking_node_for_set",self.agent.booking_node_for_set)
        workflow.add_node("booking_node_for_reschedule",self.agent.booking_node_for_reschedule)

        workflow.add_edge(START,"Supervisor")
        workflow.add_conditional_edges("Supervisor",self.agent.router,{"information":"information_node","booking":"booking_node","end":END})
        workflow.add_conditional_edges("information_node",self.agent.router_information,{"by_doctor":"information_node_by_doctor","by_specialization":"information_node_by_specialist","end":END})
        workflow.add_edge("information_node_by_doctor",END)
        workflow.add_edge("information_node_by_specialist",END)
        workflow.add_conditional_edges("booking_node",self.agent.router_booking,{"set_booking":"booking_node_for_set",
        "cancel_booking":"booking_node_for_cancel","reschedule_booking":"booking_node_for_reschedule","end":END})

        workflow.add_edge("booking_node_for_cancel",END)
        workflow.add_edge("booking_node_for_set",END)
        workflow.add_edge("booking_node_for_reschedule",END)

        app = workflow.compile()
        return app
    
    def execute(self,input_dict):
        app = self.graph()
        ## example of input_dict
        ## question = "I want to cancel session with doctor john doe on 08-08-2024 15:00 "
        ##inputs = {"question":question,"user_id":1000097.0}
        response = app.invoke(input_dict)
        return response
    


