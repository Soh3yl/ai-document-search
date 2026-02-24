from django.core.management.base import BaseCommand
from documents.models import Document, Question, Tag

class Command(BaseCommand):
    help = 'ایجاد داده‌های نمونه (۳ سند و ۲ پرسش) برای ارزیابی سیستم'

    def handle(self, *args, **kwargs):
        if Document.objects.exists() or Question.objects.exists():
            self.stdout.write(self.style.WARNING('داده‌های نمونه از قبل در دیتابیس وجود دارند.'))
            return

        self.stdout.write(self.style.SUCCESS('در حال ایجاد داده‌های نمونه...'))

        tag_django, _ = Tag.objects.get_or_create(name='جنگو')
        tag_python, _ = Tag.objects.get_or_create(name='پایتون')
        tag_ui, _ = Tag.objects.get_or_create(name='رابط کاربری')
        tag_docker, _ = Tag.objects.get_or_create(name='داکر')

        doc1 = Document.objects.create(
            title='معرفی یک فریم‌ورک محبوب',
            content='این ابزار قدرتمند به برنامه‌نویسان کمک می‌کند تا سایت‌های پویا و امن بسازند. معماری آن بر پایه MVT است و سرعت توسعه بک‌اند را به شدت بالا می‌برد.'
        )
        doc1.tags.add(tag_django, tag_python)

        doc2 = Document.objects.create(
            title='اصول طراحی پلتفرم‌های آموزشی',
            content='برای داشتن یک تجربه کاربری خوب در سایت‌های دانشگاهی، باید رنگ‌بندی، چیدمان فرم‌ها و مسیرهای کاربری به درستی پیاده‌سازی شوند.'
        )
        doc2.tags.add(tag_ui)

        doc3 = Document.objects.create(
            title='محیط‌های ایزوله در برنامه‌نویسی',
            content='این تکنولوژی جذاب به شما اجازه می‌دهد تا برنامه‌ها و وابستگی‌های سیستم خود را بسته‌بندی کنید و آن‌ها را روی هر سروری به راحتی اجرا کنید.'
        )
        doc3.tags.add(tag_docker)

        Question.objects.create(question='جنگو چیست و چه معماری دارد؟')
        Question.objects.create(question='چگونه تجربه کاربری (UI) سایت را بهتر کنیم؟')

        self.stdout.write(self.style.SUCCESS('۳ سند و ۲ پرسش نمونه با موفقیت به دیتابیس اضافه شد!'))