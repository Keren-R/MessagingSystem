from rest_framework import status

ERRORS_STATUS_CODE_MAP = {
    "not_found": status.HTTP_404_NOT_FOUND,
    "not_authorised": status.HTTP_403_FORBIDDEN
}


def generate_error_object(error_type: str, error_msg: str):
    error_obj = {
        "error_type": error_type,
        "error_message": error_msg
    }
    return error_obj, ERRORS_STATUS_CODE_MAP[error_type]
