from django import template

register = template.Library()

@register.filter
def filter_online(services):
    return [s for s in services if s.reservation_type == 'Online']

@register.filter
def filter_presencial(services):
    return [s for s in services if s.reservation_type == 'Presencial'] 