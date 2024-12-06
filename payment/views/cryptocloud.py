from adrf.views import APIView
from adrf.requests import AsyncRequest
from rest_framework.response import Response
import jwt
from django.http import JsonResponse
from config import CRYPTOCLOUD_SECRET_KEY as secret_key
from payment.services import *
from bot.services.callback_service import send_manual_successful_payment


class Postback(APIView):
    async def post(self, request: AsyncRequest):
        # Get the parameters from the POST request
        status = request.data.get('status')
        invoice_id = request.data.get('invoice_id')
        amount_crypto = request.data.get('amount_crypto')
        currency = request.data.get('currency')
        order_id = request.data.get('order_id')
        token = request.data.get('token')

        # Check if all required parameters are present
        if not all([status, invoice_id, amount_crypto, currency, order_id, token]):
            print("missing param")
            return JsonResponse({"error": "Missing parameters"}, status=400)

        try:
            # Decode the JWT token
            jwt.decode(token, secret_key, algorithms=['HS256'])

            # change account as payed
            account: Account = await get_account_by_id(order_id)
            await account_pay(account)
            # send successfully payment newsletter to user
            bot_user = await account.get_bot_user
            await send_manual_successful_payment(bot_user.user_id)

            # Prepare the response string
            response = {
                "Payment status": status,
                "Invoice ID": invoice_id,
                "Amount in crypto": f"{amount_crypto} {currency}",
                "Order ID": order_id,
            }

            return JsonResponse(response)
        except jwt.InvalidTokenError:
            print("invalid toekn")
            return JsonResponse({"error": "Invalid token"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
