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

    def get_teams(self,
                  page: int = None,
                  per_page: int = None,
                  include_total_count: bool = None,
                  exclude_policy_constrained: bool = None) -> dict:
        """
        For regular users only returns open teams. Users with the "manage_system" permission will return teams regardless of type. The result is based on query string parameters - page and per_page.

        Must be authenticated. "manage_system" permission is required to show all teams.

        :param page: Default: 0. The page to select.
        :param per_page: Default: 60.  The number of teams per page.
        :param include_total_count: Default: false. Appends a total count of returned teams inside the response object - ex: { "teams": [], "total_count" : 0 }.
        :param exclude_policy_constrained: Default: false. If set to true, teams which are part of a data retention policy will be excluded. The sysconsole_read_compliance permission is required to use this parameter. Minimum server version: 5.35
        :return: Team list retrieval info.
        """

        url = f"{self.api_url}"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)
        if include_total_count is not None:
            self.add_to_json('include_total_count', include_total_count)
        if exclude_policy_constrained is not None:
            self.add_to_json('exclude_policy_constrained', exclude_policy_constrained)

        return self.request(url, request_type='GET', body=True)


