from django.core.cache import cache
# from django.contrib.gis.geoip2 import GeoIP2

## TODO: Fix Is GDAL installed? If it is, try setting GDAL_LIBRARY_PATH in your settings error message
## NOTE: https://stackoverflow.com/questions/70572345/django-could-not-find-the-gdal-library-osx
# def get_location_from_ip(ip):
#     g = GeoIP2()
#     return g.geos(ip)
#
# class GeoCacheMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         location = get_location_from_ip(request.META['REMOTE_ADDR'])
#         cache_key = f'geocache:{location}:{request.path}'
#         response = cache.get(cache_key)
#         if not response:
#             response = self.get_response(request)
#             cache.set(cache_key, response)
#         return response