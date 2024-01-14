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
        :param allow_open_invite: Team allow open invite to update.
        :return: Team update info.
        """

        url = f"{self.api_url}/{team_id}"

        self.reset()
        self.add_application_json_header()
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
        :return: Team patch info.
        """

        url = f"{self.api_url}/{team_id}/patch"

        self.reset()
        self.add_application_json_header()
        if display_name is not None:
            self.add_to_json('display_name', display_name)
        if description is not None:
            self.add_to_json('description', description)
        if company_name is not None:
            self.add_to_json('company_name', company_name)
        if invite_id is not None:
            self.add_to_json('invite_id', invite_id)
        if allow_open_invite is not None:
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

        Logged-in user only shows open teams Logged-in user with "manage_system" permission shows all teams.

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

    def get_user_teams(self, user_id: str) -> dict:
        """
        Get a list of teams that a user is on.

        Must be authenticated as the user or have the manage_system permission.

        :param user_id: User GUID
        :return: Team list retrieval info
        """

        url = f"{self.api_url}/{user_id}/teams"

        self.reset()

        return self.request(url, request_type='GET')

    def get_team_members(self,
                         team_id: str,
                         page: int = None,
                         per_page: int = None) -> dict:
        """
        Get a page team members list based on query string parameters - team id, page and per page.

        Must be authenticated and have the view_team permission.

        :param team_id: Team GUID
        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of users per page.
        :return: Team members retrieval info
        """

        url = f"{self.api_url}/{team_id}/members"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)

    def add_user_to_team(self,
                         team_id: str,
                         t_id: str = None,
                         user_id: str = None) -> dict:
        """
        Add user to the team by user_id.

        Must be authenticated and team be open to add self. For adding another user, authenticated user must have the add_user_to_team permission.

        :param team_id: Team GUID
        :param t_id: Team GUID
        :param user_id: user GUID
        :return: Team members creation info
        """

        url = f"{self.api_url}/{team_id}/members"

        self.reset()
        self.add_application_json_header()
        if t_id is not None:
            self.add_to_json('team_id', t_id)
        if user_id is not None:
            self.add_to_json('user_id', user_id)

        return self.request(url, request_type='POST', body=True)

    def add_user_to_team_from_invite(self, token: str) -> dict:
        """
        Using either an invite id or hash/data pair from an email invite link, add a user to a team.

        Must be authenticated.

        :param token: Token id from the invitation
        :return: Team members creation info
        """

        url = f"{self.api_url}/members/invite"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('token', token)

        return self.request(url, request_type='GET', body=True)

    def add_multiple_users_to_team(self,
                                   team_id: str,
                                   graceful: bool = None,
                                   t_id: str = None,
                                   user_id: str = None,
                                   roles: str = None,
                                   delete_at: int = None,
                                   scheme_user: bool = None,
                                   scheme_admin: bool = None,
                                   explicit_roles: str = None
                                   ) -> dict:
        """
        Add a number of users to the team by user_id.

        Must be authenticated. Authenticated user must have the add_user_to_team permission.

        :param team_id: Team GUID.
        :param graceful: Instead of aborting the operation if a user cannot be added,
        return an array that will contain both the success and added members and the ones with error,
        in form of [{"member": {...}, "user_id", "...", "error": {...}}]
        :param t_id: The ID of the team this member belongs to.
        :param user_id: The ID of the user this member relates to.
        :param roles: The complete list of roles assigned to this team member,
        as a space-separated list of role names, including any roles granted implicitly through permissions schemes.
        :param delete_at: The time in milliseconds that this team member was deleted.
        :param scheme_user: Whether this team member
        holds the default user role defined by the team's permissions scheme.
        :param scheme_admin: Whether this team member holds the default admin
        role defined by the team's permissions scheme.
        :param explicit_roles: The list of roles explicitly assigned to this team member,
        as a space separated list of role names. This list does not include any roles granted implicitly through permissions schemes.
        :return: Team members creation info
        """

        url = f"{self.api_url}/{team_id}/members/batch"

        self.reset()
        self.add_application_json_header()
        if graceful is not None:
            self.add_to_json('graceful', graceful)
        if t_id is not None:
            self.add_to_json('team_id', t_id)
        if user_id is not None:
            self.add_to_json('user_id', user_id)
        if roles is not None:
            self.add_to_json('roles', roles)
        if delete_at is not None:
            self.add_to_json('delete_at', delete_at)
        if scheme_user is not None:
            self.add_to_json('scheme_user', scheme_user)
        if scheme_admin is not None:
            self.add_to_json('scheme_admin', scheme_admin)
        if explicit_roles is not None:
            self.add_to_json('explicit_roles', explicit_roles)

        return self.request(url, request_type='POST', body=True)

    def get_team_members_for_user(self, user_id: str) -> dict:
        """
        Get a list of team members for a user. Useful for getting the ids of teams the user is
        on and the roles they have in those teams.

        Must be logged in as the user or have the edit_other_users permission.

        :param user_id: User GUID
        :return: Team members retrieval info
        """

        url = f"{self.api_url}/{user_id}/teams/members/"

        self.reset()

        return self.request(url, request_type='GET')

    def get_team_member(self,
                        team_id: str,
                        user_id: str) -> dict:
        """
        Get a team member on the system.

        Must be authenticated and have the view_team permission.

        :param team_id: Team GUID
        :param user_id: User GUID
        :return: Team members retrieval info
        """

        url = f"{self.api_url}/{team_id}/members/{user_id}"

        self.reset()

        return self.request(url, request_type='GET')

    def remove_user_from_team(self,
                              team_id: str,
                              user_id: str) -> dict:
        """
        Delete the team member object for a user, effectively removing them from a team.

        Must be logged in as the user or have the remove_user_from_team permission.

        :param team_id: Team GUID
        :param user_id: User GUID
        :return: Team members deletion info
        """

        url = f"{self.api_url}/{team_id}/members/{user_id}"

        self.reset()

        return self.request(url, request_type='DEL')

    def get_team_members_by_ids(self,
                                team_id: str,
                                user_ids: list[str]) -> dict:
        """
        Get a list of team members based on a provided array of user ids.

        Must have view_team permission for the team.

        :param team_id: Team GUID
        :param user_ids: User GUID
        :return: Team members retrieval info
        """

        url = f"{self.api_url}/{team_id}/members/ids"

        self.reset()
        self.add_application_json_header()
        if user_ids is not None:
            self.add_to_json('user_ids', user_ids)

        return self.request(url, request_type='POST', body=True)

    def get_team_stats(self, team_id: str) -> dict:
        """
        Get a team stats on the system.

        Must be authenticated and have the view_team permission.

        :param team_id: Team GUID
        :return: Team stats retrieval info
        """

        url = f"{self.api_url}/{team_id}/stats"

        self.reset()

        return self.request(url, request_type='GET')

    def regenerate_invite_id_from_team(self, team_id: str) -> dict:
        """
        Regenerates the invite ID used in invite links of a team.

        Must be authenticated and have the manage_team permission.

        :param team_id: Team GUID
        :return: Team invite ID regeneration info.
        """

        url = f"{self.api_url}/{team_id}/regenerate_invite_id"

        self.reset()

        return self.request(url, request_type='POST')

    def get_team_icon(self, team_id: str) -> dict:
        """
        Get the team icon of the team.

        Minimum server version: 4.9.

        User must be authenticated. In addition, team must be open or the user must have the view_team permission.
00
        :param team_id: Team GUID
        :return: Team icon retrieval info
        """

        url = f"{self.api_url}/{team_id}/image"

        self.reset()

        return self.request(url, request_type='GET')

    def sets_team_icon(self,
                       team_id: str,
                       image: str = None) -> dict:
        """
        Sets the team icon for the team.

        Minimum server version: 4.9

        Must be authenticated and have the manage_team permission.

        :param team_id: Team GUID
        :param image: The image to be uploaded
        :return: Team icon info
        """

        url = f"{self.api_url}/{team_id}/image"

        self.reset()
        self.add_multipart_form_data()

        if image is not None:
            self.add_file(file_path=image)

        return self.request(url, request_type='POST', files=True)

    def remove_team_icon(self, team_id: str) -> dict:
        """
        Remove the team icon for the team.

        Minimum server version: 4.10

        Must be authenticated and have the manage_team permission.

        :param team_id: Team GUID
        :return: Team icon info
        """

        url = f"{self.api_url}/{team_id}/image"

        self.reset()

        return self.request(url, request_type='DEL')

    def update_team_member_roles(self,
                                 team_id: str,
                                 user_id: str,
                                 roles: str) -> dict:
        """
        Update a team member roles. Valid team roles are "team_user", "team_admin" or both of them.
        Overwrites any previously assigned team roles.

        Must be authenticated and have the manage_team_roles permission.

        :param team_id: Team GUID
        :param user_id: User GUID
        :param roles: Space-delimited team roles to assign to the user
        :return: Team member roles update info
        """

        url = f"{self.api_url}/{team_id}/members/{user_id}/roles"

        self.reset()
        self.add_application_json_header()
        if roles is not None:
            self.add_to_json('roles', roles)

        return self.request(url, request_type='PUT', body=True)

    def update_scheme_derived_roles_of_team_member(self,
                                                   team_id: str,
                                                   user_id: str,
                                                   scheme_admin: bool,
                                                   scheme_user: bool) -> dict:
        """
        Update a team member's scheme_admin/scheme_user properties.
        Typically this should either be scheme_admin=false, scheme_user=true for ordinary team member,
        or scheme_admin=true, scheme_user=true for a team admin.

        Minimum server version: 5.0

        Must be authenticated and have the manage_team_roles permission.

        :param team_id: Team GUID
        :param user_id: User GUID
        :param scheme_admin: Scheme admin property
        :param scheme_user: Scheme user property
        :return: Team member's scheme-derived roles update info.
        """

        url = f"{self.api_url}/{team_id}/members/{user_id}/schemeRoles"

        self.reset()
        self.add_application_json_header()

        if scheme_admin is not None:
            self.add_to_json('scheme_admin', scheme_admin)
        if scheme_user is not None:
            self.add_to_json('scheme_user', scheme_user)

        return self.request(url, request_type='PUT', body=True)

    def get_team_unread_for_user(self,
                                 user_id: str,
                                 exclude_team: str,
                                 include_collapsed_threads: bool = None) -> dict:
        """
        Get the count for unread messages and mentions in the teams the user is a member of.

        Must be logged in.

        :param user_id: User GUID.
        :param exclude_team: Optional team id to be excluded from the results.
        :param include_collapsed_threads: Default: false. Boolean to determine whether the collapsed
        threads should be included or not.
        :return: Team unreads retrieval info.
        """

        url = f"{self.base_url}/users/{user_id}/teams/unread"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('exclude_team', exclude_team)
        if include_collapsed_threads is not None:
            self.add_to_json('include_collapsed_threads', include_collapsed_threads)

        return self.request(url, request_type='GET', body=True)

    def get_unread_for_team(self,
                            user_id: str,
                            team_id: str) -> dict:
        """
        Get the unread mention and message counts for a team for the specified user.

        Must be the user or have edit_other_users permission and have view_team permission for the team.

        :param user_id: User GUID.
        :param team_id: Team GUID.
        :return: Team unread count retrieval info.
        """

        url = f"{self.base_url}/users/{user_id}/teams/{team_id}/unread"

        self.reset()

        return self.request(url, request_type='GET')

    def invite_users_to_team_by_email(self,
                                      team_id: str,
                                      user_email: list[str] = None) -> dict:
        """
        Invite users to the existing team using the user's email.

        The number of emails that can be sent is rate limited to 20 per hour with a burst of 20 emails.
        If the rate limit exceeds, the error message contains details on when to retry and when the timer will be reset.

        Must have invite_user and add_user_to_team permissions for the team.

        :param team_id: Team GUID.
        :param user_email: List of user's email.
        :return: Users invite info.
        """

        url = f"{self.api_url}/{team_id}/invite/email"

        self.reset()
        self.add_application_json_header()
        if user_email is not None:
            self.add_to_json('user_email', user_email)

        return self.request(url, request_type='POST', body=True)

    def invite_guests_to_team_by_email(self,
                                       team_id: str,
                                       emails: list[str],
                                       channels: list[str],
                                       message: str=None) -> dict:
        """
        Invite guests to existing team channels usign the user's email.

        The number of emails that can be sent is rate limited to 20 per hour with a burst of 20 emails.
        If the rate limit exceeds, the error message contains details on when to retry and when the timer will be reset.

        Minimum server version: 5.16

        :param team_id: Team GUID.
        :param emails: List of emails.
        :param channels: List of channel ids.
        :param message: Message to include in the invite.
        :return: Guests invite info.
        """

        url = f"{self.api_url}/{team_id}/invite-guests/email"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('emails', emails)
        self.add_to_json('channels', channels)
        if message is not None:
            self.add_to_json('message', message)

        return self.request(url, request_type='POST', body=True)

    def invalidate_active_email_invitations(self) -> dict:
        """
        Invalidate active email invitations that have not been accepted by the user.

        Must have sysconsole_write_authentication permission.

        :return: Email invites info.
        """

        url = f"{self.api_url}/invites/email"

        self.reset()

        return self.request(url, request_type='DEL')

    def import_team_from_other_application(self,
                                           team_id: str,
                                           file: str,
                                           filesize: int,
                                           importFrom: str) -> dict:
        """
        Import a team into a existing team. Import users, channels, posts, hooks.

        Must have permission_import_team permission.

        :param team_id: Team GUID.
        :param file: A file to be uploaded in zip format.
        :param filesize: The size of the zip file to be imported.
        :param importFrom: String that defines from which application the team
        was exported to be imported into Mattermost.
        :return: JSON object containing a base64 encoded text file info.
        """

        url = f"{self.api_url}/{team_id}/import"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('file', file)
        self.add_to_json('filesize', filesize)
        self.add_to_json('importFrom', importFrom)

        return self.request(url, request_type='POST', body=True)

    def get_invite_info_for_team(self,
                                 invite_id: str) -> dict:
        """
        Get the name, display_name, description and id for a team from the invite id.

        Minimum server version: 4.0

        No authentication required.

        :param invite_id: Invite id for a team.
        :return: Team invite info
        """

        url = f"{self.api_url}/invite/{invite_id}"

        self.reset()

        return self.request(url, request_type='GET')

    def set_team_scheme(self, team_id: str, scheme_id: str) -> dict:
        """
        Set a team's scheme, more specifically sets the scheme_id value of a team record.

        Must have manage_system permission.

        Minimum server version: 5.0

        :param team_id: Team GUID
        :param scheme_id: The ID of the scheme.
        :return: Team scheme update info.
        """

        url = f"{self.api_url}/{team_id}/scheme"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('scheme_id', scheme_id)

        return self.request(url, request_type='PUT', body=True)

    def team_members_minus_group_members(self,
                                         team_id: str,
                                         group_ids: str,
                                         page: int = None,
                                         per_page: int = None) -> dict:
        """
        Get the set of users who are members of the team minus the set of users who are members of the given groups.
        Each user object contains an array of group objects representing the group memberships for that user.
        Each user object contains the boolean fields scheme_guest, scheme_user, and scheme_admin
        representing the roles that user has for the given team.

        Must have manage_system permission.

        Minimum server version: 5.14

        :param team_id: Team GUID
        :param group_ids: Default: "". A comma-separated list of group ids.
        :param page: Default: 0. The page to select.
        :param per_page: Default: 0. The number of users per page.
        :return: Users specified by the pagination info.
        """

        url = f"{self.api_url}/{team_id}/members_minus_group_members"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('group_ids', group_ids)
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)

    def search_files_in_team(self,
                             team_id: str,
                             terms: str,
                             is_or_search: bool,
                             time_zone_offset: int = None,
                             include_deleted_channels: bool = None,
                             page: int = None,
                             per_page: int = None) -> dict:
        """
        Search for files in a team based on file name, extention and file content (if file content extraction is enabled and supported for the files).
        Minimum server version: 5.34

        Must be authenticated and have the view_team permission.

        :param team_id: Team GUID
        :param terms: The search terms as input by the user. To search for files from a user include from:someusername, using a user's username. To search in a specific channel include in:somechannel, using the channel name (not the display name). To search for specific extensions included ext:extension.
        :param is_or_search: Set to true if an Or search should be performed vs an And search.
        :param time_zone_offset: Default: 0. Offset from UTC of user timezone for date searches.
        :param include_deleted_channels: Set to true if deleted channels should be included in the search. (archived channels)
        :param page: Default: 0. The page to select. (Only works with Elasticsearch)
        :param per_page: Default: 60. The number of posts per page. (Only works with Elasticsearch)
        :return: File list retrieval info.
        """

        url = f"{self.api_url}/{team_id}/files/search"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('terms', terms)
        self.add_to_json('is_or_search', is_or_search)
        if time_zone_offset is not None:
            self.add_to_json('time_zone_offset', time_zone_offset)
        if include_deleted_channels is not None:
            self.add_to_json('include_deleted_channels', include_deleted_channels)
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='POST', body=True)
