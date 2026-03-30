from django.db import models


class TelegramUser(models.Model):
    LANG_CHOICES = [
        ('uz', "O'zbek"),
        ('ru', 'Русский'),
    ]

    user_id = models.BigIntegerField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    lang = models.CharField(max_length=5, choices=LANG_CHOICES, null=True, blank=True)
    message_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} ({self.user_id})"


class ButtonClick(models.Model):
    button_key = models.CharField(max_length=50)   # masalan: "menu_jarima"
    button_name = models.CharField(max_length=100) # masalan: "Jarima va E jarima Ball"
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tugma bosish"
        verbose_name_plural = "Tugma bosishlar"
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.button_name} — {self.clicked_at}"


# ================= MENU BO'LIMLARI =================
class BaseClick(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.SET_NULL, null=True, blank=True)
    button_key = models.CharField(max_length=50)
    button_name = models.CharField(max_length=100)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-clicked_at']

    def __str__(self):
        return f"{self.button_name} — {self.clicked_at}"


class JarimaClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Jarima"
        verbose_name_plural = "🚔 Jarima bosishlar"


class SugurtaClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Sug'urta"
        verbose_name_plural = "🛡 Sug'urta bosishlar"


class MashinaClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Mashina"
        verbose_name_plural = "🚗 Mashina bosishlar"


class SmsClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "SMS"
        verbose_name_plural = "📨 SMS bosishlar"


class TonirovkaClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Tonirovka"
        verbose_name_plural = "🕶 Tonirovka bosishlar"


class TexClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Texnik ko'rik"
        verbose_name_plural = "🚧 Texnik ko'rik bosishlar"


class MikroClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Mikroqarz"
        verbose_name_plural = "💰 Mikroqarz bosishlar"


class SignalClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "AutoSignal"
        verbose_name_plural = "🚨 AutoSignal bosishlar"


class OneIdClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "ONE ID"
        verbose_name_plural = "♻️ ONE ID bosishlar"


class SlowClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Ilova ishlashi"
        verbose_name_plural = "📲 Ilova ishlashi bosishlar"


class OperatorClick(BaseClick):
    class Meta(BaseClick.Meta):
        verbose_name = "Operator"
        verbose_name_plural = "👨‍💼 Operator bosishlar"
