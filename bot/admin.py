from django.contrib import admin
from django.utils import timezone
from datetime import timedelta, datetime
import pytz
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    TelegramUser, ButtonClick,
    JarimaClick, SugurtaClick, MashinaClick, SmsClick,
    TonirovkaClick, TexClick, MikroClick, SignalClick,
    OneIdClick, SlowClick, OperatorClick
)

TASHKENT_TZ = pytz.timezone("Asia/Tashkent")

def to_utc(dt_local):
    return dt_local.astimezone(pytz.utc)

def tashkent_dt(year, month, day, hour=0, minute=0):
    return TASHKENT_TZ.localize(datetime(year, month, day, hour, minute, 0))

def fmt_tashkent(dt):
    if dt is None:
        return "—"
    return dt.astimezone(TASHKENT_TZ).strftime("%d.%m.%Y %H:%M")

# ================= STATISTIKA MIXIN =================
class StatsMixin:
    stats_field = 'clicked_at'
    change_list_template = "admin/bot/change_list.html"

    def changelist_view(self, request, extra_context=None):
        now_tashkent = datetime.now(TASHKENT_TZ)
        today = now_tashkent.date()
        now_hour = now_tashkent.hour

        model = self.model
        field = self.stats_field

        is_den = 8 <= now_hour < 20

        if is_den:
            start_dt = TASHKENT_TZ.localize(datetime(today.year, today.month, today.day, 8, 0, 0))
            den_count = model.objects.filter(**{f'{field}__gte': start_dt}).count()
            noch_count = 0
        else:
            if now_hour >= 20:
                start_dt = TASHKENT_TZ.localize(datetime(today.year, today.month, today.day, 20, 0, 0))
            else:
                yesterday = today - timedelta(days=1)
                start_dt = TASHKENT_TZ.localize(datetime(yesterday.year, yesterday.month, yesterday.day, 20, 0, 0))
            noch_count = model.objects.filter(**{f'{field}__gte': start_dt}).count()
            den_count = 0

        week_start = today - timedelta(days=today.weekday())
        week_start_dt = TASHKENT_TZ.localize(datetime(week_start.year, week_start.month, week_start.day, 0, 0, 0))
        week_count = model.objects.filter(**{f'{field}__gte': week_start_dt}).count()

        month_start_dt = TASHKENT_TZ.localize(datetime(today.year, today.month, 1, 0, 0, 0))
        month_count = model.objects.filter(**{f'{field}__gte': month_start_dt}).count()

        year_start_dt = TASHKENT_TZ.localize(datetime(today.year, 1, 1, 0, 0, 0))
        year_count = model.objects.filter(**{f'{field}__gte': year_start_dt}).count()

        total = model.objects.count()

        den_style = "border:2px solid #1d9e75;" if is_den else "border:0.5px solid rgba(0,0,0,0.08); opacity:0.45;"
        noch_style = "border:2px solid #5b6abf;" if not is_den else "border:0.5px solid rgba(0,0,0,0.08); opacity:0.45;"
        shift_text = "☀️ Kun smena · active (08:00 – 20:00)" if is_den else "🌙 Tun smena · active (20:00 – 08:00)"
        shift_color = "#1d9e75" if is_den else "#5b6abf"

        cards_html = mark_safe(f"""
        <div>
          <div style="display:flex; align-items:center; gap:16px; margin:16px 0 12px; flex-wrap:wrap;">
            <span style="font-size:13px; font-weight:600; color:{shift_color};">{shift_text}</span>
            <span style="font-size:12px; color:#bbb;">·</span>
            <span style="font-size:12px; color:#aaa;">Yangilanishiga: <strong id="stats-countdown" style="color:#888;">60s</strong></span>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:12px; margin:0 0 24px;">
            <div style="flex:1; min-width:120px; background:#fff; border-radius:12px; padding:20px 24px; {den_style}">
              <div style="font-size:11px; color:#888; text-transform:uppercase;">☀️ Kun (Den)</div>
              <div style="font-size:34px; font-weight:500; color:#1d9e75;">{den_count}</div>
            </div>
            <div style="flex:1; min-width:120px; background:#fff; border-radius:12px; padding:20px 24px; {noch_style}">
              <div style="font-size:11px; color:#888; text-transform:uppercase;">🌙 Tun (Noch)</div>
              <div style="font-size:34px; font-weight:500; color:#5b6abf;">{noch_count}</div>
            </div>
            <div style="flex:1; min-width:120px; background:#fff; border:0.5px solid rgba(0,0,0,0.1); border-radius:12px; padding:20px 24px;">
              <div style="font-size:11px; color:#888; text-transform:uppercase;">Haftalik</div>
              <div style="font-size:34px; font-weight:500; color:#378add;">{week_count}</div>
            </div>
            <div style="flex:1; min-width:120px; background:#fff; border:0.5px solid rgba(0,0,0,0.1); border-radius:12px; padding:20px 24px;">
              <div style="font-size:11px; color:#888; text-transform:uppercase;">Oylik</div>
              <div style="font-size:34px; font-weight:500; color:#ba7517;">{month_count}</div>
            </div>
            <div style="flex:1; min-width:120px; background:#fff; border:0.5px solid rgba(0,0,0,0.1); border-radius:12px; padding:20px 24px;">
              <div style="font-size:11px; color:#888; text-transform:uppercase;">Jami</div>
              <div style="font-size:34px; font-weight:500; color:#7f77dd;">{total}</div>
            </div>
          </div>
        </div>
        <script>(function(){{var s=60,e=document.getElementById('stats-countdown');setInterval(function(){{s--;if(e)e.textContent=s+'s';if(s<=0)location.reload();}},1000);}})();</script>
        """)
        extra_context = extra_context or {}
        extra_context['stats_cards'] = cards_html
        return super().changelist_view(request, extra_context=extra_context)

# ================= FOYDALANUVCHILAR ADMIN =================
@admin.register(TelegramUser)
class TelegramUserAdmin(StatsMixin, admin.ModelAdmin):
    stats_field = 'created_at'
    list_display = ('avatar_name', 'username_link', 'user_id', 'message_badge', 'lang_badge', 'created_tashkent')
    list_filter = ('lang', 'created_at')
    search_fields = ('first_name', 'last_name', 'username', 'user_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'last_seen', 'user_id')

    def created_tashkent(self, obj): return fmt_tashkent(obj.created_at)
    created_tashkent.short_description = "Vaqt"

    def avatar_name(self, obj):
        initial = (obj.first_name or '?')[0].upper()
        return format_html('<div style="display:flex;align-items:center;gap:10px"><div style="width:30px;height:30px;border-radius:50%;background:#3b82f6;color:white;display:flex;align-items:center;justify-content:center;font-weight:700">{}</div>{}</div>', initial, f"{obj.first_name} {obj.last_name or ''}")

    def username_link(self, obj):
        if obj.username: return format_html('<a href="https://t.me/{}">@{}</a>', obj.username, obj.username)
        return "—"

    def message_badge(self, obj): return format_html('<span style="background:#10b98122;color:#10b981;padding:3px 8px;border-radius:10px">💬 {}</span>', obj.message_count)

    def lang_badge(self, obj):
        flag = "🇺🇿 UZ" if obj.lang == 'uz' else "🇷🇺 RU" if obj.lang == 'ru' else "❓"
        return format_html('<span style="font-weight:700">{}</span>', flag)

# ================= CLICK ADMIN BAZASI =================
MENU_COLORS = {
    'menu_jarima': ('#ef4444', '🚔'), 'menu_sugurta': ('#3b82f6', '🛡'),
    'menu_mashina': ('#10b981', '🚗'), 'menu_sms': ('#f59e0b', '📨'),
    'menu_tonirovka': ('#8b5cf6', '🕶'), 'menu_tex': ('#06b6d4', '🚧'),
    'menu_mikro': ('#ec4899', '💰'), 'menu_signal': ('#6366f1', '🚨'),
    'menu_oneid': ('#14b8a6', '♻️'), 'menu_slow': ('#64748b', '📲'),
    'operator': ('#f97316', '👨‍💼'),
}

class BaseClickAdmin(StatsMixin, admin.ModelAdmin):
    list_display = ('button_badge', 'user_link', 'clicked_tashkent')
    list_filter = ('button_key', 'clicked_at')
    ordering = ('-clicked_at',)

    def clicked_tashkent(self, obj): return fmt_tashkent(obj.clicked_at)
    clicked_tashkent.short_description = "Vaqt"

    def button_badge(self, obj):
        color, icon = MENU_COLORS.get(obj.button_key, ('#64748b', '•'))
        return format_html('<span style="background:{}22;color:{};padding:4px 12px;border-radius:20px;font-weight:700">{} {}</span>', color, color, icon, obj.button_name)

    def user_link(self, obj):
        if obj.user: return f"{obj.user.first_name} ({obj.user.user_id})"
        return "—"

# ================= HAR BIR MENU ADMINI =================
@admin.register(JarimaClick)
class JarimaAdmin(BaseClickAdmin): pass

@admin.register(SugurtaClick)
class SugurtaAdmin(BaseClickAdmin): pass

@admin.register(MashinaClick)
class MashinaAdmin(BaseClickAdmin): pass

@admin.register(SmsClick)
class SmsAdmin(BaseClickAdmin): pass

@admin.register(TonirovkaClick)
class TonirovkaAdmin(BaseClickAdmin): pass

@admin.register(TexClick)
class TexAdmin(BaseClickAdmin): pass

@admin.register(MikroClick)
class MikroAdmin(BaseClickAdmin): pass

@admin.register(SignalClick)
class SignalAdmin(BaseClickAdmin): pass

@admin.register(OneIdClick)
class OneIdAdmin(BaseClickAdmin): pass

@admin.register(SlowClick)
class SlowAdmin(BaseClickAdmin): pass

@admin.register(OperatorClick)
class OperatorAdmin(BaseClickAdmin):
    list_display = ('operator_badge', 'user_link', 'lang_badge', 'clicked_tashkent')

    def operator_badge(self, obj):
        return format_html('<span style="background:#f9731622;color:#f97316;padding:4px 12px;border-radius:20px;font-weight:700">👨‍💼 Operator</span>')
    operator_badge.short_description = 'Tugma'

    def lang_badge(self, obj):
        if obj.user and obj.user.lang:
            return "🇺🇿 UZ" if obj.user.lang == 'uz' else "🇷🇺 RU"
        return "—"
    lang_badge.short_description = 'Til'

@admin.register(ButtonClick)
class ButtonClickAdmin(BaseClickAdmin): pass