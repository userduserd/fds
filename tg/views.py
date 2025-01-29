from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Req, Invoice, Course

class GetActiveReqView(APIView):
    def post(self, request, *args, **kwargs):
        amount = request.get("amount")


        try:
            active_req = Req.objects.filter(is_active=True).sort("?").first()
            invoice = Invoice.objects.create(amount=amount, changer=active_req.user)

            if not active_req:
                return Response({"error": "No active req found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "req": active_req.req,
                "invoice_id": invoice.uniq_id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Invalid request {e}"}, status=status.HTTP_400_BAD_REQUEST)


class GetCourseView(APIView):
    def post(self, request, *args, **kwargs):
        try:
