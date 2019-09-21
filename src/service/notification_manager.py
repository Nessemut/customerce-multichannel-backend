from src.model.notification import Notification
from ..model.shop import Shop


def serialize(notification):
    return {
        'id': notification.id,
        'background_color': notification.background_color,
        'font_color': notification.font_color,
        'text': notification.text,
        'time': notification.time,
        'url': notification.url
    }


def get_all(shop_id):
    notif_list = Notification.objects.filter(shop_id=shop_id)
    notif_array = []
    for notification in notif_list:
        notif_array.append(serialize(notification)
        )
    res = {"notifications": notif_array}

    return res


def get_notification(notification_id):
    notification = Notification.objects.get(pk=notification_id)
    res = {'notification': serialize(notification)}
    return res


def update(form, notification_id):
    notification = Notification.objects.get(pk=notification_id)
    notification.background_color = form['background_color']
    notification.font_color = form['font_color']
    notification.text = form['text']
    notification.time = form['time']
    notification.url = form['url']
    notification.save()


def create(form, shop_id):
    notification = Notification()
    notification.shop = Shop.objects.get(pk=shop_id)
    notification.background_color = form['background_color']
    notification.font_color = form['font_color']
    notification.text = form['text']
    notification.time = form['time']
    notification.url = form['url']
    notification.save()


def delete(notification_id):
    Notification.objects.get(pk=notification_id).delete()
