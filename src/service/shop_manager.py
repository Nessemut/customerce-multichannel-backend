import os

from django.conf import settings
from django.core.files.storage import default_storage

from src.model.shop import Shop
from .. import settings


def get_id(name):
    return Shop.objects.get(name=name).id


def get_chat_info(name):
    shop = Shop.objects.get(name=name)
    res = {
        'id': shop.id,
        'name': shop.name,
        'facebook_active': shop.facebook_active,
        'whatsapp_active': shop.whatsapp_active,
        'email_active': shop.email_active,
        'panel_color': shop.panel_color,
        'panel_title': shop.panel_title
    }

    if shop.facebook_active:
        res['facebook_page'] = shop.facebook_page
    if shop.email_active:
        res['email'] = shop.email
    if shop.whatsapp_active:
        res['whatsapp_number'] = shop.whatsapp_number
        res['whatsapp_text'] = shop.whatsapp_text

    return res


def get_merchant_info(shop_id):
    shop = Shop.objects.get(pk=shop_id)
    res = {
        'id': shop.id,
        'name': shop.name,
        'app_enabled': shop.app_enabled,
        'facebook_active': shop.facebook_active,
        'whatsapp_active': shop.whatsapp_active,
        'email_active': shop.email_active,
        'panel_color': shop.panel_color,
        'panel_title': shop.panel_title,
        'facebook_page': shop.facebook_page,
        'email': shop.email,
        'whatsapp_number': shop.whatsapp_number,
        'whatsapp_text': shop.whatsapp_text
    }
    return res


def update(form, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    shop.facebook_active = form['facebook_active'] == 'true'
    shop.whatsapp_active = form['whatsapp_active'] == 'true'
    shop.email_active = form['email_active'] == 'true'
    shop.panel_color = form['panel_color']
    shop.panel_title = form['panel_title']
    shop.facebook_page = form['facebook_page']
    shop.email = form['email']
    shop.whatsapp_number = form['whatsapp_number']
    shop.whatsapp_text = form['whatsapp_text']
    save_shop(shop)


def toggle_app_enabled(shop_id, enabled):
    shop = Shop.objects.get(pk=shop_id)
    shop.app_enabled = enabled
    save_shop(shop)


def get(shop_id):
    shop = Shop.objects.get(pk=shop_id)
    return shop


def get_shop(name):
    shop = Shop.objects.get(name=name)
    return shop


def create_shop(name):
    shop = Shop.create(name)
    return shop


def save_shop(shop):
    shop.save()


def authentication_correct(shopname, token):
    try:
        shop = Shop.objects.get(name=shopname)
    except Shop.DoesNotExist:
        return False
    return shop.token == token


def get_image(shopname):
    try:
        with open('{}/{}.png'.format(settings.AVATAR_PATH, shopname), "rb") as f:
            return f.read()
    except FileNotFoundError:
        with open('{}/default.png'.format(settings.AVATAR_PATH), "rb") as f:
            return f.read()


def save_image(file, shop_id):
    shopname = get(shop_id).name
    dest = '{}/{}.png'.format(settings.AVATAR_PATH, shopname)
    try:
        with default_storage.open(dest, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    except AttributeError:
        os.remove(dest)
