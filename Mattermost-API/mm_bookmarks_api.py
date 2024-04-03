from typing import Union, List, Dict
from Mattermost_Base import Base


class Bookmarks(Base):
    def __init__(self, token: str, server_url: str):
        super().__init__(token, server_url)
        self.api_url = f"{self.base_url}/channels"

    def get_chnl_bkmrks_for_chnl(self,
                                 channel_id: str,
                                 bookmarks_since: int = None) -> dict:
        """
        Gets channel bookmarks.

        Minimum server version: 9.5

        :param channel_id: Channel GUID.
        :param bookmarks_since: Timestamp to filter the bookmarks with.
        If set, the endpoint returns bookmarks that have been added, updated or deleted since its value.
        :return: Channel Bookmarks retrieval info.
        """

        url = f"{self.api_url}/{channel_id}/bookmarks"
        self.reset()
        self.add_application_json_header()
        if bookmarks_since is not None:
            self.add_to_json('bookmarks_since', bookmarks_since)

        return self.request(url, request_type='GET', body=True)

    def create_chnl_bkmrk(self,
                          channel_id: str,
                          display_name: str,
                          tp: str,
                          file_id: str = None,
                          link_url: str = None,
                          image_url: str = None,
                          emoji: str = None) -> dict:
        """
        Creates a new channel bookmark for this channel.

        Minimum server version: 9.5

        Must have the add_bookmark_public_channel or add_bookmark_private_channel depending on the channel type.
        If the channel is a DM or GM, must be a non-guest member.

        :param channel_id: Channel GUID.
        :param display_name: The name of the channel bookmark.
        :param tp: Enum: "link" "file" link for channel bookmarks that reference a link.
        link_url is requied file for channel bookmarks that reference a file.
        file_id is required.
        :param file_id: The ID of the file associated with the channel bookmark.
        Required for bookmarks of type 'file'.
        :param link_url: The URL associated with the channel bookmark.
        Required for bookmarks of type 'link'.
        :param image_url: The URL of the image associated with the channel bookmark.
        Optional, only applies for bookmarks of type 'link'.
        :param emoji: The emoji of the channel bookmark.
        :return: Channel Bookmarks creation info.
        """

        url = f"{self.api_url}/{channel_id}/bookmarks"
        self.reset()
        self.add_application_json_header()
        self.add_to_json('display_name', display_name)
        self.add_to_json('type', tp)
        if file_id is not None:
            self.add_to_json('file_id', file_id)
        if link_url is not None:
            self.add_to_json('link_url', link_url)
        if image_url is not None:
            self.add_to_json('image_url', image_url)
        if emoji is not None:
            self.add_to_json('emoji', emoji)

        return self.request(url, request_type='POST', body=True)

    def upd_chnl_bkmrk(self,
                       channel_id: str,
                       bookmark_id: str,
                       file_id: str = None,
                       display_name: str = None,
                       sort_order: int = None,
                       link_url: str = None,
                       image_url: str = None,
                       emoji: str = None,
                       tp: str = None) -> dict:
        """
        Partially update a channel bookmark by providing only the fields you want to update.
        Ommited fields will not be updated. The fields that can be updated are defined in the request body,
        all other provided fields will be ignored.

        Minimum server version: 9.5

        Must have the edit_bookmark_public_channel or edit_bookmark_private_channel depending on the channel type.
        If the channel is a DM or GM, must be a non-guest member.

        :param channel_id: Channel GUID.
        :param bookmark_id: Bookmark GUID.
        :param file_id: The ID of the file associated with the channel bookmark. Required for bookmarks of type 'file'.
        :param display_name: The name of the channel bookmark.
        :param sort_order: The order of the channel bookmark.
        :param link_url: The URL associated with the channel bookmark.
        Required for bookmarks of type 'link'.
        :param image_url: The URL of the image associated with the channel bookmark.
        :param emoji: The emoji of the channel bookmark.
        :param tp: Enum: "link" "file" link for channel bookmarks that reference a link.
        link_url is requied file for channel bookmarks that reference a file.
        file_id is required.Required for bookmarks of type 'file'.

        :return: Channel Bookmarks update info.
        """

        url = f"{self.api_url}/{channel_id}/bookmarks/{bookmark_id}"
        self.reset()
        self.add_application_json_header()
        if file_id is not None:
            self.add_to_json('file_id', file_id)
        if display_name is not None:
            self.add_to_json('display_name', display_name)
        if sort_order is not None:
            self.add_to_json('sort_order', sort_order)
        if link_url is not None:
            self.add_to_json('link_url', link_url)
        if image_url is not None:
            self.add_to_json('image_url', image_url)
        if emoji is not None:
            self.add_to_json('emoji', emoji)
        if tp is not None:
            self.add_to_json('type', tp)

        return self.request(url, request_type='PATCH', body=True)
