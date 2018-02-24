import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from .models import Profile
from .forms import ProfileModelForm
# Create your views here.

'''
login

설명:

소셜 로그인 기능

'''


def login(request):
    providers = []
    for provider in get_providers():
            try:
                provider.social_app = SocialApp.objects.get(provider=provider.id,
                                                            sites=settings.SITE_ID)
            except SocialApp.DoesNotExist:
                provider.social_app = None
            providers.append(provider)
    return render(request, 'accounts/login_form.html', {
        'providers': providers
    })


'''
profile

설명:

유저 프로필 생성 및 조회 응답.

'''


@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile is None:
        if request.method == 'POST':
            form = ProfileModelForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.info(request, '회원가입이 완료됐습니다. '
                                       '이제 눈 건강 정보를 확인하실 수 있습니다.')
                return redirect('accounts:profile')
            else:
                return render(request, 'error.html', {
                    'errors': form.errors
                })

        else:
            form = ProfileModelForm()
        return render(request, 'accounts/profile_register.html', {
            'form': form
        })

    else:
        if request.method == 'POST':
            form = ProfileModelForm(request.POST,
                                    request.FILES, instance=profile)
            if form.is_valid():
                profile = form.save(commit=True)
                messages.info(request, '프로필이 성공적으로 변경됐습니다.')

                return render(request, 'accounts/profile.html', {
                    'form': form,
                    'profile': profile
                })
            else:
                return render(request, '500.html', {
                    'errors': form.errors
                })

        form = ProfileModelForm(instance=profile)
        return render(request, 'accounts/profile.html', {
            'form': form,
            'profile': profile
        })


'''

get_ocr_data

설명:

10회 깜빡였을 때 ajax 요청을 처리하는 api
'''


def get_ocr_data(request):
    if request.user.is_authenticated():
        ocr_time = request.GET.get('ocr_time')
        profile = Profile.objects.filter(user=request.user).first()
        if datetime.datetime.now().hour < 12:
            profile.calculate_ocr_am(ocr_time)
        else:
            profile.calculate_ocr_pm(ocr_time)
        data = {"ok": True}
        return JsonResponse(data, status=200)
    else:
        data = {"ok": False, "msg": "anoymoususer"}
        return JsonResponse(data, status=403)


'''
rank_user

이번 달 유저의 눈깜빡임수 랭킹
'''


def rank_user(request):
    profile_list = Profile.objects.order_by('-ocr_month_count').all()[:10]
    return render(request, 'accounts/rank_user.html', {
        "profile_list": profile_list
    })
