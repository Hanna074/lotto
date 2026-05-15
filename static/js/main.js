// ── LOTTO 6/45 Main JS ──────────────────────────────────────

// 공 색상 자동 적용 (모든 페이지 공통)
function getBallColor(n) {
  if (n <= 10) return 'ball-yellow';
  if (n <= 20) return 'ball-blue';
  if (n <= 30) return 'ball-red';
  if (n <= 40) return 'ball-black';
  return 'ball-green';
}

document.addEventListener('DOMContentLoaded', () => {
  // ball-color-auto 클래스를 가진 모든 공에 색상 적용
  document.querySelectorAll('.ball-color-auto').forEach(ball => {
    const n = parseInt(ball.dataset.number);
    if (!isNaN(n)) {
      ball.classList.add(getBallColor(n));
    }
  });

  // 알림 자동 닫기 (4초 후)
  document.querySelectorAll('.alert.fade.show').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 4000);
  });
});
