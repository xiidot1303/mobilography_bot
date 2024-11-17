from app.models import Price


async def get_price_by_currency(currency: str) -> float:
    obj = await Price.objects.aget()
    return getattr(obj, currency)
