from typing import Union, List, Dict
from Mattermost_Base import Base


class Teams(Base):
    def __init__(self, token: str, server_url: str):
        super().__init__(token, server_url)
        self.api_url = f"{self.base_url}/teams"

    def create_team(self,
                    name: str,
                    display_name: str,
                    t_type: str) -> dict:
        """
        Create a new team on the system.

        Must be authenticated and have the create_team permission.

        :param name: Unique handler for a team, will be present in the team URL.
        :param display_name: Non-unique UI name for the team.
        :param t_type: 'O' for open, 'I' for invite only.
        :return: Team creation info.
        """

        url = f"{self.api_url}"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('name', name)
        self.add_to_json('display_name', display_name)
        self.add_to_json('type', t_type)

        return self.request(url, request_type='POST', body=True)