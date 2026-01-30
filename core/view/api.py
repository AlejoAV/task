import time

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer


class BaseAPIResponse(JSONRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response_dict = {
            'status': 'success' if status_code < 400 else 'error',
            'code': status_code,
            'message': data.get('message', 'Request Processed') if isinstance(data, dict) else 'Request failed',
            'time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'data': data
        }
        if status_code >= 400:
            response_dict['error'] = data
            response_dict['data'] = None

        return super(BaseAPIResponse, self).render(response_dict, media_type, renderer_context)
