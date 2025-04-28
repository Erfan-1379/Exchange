from .models import CurrencyHistory
from rest_framework.views import APIView
from datetime import datetime
import requests
from rest_framework.response import Response
from decouple import config

def persian_to_english_numbers(s):
    persian_numbers = '۰۱۲۳۴۵۶۷۸۹'
    english_numbers = '0123456789'
    table = str.maketrans(''.join(persian_numbers), ''.join(english_numbers))
    return s.translate(table)

class FetchPricesAPIView(APIView):
    def get(self, request):
        url = config('url')
        response = requests.get(url)
        data = response.json()
        now = datetime.utcnow()

        for item in data:
            name = item.get('name', '').strip()
            price_str = item.get('price', '').replace(',', '')
            price_str = persian_to_english_numbers(price_str)
            
            try:
                price = float(price_str)
            except ValueError:
                continue

            CurrencyHistory.objects(name=name).update_one(
                set__price=price,
                set__last_updated=now,
                upsert=True
            )
            
            CurrencyHistory(
                name=name,
                price=price,
                timestamp=now
            ).save()

        return Response({"status": "updated", "data": data})

class PriceHistoryAPIView(APIView):
    def get(self, request, currency_name):
        start = request.GET.get("start")
        end = request.GET.get("end")
        
        try:
            start_date = datetime.fromisoformat(start) 
            end_date = datetime.fromisoformat(end)
        except:
            return Response({"error": "Invalid date format"}, status=400)

        history = CurrencyHistory.objects(
            name=currency_name,
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).order_by('timestamp')

        result = [
            {
                "price": float(entry.price),
                "timestamp": entry.timestamp.isoformat()
            }
            for entry in history
        ]

        return Response({
            "currency": currency_name,
            "history": result
        })
