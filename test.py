from ToolManager import ToolManager
tools = ToolManager()
print(tools.check_availibility_by_doctor.invoke({"desired_date":{"date":"08-08-2024"},"doctor_name":"john doe"}))