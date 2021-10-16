from rest_framework.response import Response
from rest_framework.views import exception_handler


def core_exception_handler(exc, context) -> Response:  # type: ignore
    response = exception_handler(exc, context)
    handlers = {
        "ValidationError": _handle_generic_error,
        "NotFound": _handle_not_found,
        "NotAuthenticated": _handle_not_authenticated,
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response


def _handle_generic_error(exc, context, response) -> Response:  # type: ignore
    response.data = {"errors": response.data}
    response.status_code = 400
    return response


def _handle_not_found(exc, context, response) -> Response:  # type: ignore
    view = context.get("view", None)

    if view and hasattr(view, "queryset") and view.queryset is not None:
        error_key = view.queryset.model._meta.verbose_name

        response.data = {"errors": {error_key: response.data["detail"]}}

    else:
        response = _handle_generic_error(exc, context, response)

    return response


def _handle_not_authenticated(exc, context, response) -> Response:  # type: ignore
    response.data = {
        "errors": {"detail": "Authentication credentials were not provided."}
    }
    response.status_code = 401
    return response
