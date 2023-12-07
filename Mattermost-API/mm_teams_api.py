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
        For regular users only returns open teams. Users with the "manage_system" permission will
        return teams regardless of type. The result is based on query string parameters - page and per_page.

        Must be authenticated. "manage_system" permission is required to show all teams.

        :param page: Default: 0. The page to select.
        :param per_page: Default: 60.  The number of teams per page.
        :param include_total_count: Default: false. Appends a total count of returned teams inside
        the response object - ex: { "teams": [], "total_count" : 0 }.
        :param exclude_policy_constrained: Default: false. If set to true, teams which are part of a
        data retention policy will be excluded.
        The sysconsole_read_compliance permission is required to use this parameter. Minimum server version: 5.35
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

    def get_team(self, team_id: str) -> dict:
        """
        Get a team on the system.

        Must be authenticated and have the view_team permission.

        :param team_id: Team GUID.
        :return: Team retrieval info.
        """

        url = f"{self.api_url}/{team_id}"

        self.reset()

        return self.request(url, request_type='GET')

    def update_team(self,
                    team_id: str,
                    id: str,
                    display_name: str,
                    description: str,
                    company_name: str,
                    allowed_domains: str,
                    invite_id: str,
                    allow_open_invite: str) -> dict:
        """
        Update a team by providing the team object. The fields that can be updated are defined in the request body,
        all other provided fields will be ignored.

        Must have the manage_team permission.

        :param team_id: Team GUID.
        :param id: Team ID to update.
        :param display_name: Team display name to update.
        :param description: Team description to update.
        :param company_name: Team company name to update.
        :param allowed_domains: Team allowed domains to update.
        :param invite_id: Team invite ID to update.
        :param allow_open_invite: Team allow_open invite to update.
        :return: Team update info.
        """

        url = f"{self.api_url}/{team_id}"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('team_id', team_id)
        self.add_to_json('id', id)
        self.add_to_json('display_name', display_name)
        self.add_to_json('description', description)
        self.add_to_json('company_name', company_name)
        self.add_to_json('allowed_domains', allowed_domains)
        self.add_to_json('invite_id', invite_id)
        self.add_to_json('allow_open_invite', allow_open_invite)

        return self.request(url, request_type='PUT', body=True)

    def delete_team(self,
                    team_id: str,
                    permanent: bool = None) -> dict:
        """
        Soft deletes a team, by marking the team as deleted in the database. Soft deleted teams will
        not be accessible in the user interface.

        Optionally use the permanent query parameter to hard delete the team for compliance reasons.
        As of server version 5.0, to use this feature ServiceSettings.EnableAPITeamDeletion
        must be set to true in the server's configuration.

        Must have the manage_team permission.

        :param team_id: Team GUID.
        :param permanent: Default: false. Permanently delete the team, to be used for compliance reasons only.
        As of server version 5.0, ServiceSettings.EnableAPITeamDeletion must
        be set to true in the server's configuration.
        :return: Team deletion info.
        """

        url = f"{self.api_url}/{team_id}"

        self.reset()
        self.add_application_json_header()
        if permanent is not None:
            self.add_to_json('permanent', permanent)

        return self.request(url, request_type='DEL', body=True)

    def patch_team(self,
                   team_id: str,
                   display_name: str,
                   description: str,
                   company_name: str,
                   invite_id: str,
                   allow_open_invite: bool) -> dict:
        """
        Partially update a team by providing only the fields you want to update. Omitted fields will not be updated.
        The fields that can be updated are defined in the request body, all other provided fields will be ignored.

        Must have the manage_team permission.

        :param team_id: Team GUID
        :param display_name: Team display name that is to be updated.
        :param description: Team description that is to be updated.
        :param company_name: Team company_name that is to be updated.
        :param invite_id: Team invite ID that is to be updated.
        :param allow_open_invite: Team allow open invite that is to be updated.
        :return: Team deletion info.
        """

        url = f"{self.api_url}/{team_id}/patch"

        self.reset()
        self.add_application_json_header()
        if display_name is not None:
            self.add_to_json('display_name', display_name)
        if description is not None:
            self.add_to_json('description', description)
        if display_name is not None:
            self.add_to_json('company_name', company_name)
        if display_name is not None:
            self.add_to_json('invite_id', invite_id)
        if display_name is not None:
            self.add_to_json('allow_open_invite', allow_open_invite)

        return self.request(url, request_type='PUT', body=True)

    def update_team_privacy(self,
                            team_id: str,
                            privacy: str) -> dict:
        """
        Updates team's privacy allowing changing a team from Public (open) to Private (invitation only) and back.

        Minimum server version: 5.24

        manage_team permission for the team of the team.

        :param team_id: Team GUID.
        :param privacy: Team privacy setting: 'O' for a public (open) team, 'I' for a private (invitation only) team.
        :return: Team conversion info.
        """

        url = f"{self.api_url}/{team_id}/privacy"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('privacy', privacy)

        return self.request(url, request_type='PUT', body=True)

    def restore_team(self, team_id: str) -> dict:
        """
        Restore a team that was previously soft deleted.

        Minimum server version: 5.24

        Must have the manage_team permission.

        :param team_id: Team GUID
        :return: Team restore info.
        """

        url = f"{self.api_url}/{team_id}/restore"

        self.reset()
        self.add_application_json_header()

        return self.request(url, request_type='POST')

    def get_team_by_name(self, name: str) -> dict:
        """
        Get a team based on provided name string

        Must be authenticated, team type is open and have the view_team permission.

        :param name: Team Name
        :return: Team retrieval info.
        """

        url = f"{self.api_url}/name/{name}"

        self.reset()
        self.add_application_json_header()

        return self.request(url, request_type='GET')

    def search_teams(self,
                     term: str = None,
                     page: str = None,
                     per_page: str = None,
                     allow_open_invite: bool = None,
                     group_constrained: bool = None,
                     exclude_policy_constrained: bool = None) -> dict:
        """
        Search teams based on search term and options provided in the request body.

        Logged in user only shows open teams Logged in user with "manage_system" permission shows all teams.

        :param term: The search term to match against the name or display name of teams
        :param page: The page number to return, if paginated. If this parameter is not present with the
        per_page parameter then the results will be returned un-paged.
        :param per_page: The number of entries to return per page, if paginated.
        If this parameter is not present with the page parameter then the results will be returned un-paged.
        :param allow_open_invite: Filters results to teams where allow_open_invite is set to true or false,
        excludes group constrained channels if this filter option is passed. If this filter option is not passed
        then the query will remain unchanged. Minimum server version: 5.28
        :param group_constrained: Filters results to teams where group_constrained is set to true or false,
        returns the union of results when used with allow_open_invite If the filter option is not passed then
        the query will remain unchanged. Minimum server version: 5.28
        :param exclude_policy_constrained: Default: false. If set to true, only teams which do not
        have a granular retention policy assigned to them will be returned.
        The sysconsole_read_compliance_data_retention permission is required to use this parameter.
        Minimum server version: 5.35
        :return: Paginated team info.
        """

        url = f"{self.api_url}/search"

        self.reset()
        self.add_application_json_header()
        if term is not None:
            self.add_to_json('term', term)
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)
        if allow_open_invite is not None:
            self.add_to_json('allow_open_invite', allow_open_invite)
        if group_constrained is not None:
            self.add_to_json('group_constrained', group_constrained)
        if exclude_policy_constrained is not None:
            self.add_to_json('exclude_policy_constrained', exclude_policy_constrained)

        return self.request(url, request_type='POST', body=True)

    def check_if_team_exists(self, name: str) -> dict:
        """
        Check if the team exists based on a team name.

        Must be authenticated.

        :param name: Team Name
        :return: Team retrieval info
        """

        url = f"{self.api_url}/name/{name}/exists"

        self.reset()

        return self.request(url, request_type='GET')
