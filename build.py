# -*- coding: utf-8 -*-
"""Собирает статический сайт в dist/. Запуск: python3 build.py"""
import json, os, shutil, html
from data import *

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
S = SITE
e = html.escape
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
ARR_L = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 12H5M11 6l-6 6 6 6"/></svg>'
PHONE_IC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
WA_IC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.9" aria-hidden="true"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/><path d="M9 9.5c.3 2 2.5 4.2 4.5 4.5l1.2-1.2 1.8.8"/></svg>'
TG_IC = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true"><path d="M21 4L3 11l6 2 2 6 3-4 5 4z"/><path d="M9 13l8-6"/></svg>'
MAX_IC = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><path d="M5 18V7l7 7 7-7v11"/></svg>'
CHEV = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
LOGO_SVG = '<svg width="42" height="42" viewBox="0 0 42 42" aria-hidden="true" fill="none" stroke="#E7C3A3" stroke-width="1.6"><rect x="1" y="1" width="40" height="40" rx="3"/><rect x="7" y="7" width="28" height="28" rx="2"/><path d="M13 13h16v16H13z"/><path d="M21 13v16M13 21h16"/></svg>'


def img(n, small=False):
    return f"/img/p/{n}{'-s' if small else ''}.webp"


def ic(path, size=22, color="currentColor", sw=1.5):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{path}"/></svg>'


def messengers(cls="mess"):
    out = f'<a class="{cls} wa hide-m" href="https://wa.me/{S["wa"]}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">{WA_IC}</a>'
    out += f'<a class="{cls} tg hide-m" href="{S["tg"]}" target="_blank" rel="noopener" aria-label="Написать в Telegram">{TG_IC}</a>'
    if S["max"]:
        out += f'<a class="{cls} max hide-m" href="{S["max"]}" target="_blank" rel="noopener" aria-label="Написать в MAX">{MAX_IC}</a>'
    return out


def header():
    cols = "".join(f'<div><h4>{e(t)}</h4>' + "".join(f'<a href="{h}">{e(n)}</a>' for n, h in links) + '</div>' for t, links in MENU)
    promo = ('<div class="mega-promo"><span class="gift" aria-hidden="true">🎁</span><b>Светильники в подарок!</b>'
             '<span>Дарим светодиодные светильники любого цвета на выбор.</span><a class="link-arrow" href="/akcii/">Все акции ' + ARR + '</a></div>')
    nav_items = [("Цены", "/#calc"), ("Наши работы", "/raboty/"), ("Акции", "/akcii/"), ("О компании", "/o-kompanii/"), ("Статьи", "/stati/"), ("Контакты", "/kontakty/")]
    nav = (f'<div class="dd"><button type="button" aria-expanded="false" aria-haspopup="true">Каталог {CHEV}</button><div class="mega">{cols}{promo}</div></div>'
           + "".join(f'<a href="{h}">{n}</a>' for n, h in nav_items))
    mob = '<a href="/katalog/">Каталог</a>' + "".join(f'<a class="sub" href="/katalog/{t["slug"]}/">{e(t["short"])}</a>' for t in TYPES) + "".join(f'<a href="{h}">{n}</a>' for n, h in nav_items)
    mob += f'<a class="tel" href="tel:{S["phone_href"]}">{S["phone"]}</a>'
    return f'''<header class="hdr"><div class="wrap hdr-in">
<a class="logo" href="/">{LOGO_SVG}<span><b>{S["name"]}</b><small>натяжные потолки</small></span></a>
<nav class="nav" aria-label="Основное меню">{nav}</nav>
<div class="hdr-r"><a class="tel hide-m" href="tel:{S["phone_href"]}">{PHONE_IC}<span>{S["phone"]}</span></a>{messengers()}
<button type="button" class="btn-cb hide-m" data-cb>Заказать звонок</button>
<button type="button" class="burger" aria-label="Меню" aria-expanded="false"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button></div>
</div><nav class="mob" aria-label="Мобильное меню">{mob}</nav></header>'''


def form(topic="Консультация", dark=True, btn="Получить консультацию"):
    return f'''<form class="form" data-topic="{e(topic)}" novalidate>
<div class="f2"><label class="f">Имя<input type="text" name="name" placeholder="Как к вам обращаться" autocomplete="name"></label>
<label class="f">Телефон<input type="tel" name="tel" placeholder="+7 (___) ___-__-__" required autocomplete="tel" pattern="[0-9+()\\s-]{{10,}}"></label></div>
<button type="submit" class="btn">{btn} {ARR}</button>
<label class="agree"><input type="checkbox" required><span>Даю согласие на обработку персональных данных в соответствии с <a href="/politika/">политикой конфиденциальности</a></span></label>
<p class="ok">Спасибо! Откроется WhatsApp с вашей заявкой — отправьте сообщение, и мы перезвоним.</p>
</form>'''


def footer():
    cols = [("Каталог", [(t["short"], f"/katalog/{t['slug']}/") for t in TYPES]),
            ("Услуги и цены", [("Калькулятор", "/#calc"), ("Замер", "/#calc"), ("Визуализация", "/#viz"), ("Акции", "/akcii/"), ("Рассрочка", "/akcii/")]),
            ("Компания", [("О компании", "/o-kompanii/"), ("Наши работы", "/raboty/"), ("Статьи", "/stati/"), ("Вопрос-ответ", "/#faq"), ("Контакты", "/kontakty/")])]
    navs = "".join(f'<nav aria-label="{t}"><b class="t">{t}</b>' + "".join(f'<a href="{h}">{e(n)}</a>' for n, h in l) + '</nav>' for t, l in cols)
    email = f'<a href="mailto:{S["email"]}">{S["email"]}</a>' if S["email"] else ""
    legal = f' · {e(S["legal"])}' if S["legal"] else ""
    return f'''<footer class="foot"><div class="wrap foot-t">
<div><a class="logo" href="/">{LOGO_SVG}<span><b>{S["name"]}</b><small>натяжные потолки</small></span></a><p style="color:#BFB3A8;max-width:260px">Натяжные потолки и освещение в Москве и Московской области</p></div>
{navs}
<div><a href="tel:{S["phone_href"]}" style="color:#fff;font-weight:700;font-size:17px">{S["phone"]}</a><span>{S["address"]}</span>{email}<span>{S["hours_calls"]}</span>
<span style="display:flex;gap:10px;margin-top:6px">{messengers("mess").replace(" hide-m", "")}</span></div>
</div><div class="wrap foot-b"><span>© 2014–2026 {S["name"]}{legal}</span><span style="display:flex;flex-wrap:wrap;gap:8px 24px"><a href="/politika/">Политика конфиденциальности</a><a href="/politika/#soglasie">Согласие на обработку персональных данных</a></span></div></footer>
<div class="modal" role="dialog" aria-modal="true" aria-label="Заказать звонок"><div class="modal-b"><button type="button" class="x" aria-label="Закрыть">×</button>
<h2 style="font-size:24px;font-weight:600;padding-right:40px">Перезвоним и ответим на вопросы</h2><p class="lead" style="font-size:14.5px">Оставьте номер — менеджер свяжется с вами. {S["hours_calls"]}.</p>
{form("Обратный звонок", btn="Жду звонка")}</div></div>
<div class="lb" role="dialog" aria-label="Фото"><button class="x" type="button" aria-label="Закрыть">×</button><img src="data:," alt=""></div>'''


def page(path, title, desc, body, light_top=False):
    cfg = {"heroInterval": S["hero_interval_ms"], "wa": S["wa"], "prices": PRICES}
    doc = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="https://{S["domain"]}{path}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://{S["domain"]}{img(HERO[0])}">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v={VERSION}"></head>
<body{' class="light-top"' if light_top else ''}>{header()}<main>{body}</main>{footer()}
<script>window.SITE={json.dumps(cfg, ensure_ascii=False)}</script><script src="/js/main.js?v={VERSION}" defer></script></body></html>'''
    out = os.path.join(DIST, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(DIST, path.strip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)


# ---------------- blocks ----------------
def rates():
    ya = '<span class="ic" style="background:#FC3F1D;color:#fff">Я</span>'
    gis = '<span class="ic" style="background:#19AA1E;color:#fff">2</span>'
    av = ('<span class="ic" style="background:#fff"><svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><circle cx="6" cy="6" r="4" fill="#04E061"/>'
          '<circle cx="14.5" cy="5.5" r="2.5" fill="#FF4053"/><circle cx="6" cy="14.5" r="2.5" fill="#965EEB"/><circle cx="14" cy="14" r="4" fill="#0AF"/></svg></span>')
    return (f'<div class="rates"><a class="rate" href="{S["yandex"]}" target="_blank" rel="noopener">{ya}Яндекс Карты <span class="star">★</span></a>'
            f'<a class="rate" href="{S["gis"]}" target="_blank" rel="noopener">{gis}2ГИС <span class="star">★</span></a>'
            f'<a class="rate" href="{S["avito"]}" target="_blank" rel="noopener">{av}Авито <span class="star">★</span></a></div>')


def calc_block(canvas="mat", title="Узнайте ориентировочную стоимость потолка", eyebrow="Онлайн-калькулятор"):
    chips = "".join(f'<button type="button" class="chip" data-v="{k}" aria-pressed="false">{v["name"]}</button>' for k, v in PRICES["canvas"].items())
    opts = "".join(f'<option value="{k}">{v["name"].replace(" профиль", "")}</option>' for k, v in PRICES["profile"].items())
    return f'''<section id="calc" class="wrap sec"><div class="calc rv" data-canvas="{canvas}">
<svg aria-hidden="true" viewBox="0 0 1200 360" preserveAspectRatio="none"><path d="M380 360 C520 300 640 200 760 0" stroke="#F3D3B4" stroke-opacity=".18" stroke-width="22" fill="none"/><path d="M380 360 C520 300 640 200 760 0" stroke="#FBE6D2" stroke-opacity=".85" stroke-width="2" fill="none"/><path d="M0 360 L380 360 C520 300 640 200 760 0 L0 0 Z" fill="#2E2723" fill-opacity=".55"/></svg>
<div class="calc-l"><span class="eyebrow">{eyebrow}</span><h2 class="h2" style="max-width:520px">{title}</h2>
<p>Укажите площадь, полотно и профиль. После замера смета фиксируется в договоре и не меняется.</p>
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;margin-top:6px"><a href="#" data-cb class="btn">Получить точную смету {ARR}</a>
<span class="calc-sum"><small>Ориентировочно</small><b>—</b></span></div></div>
<div class="calc-f"><div><label for="c-area-{canvas}">Площадь помещения <b class="area-out">18 м²</b></label><input id="c-area-{canvas}" type="range" name="area" min="4" max="120" step="1" value="18"></div>
<div><span class="lbl">Тип полотна</span><div class="chips" style="margin-top:10px">{chips}</div></div>
<div class="row2"><div><label for="c-prof-{canvas}">Профиль</label><select id="c-prof-{canvas}" name="profile" style="margin-top:8px">{opts}</select></div>
<div><span class="lbl">Светильники, шт</span><div class="num" data-k="lamps" style="margin-top:8px"><button type="button" data-d="-1" aria-label="Меньше">−</button><output>4</output><button type="button" data-d="1" aria-label="Больше">+</button></div></div></div>
<p class="calc-note"></p></div></div></section>'''


def catalog_cards(types):
    return "".join(f'<a class="ccard" href="/katalog/{t["slug"]}/"><img src="{img(t["photos"][0], True)}" alt="{e(t["name"])}" loading="lazy">'
                   f'<div><b>{e(t["short"])} {ARR}</b><span>{e(t["card"])}</span></div></a>' for t in types)


def geo_svg():
    k, lon0, lat0, cs = 260, 35.1, 56.98, 0.563
    P = lambda lo, la: ((lo - lon0) * k * cs + 10, (lat0 - la) * k + 10)
    outline = " ".join("%.1f,%.1f" % P(lo, la) for lo, la in MO_OUTLINE)
    cx, cy = P(37.62, 55.75)
    roads = "".join('<line class="road" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cx, cy, *P(lo, la)) for lo, la, n, b in GEO if b)
    pts = ""
    for i, (lo, la, n, big) in enumerate(GEO):
        x, y = P(lo, la)
        r = 6 if n == "Москва" else (4 if big else 3)
        pts += (f'<g class="pt{" lbl" if big else ""}" style="--d:{(i % 16) * 0.18:.2f}s"><circle class="p" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
                f'<circle class="c" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/><text x="{x + 8:.1f}" y="{y + 3:.1f}">{e(n)}</text></g>')
    return (f'<svg viewBox="0 0 770 720" role="img" aria-label="Карта: Москва и Московская область, города, где мы работаем">'
            f'<defs><radialGradient id="gl"><stop offset="0" stop-color="#F3D3B4" stop-opacity=".35"/><stop offset="1" stop-color="#F3D3B4" stop-opacity="0"/></radialGradient></defs>'
            f'<polygon class="mo" points="{outline}"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="140" fill="url(#gl)"/>{roads}'
            f'<ellipse class="mkad" cx="{cx:.1f}" cy="{cy:.1f}" rx="{0.29 * k * cs:.1f}" ry="{0.17 * k:.1f}"/>{pts}</svg>')


def faq_block():
    items = "".join(f'<details><summary>{e(q)}<i aria-hidden="true">{CHEV}</i></summary><p>{e(a)}</p></details>' for q, a in FAQ)
    left, right = items.split("</details>")[:-1][0::2], items.split("</details>")[:-1][1::2]
    col = lambda l: '<div style="display:flex;flex-direction:column;gap:12px">' + "".join(x + "</details>" for x in l) + "</div>"
    return f'''<section id="faq" class="wrap sec"><span class="eyebrow">FAQ</span><h2 class="h2" style="margin-top:12px">Вопросы, которые задают нам чаще всего</h2>
<div class="faq">{col(left)}{col(right)}</div></section>'''


def articles_block(title="Полезные статьи"):
    cards = "".join(f'<a class="art" href="/stati/{a["slug"]}/"><img src="{img(a["img"], True)}" alt="" loading="lazy"><div><b>{e(a["title"])}</b><p>{e(a["sub"])}</p><span>Читать статью →</span></div></a>' for a in ARTICLES)
    return f'''<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between"><h2 class="h2">{title}</h2><a class="link-arrow" href="/stati/">Все статьи {ARR}</a></div><div class="arts">{cards}</div></section>'''


def cta_block():
    return f'''<section class="wrap sec"><div class="cta rv"><svg aria-hidden="true" viewBox="0 0 1200 320" preserveAspectRatio="none"><path d="M560 320 C700 260 860 140 1200 110" stroke="#F3D3B4" stroke-opacity=".14" stroke-width="20" fill="none"/><path d="M560 320 C700 260 860 140 1200 110" stroke="#FBE6D2" stroke-opacity=".6" stroke-width="1.6" fill="none"/></svg>
<div class="cta-l"><h2 class="h2">Остались вопросы?</h2><p>Поможем выбрать потолок и рассчитать стоимость. Подскажем решения, подготовим предварительный расчёт и согласуем бесплатный замер в Москве или области.</p>
<div style="display:flex;flex-wrap:wrap;gap:14px 28px;font-size:14px;font-weight:600;margin-top:6px"><a href="tel:{S["phone_href"]}" style="color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:8px">{PHONE_IC}{S["phone"]}</a>
<a href="https://wa.me/{S["wa"]}" target="_blank" rel="noopener" style="color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:8px"><span class="mess wa" style="width:28px;height:28px">{WA_IC}</span>Написать в WhatsApp</a>
<a href="{S["tg"]}" target="_blank" rel="noopener" style="color:#fff;text-decoration:none;display:inline-flex;align-items:center;gap:8px"><span class="mess tg" style="width:28px;height:28px">{TG_IC}</span>Написать в Telegram</a></div></div>
{form()}</div></section>'''


def contacts_block():
    rows = f'<div><dt>Адрес офиса</dt><dd>{S["address"]}</dd></div><div><dt>Телефон</dt><dd><a href="tel:{S["phone_href"]}">{S["phone"]}</a></dd></div>'
    if S["email"]:
        rows += f'<div><dt>Электронная почта</dt><dd><a href="mailto:{S["email"]}">{S["email"]}</a></dd></div>'
    rows += f'<div><dt>Режим работы</dt><dd style="font-weight:500;font-size:15px">{S["hours_calls"]}<br>{S["hours_office"]}</dd></div>'
    btns = f'<a class="tg" href="{S["tg"]}" target="_blank" rel="noopener">{TG_IC} Telegram</a><a class="wa" href="https://wa.me/{S["wa"]}" target="_blank" rel="noopener">{WA_IC} WhatsApp</a>'
    if S["max"]:
        btns += f'<a class="max" href="{S["max"]}" target="_blank" rel="noopener">{MAX_IC} MAX</a>'
    q = html.escape(S["address"])
    return f'''<section id="contacts" class="wrap sec"><div class="cont">
<div class="cont-l rv"><span class="eyebrow">Контакты</span><h2 class="h2">Свяжитесь с нами любым удобным способом</h2><dl>{rows}</dl><div class="cont-btns">{btns}</div></div>
<div class="cont-map rv"><iframe src="https://yandex.ru/map-widget/v1/?text={q}&amp;z=15" title="Офис на Яндекс Картах" loading="lazy" allowfullscreen></iframe></div>
</div></section>'''


def phero(title, sub, photo, crumbs):
    cr = " / ".join(f'<a href="{h}">{e(n)}</a>' if h else e(n) for n, h in crumbs)
    return f'''<section class="phero"><img class="bg" src="{img(photo)}" alt=""><div class="wrap"><nav class="crumbs" aria-label="Хлебные крошки">{cr}</nav>
<h1 class="h1" style="font-size:clamp(34px,4.4vw,54px)">{title}</h1><p>{sub}</p></div></section>'''


# ---------------- pages ----------------
def home():
    slides = "".join(f'<img {"src" if i == 0 else "data-src"}="{img(n)}" alt="Наш объект: натяжной потолок" {"fetchpriority=high" if i == 0 else ""}{" class=on" if i == 0 else ""}>' for i, n in enumerate(HERO))
    dots = "".join("<i></i>" for _ in HERO)
    feats = "".join(f'<div>{ic(p, 30, "#F1E9E1", 1.3)}<span style="display:block"><b>{t}</b><span>{s}</span></span></div>' for t, s, p in FEATURES)
    # why grid: adv, media, adv, adv(wide media)...
    cells, mi = [], 0
    layout = ["a", "m", "a", "a", "mw", "a", "a"]
    ai = 0
    for c in layout:
        if c == "a" and ai < len(WHY):
            t, d, p = WHY[ai]; ai += 1
            cells.append(f'<div class="adv rv"><span class="ic">{ic(p, 22)}</span><div><b>{t}</b><p>{d}</p></div></div>')
        elif c.startswith("m"):
            n = WHY_MEDIA[mi % len(WHY_MEDIA)]; mi += 1
            cells.append(f'<div class="media kb{" wide" if c == "mw" else ""} rv"><img src="{img(n)}" alt="Наш объект" loading="lazy"></div>')
    stats = "".join(f'<div><b>{v}</b><span>{l}</span></div>' for v, l in [(S["years"], "лет опыта"), (S["works"], "выполненных работ"), (S["per_month"], "заказов в месяц"), (S["warranty"], "гарантия по договору")])
    steps = "".join(f'<li><span class="n">{i + 1:02d}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(STEPS))
    mq = "".join(f'<img src="{img(n, True)}" alt="" loading="lazy">' for n in MARQUEE)
    projects = "".join(f'<a class="wcard" href="/raboty/"><img src="{img(p, True)}" alt="{e(s)}" loading="lazy"><span style="display:flex;flex-direction:column;gap:2px"><b>{t}</b><span>{s}</span></span></a>' for t, s, p in PROJECTS)
    body = f'''
<section class="hero"><div class="hero-slides">{slides}</div>
<div class="wrap hero-in"><span class="eyebrow">Натяжные потолки в Москве и МО</span>
<h1 class="h1">Натяжные потолки <em>под ваш интерьер</em></h1>
<p>От лаконичных матовых полотен до теневых систем и световых линий. Подберём конструкцию, освещение и подготовим понятный расчёт для вашего помещения.</p>
<div class="hero-btns"><a href="#calc" class="btn">Рассчитать стоимость {ARR}</a><a href="/raboty/" class="btn btn-ghost">Посмотреть работы</a></div>
{rates()}</div>
<div class="hero-dots" aria-hidden="true">{dots}</div>
<div class="hero-ctrl"><span>01 / {len(HERO):02d}</span><button type="button" class="circ prev" aria-label="Предыдущее фото">{ARR_L}</button><button type="button" class="circ next" aria-label="Следующее фото">{ARR}</button></div></section>
<section class="feat"><div class="wrap">{feats}</div></section>
{calc_block()}
<section id="catalog" class="wrap sec split"><div class="split-t"><h2 class="h2">Какой потолок вам подходит?</h2><p class="lead">Выберите фактуру или современную конструкцию — покажем особенности, фотографии и варианты исполнения.</p><a class="link-arrow" href="/katalog/">Смотреть весь каталог {ARR}</a></div>
<div class="split-c g4">{catalog_cards([t for t in TYPES if t["slug"] in ("tenevye", "parjashchie", "matovye", "glyancevye")])}</div></section>
<section id="works" class="wrap sec split"><div class="split-t"><h2 class="h2">Наши работы</h2><p class="lead">Выполненные проекты: какие решения выбрали заказчики, как организовали свет и что вошло в монтаж.</p><a class="link-arrow" href="/raboty/">Смотреть проекты {ARR}</a></div><div class="split-c g4">{projects}</div></section>
<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between;margin-bottom:28px"><div><span class="eyebrow">Преимущества</span><h2 class="h2" style="margin-top:12px">Почему выбирают {S["name"]}</h2></div><p class="lead" style="max-width:480px">Работаем по Москве и области с 2010 года. Делаем аккуратно, по договору и с понятной сметой.</p></div>
<div class="why-grid">{"".join(cells)}</div><div class="stats">{stats}</div></section>
<section class="wrap sec"><div class="geo"><div><span class="eyebrow" style="color:var(--accent)">География</span><h2 class="h2" style="margin:12px 0 14px">Работаем по Москве и всей Московской области</h2>
<p>Выезжаем на бесплатный замер и монтаж в любой район Москвы и практически во все города области.</p>
<div class="geo-nums"><div><b>{len(GEO)}+</b><span>городов области</span></div><div><b>0 ₽</b><span>выезд на замер</span></div></div>
<div class="geo-legend"><span><i class="m"></i>Москва — офис и склад</span><span><i></i>Города, где мы работаем</span></div></div>{geo_svg()}</div></section>
<section class="wrap sec"><div class="about rv"><img src="{img("4608")}" alt="" loading="lazy"><div class="about-in"><div class="about-top"><div style="display:flex;flex-direction:column;gap:12px"><span class="eyebrow" style="color:var(--accent)">О компании</span><h2 class="h2" style="max-width:640px">{S["name"]} — натяжные потолки под ключ с {S["years"]} лет опыта</h2></div>
<p>От замера до сдачи объекта: подбираем полотно и свет, делаем точную смету и чисто монтируем. Работаем только с сертифицированными материалами.</p></div>
<div class="about-g"><div><b>С 2010 года</b><span>на рынке натяжных потолков Москвы и области</span></div><div><b>{S["works"]} объектов</b><span>квартиры, дома, офисы и коммерческие помещения</span></div><div><b>Свои бригады</b><span>опытные монтажники, чистый монтаж с пылесборником</span></div><div><b>Гарантия {S["warranty"]}</b><span>на полотно и монтаж — прописана в договоре</span></div></div>
<a href="/o-kompanii/" class="btn" style="align-self:flex-start">О компании {ARR}</a></div></div></section>
<section id="viz" class="wrap sec viz"><figure class="rv"><img src="{img("4640")}" alt="Пример: потолок со световым овалом" loading="lazy"></figure>
<div class="rv"><span class="eyebrow">Визуализация</span><h2 class="h2">Представьте потолок до установки</h2><p class="lead" style="max-width:460px">Пришлите фото комнаты и расскажите, какое решение нравится. Подготовим бесплатную визуализацию с освещением и конструкцией.</p><a href="#" data-cb class="btn">Получить визуализацию {ARR}</a></div></section>
<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between"><div><span class="eyebrow">Этапы</span><h2 class="h2" style="margin-top:12px">Как мы работаем — от заявки до сдачи</h2></div><p class="lead" style="max-width:520px">Пять понятных шагов. На каждом этапе вы знаете, что будет дальше и сколько это стоит.</p></div>
<ol class="steps"><div class="steps-bar" aria-hidden="true"><i></i></div>{steps}</ol></section>
<div class="marq" aria-hidden="true"><div class="marq-t">{mq}{mq}</div></div>
<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between"><h2 class="h2">Отзывы наших клиентов</h2><p class="lead" style="max-width:520px">Читайте отзывы на независимых площадках — там их нельзя отредактировать.</p></div>
<div class="rev-src">{rates().replace('class="rates"', 'style="display:contents"').replace('class="rate"', 'class="rate" style="background:#fff;color:var(--ink);border-color:var(--rule)"')}</div></section>
{faq_block()}
{articles_block()}
{cta_block()}
{contacts_block()}'''
    page("/", f"Натяжные потолки в Москве и МО под ключ — {S['name']}", "Натяжные потолки в Москве и Московской области: матовые, глянцевые, теневые, парящие, световые линии. Бесплатный замер, гарантия 15 лет, смета не меняется.", body)


def catalog_index():
    body = phero("Каталог натяжных потолков", "Фактуры, конструкции и освещение. Выберите вариант — покажем фото наших объектов, цены и преимущества.", "4613", [("Главная", "/"), ("Каталог", "")])
    body += f'<section class="wrap sec"><div class="g4">{catalog_cards(TYPES)}</div></section>' + calc_block() + cta_block()
    page("/katalog/", f"Каталог натяжных потолков — {S['name']}", "Все виды натяжных потолков: матовые, глянцевые, сатиновые, тканевые, с подсветкой, теневые, парящие, бесщелевые и световые линии.", body)


def type_page(t):
    cv = [c for c in CANVASES if t["canvas"] in c["t"]]
    cards = "".join(f'<div class="pcard">{"<span class=tag>" + c["tag"] + "</span>" if c["tag"] else ""}<b>{c["n"]}</b><span class="pr">{c["p"]} <small>₽/м²</small></span>'
                    f'<dl><dt>Производитель</dt><dd>{c["c"]}</dd><dt>Толщина</dt><dd>{c["th"]}</dd><dt>Ширина</dt><dd>{c["w"]}</dd><dt>Гарантия</dt><dd>{c["g"]}</dd></dl></div>' for c in cv)
    advs = "".join(f'<div class="rv"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in t["adv"])
    gal = "".join(f'<a href="{img(p)}"><img src="{img(p, True)}" alt="{e(t["name"])} — фото объекта" loading="lazy"></a>' for p in t["photos"])
    pts = "".join(f"<li>{e(x)}</li>" for x in t["points"])
    others = [o for o in TYPES if o["slug"] != t["slug"]][:4]
    body = f'''<section class="phero"><img class="bg" src="{img(t["photos"][0])}" alt=""><div class="wrap"><nav class="crumbs"><a href="/">Главная</a> / <a href="/katalog/">Каталог</a> / {e(t["short"])}</nav>
<h1 class="h1" style="font-size:clamp(34px,4.4vw,54px)">{e(t["name"])}</h1><p>{e(t["intro"])}</p><ul class="feat-list">{pts}</ul>
<div class="hero-btns"><a href="#" data-cb class="btn">Заказать {ARR}</a><a href="#calc" class="btn btn-ghost">Рассчитать стоимость</a></div></div></section>
{calc_block(t["canvas"], "Рассчитайте стоимость", e(t["short"]))}
<section class="wrap sec"><h2 class="h2">Натяжные потолки: цена за 1 м²</h2><p class="lead" style="margin-top:10px">Используем только сертифицированные полотна, разрешённые для жилых помещений.</p>{"<div class=price-g>" + cards + "</div>" if cards else ""}</section>
<section class="wrap sec"><h2 class="h2">Преимущества: {e(t["short"].lower())}</h2><div class="advs">{advs}</div></section>
<section class="wrap sec"><h2 class="h2">Фото наших объектов</h2><div class="gallery">{gal}</div></section>
<section class="wrap sec"><h2 class="h2">Другие решения</h2><div class="g4" style="margin-top:28px">{catalog_cards(others)}</div></section>
{cta_block()}'''
    page(f"/katalog/{t['slug']}/", f"{t['name']} в Москве — цена за м² | {S['name']}", t["intro"][:160], body)


def works():
    tabs = "".join(f'<button type="button" class="tab" role="tab" id="tab-{t["slug"]}" aria-controls="tp-{t["slug"]}" aria-selected="{"true" if i == 0 else "false"}">{e(t["short"])}</button>' for i, t in enumerate(TYPES))
    panels = ""
    for i, t in enumerate(TYPES):
        th = "".join(f'<button type="button" data-full="{img(p)}" aria-current="{"true" if j == 0 else "false"}" aria-label="Фото {j + 1}"><img src="{img(p, True)}" alt="" loading="lazy"></button>' for j, p in enumerate(t["photos"][:5]))
        panels += (f'<div class="tpanel" role="tabpanel" id="tp-{t["slug"]}" aria-labelledby="tab-{t["slug"]}"{"" if i == 0 else " hidden"}>'
                   f'<div class="gal"><div class="gal-main"><img src="{img(t["photos"][0])}" alt="{e(t["name"])}" loading="lazy"><button type="button" class="circ prev" aria-label="Назад">{ARR_L}</button><button type="button" class="circ next" aria-label="Вперёд">{ARR}</button></div><div class="thumbs">{th}</div></div>'
                   f'<div class="txt"><h3>{e(t["name"])}</h3><p class="lead">{e(t["intro"])}</p><a class="btn btn-line" href="/katalog/{t["slug"]}/">Подробнее {ARR}</a></div></div>')
    allp = sorted({p for t in TYPES for p in t["photos"]} | set(MARQUEE) | set(HERO))
    gal = "".join(f'<a href="{img(p)}"><img src="{img(p, True)}" alt="Наш объект" loading="lazy"></a>' for p in allp)
    body = phero("Наши работы", "Фотографии объектов, которые мы сделали в Москве и области: квартиры, дома, санузлы и коммерческие помещения.", "4638", [("Главная", "/"), ("Наши работы", "")])
    body += f'<section class="wrap sec"><h2 class="h2">Фотогалерея объектов</h2><div class="gallery">{gal}</div></section>'
    body += f'<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between"><h2 class="h2">Установим любой вид натяжного потолка</h2><p class="lead" style="max-width:460px">Расскажем об особенностях каждого варианта, чтобы вы сделали свой выбор.</p></div><div class="tabs" role="tablist" aria-label="Виды потолков">{tabs}</div>{panels}</section>'
    body += cta_block()
    page("/raboty/", f"Наши работы — фото натяжных потолков | {S['name']}", "Фото выполненных работ: теневые, парящие, матовые потолки, световые линии и подсветка в Москве и области.", body)


def promos():
    cards = "".join(f'<div class="promo {c} rv"><span class="big">{b}</span><b>{e(t)}</b><p>{e(d)}</p><a href="#" data-cb class="btn">Хочу также</a></div>' for b, t, d, c in PROMOS)
    body = phero("Акции", "Лучшие спецпредложения — установите натяжные потолки с выгодой.", "4589", [("Главная", "/"), ("Акции", "")])
    body += f'<section class="wrap sec"><div class="promos">{cards}</div><p class="lead" style="margin-top:20px;font-size:14px">Условия акций уточняйте у менеджера. Акции не суммируются, если не указано иное.</p></section>' + calc_block() + cta_block()
    page("/akcii/", f"Акции на натяжные потолки — {S['name']}", "Скидки новосёлам и пенсионерам, светильники в подарок, рассрочка 0%, скидка в день замера.", body)


def about():
    stats = "".join(f'<div><b>{v}</b><span>{l}</span></div>' for v, l in [(S["years"], "лет опыта"), (S["works"], "выполненных работ"), (S["per_month"], "заказов в месяц"), (S["warranty"], "гарантия по договору")])
    advs = "".join(f'<div class="rv"><b>{t}</b><p>{d}</p></div>' for t, d, p in WHY[:4])
    body = phero(f"О компании {S['name']}", "Натяжные потолки под ключ в Москве и Московской области. Уют. Качество. Надёжность.", "4608", [("Главная", "/"), ("О компании", "")])
    body += f'''<section class="wrap sec split"><div class="split-t" style="max-width:520px;flex-basis:420px"><h2 class="h2">Делаем потолки, которые создают атмосферу</h2>
<p class="lead">Мы занимаемся натяжными потолками больше {S["years"].rstrip("+")} лет. За это время сделали более {S["works"].rstrip("+")} объектов — от небольших санузлов до загородных домов со сложными световыми сценариями.</p>
<p class="lead">Начинаем с бесплатной консультации и замера, подбираем полотно, профиль и освещение, фиксируем смету в договоре. Монтируем чисто — с пылесборником — и сдаём работу с гарантией.</p>
<p class="lead">Работаем только с сертифицированными материалами от проверенных производителей.</p></div>
<div class="split-c" style="display:grid;grid-template-columns:1fr 1fr;gap:14px"><img src="{img("4576")}" alt="" style="border-radius:16px;aspect-ratio:3/4;object-fit:cover;width:100%"><img src="{img("4661")}" alt="" style="border-radius:16px;aspect-ratio:3/4;object-fit:cover;width:100%;margin-top:40px"></div></section>
<section class="wrap sec"><div class="stats" style="border:0;margin:0">{stats}</div></section>
<section class="wrap sec"><h2 class="h2">Наши принципы</h2><div class="advs">{advs}</div></section>'''
    body += cta_block() + contacts_block()
    page("/o-kompanii/", f"О компании — {S['name']}", f"{S['name']}: натяжные потолки в Москве и области, {S['years']} лет опыта, {S['works']} выполненных работ, гарантия {S['warranty']}.", body)


def contacts():
    body = phero("Контакты", f"{S['address']}. {S['hours_calls']}.", "4628", [("Главная", "/"), ("Контакты", "")]) + contacts_block() + cta_block()
    page("/kontakty/", f"Контакты — {S['name']}", f"Телефон {S['phone']}, адрес: {S['address']}. WhatsApp и Telegram.", body)


def articles():
    body = phero("Статьи", "Полезное о натяжных потолках: как выбрать, что учесть при ремонте и что делать в непредвиденных ситуациях.", "4620", [("Главная", "/"), ("Статьи", "")])
    cards = "".join(f'<a class="art" href="/stati/{a["slug"]}/"><img src="{img(a["img"], True)}" alt="" loading="lazy"><div><b>{e(a["title"])}</b><p>{e(a["sub"])}</p><span>Читать статью →</span></div></a>' for a in ARTICLES)
    body += f'<section class="wrap sec"><div class="arts" style="margin:0">{cards}</div></section>' + cta_block()
    page("/stati/", f"Статьи о натяжных потолках — {S['name']}", "Полезные статьи о натяжных потолках.", body)
    for a in ARTICLES:
        parts = ""
        for kind, val in a["body"]:
            if kind == "ul":
                parts += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in val) + "</ul>"
            else:
                parts += f"<{kind}>{e(val)}</{kind}>"
        b = phero(e(a["title"]), e(a["sub"]), a["img"], [("Главная", "/"), ("Статьи", "/stati/"), (a["title"], "")])
        b += f'<section class="wrap sec"><article class="prose">{parts}<p><a class="btn" href="#" data-cb>Задать вопрос мастеру {ARR}</a></p></article></section>'
        b += articles_block("Другие статьи") + cta_block()
        page(f"/stati/{a['slug']}/", f"{a['title']} — {S['name']}", a["sub"], b)


def policy():
    op = S["legal"] or f"{S['name']} (реквизиты оператора указываются в договоре)"
    body = phero("Политика конфиденциальности", "Порядок обработки и защиты персональных данных пользователей сайта.", "4600", [("Главная", "/"), ("Политика", "")])
    body += f'''<section class="wrap sec"><article class="prose">
<h2>1. Общие положения</h2><p>Настоящая политика определяет порядок обработки персональных данных пользователей сайта {S["domain"]} в соответствии с Федеральным законом № 152-ФЗ «О персональных данных». Оператор — {e(op)}.</p>
<h2>2. Какие данные мы обрабатываем</h2><p>Имя и номер телефона, которые вы указываете в формах на сайте, а также содержание вашего обращения.</p>
<h2>3. Цели обработки</h2><p>Связь с вами для консультации, расчёта стоимости, согласования замера и выполнения работ.</p>
<h2>4. Передача данных</h2><p>Мы не передаём персональные данные третьим лицам, за исключением случаев, предусмотренных законодательством РФ. Заявки могут передаваться через мессенджеры (WhatsApp, Telegram), выбранные вами для связи.</p>
<h2>5. Хранение и защита</h2><p>Данные хранятся не дольше, чем этого требуют цели обработки, и защищаются от несанкционированного доступа.</p>
<h2>6. Ваши права</h2><p>Вы можете запросить сведения об обработке ваших данных, потребовать их уточнения или удаления, а также отозвать согласие, написав нам или позвонив по телефону {S["phone"]}.</p>
<h2 id="soglasie">Согласие на обработку персональных данных</h2><p>Отправляя форму на сайте и отмечая соответствующий пункт, вы даёте согласие оператору на обработку указанных вами персональных данных (имя, телефон) в целях, указанных в разделе 3, с использованием средств автоматизации и без них. Согласие действует до его отзыва.</p>
</article></section>'''
    page("/politika/", f"Политика конфиденциальности — {S['name']}", "Политика обработки персональных данных.", body)


def notfound():
    body = phero("Страница не найдена", "Возможно, она переехала. Начните с главной или каталога.", "4590", [("Главная", "/"), ("404", "")])
    body += f'<section class="wrap sec" style="display:flex;gap:14px;flex-wrap:wrap"><a class="btn" href="/">На главную {ARR}</a><a class="btn btn-line" href="/katalog/">Каталог</a></section>'
    page("/404.html", f"Страница не найдена — {S['name']}", "404", body)


def main():
    global VERSION
    import hashlib
    h = hashlib.md5()
    for p in ("src/css/style.css", "src/js/main.js", "data.py"):
        h.update(open(os.path.join(ROOT, p), "rb").read())
    VERSION = h.hexdigest()[:8]
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, "src"), DIST)
    home(); catalog_index(); works(); promos(); about(); contacts(); articles(); policy(); notfound()
    for t in TYPES:
        type_page(t)
    urls = ["/", "/katalog/", "/raboty/", "/akcii/", "/o-kompanii/", "/kontakty/", "/stati/"] + [f"/katalog/{t['slug']}/" for t in TYPES] + [f"/stati/{a['slug']}/" for a in ARTICLES]
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://{S['domain']}{u}</loc></url>" for u in urls) + "</urlset>")
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: https://{S['domain']}/sitemap.xml\n")
    print("built", len(urls), "pages ->", DIST)


VERSION = "dev"
if __name__ == "__main__":
    main()
