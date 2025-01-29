from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Req

class GetActiveReqView(APIView):
    def post(self, request, *args, **kwargs):
        print("SOME1 PINGED")
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            active_req = Req.objects.filter(is_active=True).first()
            if not active_req:
                return Response({"error": "No active req found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "id": active_req.id,
                "user_id": active_req.user_id,
                "bank": active_req.bank,
                "name": active_req.name,
                "req": active_req.req,
                "is_active": active_req.is_active
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Invalid request {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # user_id = request.data.get('user_id')
        # if not user_id:
        #     return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            active_req = Req.objects.filter(is_active=True).first()
            if not active_req:
                return Response({"error": "No active req found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "id": active_req.id,
                "user_id": active_req.user_id,
                "bank": active_req.bank,
                "name": active_req.name,
                "req": active_req.req,
                "is_active": active_req.is_active
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Invalid request {e}"}, status=status.HTTP_400_BAD_REQUEST)
