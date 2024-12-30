from app.models import Price


async def get_price_by_id_and_currency(price_id, currency: str) -> float:
    obj = await Price.objects.aget(id=price_id)
    return getattr(obj, currency)


async def get_price_by_id(id: int) -> None | Price:
    obj = await Price.objects.filter(id=id).afirst()
    return obj
