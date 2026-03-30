from datetime import timedelta

from bot.models import ButtonClick


def button_stats_view(request):
    now = timezone.now()
    today = now.date()
    period = request.GET.get('period', 'day')

    if period == 'day':
        start = now - timedelta(days=1)
        label = "Bugun"
    elif period == 'month':
        start = now - timedelta(days=30)
        label = "So'nggi 30 kun"
    elif period == 'year':
        start = now - timedelta(days=365)
        label = "So'nggi 1 yil"
    else:
        start = now - timedelta(days=1)
        label = "Bugun"

    all_buttons = ButtonClick.objects.values('button_key', 'button_name').distinct()
    buttons_data = []
    for btn in all_buttons:
        key = btn['button_key']
        name = btn['button_name']

        # Kunlik bosilishlar (so‘nggi 7 kun)
        daily_counts = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            count = ButtonClick.objects.filter(button_key=key, clicked_at__date=day).count()
            daily_counts.append({'date': day.strftime("%d.%m"), 'count': count})

        # Oylik bosilishlar (so‘nggi 12 oy)
        monthly_counts = []
        for i in range(11, -1, -1):
            month_start = (now - timedelta(days=30 * i)).replace(day=1).date()
            month_end = (month_start + timedelta(days=32)).replace(day=1)
            count = ButtonClick.objects.filter(
                button_key=key,
                clicked_at__date__gte=month_start,
                clicked_at__date__lt=month_end
            ).count()
            monthly_counts.append({'date': month_start.strftime("%m.%Y"), 'count': count})

        total_day = ButtonClick.objects.filter(button_key=key, clicked_at__date=today).count()
        total_month = ButtonClick.objects.filter(button_key=key, clicked_at__date__gte=today.replace(day=1)).count()
        total_year = ButtonClick.objects.filter(button_key=key, clicked_at__date__gte=today.replace(month=1, day=1)).count()
        total_all = ButtonClick.objects.filter(button_key=key).count()

        buttons_data.append({
            'key': key,
            'name': name,
            'daily_counts': daily_counts,
            'monthly_counts': monthly_counts,
            'total_day': total_day,
            'total_month': total_month,
            'total_year': total_year,
            'total_all': total_all,
        })

    context = {
        'title': 'Tugma Statistikasi',
        'period': period,
        'label': label,
        'buttons_data': buttons_data,  # <-- shu nom template bilan mos bo‘lishi kerak
    }

    return render(request, 'admin/button_stats.html', context)


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def bot_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # bot update queue ga qo‘yish
        # bot_app.update_queue.put(data)
    return HttpResponse("Bot ishlayapti!")