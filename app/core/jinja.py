from app.core.templates import templates


def configure_jinja():

    def inject_i18n(request):

        return {
            "t": request.state.i18n
        }

    templates.context_processors.append(inject_i18n)