#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from asyncio import streams
from distutils.command.config import config
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
from urllib import response
from urllib.parse import urlparse

import requests
import json
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator
from datetime import datetime, timedelta



# Source
class SourceShortcut(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        base_url = "https://api.app.shortcut.com/"
        try:
            response = requests.request(
                "GET",
                url=base_url,
                headers={
                    "Content-Type": "application/json",
                    "Shortcut-Token": config["api_token"],
                },
            )

            if response.status_code != 200:
                message = response.json()
                error_message = message.get("error")
                if error_message:
                    return False, error_message
                response.raise_for_status()
        except Exception as e:
            return False, e

        return True, None


    
    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        authenticator = TokenAuthenticator(config["api_token"])
        """
        TODO: Replace the streams below with your own streams.

        :param config: A Mapping of the user input configuration as defined in the connector spec.
        """
        
        
        list = [{"start": "2017-10-01", "end": "2020-01-31"}, 
        {"start": "2020-02-01", "end": "2020-06-30"}, 
        {"start": "2020-07-01", "end": "2020-09-30"}, 
        {"start": "2020-10-01", "end": "2020-12-31"}, 
        {"start": "2021-01-01", "end": "2021-03-01"}, 
        {"start": "2021-03-02", "end": "2021-06-30"},
        {"start": "2021-07-01", "end": "2021-10-31"}, 
        {"start": "2021-11-01", "end": "2021-12-31"}, 
        {"start": "2022-01-01", "end": "2022-02-27"},
        {"start": "2022-02-28", "end": "2022-03-01"}]

        


        # for i in list:
        #     x = self.stories.append(Stories(start_date=i["start"], end_date=i["end"], auth=config["api_token"]))
        #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(i) + " - XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        #auth = TokenAuthenticator(token="api_key")  # Oauth2Authenticator is also available if you need oauth support
        return [Categories(start_date=config['start_date'], auth=config["api_token"])
        ,EntityTemplates(start_date=config['start_date'], auth=config["api_token"])
        ,EpicWorkflows(start_date=config['start_date'], auth=config["api_token"])
        ,Epics(start_date=config['start_date'], auth=config["api_token"])
        ,Files(start_date=config['start_date'], auth=config["api_token"])
        ,Groups(start_date=config['start_date'], auth=config["api_token"])
        ,Iterations(start_date=config['start_date'], auth=config["api_token"])
        ,Labels(start_date=config['start_date'], auth=config["api_token"])
        ,LinkedFiles(start_date=config['start_date'], auth=config["api_token"])
        ,Member(start_date=config['start_date'], auth=config["api_token"])
        ,Members(start_date=config['start_date'], auth=config["api_token"])
        ,Milestones(start_date=config['start_date'], auth=config["api_token"])
        ,Projects(start_date=config['start_date'], auth=config["api_token"])
        ,Repositories(start_date=config['start_date'], auth=config["api_token"])
        ,Stories(start_date="2017-10-01", end_date="2020-01-31", auth=config["api_token"])
        ,Stories2(start_date="2020-02-01", end_date="2020-06-30", auth=config["api_token"])
        ,Stories3(start_date="2020-07-01", end_date="2020-09-30", auth=config["api_token"])
        ,Stories4(start_date="2020-10-01", end_date="2020-12-31", auth=config["api_token"])
        ,Stories5(start_date="2021-01-01", end_date="2021-03-01", auth=config["api_token"])
        ,Stories6(start_date="2021-03-02", end_date="2021-05-31", auth=config["api_token"])
        ,Stories7(start_date="2021-06-01", end_date="2021-08-31", auth=config["api_token"])
        ,Stories8(start_date="2021-09-01", end_date="2021-11-30", auth=config["api_token"])
        ,Stories9(start_date="2021-12-01", end_date="2022-01-31", auth=config["api_token"])
        ,Stories10(start_date="2022-02-01", end_date="2022-03-31", auth=config["api_token"])
        ,Workflows(start_date=config['start_date'], auth=config["api_token"])]



class Categories(HttpStream): 
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "categories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class EntityTemplates(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "entity-templates"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None


class EpicWorkflows(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "epic-workflow"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        return [response.json()]
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Epics(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "epics"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None


class Files(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "files"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Groups(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "groups"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Iterations(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "iterations"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Labels(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "labels"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None


class LinkedFiles(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "linked-files"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Member(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "member"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return [response.json()]
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Members(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "members"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Milestones(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "milestones"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Projects(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "projects"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None



class Repositories(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "repositories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None




class Stories(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []




class Stories2(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []





class Stories3(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Stories4(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Stories5(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Stories6(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []




class Stories7(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Stories8(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Stories9(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Stories10(HttpStream):
    url_base = "https://api.app.shortcut.com"
    cursor_field = "updated_at"
    primary_key = "id"
    #query = "completed:2017-01-01..2020-12-31"
    query = ""
    page_size = 1
    pg_count = 0
    token = ""
    i = 0
    list = []
        
    

    def __init__(self, auth: str, start_date: datetime, end_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.auth = auth
        self.query = 'created:' + self.start_date + '..' + self.end_date


    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "api/v3/search/stories"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}


    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        params = {"page_size": self.page_size, "query": self.query, "token": self.auth}
        if next_page_token:
            #print(next_page_token)
            return next_page_token.lstrip("api/v3/search/stories?") + '&token=' + self.auth
        else:
            return params

    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        #while self.pg_count < response.json().get("total"):
        try:
            decode_response = response.json()
            next_page_token = decode_response.get("next")
            self.pg_count += 1
            if response.status_code != 200:
                message = response.json()
                error_message = message.get("XXXXXXXXXXXXXXXXX - error - PPPPPPPPPPPPPPPPPPP")
                if error_message:
                    return False, error_message
            response.raise_for_status()
            return next_page_token
        except Exception as e:
            return False, e    

        

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        self.i = self.i+1
        #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - ITERATION - " + str(self.i))
        self.list.append(response.json()["data"][0])
        # if response.json().get("next") != None:
        #     #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - " + response.json().get("next"))
        if response.json().get("next") == None:
            #print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - NONE REACHED - ")
            #print(len(self.list))
            return self.list
            # for y,x in enumerate(self.list):
            #     print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX - THIS IS THE OUTPUT - " + str(y)) 
            #     print(x)
                # print(x["data"][0])
                # print(type(x["data"][0]))
                # print(type(response.json()))
                #print(self.list[0]["data"][0])
        
        
        return []



class Workflows(HttpStream):
    url_base = "https://api.app.shortcut.com/api/v3/"
    cursor_field = "updated_at"
    primary_key = "id"
    

    def __init__(self, auth: str, start_date: datetime, **kwargs):
        super().__init__()
        self.start_date = start_date
        self.auth = auth

    def path(self, stream_state: Mapping[str, Any] = None, 
        next_page_token: Mapping[str, Any] = None,
        stream_slice: Mapping[str, Any] = None) -> str:
        return "workflows"
    
    
    def request_headers(
        self, 
        stream_state: Mapping[str, Any], 
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Mapping[str, Any]:
        return {"Content-Type": "application/json","Shortcut-Token": self.auth}

    def parse_response(
        self,
        response: requests.Response,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, Any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> Iterable[Mapping]:
        # The response is a simple JSON whose schema matches our stream's schema exactly, 
        # so we just return a list containing the response
        x=response.json()
        print(type(x))
        return response.json()
    
    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        # The API does not offer pagination, 
        # so we return None to indicate there are no more pages in the response
        return None


