from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Req, Invoice, Course

class GetActiveReqView(APIView):
    def post(self, request, *args, **kwargs):
        amount = request.data.get("amount")
        bot = request.data.get("bot")
        try:
            active_req = Req.objects.filter(is_active=True).order_by("?").first()
            invoice = Invoice.objects.create(amount=amount, changer=active_req.user, req=active_req, bot_user=bot)
            invoice.save()
            if not active_req:
                return Response({"error": "No active req found"}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "req": active_req.req,
                "invoice_id": invoice.uniq_id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Invalid request {e}"}, status=status.HTTP_400_BAD_REQUEST)


class GetCourseView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            course = Course.objects.first()
            return Response({"course": f"{course.kzt_course}"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)


class CheckInvoiceView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            uniq_id = request.data.get("uniq_id")
            invoice = Invoice.objects.get(uniq_id=uniq_id)
            return Response({"status": invoice.is_complete, "amount": invoice.amount}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)