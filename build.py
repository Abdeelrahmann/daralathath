#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
يولّد index.html و room_XX.html و product.html و sitemap.xml من بيانات الغرف أدناه.
التشغيل (من داخل فولدر الموقع):   python3 tools/build.py
لتعديل اسم/وصف غرفة أو رقم الواتساب: عدّل الجزء الخاص بها أدناه ثم أعد التشغيل.
"""
import json, os, html
from urllib.parse import quote
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://darelathath.com"
BRAND = "دار الأثاث لغرف النوم"
PHONE_LOCAL = "0576979199"
PHONE_INTL = "+966576979199"
WHATSAPP_NUMBER = "966576979199"
LASTMOD = "2026-09-28"

# (اللون/الطابع, تفاصيل القطع)
ROOMS = [
 ("أبيض وخشبي", "دولاب بضلف ومرايا، تسريحة بمرآة دائرية مضيئة وبوف"),
 ("بني خشبي", "سرير بهيدبورد مخطط، تسريحة بمرآة دائرية وبوف، ودولاب بضلف خشبية"),
 ("أبيض ورمادي", "سرير بهيدبورد مبطن بمربعات، تسريحة بمرآة دائرية وبوف، ودولاب بمرايا"),
 ("بيج وبني", "سرير بهيدبورد مبطن بمربعات بارزة، تسريحة بمرآة وبوف، ودولاب بمرايا"),
 ("رمادي وبيج", "سرير بهيدبورد بتصميم هندسي، تسريحة بمرآة دائرية، ودولاب بتقسيم داخلي"),
 ("بني خشبي دافئ", "سرير بهيدبورد هندسي، تسريحة بمرآة دائرية، ودولاب بضلف خشبية وزجاج داكن"),
 ("كريمي", "دولاب بضلف كبيرة ومرايا، تسريحة بمرآة دائرية وبوف، وسرير بسيط"),
 ("بيج رمادي", "دولاب بضلف ومرايا، سرير، وتسريحة بمرآة دائرية وبوف"),
 ("بيج ورمادي داكن", "سرير بهيدبورد هندسي، دولاب بضلف وزجاج داكن، وتسريحة بمرآة دائرية"),
 ("بني داكن وأبيض", "تسريحة بمرآة دائرية مضيئة، سرير بهيدبورد مبطن، ودولاب بضلف"),
 ("أبيض وأسود", "دولاب بضلف بيضاء مع زجاج أسود، سرير، وتسريحة بمرآة وبوف"),
 ("بيج وكريمي", "سرير بهيدبورد مبطن مخطط، تسريحة بمرآة دائرية وبوف، ودولاب بمرايا"),
 ("رمادي حجري", "دولاب بضلف رمادية، تسريحة بمرآة دائرية وبوف، وسرير بهيدبورد داكن"),
 ("سريرين مفرد رمادي", "سريران مفردان بهيدبورد داكن، تسريحة بمرآة دائرية، ودولاب بضلف"),
 ("أبيض وكريمي", "تسريحة بمرآة دائرية وبوف، سرير بهيدبورد مبطن، ودولاب بضلف"),
 ("أبيض", "سرير بهيدبورد أبيض، تسريحة بمرآة، ودولاب بضلف ومرايا"),
 ("بيج وأسود", "تسريحة بمرآة كبيرة وبوف أسود، سرير بهيدبورد داكن، ودولاب بمرايا"),
 ("كريمي كلاسيكي", "سرير بهيدبورد كلاسيكي، تسريحة بمرآة دائرية، ودولاب بمرايا"),
 ("رمادي حجري", "سرير بهيدبورد بتصميم هندسي، تسريحة بمرآة دائرية وبوف، ودولاب بضلف وزجاج داكن"),
]

def wa(text):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}"

# رقم الصورة اللي تظهر كغلاف للكارت وأول صورة في المعرض (photo_N.jpg) — عدّلها لو حبيت
COVERS = {1:3, 2:2, 3:3, 4:1, 5:2, 6:2, 7:3, 8:2, 9:1, 10:3, 11:2, 12:2, 13:3, 14:1, 15:2, 16:3, 17:3, 18:3, 19:1}

products = []
def list_photos(pid, cover_no=None):
    """الصور المنفصلة photo_1.jpg, photo_2.jpg ... داخل فولدر الغرفة. الغلاف = أنسب صورة للكارت."""
    folder = os.path.join(ROOT, "assets", "rooms", pid)
    names = sorted(f for f in os.listdir(folder) if f.startswith("photo_") and f.endswith(".jpg"))
    if not names:  # احتياط: لو مفيش صور منفصلة نستخدم الصورة الأصلية
        names = ["original.jpg"]
    info = {n: Image.open(os.path.join(folder, n)).size for n in names}
    # الغلاف: أقرب نسبة عرض/ارتفاع للكارت (≈1.4)، وعند التقارب الأكبر مساحة
    cover = f"photo_{cover_no}.jpg" if cover_no and f"photo_{cover_no}.jpg" in names else \
        min(names, key=lambda n: (round(abs(info[n][0] / info[n][1] - 1.4), 1), -info[n][0] * info[n][1]))
    ordered = [cover] + [n for n in names if n != cover]
    return [f"assets/rooms/{pid}/{n}" for n in ordered], [info[n] for n in ordered]

for i, (color, details) in enumerate(ROOMS, 1):
    n = f"{i:02d}"
    pid = f"room_{n}"
    imgs, sizes = list_photos(pid, COVERS.get(i))
    cover = imgs[0]
    csize = sizes[0]
    name = f"غرفة نوم {color} موديل {n}"
    short = "، ".join(details.split("، ")[:2])
    desc = f"{name}: {details}. تصميم أنيق يجمع بين الجمال والراحة."
    products.append(dict(id=pid, n=n, name=name, short=short, desc=desc,
                         cover=cover, csize=csize, images=imgs, sizes=sizes,
                         url=f"{DOMAIN}/{pid}.html"))

e = html.escape
HEAD_COMMON = f'''<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="index, follow">
  <meta name="author" content="{BRAND}">
  <meta name="theme-color" content="#211913">
  <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23211913'/%3E%3Ctext x='32' y='46' font-size='40' text-anchor='middle' fill='%23d5a257'%3E%E2%8C%82%3C/text%3E%3C/svg%3E">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">'''

FOOTER = f'<footer>© 2026 {BRAND} — جميع الحقوق محفوظة</footer>'

def header(home):
    if home:
        tools = '<div class="left-tools"></div>'
        logo = '#home'
        nav = '''<a class="active" href="#home">الرئيسية</a>
    <a href="#bedrooms">غرف النوم</a>
    <a href="#about">من نحن</a>
    <a href="#contact">تواصل معنا</a>'''
    else:
        tools = '<div class="left-tools"><a class="icon-btn" aria-label="العودة للرئيسية" href="index.html">⌂</a></div>'
        logo = 'index.html'
        nav = '''<a href="index.html#home">الرئيسية</a>
    <a class="active" href="index.html#bedrooms">غرف النوم</a>
    <a href="index.html#about">من نحن</a>
    <a href="index.html#contact">تواصل معنا</a>'''
    return f'''<header class="topbar">
  <div class="container nav-wrap">
    {tools}
    <a class="logo" href="{logo}">
      <div class="logo-icon">⌂</div>
      <div><strong>دار الأثاث</strong><small>لغرف النوم</small></div>
    </a>
    <a class="phone" href="tel:{PHONE_LOCAL}">
      <span class="wa">◔</span>
      <span><small>تواصل معنا</small><b>{PHONE_LOCAL}</b></span>
    </a>
  </div>
  <nav class="nav container">
    {nav}
  </nav>
</header>'''

WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>'

def fab(link):
    return f'<a class="wa-fab" href="{link}" target="_blank" rel="noopener" aria-label="تواصل عبر واتساب">{WA_ICON}</a>'

HOME_WA = wa("السلام عليكم، أريد الاستفسار عن غرف النوم.")

# ---------------- index ----------------
cards = []
for idx, p in enumerate(products):
    w, h = p["csize"]
    cards.append(f'''    <article class="card">
      <div class="pic">
        {'<span class="new">جديد</span>' if idx == 0 else ''}
        <img src="{p['cover']}" alt="{e(p['name'])}" width="{w}" height="{h}" loading="{'eager' if idx < 5 else 'lazy'}" decoding="async">
      </div>
      <div class="body">
        <h3>{e(p['name'])}</h3>
        <p>{e(p['short'])}</p>
        <a href="{p['id']}.html" aria-label="عرض تفاصيل {e(p['name'])}">عرض التفاصيل</a>
      </div>
    </article>''')

index_schema = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "FurnitureStore", "@id": f"{DOMAIN}/#business", "name": BRAND,
     "url": f"{DOMAIN}/", "telephone": PHONE_INTL,
     "image": f"{DOMAIN}/assets/hero.jpg",
     "areaServed": {"@type": "Country", "name": "المملكة العربية السعودية"},
     "description": "عرض تصاميم غرف نوم متنوعة والتواصل عبر واتساب للاستفسار."},
    {"@type": "WebSite", "@id": f"{DOMAIN}/#website", "url": f"{DOMAIN}/", "name": BRAND, "inLanguage": "ar"},
    {"@type": "ItemList", "name": "غرف النوم",
     "itemListElement": [{"@type": "ListItem", "position": i+1, "url": p["url"], "name": p["name"]} for i, p in enumerate(products)]}
  ]
}

index_html = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
  {HEAD_COMMON}
  <title>غرف نوم وأثاث | دار الأثاث لغرف النوم</title>
  <meta name="description" content="دار الأثاث لغرف النوم — شاهد {len(products)} تصميماً لغرف النوم بصور حقيقية: سرير وتسريحة ودولاب بألوان وموديلات متنوعة. تواصل معنا عبر واتساب للاستفسار.">
  <link rel="canonical" href="{DOMAIN}/">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="غرف نوم وأثاث | {BRAND}">
  <meta property="og:description" content="شاهد تصاميم غرف النوم بصور حقيقية وتواصل معنا عبر واتساب للاستفسار.">
  <meta property="og:url" content="{DOMAIN}/">
  <meta property="og:image" content="{DOMAIN}/assets/hero.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(index_schema, ensure_ascii=False)}</script>
</head>
<body>

{header(True)}

<main id="home">
  <section class="hero">
    <img src="assets/hero.jpg" alt="غرفة نوم فاخرة" width="2076" height="612" fetchpriority="high">
    <div class="hero-shade"></div>
    <div class="container hero-content">
      <div>
        <h1>دار الأثاث<br><span>لغرف النوم</span></h1>
        <p>حيث يلتقي الفخامة بالراحة</p>
        <div class="actions">
          <a class="btn outline" href="#bedrooms">تصفح غرف النوم <b>‹</b></a>
          <a class="btn gold" href="{HOME_WA}" target="_blank" rel="noopener">تواصل عبر واتساب <b>◔</b></a>
        </div>
      </div>
    </div>
  </section>

  <section class="features">
    <div class="container feature-grid">
      <div><span>♢</span><div><b>جودة عالية</b><small>ضمانات عالية الجودة تضمن لك المتانة</small></div></div>
      <div><span>▣</span><div><b>توصيل سريع</b><small>توصيل وتركيب في جميع مناطق المملكة</small></div></div>
      <div><span>✦</span><div><b>تصاميم متنوعة</b><small>مجموعة واسعة من التصاميم الكلاسيكية والمودرن</small></div></div>
      <div><span>♧</span><div><b>خدمة عملاء متميزة</b><small>نحن هنا لخدمتك على مدار الساعة</small></div></div>
    </div>
  </section>

  <section class="products-section" id="bedrooms">
    <div class="section-title">
      <span>اختياراتنا</span>
      <h2>أحدث غرف النوم</h2>
      <div class="line">◆</div>
    </div>

    <div class="container products" id="productsContainer">
{chr(10).join(cards)}
    </div>
  </section>

  <section class="cta" id="offers">
    <div class="container cta-inner">
      <div><h2>جاهز لتجديد غرفة نومك؟</h2><p>تواصل معنا الآن واحصل على أفضل التفاصيل والتصاميم</p></div>
      <div class="cta-contact"><b>{PHONE_LOCAL}</b><a href="{HOME_WA}" target="_blank" rel="noopener">تواصل معنا الآن ◔</a></div>
    </div>
  </section>

  <section class="about" id="about">
    <div class="container">
      <h2>من نحن</h2>
      <p>{BRAND} تعرض لك تشكيلة من تصاميم غرف النوم بألوان وموديلات متنوعة، وبصور حقيقية للقطع. تصفّح الموديلات، وتواصل معنا عبر واتساب للاستفسار عن أي غرفة وتفاصيلها.</p>
    </div>
  </section>

  <section class="contact" id="contact">
    <div class="container">
      <h2>تواصل معنا</h2>
      <a href="tel:{PHONE_LOCAL}">{PHONE_LOCAL}</a>
      <p><a href="{HOME_WA}" target="_blank" rel="noopener" style="font-size:14px">أو راسلنا مباشرة عبر واتساب</a></p>
    </div>
  </section>
</main>

{FOOTER}
{fab(HOME_WA)}
</body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(index_html)

# ---------------- room pages ----------------
for i, p in enumerate(products):
    prev_p = products[i-1] if i > 0 else None
    next_p = products[i+1] if i < len(products)-1 else None
    og_img = f"{DOMAIN}/{p['images'][0]}"
    title = f"{p['name']} | {BRAND}"
    msg = wa(f"السلام عليكم، أريد الاستفسار عن هذا المنتج: {p['name']}\n{p['url']}")
    schema = {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "Product", "name": p["name"], "description": p["desc"], "sku": p["id"],
         "image": [f"{DOMAIN}/{s}" for s in p["images"]],
         "brand": {"@type": "Brand", "name": BRAND}, "url": p["url"]},
        {"@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": f"{DOMAIN}/"},
          {"@type": "ListItem", "position": 2, "name": "غرف النوم", "item": f"{DOMAIN}/#bedrooms"},
          {"@type": "ListItem", "position": 3, "name": p["name"], "item": p["url"]}]}
      ]
    }
    thumbs = "\n          ".join(
        f'<button type="button" class="thumbnail{" selected" if k==0 else ""}" data-src="{s}" aria-label="صورة {k+1}"><img src="{s}" alt="{e(p["name"])} - صورة {k+1}" width="{p["sizes"][k][0]}" height="{p["sizes"][k][1]}" loading="lazy"></button>'
        for k, s in enumerate(p["images"]))
    navs = ""
    if prev_p: navs += f'<a href="{prev_p["id"]}.html">› {e(prev_p["name"])}</a>'
    else: navs += "<span></span>"
    if next_p: navs += f'<a href="{next_p["id"]}.html">{e(next_p["name"])} ‹</a>'
    page = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
  {HEAD_COMMON}
  <link rel="stylesheet" href="product.css">
  <title>{e(title)}</title>
  <meta name="description" content="{e(p['desc'])} شاهد الصور الحقيقية وتواصل معنا عبر واتساب للاستفسار.">
  <link rel="canonical" href="{p['url']}">
  <meta property="og:type" content="product">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(p['desc'])}">
  <meta property="og:url" content="{p['url']}">
  <meta property="og:image" content="{og_img}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
{header(False)}

<main>
  <section class="product-details container" id="productDetails">
    <a class="back-link" href="index.html#bedrooms">‹ العودة إلى غرف النوم</a>
    <div class="product-layout">
      <div class="gallery">
        <div class="main-image-wrap">
          <img id="mainProductImage" src="{p['images'][0]}" alt="{e(p['name'])}" width="{p['sizes'][0][0]}" height="{p['sizes'][0][1]}" fetchpriority="high">
        </div>
        <div class="thumbnails" id="thumbnails">
          {thumbs}
        </div>
      </div>

      <div class="product-info">
        <span class="product-label">{BRAND}</span>
        <h1 id="productName">{e(p['name'])}</h1>
        <div class="product-line">◆</div>
        <p id="productDescription">{e(p['desc'])}</p>
        <a class="product-whatsapp" id="whatsappButton" href="{msg}" target="_blank" rel="noopener">
          <span>◔</span> استفسر عن هذا المنتج
        </a>
      </div>
    </div>
    <div class="room-nav">{navs}</div>
  </section>
</main>

{FOOTER}
{fab(msg)}

<script>
document.querySelectorAll('.thumbnail').forEach(function (t) {{
  t.addEventListener('click', function () {{
    document.getElementById('mainProductImage').src = t.dataset.src;
    document.querySelectorAll('.thumbnail').forEach(function (x) {{ x.classList.remove('selected'); }});
    t.classList.add('selected');
  }});
}});
</script>
</body>
</html>
'''
    open(os.path.join(ROOT, f"{p['id']}.html"), "w", encoding="utf-8").write(page)

# ---------------- legacy product.html (redirect) ----------------
legacy = f'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="{DOMAIN}/">
<title>{BRAND}</title>
<script>
var id = new URLSearchParams(location.search).get('id');
location.replace(/^room_\\d{{2}}$/.test(id || '') ? id + '.html' : 'index.html#bedrooms');
</script>
<noscript><meta http-equiv="refresh" content="0;url=index.html"></noscript>
</head>
<body><a href="index.html#bedrooms">غرف النوم</a></body>
</html>
'''
open(os.path.join(ROOT, "product.html"), "w", encoding="utf-8").write(legacy)

# ---------------- sitemap ----------------
urls = [f"{DOMAIN}/"] + [p["url"] for p in products]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sm += f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{LASTMOD}</lastmod>\n  </url>\n"
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
print("done:", len(products), "rooms")
