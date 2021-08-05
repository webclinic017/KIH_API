from typing import Any, Dict

import api.responses


def lambda_event(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    parameters = event["queryStringParameters"]
    if parameters is None:
        return api.responses.__get_client_error_response("No parameters")

    api_token = parameters["apiToken"]
    if not api.responses.is_authenticated(api_token):
        return api.responses.__get_unauthenticated_response()

    return api.process_request(event)