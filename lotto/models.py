from django.db import models
from django.contrib.auth.models import User


class Drawing(models.Model):
    """추첨 회차"""
    draw_number  = models.PositiveIntegerField(unique=True, verbose_name='회차')
    draw_date    = models.DateField(verbose_name='추첨일')
    numbers      = models.JSONField(default=list, verbose_name='당첨 번호')   # [1, 5, 12, 23, 34, 45]
    bonus        = models.PositiveIntegerField(null=True, blank=True, verbose_name='보너스 번호')
    is_completed = models.BooleanField(default=False, verbose_name='추첨 완료')
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-draw_number']
        verbose_name = '추첨 회차'
        verbose_name_plural = '추첨 회차 목록'

    def __str__(self):
        status = '완료' if self.is_completed else '대기'
        return f'제{self.draw_number}회 ({self.draw_date}) [{status}]'

    def numbers_display(self):
        return ', '.join(str(n) for n in self.numbers)


class LottoPurchase(models.Model):
    """복권 구매 내역"""
    PURCHASE_TYPE = [
        ('manual', '수동'),
        ('auto',   '자동'),
    ]
    user          = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='구매자')
    drawing       = models.ForeignKey(Drawing, on_delete=models.CASCADE, verbose_name='회차')
    numbers       = models.JSONField(verbose_name='선택 번호')   # [3, 7, 15, 22, 38, 44]
    purchase_type = models.CharField(max_length=10, choices=PURCHASE_TYPE, verbose_name='구매 유형')
    purchased_at  = models.DateTimeField(auto_now_add=True, verbose_name='구매 일시')

    class Meta:
        ordering = ['-purchased_at']
        verbose_name = '복권 구매'
        verbose_name_plural = '복권 구매 목록'

    def __str__(self):
        return f'{self.user.username} - 제{self.drawing.draw_number}회 [{self.get_purchase_type_display()}]'

    def numbers_display(self):
        return self.numbers


class WinRecord(models.Model):
    """당첨 내역"""
    RANK_CHOICES = [
        (1, '1등'),
        (2, '2등'),
        (3, '3등'),
        (4, '4등'),
        (5, '5등'),
    ]
    purchase     = models.OneToOneField(LottoPurchase, on_delete=models.CASCADE, verbose_name='구매 내역')
    rank         = models.PositiveIntegerField(choices=RANK_CHOICES, verbose_name='등수')
    prize_amount = models.PositiveBigIntegerField(verbose_name='당첨금')
    confirmed_at = models.DateTimeField(auto_now_add=True, verbose_name='당첨 확정 일시')

    class Meta:
        ordering = ['rank', '-confirmed_at']
        verbose_name = '당첨 내역'
        verbose_name_plural = '당첨 내역 목록'

    def __str__(self):
        return f'{self.purchase.user.username} - {self.get_rank_display()} ({self.prize_amount:,}원)'
