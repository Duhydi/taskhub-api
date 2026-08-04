from app.schemas.error import ErrorResponse


BAD_REQUEST_RESPONSE = {
    400: {
        "model": ErrorResponse,
        "description": "The request is invalid.",
    },
}

UNAUTHORIZED_RESPONSE = {
    401: {
        "model": ErrorResponse,
        "description": (
            "Access token is missing, invalid, or expired."
        ),
    },
}

FORBIDDEN_RESPONSE = {
    403: {
        "model": ErrorResponse,
        "description": (
            "The authenticated user does not have permission."
        ),
    },
}

NOT_FOUND_RESPONSE = {
    404: {
        "model": ErrorResponse,
        "description": "The requested resource was not found.",
    },
}

CONFLICT_RESPONSE = {
    409: {
        "model": ErrorResponse,
        "description": (
            "The request conflicts with existing data."
        ),
    },
}


AUTH_RESPONSES = {
    **UNAUTHORIZED_RESPONSE,
}

RBAC_RESPONSES = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
}

RESOURCE_RESPONSES = {
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
}

MUTATION_RESPONSES = {
    **BAD_REQUEST_RESPONSE,
    **UNAUTHORIZED_RESPONSE,
    **FORBIDDEN_RESPONSE,
    **NOT_FOUND_RESPONSE,
    **CONFLICT_RESPONSE,
}