import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  # اضافه شدن سیستم کش جنگو
from .search import find_relevant_documents
from .llm_service import generate_answer
from .models import Question

@csrf_exempt 
def search_documents_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get('question', '')

            if not user_question:
                return JsonResponse({'error': 'لطفاً پرسش خود را در قالب {"question": "..."} ارسال کنید.'}, status=400)

            cache_key = f"search_cache_{user_question}"
            cached_data = cache.get(cache_key)
            
            if cached_data:
                return JsonResponse(cached_data, status=200, json_dumps_params={'ensure_ascii': False})

            results = find_relevant_documents(user_question)

            if results:
                generated_answer = generate_answer(user_question, results)
                Question.objects.create(question=user_question, answer=generated_answer)
            else:
                generated_answer = "سند مرتبطی برای پاسخ به این پرسش یافت نشد."

            response_data = []
            for item in results:
                doc = item['document']
                response_data.append({
                    'id': doc.id,
                    'title': doc.title,
                    'score': item['score'],
                    'content_snippet': doc.content[:100] + '...' 
                })

            final_response = {
                'generated_answer': generated_answer,
                'results': response_data,
                'cached': False 
            }

            cached_response_to_save = final_response.copy()
            cached_response_to_save['cached'] = True 
            
            cache.set(cache_key, cached_response_to_save, timeout=900)

            return JsonResponse(final_response, status=200, json_dumps_params={'ensure_ascii': False})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'فقط درخواست‌های POST مجاز هستند.'}, status=405)