def get_headers(authorization_dict: dict):
    return authorization_dict["headers"]

def get_base_url(authorization_dict: dict):
    return authorization_dict["base_url"]

def update_path_with_query_params(path: str, authorization_dict: dict) -> str:
    if authorization_dict.get("query_params"):
        query_params = authorization_dict["query_params"]
        path += "?"
        for key, value in query_params.items():
            path += f"{key}={value}&"
        path = path[:-1]
    return path

def update_request_body_with_authorization_data(request_body: dict, authorization_dict: dict):
    if authorization_dict.get("request_body"):
        for key, value in authorization_dict["request_body"].items():
            request_body[key] = value
    return request_body

def update_request(path: str, headers: dict, requestBody: dict, authorization_dict: dict) -> (str, dict, dict):
    headers = get_headers(authorization_dict)
    path = update_path_with_query_params(path, authorization_dict)
    requestBody = update_request_body_with_authorization_data(requestBody, authorization_dict)
    return path, headers, requestBody