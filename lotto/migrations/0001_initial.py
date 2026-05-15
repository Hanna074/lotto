from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_number', models.PositiveIntegerField(unique=True, verbose_name='회차')),
                ('draw_date', models.DateField(verbose_name='추첨일')),
                ('numbers', models.JSONField(default=list, verbose_name='당첨 번호')),
                ('bonus', models.PositiveIntegerField(blank=True, null=True, verbose_name='보너스 번호')),
                ('is_completed', models.BooleanField(default=False, verbose_name='추첨 완료')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '추첨 회차',
                'verbose_name_plural': '추첨 회차 목록',
                'ordering': ['-draw_number'],
            },
        ),
        migrations.CreateModel(
            name='LottoPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numbers', models.JSONField(verbose_name='선택 번호')),
                ('purchase_type', models.CharField(choices=[('manual', '수동'), ('auto', '자동')], max_length=10, verbose_name='구매 유형')),
                ('purchased_at', models.DateTimeField(auto_now_add=True, verbose_name='구매 일시')),
                ('drawing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lotto.drawing', verbose_name='회차')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='구매자')),
            ],
            options={
                'verbose_name': '복권 구매',
                'verbose_name_plural': '복권 구매 목록',
                'ordering': ['-purchased_at'],
            },
        ),
        migrations.CreateModel(
            name='WinRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.PositiveIntegerField(choices=[(1, '1등'), (2, '2등'), (3, '3등'), (4, '4등'), (5, '5등')], verbose_name='등수')),
                ('prize_amount', models.PositiveBigIntegerField(verbose_name='당첨금')),
                ('confirmed_at', models.DateTimeField(auto_now_add=True, verbose_name='당첨 확정 일시')),
                ('purchase', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lotto.lottopurchase', verbose_name='구매 내역')),
            ],
            options={
                'verbose_name': '당첨 내역',
                'verbose_name_plural': '당첨 내역 목록',
                'ordering': ['rank', '-confirmed_at'],
            },
        ),
    ]
