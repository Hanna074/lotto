import random
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
from lotto.models import Drawing, LottoPurchase, WinRecord
from lotto.utils import check_rank, get_prize


def _calculate_winners(drawing):
    """추첨 완료 후 당첨자 일괄 계산"""
    purchases = LottoPurchase.objects.filter(drawing=drawing)
    win_count = 0
    for purchase in purchases:
        rank = check_rank(purchase.numbers, drawing.numbers, drawing.bonus)
        if rank is not None:
            WinRecord.objects.update_or_create(
                purchase=purchase,
                defaults={'rank': rank, 'prize_amount': get_prize(rank)},
            )
            win_count += 1
    return win_count


@staff_member_required
def sales_list(request):
    """판매 내역 조회"""
    purchases = LottoPurchase.objects.select_related(
        'user', 'drawing'
    ).order_by('-purchased_at')

    # 회차 필터
    draw_filter = request.GET.get('draw', '')
    if draw_filter:
        purchases = purchases.filter(drawing__draw_number=draw_filter)

    drawings = Drawing.objects.all()
    total = purchases.count()
    auto_count   = purchases.filter(purchase_type='auto').count()
    manual_count = purchases.filter(purchase_type='manual').count()

    return render(request, 'manager/sales.html', {
        'purchases':    purchases,
        'drawings':     drawings,
        'draw_filter':  draw_filter,
        'total':        total,
        'auto_count':   auto_count,
        'manual_count': manual_count,
    })


@staff_member_required
def run_draw(request):
    """추첨 실행"""
    current_drawing = Drawing.objects.filter(is_completed=False).order_by('draw_number').last()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create_round':
            # 새 회차 생성
            last = Drawing.objects.order_by('-draw_number').first()
            next_num  = (last.draw_number + 1) if last else 1
            next_date = date.today() + timedelta(days=7)
            Drawing.objects.create(draw_number=next_num, draw_date=next_date)
            messages.success(request, f'제{next_num}회 회차가 생성되었습니다.')
            return redirect('run_draw')

        if action == 'draw' and current_drawing:
            pool    = random.sample(range(1, 46), 7)
            numbers = sorted(pool[:6])
            bonus   = pool[6]
            current_drawing.numbers      = numbers
            current_drawing.bonus        = bonus
            current_drawing.is_completed = True
            current_drawing.save()
            win_count = _calculate_winners(current_drawing)
            messages.success(
                request,
                f'제{current_drawing.draw_number}회 추첨 완료! '
                f'당첨 번호: {", ".join(map(str, numbers))} + 보너스 {bonus} / '
                f'당첨자 {win_count}명'
            )
            return redirect('manager_winners')

    completed = Drawing.objects.filter(is_completed=True)
    return render(request, 'manager/draw.html', {
        'current_drawing': current_drawing,
        'completed':       completed,
    })


@staff_member_required
def winners_list(request):
    """당첨 내역 조회"""
    win_records = WinRecord.objects.select_related(
        'purchase__user', 'purchase__drawing'
    ).order_by('rank', '-confirmed_at')

    draw_filter = request.GET.get('draw', '')
    if draw_filter:
        win_records = win_records.filter(purchase__drawing__draw_number=draw_filter)

    drawings    = Drawing.objects.filter(is_completed=True)
    rank_stats  = win_records.values('rank').annotate(cnt=Count('id')).order_by('rank')

    return render(request, 'manager/winners.html', {
        'win_records': win_records,
        'drawings':    drawings,
        'draw_filter': draw_filter,
        'rank_stats':  rank_stats,
    })
