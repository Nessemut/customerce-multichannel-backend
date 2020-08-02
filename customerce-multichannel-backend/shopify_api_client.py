import datetime
from json import dumps, loads

import requests

from . import settings
from .service.shop_manager import save_shop

REDIRECT_URL = "http://{}.myshopify.com/admin/oauth/authorize?client_id={}&redirect_uri={}&scope={}"
SHOP_ADMIN_URL = "https://{}.myshopify.com/admin/{}"
ACCESS_TOKEN_URL = "https://{}.myshopify.com/admin/oauth/access_token"


class ShopifyApiClient:

    def __init__(self, shop):
        self.shop = shop

    def build_header(self):
        header = {
            'X-Shopify-Access-Token': self.shop.token,
            'Content-Type': 'application/json'
        }
        return header

    def get_url(self, context):
        return SHOP_ADMIN_URL.format(self.shop.name, context)

    def token_valid(self):
        url = self.get_url('shop.json')
        r = requests.get(url, headers=self.build_header())
        return not r.status_code == 401

    def confirm_installation(self, auth):
        r = requests.post(
            ACCESS_TOKEN_URL.format(self.shop.name),
            data={
                'client_id': settings.SHOPIFY_API_KEY,
                'client_secret': settings.SHOPIFY_API_SECRET,
                'code': auth
            }
        )

        self.shop.token = (r.json()["access_token"])
        save_shop(self.shop)

    def redirect_to_install_confirmation(self):
        url = REDIRECT_URL.format(
            self.shop.name,
            settings.SHOPIFY_API_KEY,
            "{}/install/confirm".format(settings.APP_URL),
            settings.APP_SCOPES)
        return url

    def add_script_tag(self):
        url = self.get_url('script_tags.json')

        if self.shop.script_tag_id is None:
            r = requests.post(
                url,
                data=dumps({
                    "script_tag": {
                        "event": "onload",
                        "src": settings.APP_URL + '/scriptag'
                    }
                }),
                headers=self.build_header()
            )

            if r.status_code == 201:
                self.shop.script_tag_id = loads(r.content)['script_tag']['id']
                save_shop(self.shop)

    def remove_script_tag(self):
        url = self.get_url('script_tags/{}.json'.format(self.shop.script_tag_id))
        r = requests.delete(url, headers=self.build_header())

        if r.status_code == 200:
            self.shop.script_tag_id = None
            save_shop(self.shop)

    def add_billing(self):
        url = self.get_url('recurring_application_charges.json')
        trial_days = self.get_trial_period()
        test = settings.DEBUG or self.shop.name in settings.PAYMENT_FREE_SHOPS
        if self.shop.name in settings.OLD_PRICE_SHOPS:
            price = settings.OLD_APP_PRICE
        else:
            price = settings.APP_PRICE

        r = requests.post(
            url,
            data=dumps({
                "recurring_application_charge": {
                    "name": "Recurring charge",
                    "price": price,
                    "test": test,
                    "trial_days": trial_days,
                    "return_url": '{}/redirect?shop={}'.format(settings.APP_URL, self.shop.name)
                }
            }),
            headers=self.build_header()
        )

        if r.status_code == 201:
            rdict = loads(r.content)['recurring_application_charge']
            self.shop.billing_id = rdict['id']
            save_shop(self.shop)
            return rdict['confirmation_url']

        return None

    def activate_billing(self):
        url = self.get_url('recurring_application_charges/{}/activate.json'.format(self.shop.billing_id))
        r = requests.post(url, headers=self.build_header())
        return r.status_code

    def get_trial_period(self):
        installed = datetime.datetime.strptime(str(self.shop.install_date)[:19], '%Y-%m-%d %H:%M:%S')
        today = datetime.datetime.today()
        period = settings.APP_TRIAL_PERIOD - (today - installed).days

        if period < 0:
            return 0
        if period > settings.APP_TRIAL_PERIOD:
            return settings.APP_TRIAL_PERIOD
        return period
