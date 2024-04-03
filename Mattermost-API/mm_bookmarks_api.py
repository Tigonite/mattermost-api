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
