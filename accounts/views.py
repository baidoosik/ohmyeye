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
            form = ProfileModelForm(None, request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=True)
                messages.info(request, '회원가입이 완료됐습니다. '
                                       '이제 눈 건강 정보를 확인하실 수 있습니다.')
                return redirect('event:event_list')
            else:
                return render(request, 'error.html', {
                    'errors': form.errors
                })

        else:
            user = request.user
            form = ProfileModelForm(user)
        return render(request, 'accounts/profile_register.html', {
            'form': form
        })

    else:
        if request.method == 'POST':
            form = ProfileModelForm(None, request.POST,
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

        form = ProfileModelForm(None, instance=profile)
        return render(request, 'accounts/profile.html', {
            'form': form,
            'profile': profile
        })