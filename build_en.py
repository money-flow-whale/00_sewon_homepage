# 영문 페이지 en/index.html을 index.html에서 만든다(2026-11-12).
# index.html의 data-ko/data-en 짝을 영어로 채우고, 경로를 한 단계 위로 바꾼다.
# index.html을 고친 뒤에는 `python build_en.py`를 다시 실행하고 en/index.html도 함께 커밋한다.
import os, re

root = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(root, "index.html"), encoding="utf-8").read()

# data-ko="X" data-en="Y" ...>X<  →  >Y<  (요소 안 글자가 data-ko와 같은 것만)
pat = re.compile(r'(<[a-z0-9]+\b[^>]*?data-ko="([^"]*)"[^>]*?data-en="([^"]*)"[^>]*>)([^<]*)<')
n = 0
def sub(m):
    global n
    if m.group(4) != m.group(2):
        return m.group(0)
    n += 1
    return m.group(1) + m.group(3) + "<"
s = pat.sub(sub, s)
total = len(re.findall(r'data-ko="', s))

s = s.replace('<html lang="ko">', '<html lang="en" data-page="en">', 1)
s = s.replace("<title>주식회사 세원비전 | Sewon Vision Co., Ltd.</title>", "<title>Sewon Vision Co., Ltd. | Mobile Software & E-commerce</title>", 1)
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Sewon Vision Co., Ltd. - a Korean company building mobile apps, websites and e-commerce systems, and the owner of the eyewear brand MONO SUN WORKS.">', s, count=1)
s = s.replace('<link rel="canonical" href="https://sewonvision.com/">', '<link rel="canonical" href="https://sewonvision.com/en/">', 1)
s = s.replace('<button id="langBtn" class="lang-btn">EN</button>', '<button id="langBtn" class="lang-btn">한</button>', 1)
s = s.replace('aria-label="메뉴"', 'aria-label="Menu"')
s = s.replace('alt="MONO SUN WORKS 아이웨어 브랜드 대표 이미지"', 'alt="MONO SUN WORKS eyewear brand image"')
s = s.replace('alt="로또명당 앱 아이콘"', 'alt="Lotto Myeongdang app icon"')
for a in ('src="assets/', 'href="privacy.html"', 'href="terms.html"'):
    s = s.replace(a, a.replace('="', '="../'))

os.makedirs(os.path.join(root, "en"), exist_ok=True)
open(os.path.join(root, "en", "index.html"), "w", encoding="utf-8", newline="\n").write(s)
left = re.findall(r'[가-힣]+', re.sub(r'data-ko="[^"]*"|<script>.*?</script>|<!--.*?-->', '', s, flags=re.S))
print(f"translated {n}/{total} elements; Korean left outside data-ko/comments/script: {left[:20]}")
