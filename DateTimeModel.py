import re
from pydantic import BaseModel,Field,field_validator

class DateTimeModel(BaseModel):
    date:str = Field(description="properly fomatted date",pattern = r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$')

    @field_validator("date")
    def date_validator(cls,value):
        if not re.match(r'^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$',value):
            raise ValueError(f"Date must me in correct format 'DD-MM-YYYY HH:MM':{value}")
        else:
            return value

class DateModel(BaseModel):
    date:str = Field(description="properly formatted date",pattern = r'^\d{2}-\d{2}-\d{4}$')
    @field_validator("date")
    def date_validator(cls,value):
        if not re.match(r'^\d{2}-\d{2}-\d{4}',value):
            raise ValueError(f"Date must be in correct format 'DD-MM-YYYY':{value}")
        else:
            return value

class UniqueIdentificationNumber(BaseModel):
    id:int = Field(description = "a unique number withe 7 or 8 digits")
    @field_validator("id")
    def id_validator(cls,value):
        if not re.match(r'^\d{7,8}$',str(value)):
            raise ValueError("The value must be of 7 or 8 digits")
        return value
    
    