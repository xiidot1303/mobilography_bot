from app.views import *
from config import WEBSITE_URL
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from bot.services import *
from bot.services.newsletter_service import *
from bot.control.updater import application


async def view_video(request: HttpRequest):
    return redirect(WEBSITE_URL)


@method_decorator(csrf_exempt, name='dispatch')
class PersonalInfoForm(View):
    async def post(self, request: HttpRequest, *agrs, **kwargs):
        name, phone, user_id, price_id = (
            request.POST["name"], request.POST["phone"], 
            request.POST["user_id"], request.POST["price_id"]
            )
        bot_user: Bot_user = await get_object_by_user_id(user_id)
        # update bot user details
        bot_user.name, bot_user.phone, bot_user.price_id = name, phone, price_id
        await bot_user.asave()
        # send payment invoice
        await send_payment_providers(application, user_id)
        return HttpResponse()

    async def get(self, request: HttpRequest, *agrs, **kwargs):
        price_id = request.GET.get('tgWebAppStartParam', None)
        context = {
            'price_id': price_id
        }
        return render(request, "personal_info_form.html", context=context)