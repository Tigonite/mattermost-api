from typing import Union, List, Dict
from Mattermost_Base import Base


class Teams(Base):
    def __init__(self, token: str, server_url: str):
        super().__init__(token, server_url)
        self.api_url = f"{self.base_url}/teams"