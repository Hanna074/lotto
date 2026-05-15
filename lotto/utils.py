"""
당첨 등수 계산 및 당첨금 산정 유틸리티
"""

# 등수별 고정 당첨금 (4등, 5등)
PRIZE_TABLE = {
    4: 50_000,
    5: 5_000,
}

# 1~3등 당첨금 비율 (실제 로또는 변동이지만 데모용 고정값)
FIXED_PRIZE = {
    1: 2_000_000_000,  # 20억
    2:    60_000_000,  # 6천만
    3:     1_500_000,  # 150만
}


def check_rank(my_numbers, win_numbers, bonus):
    """
    당첨 등수를 반환한다. 낙첨 시 None.
    my_numbers, win_numbers: list of int
    bonus: int
    """
    my_set  = set(my_numbers)
    win_set = set(win_numbers)
    match   = len(my_set & win_set)
    has_bonus = bonus in my_set

    if match == 6:
        return 1
    if match == 5 and has_bonus:
        return 2
    if match == 5:
        return 3
    if match == 4:
        return 4
    if match == 3:
        return 5
    return None


def get_prize(rank):
    """등수에 해당하는 당첨금 반환"""
    return FIXED_PRIZE.get(rank, PRIZE_TABLE.get(rank, 0))


def rank_label(rank):
    if rank is None:
        return '낙첨'
    return f'{rank}등'


def rank_badge_class(rank):
    """Bootstrap badge 색상"""
    mapping = {
        1: 'badge-rank-1',
        2: 'badge-rank-2',
        3: 'badge-rank-3',
        4: 'badge-rank-4',
        5: 'badge-rank-5',
    }
    return mapping.get(rank, 'badge-rank-lose')
