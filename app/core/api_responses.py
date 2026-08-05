from typing import Any

ApiResponses = dict[int | str, dict[str, Any]]

BAD_REQUEST_RESPONSE: ApiResponses = {
    400: {
        "description": "Bad Request",
    },
}

UNAUTHORIZED_RESPONSE: ApiResponses = {
    401: {
        "description": "Unauthorized",
    },
}

FORBIDDEN_RESPONSE: ApiResponses = {
    403: {
        "description": "Forbidden",
    },
}

NOT_FOUND_RESPONSE: ApiResponses = {
    404: {
        "description": "Resource Not Found",
    },
}

CONFLICT_RESPONSE: ApiResponses = {
    409: {
        "description": "Conflict",
    },
}

RESOURCE_RESPONSES: ApiResponses = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
}

MUTATION_RESPONSES: ApiResponses = {
    **BAD_REQUEST_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
    **CONFLICT_RESPONSE,
}