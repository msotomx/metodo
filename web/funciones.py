from django import template
register = template.Library()

@register.simple_tag
def saludo():
    return "Hola desde saludo"
