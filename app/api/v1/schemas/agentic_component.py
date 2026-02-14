from pydantic import BaseModel


class ComponentSidebarItem(BaseModel):
    type: str
    name: str
    category: str
    icon: str
    color: str

    model_config = {"from_attributes": True}
