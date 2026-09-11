from starlette.middleware.base import BaseHTTPMiddleware

from app.services.i18n import I18N


class LocalizationMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        language = "pt-BR"

        if "session" in request.scope:
            language = request.session.get("language", "pt-BR")

        request.state.language = language
        request.state.i18n = I18N(language)

        response = await call_next(request)

        return response