from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="نام برچسب"
    )

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    def __str__(self):
        return self.name


class Document(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )
    content = models.TextField(
        blank=False,
        verbose_name="متن"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='documents',
        verbose_name="برچسب‌ها"
    )

    class Meta:
        verbose_name = "سند"
        verbose_name_plural = "اسناد"

    def __str__(self):
        return self.title


class Question(models.Model):
    question = models.TextField(
        verbose_name="پرسش"
    )
    answer = models.TextField(
        blank=True,
        null=True,
        verbose_name='پاسخ'
    )

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات"

    def __str__(self):
        return self.question[:50]
