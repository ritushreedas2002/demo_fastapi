from pydantic import BaseModel
from typing import List,Optional,Union
class BlogModel(BaseModel):
    title:str
    sub_title:str
    content:str
    author:str
    tags:list
    

class UpdateBlogModel(BaseModel):
    title:Union[str,None]=None
    sub_title:Optional[str]=None
    content:Optional[str]=None
    author:Optional[str]=None
    tags:Optional[list]=None
    

