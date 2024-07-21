from rest_framework.renderers import JSONRenderer

class GlobalResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "status": "success",
            "code": status_code,
            "data": data,
            "message": None
        }

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None

            # Handle validation errors
            if isinstance(data, dict):
                if 'detail' in data:
                    response["message"] = data['detail']
                elif 'non_field_errors' in data:
                    response["message"] = data['non_field_errors']
                else:
                    response["message"] = "Validation failed, check the data sent"
                    response["errors"] = self.format_validation_errors(data)
            else:
                response["message"] = data

        return super(GlobalResponseRenderer, self).render(response, accepted_media_type, renderer_context)

    def format_validation_errors(self, errors):
        message = []
        for field, error_list in errors.items():
            for error in error_list:
                message.append(f"{field}: {error}")
        return message
