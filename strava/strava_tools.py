import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action, Tool
from typing import Optional, Type
import json

class GetActivityRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity.')
    include_all_efforts: Optional[bool] = Field(None, description='To include all segment efforts.')

class GetActivityResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    activity: dict = Field(..., description='The details of the activity.')

class GetActivity(Action):
    """
    Get activity details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Activity'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetActivityRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetActivityResponse
    
    def execute(self, request: GetActivityRequest, authorisation_data: dict) -> GetActivityResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id
        if request.include_all_efforts:
            include_all_efforts = request.include_all_efforts
        else:
            include_all_efforts = True
        
        params = {
            'include_all_efforts': include_all_efforts
        }

        response = requests.get(f'https://www.strava.com/api/v3/activities/{activity_id}', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return GetActivityResponse(success=False, activity=response_json)
        
        return GetActivityResponse(success=True, activity=response_json)


# GetAthlete action
class GetAthleteRequest(BaseModel):
    pass

class GetAthleteResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    athlete: dict = Field(..., description='The details of the athlete.')

class GetAthlete(Action):
    """
    Get athlete details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Athlete'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetAthleteRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetAthleteResponse
    
    def execute(self, request: GetAthleteRequest, authorisation_data: dict) -> GetAthleteResponse:
        headers = authorisation_data["headers"]

        response = requests.get(f'https://www.strava.com/api/v3/athlete', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetAthleteResponse(success=False, athlete=response_json)
        
        return GetAthleteResponse(success=True, athlete=response_json)


# GetAthleteStats action
class GetAthleteStatsRequest(BaseModel):
    athlete_id: int = Field(..., description='The id of the athlete.')

class GetAthleteStatsResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    stats: dict = Field(..., description='The statistics of the athlete.')

class GetAthleteStats(Action):
    """
    Get athlete statistics.
    """
    @property
    def display_name(self) -> str:
        return 'Get Athlete Stats'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetAthleteStatsRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetAthleteStatsResponse
    
    def execute(self, request: GetAthleteStatsRequest, authorisation_data: dict) -> GetAthleteStatsResponse:
        headers = authorisation_data["headers"]
        athlete_id = request.athlete_id

        response = requests.get(f'https://www.strava.com/api/v3/athletes/{athlete_id}/stats', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetAthleteStatsResponse(success=False, stats=response_json)
        
        return GetAthleteStatsResponse(success=True, stats=response_json)


# GetAthleteZones action
class GetAthleteZonesRequest(BaseModel):
    pass 

class GetAthleteZonesResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    zones: dict = Field(..., description='The zones of the athlete.')

class GetAthleteZones(Action):
    """
    Returns the the authenticated athlete's heart rate and power zones.
    """
    @property
    def display_name(self) -> str:
        return 'Get Athlete Zones'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetAthleteZonesRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetAthleteZonesResponse
    
    def execute(self, authorisation_data: dict) -> GetAthleteZonesResponse:
        headers = authorisation_data["headers"]

        response = requests.get(f'https://www.strava.com/api/v3/athlete/zones', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetAthleteZonesResponse(success=False, zones=response_json)
        
        return GetAthleteZonesResponse(success=True, zones=response_json)


# GetClub action
class GetClubRequest(BaseModel):
    club_id: int = Field(..., description='The id of the club.')

class GetClubResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    club: dict = Field(..., description='The details of the club.')

class GetClub(Action):
    """
    Get club details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Club'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetClubRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetClubResponse
    
    def execute(self, request: GetClubRequest, authorisation_data: dict) -> GetClubResponse:
        headers = authorisation_data["headers"]
        club_id = request.club_id

        response = requests.get(f'https://www.strava.com/api/v3/clubs/{club_id}', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetClubResponse(success=False, club=response_json)
        
        return GetClubResponse(success=True, club=response_json)

# GetClubActivities action
class GetClubActivitiesRequest(BaseModel):
    club_id: int = Field(..., description='The id of the club.')
    page: Optional[int] = Field(default=1, description='The page number of the activities.') 
    per_page: Optional[int] = Field(default=30, description='The number of activities per page.')

class GetClubActivitiesResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    activities: dict = Field(..., description='The activities of the club.')

class GetClubActivities(Action):
    """
    Get club activities.
    """
    @property
    def display_name(self) -> str:
        return 'Get Club Activities'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetClubActivitiesRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetClubActivitiesResponse
    
    def execute(self, request: GetClubActivitiesRequest, authorisation_data: dict) -> GetClubActivitiesResponse:
        headers = authorisation_data["headers"]
        club_id = request.club_id
        params = {
            'page': request.page,
            'per_page': request.per_page
        }

        response = requests.get(f'https://www.strava.com/api/v3/clubs/{club_id}/activities', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return GetClubActivitiesResponse(success=False, activities=response_json)
        
        return GetClubActivitiesResponse(success=True, activities=response_json)


# GetGear action
class GetGearRequest(BaseModel):
    gear_id: str = Field(..., description='The id of the gear.')

class GetGearResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    gear: dict = Field(..., description='The details of the gear.')

class GetGear(Action):
    """
    Get gear details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Gear'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetGearRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetGearResponse
    
    def execute(self, request: GetGearRequest, authorisation_data: dict) -> GetGearResponse:
        headers = authorisation_data["headers"]
        gear_id = request.gear_id

        response = requests.get(f'https://www.strava.com/api/v3/gear/{gear_id}', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetGearResponse(success=False, gear=response_json)
        
        return GetGearResponse(success=True, gear=response_json)


# GetRoute action
class GetRouteRequest(BaseModel):
    route_id: int = Field(..., description='The id of the route.')

class GetRouteResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    route: dict = Field(..., description='The details of the route.')

class GetRoute(Action):
    """
    Get route details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Route'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetRouteRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetRouteResponse
    
    def execute(self, request: GetRouteRequest, authorisation_data: dict) -> GetRouteResponse:
        headers = authorisation_data["headers"]
        route_id = request.route_id

        response = requests.get(f'https://www.strava.com/api/v3/routes/{route_id}', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetRouteResponse(success=False, route=response_json)
        
        return GetRouteResponse(success=True, route=response_json)


# GetSegment action
class GetSegmentRequest(BaseModel):
    segment_id: int = Field(..., description='The id of the segment.')

class GetSegmentResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    segment: dict = Field(..., description='The details of the segment.')

class GetSegment(Action):
    """
    Get segment details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Segment'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetSegmentRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetSegmentResponse
    
    def execute(self, request: GetSegmentRequest, authorisation_data: dict) -> GetSegmentResponse:
        headers = authorisation_data["headers"]
        segment_id = request.segment_id

        response = requests.get(f'https://www.strava.com/api/v3/segments/{segment_id}', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetSegmentResponse(success=False, segment=response_json)
        
        return GetSegmentResponse(success=True, segment=response_json)


# GetSegmentEffort action
class GetSegmentEffortRequest(BaseModel):
    segment_effort_id: int = Field(..., description='The id of the segment effort.')

class GetSegmentEffortResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    segment_effort: dict = Field(..., description='The details of the segment effort.')

class GetSegmentEffort(Action):
    """
    Get segment effort details.
    """
    @property
    def display_name(self) -> str:
        return 'Get Segment Effort'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetSegmentEffortRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetSegmentEffortResponse
    
    def execute(self, request: GetSegmentEffortRequest, authorisation_data: dict) -> GetSegmentEffortResponse:
        headers = authorisation_data["headers"]
        segment_effort_id = request.segment_effort_id

        response = requests.get(f'https://www.strava.com/api/v3/segment_efforts/{segment_effort_id}', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetSegmentEffortResponse(success=False, segment_effort=response_json)
        
        return GetSegmentEffortResponse(success=True, segment_effort=response_json)


# GetStreams action
class GetStreamsRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity.')
    stream_types: str = Field(..., description='Desired stream types. May take one of the following values')
    key_by_type: Optional[bool] = Field(default=True, description='Must be true to return streams')

class GetStreamsResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    streams: dict = Field(..., description='The streams data for the activity.')

class GetStreams(Action):
    """
    Get activity streams.
    """
    @property
    def display_name(self) -> str:
        return 'Get Streams'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetStreamsRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetStreamsResponse
    
    def execute(self, request: GetStreamsRequest, authorisation_data: dict) -> GetStreamsResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id
        params = {
            "keys": request.stream_types,
            'key_by_type': request.key_by_type
        }

        response = requests.get(f'https://www.strava.com/api/v3/activities/{activity_id}/streams', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return GetStreamsResponse(success=False, streams=response_json)
        
        return GetStreamsResponse(success=True, streams=response_json)


# # UploadActivity action
# class UploadActivityRequest(BaseModel):
#     file_path: str = Field(..., description='Path to the file to upload.')

# class UploadActivityResponse(BaseModel):
#     success: bool = Field(..., description='Whether the request was successful.')
#     activity_id: int = Field(None, description='The id of the uploaded activity, if successful.')

# class UploadActivity(Action):
#     """
#     Upload activity.
#     """
#     @property
#     def display_name(self) -> str:
#         return 'Upload Activity'
    
#     @property
#     def request_schema(self) -> Type[BaseModel]:
#         return UploadActivityRequest
    
#     @property
#     def response_schema(self) -> Type[BaseModel]:
#         return UploadActivityResponse
    
#     def execute(self, request: UploadActivityRequest, authorisation_data: dict) -> UploadActivityResponse:
#         headers = authorisation_data["headers"]
#         file_path = request.file_path

#         # Implementation to upload activity file to Strava
#         # Example: Using requests.post() to upload the file to the Strava API
#         # This implementation may vary based on the specific requirements and API specifications

#         return UploadActivityResponse(success=True, activity_id=123456)  # Dummy response, actual implementation needed

# CreateActivity action
class CreateActivityRequest(BaseModel):
    name: str = Field(..., description='The name of the activity.')
    type: str = Field(..., description='The type of the activity (e.g., "ride", "run").')
    sport_type: str = Field(..., description='The sport type of the activity (e.g., Run, MountainBikeRide, Ride, etc.).')
    start_date_local: str = Field(..., description='The local start date time of the activity in ISO 8601 format.')
    elapsed_time: int = Field(..., description='The elapsed time of the activity in seconds.')
    description: str = Field(None, description='Optional description of the activity.')
    distance: float = Field(None, description='Optional distance of the activity.')
    trainer: bool = Field(None, description='Set to 1 to mark as a trainer activity')
    commute: bool = Field(None, description='Set to 1 to mark as a commute')

class CreateActivityResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    activity: dict = Field(None, description='The details of the created activity, if successful.')

class CreateActivity(Action):
    """
    Create a new activity.
    """
    @property
    def display_name(self) -> str:
        return 'Create Activity'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return CreateActivityRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return CreateActivityResponse
    
    def execute(self, request: CreateActivityRequest, authorisation_data: dict) -> CreateActivityResponse:
        headers = authorisation_data["headers"]
        data = request.dict()

        response = requests.post('https://www.strava.com/api/v3/activities', headers=headers, json=data)
        response_json = response.json()
        if response.status_code != 201:
            return CreateActivityResponse(success=False, activity=response_json)
        
        return CreateActivityResponse(success=True, activity=response_json)


# UpdateActivity action
class UpdateActivityRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity to update.')
    name: str = Field(None, description='Optional new name of the activity.')
    type: str = Field(None, description='Optional new type of the activity (e.g., "ride", "run").')
    description: str = Field(None, description='Optional new description of the activity.')
    private: bool = Field(None, description='Optional flag to update activity privacy.')
    commute: bool = Field(None, description='Optional flag to update activity commute status.')

class UpdateActivityResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    activity: dict = Field(None, description='The updated details of the activity, if successful.')

class UpdateActivity(Action):
    """
    Update an existing activity.
    """
    @property
    def display_name(self) -> str:
        return 'Update Activity'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return UpdateActivityRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return UpdateActivityResponse
    
    def execute(self, request: UpdateActivityRequest, authorisation_data: dict) -> UpdateActivityResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id
        data = {
            'name': request.name,
            'type': request.type,
            'description': request.description,
            'private': request.private,
            'commute': request.commute
        }
        # filter none values 
        data = {k: v for k, v in data.items() if v is not None}

        data_json = json.dumps(data)

        response = requests.put(f'https://www.strava.com/api/v3/activities/{activity_id}', headers=headers, json=data_json)
        response_json = response.json()
        if response.status_code != 200:
            return UpdateActivityResponse(success=False, activity=response_json)
        
        return UpdateActivityResponse(success=True, activity=response_json)


# ListActivityComments action
class ListActivityCommentsRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity.')
    page: Optional[int] = Field(default=1, description='The page number of the comments.')
    page_size: Optional[int] = Field(default=30, description='The number of comments per page.')

class ListActivityCommentsResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    comments: dict = Field(..., description='The comments on the activity.')

class ListActivityComments(Action):
    """
    List comments on an activity.
    """
    @property
    def display_name(self) -> str:
        return 'List Activity Comments'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return ListActivityCommentsRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return ListActivityCommentsResponse
    
    def execute(self, request: ListActivityCommentsRequest, authorisation_data: dict) -> ListActivityCommentsResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id
        params = {
            'page': request.page,
            'page_size': request.page_size
        }

        response = requests.get(f'https://www.strava.com/api/v3/activities/{activity_id}/comments', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return ListActivityCommentsResponse(success=False, comments=response_json)
        
        return ListActivityCommentsResponse(success=True, comments=response_json)


# ListActivityKudoers action
class ListActivityKudoersRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity.')
    page: Optional[int] = Field(default=1, description='The page number of the kudoers.')
    per_page: Optional[int] = Field(default=30, description='The number of kudoers per page.')

class ListActivityKudoersResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    kudoers: dict = Field(..., description='The users who gave kudos to the activity.')

class ListActivityKudoers(Action):
    """
    List users who gave kudos to an activity.
    """
    @property
    def display_name(self) -> str:
        return 'List Activity Kudoers'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return ListActivityKudoersRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return ListActivityKudoersResponse
    
    def execute(self, request: ListActivityKudoersRequest, authorisation_data: dict) -> ListActivityKudoersResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id
        params = {
            'page': request.page,
            'per_page': request.per_page
        }

        response = requests.get(f'https://www.strava.com/api/v3/activities/{activity_id}/kudos', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return ListActivityKudoersResponse(success=False, kudoers=response_json)
        
        return ListActivityKudoersResponse(success=True, kudoers=response_json)


# ListActivityLaps action
class ListActivityLapsRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity.')

class ListActivityLapsResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    laps: dict = Field(..., description='The laps data for the activity.')

class ListActivityLaps(Action):
    """
    List laps for an activity.
    """
    @property
    def display_name(self) -> str:
        return 'List Activity Laps'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return ListActivityLapsRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return ListActivityLapsResponse
    
    def execute(self, request: ListActivityLapsRequest, authorisation_data: dict) -> ListActivityLapsResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id

        response = requests.get(f'https://www.strava.com/api/v3/activities/{activity_id}/laps', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return ListActivityLapsResponse(success=False, laps=response_json)
        
        return ListActivityLapsResponse(success=True, laps=response_json)


# GetActivityZones action
class GetActivityZonesRequest(BaseModel):
    activity_id: int = Field(..., description='The id of the activity.')

class GetActivityZonesResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    zones: dict = Field(..., description='The zones data for the activity.')

class GetActivityZones(Action):
    """
    Get activity zones.
    """
    @property
    def display_name(self) -> str:
        return 'Get Activity Zones'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetActivityZonesRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetActivityZonesResponse
    
    def execute(self, request: GetActivityZonesRequest, authorisation_data: dict) -> GetActivityZonesResponse:
        headers = authorisation_data["headers"]
        activity_id = request.activity_id

        response = requests.get(f'https://www.strava.com/api/v3/activities/{activity_id}/zones', headers=headers)
        response_json = response.json()
        if response.status_code != 200:
            return GetActivityZonesResponse(success=False, zones=response_json)
        
        return GetActivityZonesResponse(success=True, zones=response_json)


# ListClubMembers action
class ListClubMembersRequest(BaseModel):
    club_id: int = Field(..., description='The id of the club.')
    page: Optional[int] = Field(default=1, description='The page number of the members.')
    per_page: Optional[int] = Field(default=30, description='The number of members per page.')

class ListClubMembersResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    members: list = Field(..., description='The members of the club.')

class ListClubMembers(Action):
    """
    List members of a club.
    """
    @property
    def display_name(self) -> str:
        return 'List Club Members'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return ListClubMembersRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return ListClubMembersResponse
    
    def execute(self, request: ListClubMembersRequest, authorisation_data: dict) -> ListClubMembersResponse:
        headers = authorisation_data["headers"]
        club_id = request.club_id
        params = {
            'page': request.page,
            'per_page': request.per_page
        }

        response = requests.get(f'https://www.strava.com/api/v3/clubs/{club_id}/members', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return ListClubMembersResponse(success=False, members=response_json)
        
        return ListClubMembersResponse(success=True, members=response_json)


# UpdateAthlete action
class UpdateAthleteRequest(BaseModel):
    weight: float = Field(None, description='Optional new weight of the athlete.')

class UpdateAthleteResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    athlete: dict = Field(None, description='The updated details of the athlete, if successful.')

class UpdateAthlete(Action):
    """
    Update athlete details.
    """
    @property
    def display_name(self) -> str:
        return 'Update Athlete'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return UpdateAthleteRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return UpdateAthleteResponse
    
    def execute(self, request: UpdateAthleteRequest, authorisation_data: dict) -> UpdateAthleteResponse:
        headers = authorisation_data["headers"]
        data = {
            'weight': request.weight
        }
        data_json = json.dumps(data)

        response = requests.put('https://www.strava.com/api/v3/athlete', headers=headers, json=data_json)
        response_json = response.json()
        if response.status_code != 200:
            return UpdateAthleteResponse(success=False, athlete=response_json)
        
        return UpdateAthleteResponse(success=True, athlete=response_json)


# ListAthleteRoutes action
class ListAthleteRoutesRequest(BaseModel):
    athlete_id: int = Field(..., description='The id of the athlete.')
    page: Optional[int] = Field(default=1, description='The page number of the routes.')
    per_page: Optional[int] = Field(default=30, description='The number of routes per page.')

class ListAthleteRoutesResponse(BaseModel):
    success: bool = Field(..., description='Whether the request was successful.')
    routes: dict = Field(..., description='The routes of the athlete.')

class ListAthleteRoutes(Action):
    """
    List routes of an athlete.
    """
    @property
    def display_name(self) -> str:
        return 'List Athlete Routes'
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return ListAthleteRoutesRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return ListAthleteRoutesResponse
    
    def execute(self, request: ListAthleteRoutesRequest, authorisation_data: dict) -> ListAthleteRoutesResponse:
        headers = authorisation_data["headers"]
        athlete_id = request.athlete_id
        params = {
            'page': request.page,
            'per_page': request.per_page
        }

        response = requests.get(f'https://www.strava.com/api/v3/athletes/{athlete_id}/routes', headers=headers, params=params)
        response_json = response.json()
        if response.status_code != 200:
            return ListAthleteRoutesResponse(success=False, routes=response_json)
        
        return ListAthleteRoutesResponse(success=True, routes=response_json)


class Strava(Tool):
    def actions(self) -> list:
        return [
            GetActivity,
            GetAthlete,
            GetAthleteStats,
            GetAthleteZones,
            GetClub,
            GetClubActivities,
            GetGear,
            GetRoute,
            GetSegment,
            GetSegmentEffort,
            GetStreams,
            CreateActivity,
            UpdateActivity,
            ListActivityComments,
            ListActivityKudoers,
            ListActivityLaps,
            GetActivityZones,
            ListClubMembers,
            UpdateAthlete,
            ListAthleteRoutes,
        ]
    
    def triggers(self) -> list:
        return []
    
__all__ = ['Strava']