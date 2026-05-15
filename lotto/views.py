import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Drawing, LottoPurchase, WinRecord
from .utils import check_rank, get_prize, rank_label, rank_badge_class


def home(request):
    """메인 페이지 - 최근 당첨 번호 표시"""
    latest_drawing = Drawing.objects.filter(is_completed=True).first()
    upcoming = Drawing.objects.filter(is_completed=False).last()
    recent_drawings = Drawing.objects.filter(is_completed=True)[:5]
    return render(request, 'lotto/home.html', {
        'latest_drawing': latest_drawing,
        'upcoming': upcoming,
        'recent_drawings': recent_drawings,
    })


@login_required
def buy_ticket(request):
    """복권 구매 (수동 / 자동)"""
    current_drawing = Drawing.objects.filter(is_completed=False).order_by('draw_number').last()

    if not current_drawing:
        messages.warning(request, '현재 판매 중인 회차가 없습니다. 관리자에게 문의하세요.')
        return redirect('home')

    if request.method == 'POST':
        purchase_type = request.POST.get('type', 'auto')

        if purchase_type == 'auto':
            numbers = sorted(random.sample(range(1, 46), 6))
        else:
            try:
                numbers = []
                for i in range(1, 7):
                    n = int(request.POST.get(f'n{i}', 0))
                    if not (1 <= n <= 45):
                        raise ValueError(f'번호 {n}은 1~45 사이여야 합니다.')
                    numbers.append(n)
                if len(set(numbers)) != 6:
                    raise ValueError('번호가 중복되었습니다.')
                numbers = sorted(numbers)
            except (ValueError, TypeError) as e:
                messages.error(request, f'번호 입력 오류: {e}')
                return render(request, 'lotto/buy.html', {'drawing': current_drawing, 'numbers_range': range(1, 46)})

        LottoPurchase.objects.create(
            user=request.user,
            drawing=current_drawing,
            numbers=numbers,
            purchase_type=purchase_type,
        )
        messages.success(request, f'제{current_drawing.draw_number}회 복권 구매 완료! 번호: {", ".join(map(str, numbers))}')
        return redirect('my_tickets')

    return render(request, 'lotto/buy.html', {
        'drawing': current_drawing,
        'numbers_range': range(1, 46),
    })


@login_required
def my_tickets(request):
    """내 구매 내역 및 당첨 확인"""
    purchases = LottoPurchase.objects.filter(
        user=request.user
    ).select_related('drawing').order_by('-purchased_at')

    tickets = []
    for purchase in purchases:
        d = purchase.drawing
        if d.is_completed:
            rank = check_rank(purchase.numbers, d.numbers, d.bonus)
            result = rank_label(rank)
            badge  = rank_badge_class(rank)
            prize  = get_prize(rank) if rank else 0
        else:
            result = '미추첨'
            badge  = 'badge-rank-pending'
            prize  = 0
        tickets.append({
            'purchase': purchase,
            'result':   result,
            'badge':    badge,
            'prize':    prize,
        })

    return render(request, 'lotto/my_tickets.html', {'tickets': tickets})
