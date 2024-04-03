from typing import Union, List, Dict
from Mattermost_Base import Base


class Users(Base):
    def __init__(self, token: str, server_url: str):
        super().__init__(token, server_url)
        self.api_url = f"{self.base_url}/users"

    def login_to_mattermost_server(self,
                                   id: str = None,
                                   login_id: str = None,
                                   token: str = None,
                                   device_id: str = None,
                                   ldap_only: bool = None,
                                   password: str = None) -> dict:
        """
        Logins to Mattermost server.

        No permission required

        :param id: User ID for authentication.
        :param login_id: User login ID for authentication.
        :param token: User token for authentication.
        :param device_id: User device ID for authentication.
        :param ldap_only: User LDAP only for authentication.
        :param password: User password for authentication.
        :return: User login info.
        """

        url = f"{self.api_url}/login"

        self.reset()
        self.add_application_json_header()
        if id is not None:
            self.add_to_json('id', id)
        if login_id is not None:
            self.add_to_json('login_id', login_id)
        if token is not None:
            self.add_to_json('token', token)
        if device_id is not None:
            self.add_to_json('device_id', device_id)
        if ldap_only is not None:
            self.add_to_json('ldap_only', ldap_only)
        if password is not None:
            self.add_to_json('password', password)

        return self.request(url, request_type='POST', body=True)

    def autologin_to_mm_server_using_cws_token(self,
                                               login_id: str = None,
                                               cws_token: str = None) -> dict:
        """
        CWS stands for Customer Web Server which is the cloud service used to manage cloud instances.

        A Cloud license is required

        :param login_id: User login ID for authentication.
        :param cws_token: User CWS token for authentication.
        :return: User login info.
        """

        url = f"{self.api_url}/login/cws"

        self.reset()
        self.add_application_json_header()
        if login_id is not None:
            self.add_to_json('login_id', login_id)
        if cws_token is not None:
            self.add_to_json('cws_token', cws_token)

        return self.request(url, request_type='POST', body=True)

    def logout_from_mm_server(self) -> dict:
        """
        Logout from the Mattermost server.

        An active session is required

        :return: User logout info.
        """

        url = f"{self.api_url}/logout"

        self.reset()

        return self.request(url, request_type='POST')

    def create_user(self,
                    email: str,
                    username: str,
                    t: str = None,
                    iid: str = None,
                    first_name: str = None,
                    last_name: str = None,
                    nickname: str = None,
                    auth_data: str = None,
                    auth_service: str = None,
                    password: str = None,
                    locale: str = None,
                    props: dict = None,
                    notify_props: dict = None) -> dict:
        """
        Create a new user on the system. Password is required for email login.
        For other authentication types such as LDAP or SAML, auth_data and auth_service fields are required.

        No permission required for creating email/username accounts on an open server.
        Auth Token is required for other authentication types such as LDAP or SAML.

        :param email: User email to be created.
        :param username: User username to be created.
        :param t: Token id from an email invitation.
        :param iid: Token id from an invitation link.
        :param first_name: User first name to be created.
        :param last_name: User last name to be created.
        :param nickname: User nickname to be created.
        :param auth_data: Service-specific authentication data, such as email address.
        :param auth_service: The authentication service, one of
        "email", "gitlab", "ldap", "saml", "office365", "google", and "".
        :param password: The password used for email authentication.
        :param locale: User locale to be created.
        :param props: User props to be created.
        :param notify_props: User notify props to be created.
        :return: User creation info.
        """

        url = f"{self.api_url}"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('email', email)
        self.add_to_json('username', username)
        if t is not None:
            self.add_to_json('t', t)
        if iid is not None:
            self.add_to_json('iid', iid)
        if first_name is not None:
            self.add_to_json('first_name', first_name)
        if last_name is not None:
            self.add_to_json('last_name', last_name)
        if nickname is not None:
            self.add_to_json('nickname', nickname)
        if auth_data is not None:
            self.add_to_json('auth_data', auth_data)
        if auth_service is not None:
            self.add_to_json('auth_service', auth_service)
        if password is not None:
            self.add_to_json('password', password)
        if locale is not None:
            self.add_to_json('locale', locale)
        if props is not None:
            self.add_to_json('props', props)
        if notify_props is not None:
            self.add_to_json('notify_props', notify_props)

        return self.request(url, request_type='POST', body=True)

    def get_users(self,
                  page: int = None,
                  per_page: int = None,
                  in_team: str = None,
                  not_in_team: str = None,
                  in_channel: str = None,
                  not_in_channel: str = None,
                  in_group: str = None,
                  group_constrained: bool = None,
                  without_team: bool = None,
                  active: bool = None,
                  inactive: bool = None,
                  role: str = None,
                  sort: str = None,
                  roles: str = None,
                  channel_roles: str = None,
                  team_roles: str = None) -> dict:
        """
        Get a page of a list of users. Based on query string parameters,
        select users from a team, channel, or select users not in a specific channel.
        Since server version 4.0, some basic sorting is available using the sort query parameter.
        Sorting is currently only supported when selecting users on a team.

        Requires an active session and (if specified) membership to the channel or team being selected from.

        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of users per page. There is a maximum limit of 200 users per page.
        :param in_team: The ID of the team to get users for.
        :param not_in_team: The ID of the team to exclude users for. Must not be used with "in_team" query parameter.
        :param in_channel: The ID of the channel to get users for.
        :param not_in_channel: The ID of the channel to exclude users for.
        Must be used with "in_channel" query parameter.
        :param in_group: The ID of the group to get users for. Must have manage_system permission.
        :param group_constrained: When used with not_in_channel or not_in_team,
        returns only the users that are allowed to join the channel or team based on its group constrains.
        :param without_team: Whether or not to list users that are not on any team.
        This option takes precendence over in_team, in_channel, and not_in_channel.
        :param active: Whether or not to list only users that are active.
        This option cannot be used along with the inactive option.
        :param inactive: Whether or not to list only users that are deactivated.
        This option cannot be used along with the active option.
        :param role: Returns users that have this role.
        :param sort: Sort is only available in conjunction with certain options below.
        The paging parameter is also always available.
        in_team Can be "", "last_activity_at" or "create_at". When left blank, sorting is done by username.
        Minimum server version: 4.0
        in_channel Can be "", "status". When left blank, sorting is done by username. status will sort by User's
        current status (Online, Away, DND, Offline), then by Username. Minimum server version: 4.7
        in_group Can be "", "display_name". When left blank, sorting is done by username.
        display_name will sort alphabetically by user's display name. Minimum server version: 7.7
        :param roles: Comma separated string used to filter users based on any of the specified system roles
        Example: ?roles=system_admin,system_user will return users that are either system admins or system users
        Minimum server version: 5.26
        :param channel_roles: Comma separated string used to filter users based on any of the specified channel roles,
        can only be used in conjunction with in_channel
        Example: ?in_channel=4eb6axxw7fg3je5iyasnfudc5y&channel_roles=channel_user will return users that are only
        channel users and not admins or guests. Minimum server version: 5.26
        :param team_roles: Comma separated string used to filter users based on any of the specified team roles,
        can only be used in conjunction with in_team. Example: ?in_team=4eb6axxw7fg3je5iyasnfudc5y&team_roles=team_user
        will return users that are only team users and not admins or guests. Minimum server version: 5.26
        :return: User page retrieval info.
        """

        url = f"{self.api_url}"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)
        if in_team is not None:
            self.add_to_json('in_team', in_team)
        if not_in_team is not None:
            self.add_to_json('not_in_team', not_in_team)
        if in_channel is not None:
            self.add_to_json('in_channel', in_channel)
        if not_in_channel is not None:
            self.add_to_json('not_in_channel', not_in_channel)
        if in_group is not None:
            self.add_to_json('in_group', in_group)
        if group_constrained is not None:
            self.add_to_json('group_constrained', group_constrained)
        if without_team is not None:
            self.add_to_json('without_team', without_team)
        if active is not None:
            self.add_to_json('active', active)
        if inactive is not None:
            self.add_to_json('inactive', inactive)
        if role is not None:
            self.add_to_json('role', role)
        if sort is not None:
            self.add_to_json('sort', sort)
        if roles is not None:
            self.add_to_json('roles', roles)
        if channel_roles is not None:
            self.add_to_json('channel_roles', channel_roles)
        if team_roles is not None:
            self.add_to_json('team_roles', team_roles)

        return self.request(url, request_type='GET', body=True)

    def permanent_delete_all_users(self) -> dict:
        """
        Permanently deletes all users and all their related information, including posts.

        Minimum server version: 5.26.0

        Local mode only: This endpoint is only available through local mode.

        :return: Delete request info.
        """

        url = f"{self.api_url}"

        self.reset()

        return self.request(url, request_type='DEL')

    def get_users_by_ids(self,
                         since: int = None,
                         user_ids: list[str] = None) -> dict:
        """
        Get a list of users based on a provided list of user ids.

        Requires an active session but no other permissions.

        :param since: Only return users that have been modified since the given Unix timestamp (in milliseconds).
        :param user_ids: List of user ids.
        :return: User list retrieval info.
        """

        url = f"{self.api_url}/ids"

        self.reset()
        self.add_application_json_header()
        if since is not None:
            self.add_to_json('since', since)
        if user_ids is not None:
            self.add_to_json('user_ids', user_ids)

        return self.request(url, request_type='POST', body=True)

    def get_users_by_group_channels_ids(self, channel_ids: list[str] = None) -> dict:
        """
        Get an object containing a key per group channel id in the query and
        its value as a list of users members of that group channel.

        The user must be a member of the group ids in the query, or they will be omitted from the response.

        Requires an active session but no other permissions.

        :param channel_ids: List of group channel ids
        :return: User list retrieval info.
        """

        url = f"{self.api_url}/group_channels"

        self.reset()
        self.add_application_json_header()
        if channel_ids is not None:
            self.add_to_json('channel_ids', channel_ids)

        return self.request(url, request_type='POST', body=True)

    def get_users_by_usernames(self, usernames: list[str] = None) -> dict:
        """
        Get a list of users based on a provided list of usernames.

        Requires an active session but no other permissions.

        :param usernames: List of usernames.
        :return: User list retrieval info.
        """

        url = f"{self.api_url}/usernames"

        self.reset()
        self.add_application_json_header()
        if usernames is not None:
            self.add_to_json('usernames', usernames)

        return self.request(url, request_type='POST', body=True)

    def search_users(self,
                     term: str,
                     team_id=None,
                     not_in_team_id: str = None,
                     in_channel_id: str = None,
                     not_in_channel_id=None,
                     in_group_id: str = None,
                     group_constrained: bool = None,
                     allow_inactive: bool = None,
                     without_team: bool = None,
                     limit: int = None) -> dict:
        """
        Get a list of users based on search criteria provided in the request body.
        Searches are typically done against username, full name, nickname and email unless
        otherwise configured by the server.

        Requires an active session and read_channel and/or view_team permissions for any channels or
        teams specified in the request body.

        :param term: The term to match against username, full name, nickname and email
        :param team_id: If provided, only search users on this team.
        :param not_in_team_id: If provided, only search users not on this team.
        :param in_channel_id: If provided, only search users in this channel.
        :param not_in_channel_id: If provided, only search users not in this channel.
        Must specifiy team_id when using this option
        :param in_group_id:If provided, only search users in this group. Must have manage_system permission.
        :param group_constrained: When used with not_in_channel_id or not_in_team_id, returns only the
        users that are allowed to join the channel or team based on its group constrains.
        :param allow_inactive: When true, include deactivated users in the results
        :param without_team: Set this to true if you would like to search for users that are not on a team.
        This option takes precendence over team_id, in_channel_id, and not_in_channel_id.
        :param limit: Default: 100. The maximum number of users to return in the results
        :return: User list retrieval info.
        """

        url = f"{self.api_url}/search"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('term', term)
        if team_id is not None:
            self.add_to_json('team_id', team_id)
        if not_in_team_id is not None:
            self.add_to_json('not_in_team_id', not_in_team_id)
        if in_channel_id is not None:
            self.add_to_json('in_channel_id', in_channel_id)
        if not_in_channel_id is not None:
            self.add_to_json('not_in_channel_id', not_in_channel_id)
        if in_group_id is not None:
            self.add_to_json('in_group_id', in_group_id)
        if group_constrained is not None:
            self.add_to_json('group_constrained', group_constrained)
        if allow_inactive is not None:
            self.add_to_json('allow_inactive', allow_inactive)
        if without_team is not None:
            self.add_to_json('without_team', without_team)
        if limit is not None:
            self.add_to_json('limit', limit)

        return self.request(url, request_type='POST', body=True)

    def autocomplete_users(self,
                           name: str,
                           team_id: str = None,
                           channel_id: str = None,
                           limit: int = None) -> dict:
        """
        Get a list of users for the purpose of autocompleting based on the provided search term.
        Specify a combination of team_id and channel_id to filter results further.

        Requires an active session and view_team and read_channel
        on any teams or channels used to filter the results further.

        :param name: Username, nickname first name or last name
        :param team_id: Team ID
        :param channel_id: Channel ID
        :param limit: Default: 100. The maximum number of users to return in each subresult
        Available as of server version 5.6. Defaults to 100 if not provided or on an earlier server version.
        :return: User autocomplete info.
        """

        url = f"{self.api_url}/autocomplete"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('name', name)
        if team_id is not None:
            self.add_to_json('team_id', team_id)
        if channel_id is not None:
            self.add_to_json('channel_id', channel_id)
        if limit is not None:
            self.add_to_json('limit', limit)

        return self.request(url, request_type='GET', body=True)

    def get_user_ids_of_known_users(self) -> dict:
        """
        Get the list of user IDs of users with any direct relationship with a user.
        That means any user sharing any channel, including direct and group channels.

        Must be authenticated.

        Minimum server version: 5.23

        :return: Known user's IDs retrieval info.
        """

        url = f"{self.api_url}/known"

        self.reset()

        return self.request(url, request_type='GET')

    def get_total_count_of_users_in_the_system(self) -> dict:
        """
        Get a total count of users in the system.

        Must be authenticated.

        :return: User state retrieval info.
        """

        url = f"{self.api_url}/stats"

        self.reset()

        return self.request(url, request_type='GET')

    def get_total_count_of_users_in_system_matching_specified_filters(self,
                                                                      in_team: str = None,
                                                                      in_channel: str = None,
                                                                      include_deleted: bool = None,
                                                                      include_bots: bool = None,
                                                                      roles: str = None,
                                                                      channel_roles: str = None,
                                                                      team_roles: str = None) -> dict:
        """
        Get a count of users in the system matching the specified filters.

        Minimum server version: 5.26

        Must have manage_system permission.

        :param in_team: The ID of the team to get user stats for.
        :param in_channel: The ID of the channel to get user stats for.
        :param include_deleted: If deleted accounts should be included in the count.
        :param include_bots: If bot accounts should be included in the count.
        :param roles: Comma separated string used to filter users based on any of the specified system roles
        Example: ?roles=system_admin,system_user will include users that are either system admins or system users
        :param channel_roles: Comma separated string used to filter users based on any of the specified channel roles,
        can only be used in conjunction with in_channel
        Example: ?in_channel=4eb6axxw7fg3je5iyasnfudc5y&channel_roles=channel_user will include users that are only
        channel users and not admins or guests
        :param team_roles: Comma separated string used to filter users based on any of the specified team roles,
        can only be used in conjunction with in_team
        Example: ?in_team=4eb6axxw7fg3je5iyasnfudc5y&team_roles=team_user will include users that are only team
        users and not admins or guests
        :return: Filtered user stats retrieval info.
        """

        url = f"{self.api_url}/stats/filtered"

        self.reset()
        self.add_application_json_header()
        if in_team is not None:
            self.add_to_json('in_team', in_team)
        if in_channel is not None:
            self.add_to_json('in_channel', in_channel)
        if include_deleted is not None:
            self.add_to_json('include_deleted', include_deleted)
        if include_bots is not None:
            self.add_to_json('include_bots', include_bots)
        if roles is not None:
            self.add_to_json('roles', roles)
        if channel_roles is not None:
            self.add_to_json('channel_roles', channel_roles)
        if team_roles is not None:
            self.add_to_json('team_roles', team_roles)

        return self.request(url, request_type='GET', body=True)

    def get_user(self, user_id: str) -> dict:
        """
        Get a user a object. Sensitive information will be sanitized out.

        Requires an active session but no other permissions.

        :param user_id: User GUID. This can also be "me" which will point to the current user.
        :return: User retrieval info.
        """

        url = f"{self.api_url}/{user_id}"

        self.reset()

        return self.request(url, request_type='GET')

    def update_user(self,
                    user_id: str,
                    id: str,
                    email: str,
                    username: str,
                    first_name: str = None,
                    last_name: str = None,
                    nickname: str = None,
                    locale: str = None,
                    position: str = None,
                    timezone: dict = None,
                    props: str = None,
                    notify_props: dict = None) -> dict:
        """
        Update a user by providing the user object. The fields that can be updated are defined in the request body,
        all other provided fields will be ignored. Any fields not included in the request body will be set to
        null or reverted to default values.

        Must be logged in as the user being updated or have the edit_other_users permission.

        :param user_id: User GUID
        :param id: User ID that is to be updated
        :param email: User email that is to be updated
        :param username: User's username that is to be updated
        :param first_name: User's first name to update
        :param last_name: User's last name to update
        :param nickname: User's nickname to update
        :param locale: User's locale to update
        :param position:  User's position to update
        :param timezone: User's timezone to update
        :param props: User's props to update
        :param notify_props: User's notify props to update
        :return: User update info
        """

        url = f"{self.api_url}/{user_id}"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('id', id)
        self.add_to_json('email', email)
        self.add_to_json('username', username)
        if first_name is not None:
            self.add_to_json('first_name', first_name)
        if last_name is not None:
            self.add_to_json('last_name', last_name)
        if nickname is not None:
            self.add_to_json('nickname', nickname)
        if locale is not None:
            self.add_to_json('locale', locale)
        if position is not None:
            self.add_to_json('position', position)
        if timezone is not None:
            self.add_to_json('timezone', timezone)
        if props is not None:
            self.add_to_json('props', props)
        if notify_props is not None:
            self.add_to_json('notify_props', notify_props)

        return self.request(url, request_type='PUT', body=True)

    def deactivate_user_account(self, user_id: str) -> dict:
        """
        Deactivates the user and revokes all its sessions by archiving its user object.
        As of server version 5.28, optionally use the permanent=true query parameter to permanently delete
        the user for compliance reasons. To use this feature ServiceSettings.EnableAPIUserDeletion must be set to
        true in the server's configuration.

        Must be logged in as the user being deactivated or have the edit_other_users permission.

        :param user_id: User GUID
        :return: User deactivation info
        """

        url = f"{self.api_url}/{user_id}"

        self.reset()

        return self.request(url, request_type='DEL')

    def patch_user(self,
                   user_id: str,
                   email: str = None,
                   username: str = None,
                   first_name: str = None,
                   last_name: str = None,
                   nickname: str = None,
                   locale: str = None,
                   position: str = None,
                   props: dict = None,
                   notify_props: dict = None) -> dict:
        """
        Partially update a user by providing only the fields you want to update. Omitted fields will not be updated.
        The fields that can be updated are defined in the request body, all other provided fields will be ignored.

        Must be logged in as the user being updated or have the edit_other_users permission.

        :param user_id: User GUID
        :param email: User's email to update
        :param username: User's username to update
        :param first_name: User's first name to update
        :param last_name: User's last name to update
        :param nickname: User's nickname to update
        :param locale: User's locale to update
        :param position: User's position to update
        :param props: User's props to update
        :param notify_props: User's props to update
        :return:  User patch info
        """

        url = f"{self.api_url}/{user_id}/patch"

        self.reset()
        self.add_application_json_header()
        if email is not None:
            self.add_to_json('email', email)
        if username is not None:
            self.add_to_json('username', username)
        if first_name is not None:
            self.add_to_json('first_name', first_name)
        if last_name is not None:
            self.add_to_json('last_name', last_name)
        if nickname is not None:
            self.add_to_json('nickname', nickname)
        if locale is not None:
            self.add_to_json('locale', locale)
        if position is not None:
            self.add_to_json('position', position)
        if props is not None:
            self.add_to_json('props', props)
        if notify_props is not None:
            self.add_to_json('notify_props', notify_props)

        return self.request(url, request_type='PUT', body=True)

    def update_user_roles(self,
                          user_id: str,
                          roles: str) -> dict:
        """
        Update a user's system-level roles. Valid user roles are "system_user", "system_admin" or both of them.
        Overwrites any previously assigned system-level roles.

        Must have the manage_roles permission.

        :param user_id: User GUID
        :param roles: Space-delimited system roles to assign to the user
        :return: User roles update info
        """

        url = f"{self.api_url}/{user_id}/roles"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('roles', roles)

        return self.request(url, request_type='PUT', body=True)

    def update_user_active_status(self,
                                  user_id: str,
                                  active: bool) -> dict:
        """
        Update user active or inactive status.
        Since server version 4.6, users using a SSO provider to login can be activated or
        deactivated with this endpoint. However, if their activation status in Mattermost does not reflect their
        status in the SSO provider, the next synchronization or login by that user will reset the activation
        status to that of their account in the SSO provider. Server versions 4.5 and before do not allow activation
        or deactivation of SSO users from this endpoint.

        User can deactivate themselves. User with manage_system permission can activate or deactivate a user.

        :param user_id: User GUID
        :param active: Use true to set the user active, false for inactive
        :return: User active status update info
        """

        url = f"{self.api_url}/{user_id}/active"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('active', active)

        return self.request(url, request_type='PUT', body=True)

    def get_user_profile_image(self,
                               user_id: str,
                               _: str = None) -> dict:
        """
        Get a user's profile image based on user_id string parameter.

        Must be logged in.

        :param user_id: User GUID
        :param _: Not used by the server. Clients can pass in the last picture update
        time of the user to potentially take advantage of caching
        :return: User's profile image info
        """

        url = f"{self.api_url}/{user_id}/image"

        self.reset()
        self.add_application_json_header()
        if _ is not None:
            self.add_to_json('_', _)

        return self.request(url, request_type='GET', body=True)

    def set_user_profile_image(self,
                               user_id: str,
                               image: str) -> dict:
        """
        Set a user's profile image based on user_id string parameter.

        Must be logged in as the user being updated or have the edit_other_users permission.

        :param user_id: User GUID
        :param image: The image to be uploaded
        :return: Profile image setting info
        """

        url = f"{self.api_url}/{user_id}/image"

        self.reset()
        self.add_multipart_form_data_header()
        self.add_file(file_path=image)

        return self.request(url, request_type='POST', files=True)

    def delete_user_profile_image(self,
                                  user_id: str) -> dict:
        """
        Delete user's profile image and reset to default image based on user_id string parameter.

        Must be logged in as the user being updated or have the edit_other_users permission.

        Minimum server version: 5.5

        :param user_id: User GUID
        :return: Profile image reset info
        """

        url = f"{self.api_url}/{user_id}/image"

        self.reset()

        return self.request(url, request_type='DEL')

    def return_user_default_profile_image(self, user_id: str) -> dict:
        """
        Returns the default (generated) user profile image based on user_id string parameter.

        Must be logged in. Minimum server version: 5.5

        :param user_id: User GUID
        :return: Default profile image info
        """

        url = f"{self.api_url}/{user_id}/image/default"

        self.reset()

        return self.request(url, request_type='GET')

    def get_user_by_username(self, username: str) -> dict:
        """
        Get a user object by providing a username. Sensitive information will be sanitized out.

        Requires an active session but no other permissions.

        :param username: Username
        :return: User retrieval info
        """

        url = f"{self.api_url}/username/{username}"

        self.reset()

        return self.request(url, request_type='GET')

    def reset_password(self,
                       code: str,
                       new_password: str) -> dict:
        """
        Update the password for a user using a one-use, timed recovery code tied to the user's account.
        Only works for non-SSO users.

        No permissions required.

        :param code: The recovery code.
        :param new_password: The new password for the user.
        :return: User password update info.
        """

        url = f"{self.api_url}/password/reset"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('code', code)
        self.add_to_json('new_password', new_password)

        return self.request(url, request_type='POST', body=True)

    def update_user_mfa(self,
                        user_id: str,
                        activate: bool,
                        code: str = None) -> dict:
        """
        Activates multi-factor authentication for the user if activate is true and a valid code is provided.
        If activate is false, then code is not required and multi-factor authentication is disabled for the user.

        Must be logged in as the user being updated or have the edit_other_users permission.

        :param user_id: User GUID
        :param activate: Use true to activate, false to deactivate
        :param code: The code produced by your MFA client. Required if activate is true
        :return: User MFA update info
        """

        url = f"{self.api_url}/{user_id}/mfa"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('activate', activate)
        if code is not None:
            self.add_to_json('code', code)

        return self.request(url, request_type='PUT', body=True)

    def generate_mfa_secret(self,
                            user_id: str) -> dict:
        """
        Generates a multi-factor authentication secret for a user and returns it
        as a string and as base64 encoded QR code image.

        Must be logged in as the user or have the edit_other_users permission.

        :param user_id: User GUID
        :return: MFA secret generation info
        """

        url = f"{self.api_url}/{user_id}/mfa/generate"

        self.reset()

        return self.request(url, request_type='POST')

    def demote_user_to_guest(self, user_id: str) -> dict:
        """
        Convert a regular user into a guest. This will convert the user into a
        guest for the whole system while retaining their existing team and channel memberships.

        Minimum server version: 5.16

        Must be logged in as the user or have the demote_to_guest permission.

        :param user_id: User GUID
        :return: User demotion info
        """

        url = f"{self.api_url}/{user_id}/demote"

        self.reset()

        return self.request(url, request_type='POST')

    def promote_guest_to_user(self, user_id: str) -> dict:
        """
        Convert a guest into a regular user. This will convert the guest into a user for the whole system
        while retaining any team and channel memberships and automatically joining them to the default channels.

        Minimum server version: 5.16

        Must be logged in as the user or have the promote_guest permission.

        :param user_id: User GUID
        :return: Guest promotion info
        """

        url = f"{self.api_url}/{user_id}/promote"

        self.reset()

        return self.request(url, request_type='POST')

    def convert_user_to_bot(self, user_id: str) -> dict:
        """
        Convert a user into a bot.

        Minimum server version: 5.26

        Must have manage_system permission.

        :param user_id: User GUID
        :return: User conversion info
        """

        url = f"{self.api_url}/{user_id}/convert_to_bot"

        self.reset()

        return self.request(url, request_type='POST')

    def check_mfa(self, login_id: str) -> dict:
        """
        Check if a user has multi-factor authentication active on their account by providing a login id.
        Used to check whether an MFA code needs to be provided when logging in.

        No permission required.

        :param login_id: The email or username used to login
        :return: MFA check info
        """

        url = f"{self.api_url}/mfa"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('login_id', login_id)

        return self.request(url, request_type='POST', body=True)

    def update_user_password(self,
                             user_id: str,
                             new_password: str,
                             current_password: str = None) -> dict:
        """
        Update a user's password. New password must meet password policy set by server configuration.
        Current password is required if you're updating your own password.

        Must be logged in as the user the password is being changed for or have manage_system permission.

        :param user_id: User GUID
        :param new_password: The new password for the user.
        :param current_password: The current password for the user.
        :return: User password update info.
        """

        url = f"{self.api_url}/{user_id}/password"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('new_password', new_password)
        if current_password is not None:
            self.add_to_json('current_password', current_password)

        return self.request(url, request_type='PUT', body=True)

    def send_password_reset_email(self, email: str) -> dict:
        """
        Send an email containing a link for resetting the user's password. The link will contain a one-use,
        timed recovery code tied to the user's account. Only works for non-SSO users.

        No permissions required.

        :param  email: The email of the user
        :return: Email info
        """

        url = f"{self.api_url}/password/reset/send"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('email', email)

        return self.request(url, request_type='POST', body=True)

    def get_user_by_email(self, email: str) -> dict:
        """
        Get a user object by providing a user email. Sensitive information will be sanitized out.

        Requires an active session and for the current session to be able to view another user's
        email based on the server's privacy settings.

        :param  email: User Email
        :return: User retrieval info
        """

        url = f"{self.api_url}/email/{email}"

        self.reset()

        return self.request(url, request_type='GET')

    def get_user_sessions(self, user_id: str) -> dict:
        """
        Get a list of sessions by providing the user GUID. Sensitive information will be sanitized out.

        Must be logged in as the user being updated or have the edit_other_users permission.

        :param  user_id: User GUID
        :return: User session retrieval info
        """

        url = f"{self.api_url}/{user_id}/sessions"

        self.reset()

        return self.request(url, request_type='GET')

    def revoke_user_session(self,
                            user_id: str,
                            session_id: str) -> dict:
        """
        Revokes a user session from the provided user id and session id strings.

        Must be logged in as the user being updated or have the edit_other_users permission.

        :param  user_id: User GUID
        :param session_id: The session GUID to revoke.
        :return: User session revoke info
        """

        url = f"{self.api_url}/{user_id}/sessions/revoke"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('session_id', session_id)

        return self.request(url, request_type='POST', body=True)

    def revoke_all_active_sessions_for_user(self, user_id: str) -> dict:
        """
        Revokes all user sessions from the provided user id and session id strings.

        Must be logged in as the user being updated or have the edit_other_users permission.

        Minimum server version: 4.4

        :param  user_id: User GUID
        :return: User session revoke info
        """

        url = f"{self.api_url}/{user_id}/sessions/revoke/all"

        self.reset()

        return self.request(url, request_type='POST')

    def attach_mobile_device(self, device_id: str) -> dict:
        """
        Attach a mobile device id to the currently logged in session.
        This will enable push notifications for a user, if configured by the server.

        Must be authenticated.

        :param  device_id: Mobile device id. For Android prefix the id with android: and Apple with apple:
        :return: Device id attach info
        """

        url = f"{self.api_url}/sessions/device"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('device_id', device_id)

        return self.request(url, request_type='PUT', body=True)

    def get_user_audits(self, user_id: str) -> dict:
        """
        Get a list of audit by providing the user GUID.

        Must be logged in as the user or have the edit_other_users permission.

        :param  user_id: User GUID.
        :return: User audits retrieval info.
        """

        url = f"{self.api_url}/{user_id}/audits"

        self.reset()

        return self.request(url, request_type='GET')

    def verify_user_email_by_id(self, user_id: str) -> dict:
        """
        Verify the email used by a user without a token.

        Minimum server version: 5.24

        Must have manage_system permission.

        :param  user_id: User GUID.
        :return: User email verification info.
        """

        url = f"{self.api_url}/{user_id}/email/verify/member"

        self.reset()

        return self.request(url, request_type='POST')

    def verify_user_email(self, token: str) -> dict:
        """
        Verify the email used by a user to sign-up their account with.

        No permissions required.

        :param token: The token given to validate the email.
        :return: User email verification info.
        """

        url = f"{self.api_url}/email/verify"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('token', token)

        return self.request(url, request_type='POST')

    def send_verification_email(self, email: str) -> dict:
        """
        Send an email with a verification link to a user that has an email matching the one in the request body.
        This endpoint will return success even if the email does not match any users on the system.

        No permissions required.

        :param  email: Email of a user.
        :return: User email info.
        """

        url = f"{self.api_url}/email/verify/send"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('email', email)

        return self.request(url, request_type='POST')

    def switch_login_method(self,
                            current_service: str,
                            new_service: str,
                            email: str = None,
                            password: str = None,
                            mfa_code: str = None,
                            ldap_id: str = None):
        """
        Switch a user's login method from using email to OAuth2/SAML/LDAP or back to email.
        When switching to OAuth2/SAML, account switching is not complete until the user follows the returned
        link and completes any steps on the OAuth2/SAML service provider.
        To switch from email to OAuth2/SAML, specify current_service, new_service, email and password.
        To switch from OAuth2/SAML to email, specify current_service, new_service, email and new_password.
        To switch from email to LDAP/AD, specify current_service, new_service, email, password,
        ldap_ip and new_password (this is the user's LDAP password).
        To switch from LDAP/AD to email, specify current_service, new_service, ldap_ip, password
        (this is the user's LDAP password), email and new_password.
        Additionally, specify mfa_code when trying to switch an account on LDAP/AD or email that has MFA activated.

        No current authentication required except when switching from OAuth2/SAML to email.

        :param current_service: The service the user currently uses to login.
        :param new_service: The service the user will use to login.
        :param email: The email of the user.
        :param password: The password used with the current service.
        :param mfa_code: The MFA code of the current service.
        :param ldap_id: The LDAP/AD id of the user.
        :return: Login method info.
        """

        url = f"{self.api_url}/login/switch"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('current_service', current_service)
        self.add_to_json('new_service', new_service)
        if email is not None:
            self.add_to_json('email', email)
        if password is not None:
            self.add_to_json('password', password)
        if mfa_code is not None:
            self.add_to_json('mfa_code', mfa_code)
        if ldap_id is not None:
            self.add_to_json('ldap_id', ldap_id)

        return self.request(url, request_type='POST', body=True)

    def create_user_access_token(self,
                                 user_id: str,
                                 description: str) -> dict:
        """
        Generate a user access token that can be used to authenticate with the Mattermost REST API.

        Minimum server version: 4.1.

        Must have create_user_access_token permission. For non-self requests,
        must also have the edit_other_users permission.

        :param user_id: User GUID.
        :param description: A description of the token usage.
        :return: User email info.
        """

        url = f"{self.api_url}/{user_id}/tokens"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('description', description)

        return self.request(url, request_type='POST', body=True)

    def get_user_access_tokens(self,
                               user_id: str,
                               page: int = None,
                               per_page: int = None) -> dict:
        """
        Get a list of user access tokens for a user. Does not include the actual authentication tokens.
        Use query parameters for paging.

        Minimum server version: 4.1.

        Must have read_user_access_token permission.
        For non-self requests, must also have the edit_other_users permission.

        :param user_id: User GUID.
        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of tokens per page.
        :return: User access tokens retrieval info.
        """

        url = f"{self.api_url}/{user_id}/tokens"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)

    def get_user_access_tokens_page(self,
                                    page: int = None,
                                    per_page: int = None) -> dict:
        """
        Get a page of user access tokens for users on the system.
        Does not include the actual authentication tokens. Use query parameters for paging.

        Minimum server version: 4.7.

        Must have manage_system permission.

        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of tokens per page.
        :return: User access tokens retrieval info.
        """

        url = f"{self.api_url}/tokens"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)

    def revoke_user_access_token(self, token_id: str) -> dict:
        """
        Revoke a user access token and delete any sessions using the token.

        Minimum server version: 4.1.

        Must have revoke_user_access_token permission. For non-self requests,
        must also have the edit_other_users permission.

        :param token_id: The user access token GUID to revoke.
        :return: User access token revoke info.
        """

        url = f"{self.api_url}/tokens/revoke"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('token_id', token_id)

        return self.request(url, request_type='POST', body=True)

    def get_user_access_token(self, token_id: str) -> dict:
        """
        Get a user access token. Does not include the actual authentication token.

        Minimum server version: 4.1

        Must have read_user_access_token permission.
        For non-self requests, must also have the edit_other_users permission.

        :param token_id: User access token GUID.
        :return: User access token retrieval info.
        """

        url = f"{self.api_url}/tokens/{token_id}"

        self.reset()

        return self.request(url, request_type='GET')

    def disable_personal_access_token(self, token_id: str) -> dict:
        """
        Disable a personal access token and delete any sessions using the token.
        The token can be re-enabled using /users/tokens/enable.

        Minimum server version: 4.4.

        Must have revoke_user_access_token permission.
        For non-self requests, must also have the edit_other_users permission.

        :param token_id: User access token GUID.
        :return: Personal access token disabling info.
        """

        url = f"{self.api_url}/tokens/disable"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('token_id', token_id)

        return self.request(url, request_type='POST', body=True)

    def enable_personal_access_token(self, token_id: str) -> dict:
        """
        Re-enable a personal access token that has been disabled.

        Minimum server version: 4.4

        Must have create_user_access_token permission.
        For non-self requests, must also have the edit_other_users permission.

        :param token_id: The personal access token GUID to enable.
        :return: Personal access token enable info.
        """

        url = f"{self.api_url}/tokens/enable"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('token_id', token_id)

        return self.request(url, request_type='POST', body=True)

    def search_tokens(self, term: str) -> dict:
        """
        Get a list of tokens based on search criteria provided in the request body.
        Searches are done against the token id, user id and username.

        Minimum server version: 4.7

        Must have manage_system permission.

        :param term: The search term to match against the token id, user id or username.
        :return: Personal access token search info.
        """

        url = f"{self.api_url}/tokens/search"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('term', term)

        return self.request(url, request_type='POST', body=True)

    def update_user_authentication_method(self,
                                          user_id: str,
                                          auth_data: str,
                                          auth_service: str) -> dict:
        """
        Updates a user's authentication method.
        This can be used to change them to/from LDAP authentication for example.

        Minimum server version: 4.6.

        Must have the edit_other_users permission.

        :param user_id: User GUID
        :param auth_data: Service-specific authentication data
        :param auth_service: The authentication service such as "email", "gitlab", or "ldap"
        :return: User auth update info.
        """

        url = f"{self.api_url}/{user_id}/auth"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('auth_data', auth_data)
        self.add_to_json('auth_service', auth_service)

        return self.request(url, request_type='PUT', body=True)

    def record_user_action_when_they_accept_or_decline_custom_tos(self,
                                                                  user_id: str,
                                                                  serviceTermsId: str,
                                                                  accepted: str) -> dict:
        """
        Records user action when they accept or decline custom terms of service. Records the action in audit table.
        Updates user's last accepted terms of service ID if they accepted it.

        Minimum server version: 5.4

        Must be logged in as the user being acted on.

        :param user_id: User GUID
        :param serviceTermsId: Service-specific authentication data
        :param accepted: true or false, indicates whether the user accepted or rejected the terms of service.
        :return: TOS record info.
        """

        url = f"{self.api_url}/{user_id}/terms_of_service"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('serviceTermsId', serviceTermsId)
        self.add_to_json('accepted', accepted)

        return self.request(url, request_type='POST', body=True)

    def fetch_user_latest_tos_action_if_was_for_acceptance(self, user_id: str) -> dict:
        """
        Will be deprecated in v6.0 Fetches user's latest terms of
        service action if the latest action was for acceptance.

        Minimum server version: 5.6

        Must be logged in as the user being acted on.

        :param user_id: User GUID
        :return: User accepted terms of service info.
        """

        url = f"{self.api_url}/{user_id}/terms_of_service"

        self.reset()

        return self.request(url, request_type='GET')

    def revoke_all_sessions_from_all_users(self) -> dict:
        """
        For any session currently on the server (including admin) it will be revoked. Clients will be notified to log out users.

        Minimum server version: 5.14

        Must have manage_system permission.

        :return: Sessions revoke info.
        """
        url = f"{self.api_url}/sessions/revoke/all"

        self.reset()

        return self.request(url, request_type='POST')

    def publish_user_typing_websocket_event(self,
                                            user_id: str,
                                            channel_id: str,
                                            parent_id: str = None) -> dict:
        """
        Notify users in the given channel via websocket that the given user is typing.

        Minimum server version: 5.26

        Must have manage_system permission to publish for any user other than oneself.

        :param user_id: User GUID
        :param channel_id: The id of the channel to which to direct the typing event.
        :param parent_id: The optional id of the root post of the thread to which the user is replying. If unset, the typing event is directed at the entire channel.
        :return: User typing websocket event info.
        """

        url = f"{self.api_url}/{user_id}/typing"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('channel_id', channel_id)
        if parent_id is not None:
            self.add_to_json('parent_id', parent_id)

        return self.request(url, request_type='POST', body=True)

    def get_uploads_for_user(self, user_id: str) -> dict:
        """
        Gets all the upload sessions belonging to a user.

        Minimum server version: 5.28

        Must be logged in as the user who created the upload sessions.

        :param user_id: The ID of the user. This can also be "me" which will point to the current user.
        :return: User upload retrieval info.
        """

        url = f"{self.api_url}/{user_id}/uploads"

        self.reset()

        return self.request(url, request_type='GET')

    def get_all_channel_members_from_all_teams_for_user(self,
                                                        user_id: str,
                                                        page: int = None,
                                                        pageSize: int = None) -> dict:
        """
        Get all channel members from all teams for a user.

        Minimum server version: 6.2.0

        Logged in as the user, or have edit_other_users permission.

        :param user_id: The ID of the user. This can also be "me" which will point to the current user.
        :param page: Page specifies which part of the results to return, by PageSize.
        :param pageSize: PageSize specifies the size of the returned chunk of results.
        :return: User upload retrieval info.
        """

        url = f"{self.api_url}/{user_id}/channel_members"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if pageSize is not None:
            self.add_to_json('pageSize', pageSize)

        return self.request(url, request_type='GET', body=True)

    def migrate_user_accounts_authentication_type_to_ldap(self,
                                                          t_from: str,
                                                          match_field: str,
                                                          force: bool) -> dict:
        """
        Migrates accounts from one authentication provider to another.
        For example, you can upgrade your authentication provider from email to LDAP.

        Minimum server version: 5.28

        Must have manage_system permission.

        :param t_from: The current authentication type for the matched users.
        :param match_field: Foreign user field name to match.
        :param force: Toggle force migration.
        :return: Migration info.
        """

        url = f"{self.api_url}/migrate_auth/ldap"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('from', t_from)
        self.add_to_json('match_field', match_field)
        self.add_to_json('force', force)

        return self.request(url, request_type='POST', body=True)

    def migrate_user_accounts_authentication_type_to_saml(self,
                                                          t_from: str,
                                                          matches: str,
                                                          auto: bool) -> dict:
        """
        Migrates accounts from one authentication provider to another. For example, you can upgrade your authentication provider from email to SAML.

        Minimum server version: 5.28

        Must have manage_system permission.

        :param t_from: The current authentication type for the matched users.
        :param matches: Users map.
        :param auto: Toggle auto migration.
        :return: Migration info.
        """

        url = f"{self.api_url}/migrate_auth/saml"

        self.reset()
        self.add_application_json_header()
        self.add_to_json('from', t_from)
        self.add_to_json('matches', matches)
        self.add_to_json('auto', auto)

        return self.request(url, request_type='POST', body=True)

    def get_users_with_invalid_emails(self,
                                      page: int = None,
                                      per_page: int = None) -> dict:
        """
        Get users whose emails are considered invalid.
        It is an error to invoke this API if your team settings enable an open server.

        Requires sysconsole_read_user_management_users.

        :param page: Default: 0. The page to select.
        :param per_page: Default: 60. The number of users per page. There is a maximum limit of 200 users per page.
        :return: User page retrieval info.
        """

        url = f"{self.api_url}/invalid_emails"

        self.reset()
        self.add_application_json_header()
        if page is not None:
            self.add_to_json('page', page)
        if per_page is not None:
            self.add_to_json('per_page', per_page)

        return self.request(url, request_type='GET', body=True)

    def convert_bot_into_user(self,
                              bot_user_id: str,
                              set_system_admin: bool = None,
                              email: str = None,
                              username: str = None,
                              password: str = None,
                              first_name: str = None,
                              last_name: str = None,
                              nickname: str = None,
                              locale: str = None,
                              position: str = None,
                              props: dict = None,
                              notify_props: dict = None) -> dict:
        """
        Convert a bot into a user.

        Minimum server version: 5.26.

        Must have manage_system permission.

        :param bot_user_id: Bot user ID.
        :param set_system_admin: Default: false. Whether to give the user the system admin role.
        :param email: Email to be used in the user creation
        :param username: Username to be used in the user creation
        :param password: Password to be used in the user creation
        :param first_name: First name to be used in the user creation
        :param last_name: Last name to be used in the user creation
        :param nickname: Nickname to be used in the user creation
        :param locale: Locale to be used in the user creation
        :param position: Position to be used in the user creation
        :param props: Props to be used in the user creation
        :param notify_props: Notify props to be used in the user creation
        :return: Bot conversion info.
        """

        url = f"{self.api_url}/{bot_user_id}/convert_to_user"

        self.reset()
        self.add_application_json_header()
        if set_system_admin is not None:
            self.add_to_json('set_system_admin', set_system_admin)
        if email is not None:
            self.add_to_json('email', email)
        if username is not None:
            self.add_to_json('username', username)
        if password is not None:
            self.add_to_json('password', password)
        if first_name is not None:
            self.add_to_json('first_name', first_name)
        if last_name is not None:
            self.add_to_json('last_name', last_name)
        if nickname is not None:
            self.add_to_json('nickname', nickname)
        if locale is not None:
            self.add_to_json('locale', locale)
        if nickname is not None:
            self.add_to_json('position', position)
        if nickname is not None:
            self.add_to_json('props', props)
        if notify_props is not None:
            self.add_to_json('notify_props', notify_props)

        return self.request(url, request_type='POST', body=True)
