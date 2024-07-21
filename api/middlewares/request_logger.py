import logging

class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"Incoming request: {request.path}")
        logging.info(f"Request method: {request.method}")
        logging.info(f"Request body: {request.body}")
        logging.info(f"Request query params: {request.GET}")
        response = self.get_response(request)
        return response
