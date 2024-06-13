from django import template

register = template.Library()

@register.filter
def duration_to_hours_minutes(value):
    if value is None:
        return "0時間0分"
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}時間{minutes}分"