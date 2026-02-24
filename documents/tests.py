import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Document, Tag, Question
from .search import find_relevant_documents

class DocumentSearchTests(TestCase):
    def setUp(self):
        """
        این تابع قبل از هر تست اجرا می‌شود تا یک دیتابیس تستی (مجازی) بسازد.
        """
        self.client = Client()
        
        self.tag_python = Tag.objects.create(name="پایتون")
        self.tag_ui = Tag.objects.create(name="رابط کاربری")
        
        self.doc1 = Document.objects.create(
            title="آموزش برنامه‌نویسی بک‌اند",
            content="برای توسعه سمت سرور، زبان‌های مختلفی وجود دارند که کدهای امنی تولید می‌کنند."
        )
        self.doc1.tags.add(self.tag_python)
        
        self.doc2 = Document.objects.create(
            title="اصول طراحی سایت",
            content="برای داشتن یک سایت زیبا، باید به چیدمان و رنگ‌بندی دقت کرد."
        )
        self.doc2.tags.add(self.tag_ui)

    def test_database_creation(self):
        """تستِ صحت ذخیره‌سازی در دیتابیس"""
        self.assertEqual(Document.objects.count(), 2)
        self.assertEqual(Tag.objects.count(), 2)
        self.assertEqual(self.doc1.tags.first().name, "پایتون")

    def test_tfidf_search_logic(self):
        """تستِ عملکرد موتور جست‌وجوی TF-IDF و تاثیر برچسب‌ها"""
        results = find_relevant_documents("پایتون چیست؟", top_n=1)
        
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]['document'], self.doc1)
        self.assertTrue(results[0]['score'] > 0)

    def test_api_search_endpoint(self):
        """تستِ صحت عملکرد API و دریافت خروجی JSON"""
        response = self.client.post(
            '/api/search/',
            data=json.dumps({"question": "چگونه سایت زیبا بسازیم؟"}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        response_data = response.json()
        self.assertIn('results', response_data)
        self.assertIn('generated_answer', response_data)
        
        self.assertEqual(response_data['results'][0]['title'], "اصول طراحی سایت")
        
        self.assertEqual(Question.objects.count(), 1)