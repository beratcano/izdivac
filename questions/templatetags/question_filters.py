from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_question_field(form, q_id):
    return form[f'question_{q_id}']