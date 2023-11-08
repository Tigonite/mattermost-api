from typing import Union, List, Dict
from Mattermost_Base import Base


class DataRetention(Base):
    def __init__(self, token: str, server_url: str):
        super().__init__(token, server_url)
        self.api_url = f"{self.base_url}/data_retention"

    def get_policies_applied_to_user_teams(self, user_id: str, page: int, per_page: int) -> dict:
        """
        Gets the policies which are applied to the all of the teams
        to which a user belongs.

        Minimum server version: 5.35
        Must be logged in as the user or have the manage_system permission.
        Requires an E20 license.

        :param user_id:	The ID of the user. This can also be "me" which will
        point to the current user.
        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of policies per page.
        There is a maximum limit of 200 per page.
        :return: Retention policy teams info.
        """
        url = f"{self.base_url}/users/{user_id}/data_retention/team_policies"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)

    def get_policies_applied_to_user_chnls(self, user_id: str, page: int, per_page: int) -> dict:
        """
        Gets the policies which are applied to the all of the channels to which a user belongs.

        Minimum server version: 5.35
        Must be logged in as the user or have the manage_system permission.
        Requires an E20 license.

        :param user_id:	The ID of the user. This can also be "me" which will point to the current user.
        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of policies per page. There is a maximum limit of 200 per page.
        :return: Retention policy channels info.
        """
        url = f"{self.base_url}/users/{user_id}/data_retention/channel_policies"
        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)