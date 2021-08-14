import typing
from typing import Dict, Any, List, Union, Callable

from requests import Response

from http_requests.models import ResponseObject

if typing.TYPE_CHECKING:
    from wise import UserProfiles


def get_response_object_data_from_response(response: Response, data: Dict[str, Any] = None) -> Dict[str, Any]:
    if data is None:
        data = response.json()
    data.update({"response": response, "is_successful": 200 <= response.status_code <= 299, "endpoint": response.url})
    return data


def get_model_from_response(response: Response, data_class: Callable) -> Union[List[ResponseObject], ResponseObject]:
    if isinstance(response.json(), Dict):
        return data_class(**get_response_object_data_from_response(response))
    elif isinstance(response.json(), List):
        data_list: List[UserProfiles] = []
        for data in response.json():
            data_list.append(data_class(**get_response_object_data_from_response(response, data)))
        return data_list  # type: ignore

    return None
