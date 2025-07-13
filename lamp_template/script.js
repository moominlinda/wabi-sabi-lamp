
document.getElementById('csvInput').addEventListener('change', function (e) {
  const file = e.target.files[0];
  if (!file) return;

  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: function (results) {
      const data = results.data;
      console.log('✅ 解析筆數：', data.length);

      const sequence = [];

      function smoothS(x) {
        const p1 = 2.8;
        const p2 = 2.5;
        const y = Math.pow(x, p1) / (Math.pow(x, p1) + Math.pow(1 - x, p2));
        return Math.min(1, y * 1.2);
      }

      data.forEach((row, i) => {
        const level = parseFloat(row['Level']);
        const proportion = parseFloat(row['Proportion']);
        if (isNaN(level) || isNaN(proportion)) {
          console.warn(`⚠️ 第 ${i + 2} 行資料錯誤，跳過`, row);
          return;
        }

        const norm = level / 9;
        const brightness = smoothS(norm);
        const duration = proportion * 4000;

        console.log(`✅ 第 ${i + 2} 行：亮度 = ${brightness.toFixed(2)}, 時長 = ${duration}ms`);
        sequence.push({ brightness, duration });
      });

      if (sequence.length > 0) {
        sequence.push({ brightness: 0, duration: 2000 }); // 黑場
        document.getElementById('status').textContent = '燈光閃爍中...';
        animateLamp(sequence);
      } else {
        document.getElementById('status').textContent = '⚠️ 無有效資料可播放';
      }
    },
    error: function (err) {
      console.error('❌ CSV 解析錯誤', err);
      document.getElementById('status').textContent = '⚠️ 讀取 CSV 時發生錯誤';
    }
  });
});

function animateLamp(sequence) {
  const lamp = document.getElementById('lamp');
  let index = 0;

  function loop() {
    const step = sequence[index];
    lamp.style.opacity = step.brightness;
    setTimeout(() => {
      index = (index + 1) % sequence.length;
      loop();
    }, step.duration);
  }

  loop();
}
