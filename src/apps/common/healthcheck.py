from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def healthcheck(request):
    return Response(data='OK')
