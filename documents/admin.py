from django.contrib import admin
from .models import Tag, Document, Question
from django.urls import path
from django.shortcuts import render
from .llm_service import generate_answer
from .search import find_relevant_documents

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_content_summary', 'created_at')
    
    list_filter = ('created_at', 'tags')
    
    search_fields = ('title', 'content')
    
    @admin.display(description='خلاصه متن')
    def get_content_summary(self, obj):
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('semantic-search/', self.admin_site.admin_view(self.semantic_search_view), name='document-semantic-search'),
        ]
        return custom_urls + urls

    def semantic_search_view(self, request):
        query = request.GET.get('q', '')
        results = []
        generated_answer = ""
        
        if query:
            results = find_relevant_documents(query)
            
            if results:
                generated_answer = generate_answer(query, results)
                Question.objects.create(question=query, answer=generated_answer)
            else:
                generated_answer = "سند مرتبطی برای پاسخ به این پرسش یافت نشد."
            
        context = dict(
            self.admin_site.each_context(request),
            query=query,
            results=results,
            generated_answer=generated_answer,
            title="جستجوی هوشمند در اسناد"
        )
        return render(request, 'admin/documents/semantic_search.html', context)

admin.site.register(Tag)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('get_question_summary', 'has_answer')
    search_fields = ('question', 'answer')
    
    @admin.display(description='خلاصه پرسش')
    def get_question_summary(self, obj):
        if len(obj.question) > 50:
            return f"{obj.question[:50]}..."
        return obj.question

    @admin.display(description='پاسخ داده شده؟', boolean=True)
    def has_answer(self, obj):
        return bool(obj.answer)