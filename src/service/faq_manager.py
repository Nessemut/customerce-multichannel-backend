from src.model.faq import Faq
from ..model.shop import Shop


def serialize(faq):
    return {
        'id': faq.id,
        'question': faq.question,
        'answer': faq.answer
    }


def get_all(shop_id):
    faq_list = Faq.objects.filter(shop_id=shop_id)
    faq_array = []
    for faq in faq_list:
        faq_array.append(serialize(faq))
    res = {"faq": faq_array}

    return res


def get_faq(faq_id):
    faq = Faq.objects.get(pk=faq_id)
    res = {'faq': serialize(faq)}
    return res


def update(form, faq_id):
    faq = Faq.objects.get(pk=faq_id)
    faq.question = form['question']
    faq.answer = form['answer']
    faq.save()


def create(form, shop_id):
    faq = Faq()
    faq.shop = Shop.objects.get(pk=shop_id)
    faq.question = form['question']
    faq.answer = form['answer']
    faq.save()


def delete(faq_id):
    Faq.objects.get(pk=faq_id).delete()
