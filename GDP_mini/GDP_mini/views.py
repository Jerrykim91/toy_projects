# # 1. 클래스형 제네릭뷰
from django.views.generic import TemplateView
# 테이블 레코드 
# from django.views.generic import CreateView
# 유저 모델의 객체를 생성
# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
# 뷰처리 진입 단계에서 적절한 권한 을 갖추었는지 판별 
# from django.contrib.auth.mixins import AccessMixin


# Create your views here.

# TemplateView
class HomeView(TemplateView):
    """
    메인 화면  
    """
    # template_name = 'main/main.html'
    template_name = 'test/index.html'
    # template_name = 'btsp/index.html'