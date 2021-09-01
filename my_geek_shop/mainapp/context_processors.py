from basketapp.models import Basket


def get_basket(request):
    return {'basket': list(Basket.objects.filter(user=request.user))} if request.user.is_authenticated else []
