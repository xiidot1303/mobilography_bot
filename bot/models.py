from django.db import models
from django.core.validators import FileExtensionValidator
from asgiref.sync import sync_to_async
from datetime import timedelta, datetime

class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='', verbose_name='Имя')
    username = models.CharField(null=True, blank=True, max_length=256, verbose_name='username')
    firstname = models.CharField(null=True, blank=True, max_length=256, verbose_name='Никнейм')
    phone = models.CharField(null=True, blank=True, max_length=16, default='', verbose_name='Телефон')
    LANG_CHOICES = [
        (0, 'uz'),
        (1, 'ru'),
    ]
    lang = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES, default=1, verbose_name='Язык')
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата регистрации')
    has_access_to_channel = models.BooleanField(default=False)

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"
    
class Message(models.Model):
    bot_users = models.ManyToManyField('bot.Bot_user', blank=True, related_name='bot_users_list', verbose_name='Пользователи бота')
    text = models.TextField(null=True, blank=False, max_length=1024, verbose_name='Текст')
    photo = models.FileField(null=True, blank=True, upload_to="message/photo/", verbose_name='Фото',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','bmp','gif'])]
    )
    video = models.FileField(
        null=True, blank=True, upload_to="message/video/", verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
        )
    file = models.FileField(null=True, blank=True, upload_to="message/file/", verbose_name='Файл')
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

class Alert(models.Model):
    bot_user = models.ForeignKey(Bot_user, blank=False, on_delete=models.CASCADE)
    text = models.TextField(blank=False, max_length=2048)
    button_text = models.CharField(max_length=64)
    url = models.CharField(max_length=255)
    when = models.BigIntegerField(null=True)
    datetime = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        now = datetime.now()
        self.datetime = now + timedelta(seconds=self.when)
        return super().save(*args, **kwargs)

    @property
    @sync_to_async
    def is_active(self):
        return not self.bot_user.has_access_to_channel