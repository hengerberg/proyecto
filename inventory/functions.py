from django.db import transaction

from .models import Inventory, InventoryCurrent


def update_inventory(chips_venta, chips_porta, usuario, tipo):
    """
    funcion que permite a los usuarios actualizar su inventario
    """
    with transaction.atomic():
        add_inventory = Inventory(
            chips_sale=chips_venta, chips_portability=chips_porta, user_id=usuario, type=tipo)
        add_inventory.save()

        current_inventory = InventoryCurrent.objects.get(user_id=usuario)
        current_inventory.chips_sale += chips_venta
        current_inventory.chips_portability += chips_porta

    current_inventory.save()


def ordenes(request, usuario):
    """
    funcion que retorna el historico del inventario de un usuario en especifico
    """
    data = {}
    try:
        #action = request.POST['action']
        #if action == 'searchdata':
        data = []
        for i in Inventory.objects.filter(user_id=usuario)[:60]:
            # data.append(i.toJSON())
            data.insert(0, i.toJSON())
        #else:
        #    data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    
    return data
