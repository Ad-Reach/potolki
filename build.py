# -*- coding: utf-8 -*-
"""Собирает статический сайт в dist/. Запуск: python3 build.py"""
import json, os, re, shutil, html
from data import *

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
S = SITE
e = html.escape
ARR = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
ARR_L = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M20 12H5M11 6l-6 6 6 6"/></svg>'
PHONE_IC = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'
WA_IC = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="#fff" stroke-width="1.7" stroke-linejoin="round" d="M12 3.2a8.8 8.8 0 0 0-7.6 13.3L3.2 20.8l4.4-1.2A8.8 8.8 0 1 0 12 3.2z"/><path fill="#fff" d="M9.1 7.6c-.2-.4-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.3.3-.9.9-.9 2.2s1 2.6 1.1 2.7c.1.2 1.9 3 4.7 4.1 2.3.9 2.8.7 3.3.7.5-.1 1.6-.7 1.8-1.3.2-.6.2-1.2.2-1.3-.1-.1-.3-.2-.5-.3l-1.7-.8c-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1-.3-.1-1.1-.4-2-1.2-.8-.7-1.3-1.5-1.4-1.8-.2-.3 0-.4.1-.5l.4-.5.3-.4c.1-.2 0-.3 0-.4l-.7-2z"/></svg>'
TG_IC = '<svg width="19" height="19" viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M20.7 3.6 2.9 10.5c-1.2.5-1.2 1.2-.2 1.5l4.6 1.4 1.7 5.4c.2.6.4.8.8.8s.6-.2.9-.5l2.2-2.1 4.6 3.4c.8.5 1.5.2 1.7-.8l3-14.2c.3-1.2-.5-1.8-1.5-1.3zM9.3 13.6l8.4-5.3c.4-.2.7-.1.4.2l-6.9 6.2-.3 3.1-1.6-4.2z"/></svg>'
MAX_IC = '<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" aria-hidden="true"><path d="M5 18V7l7 7 7-7v11"/></svg>'
CHEV = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'
LOGO_SVG = '<svg width="42" height="42" viewBox="0 0 42 42" aria-hidden="true" fill="none" stroke="#E7C3A3" stroke-width="1.6"><rect x="1" y="1" width="40" height="40" rx="3"/><rect x="7" y="7" width="28" height="28" rx="2"/><path d="M13 13h16v16H13z"/><path d="M21 13v16M13 21h16"/></svg>'


STAT_ICONS = {
    "years": "M7 3v3M17 3v3M4 9h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zM8 13h3M8 16h6",
    "works": "M21 12a9 9 0 1 1-9-9 9 9 0 0 1 9 9zM8 12.5l2.8 2.8L16.5 9.5",
    "per_month": "M3 20h18M5 16l5-5 4 3 6-7M15 7h5v5",
    "warranty": "M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6zM9 12l2 2 4-4",
}


def stats_html():
    """Цифры-преимущества: иконка + число, которое «набегает» (main.js) + подпись."""
    out = []
    for k, label in [("years", "лет опыта"), ("works", "выполненных работ"), ("per_month", "заказов в месяц"), ("warranty", "гарантия по договору")]:
        v = S[k]
        m = re.match(r"(\d+)(.*)", v)
        num = f'<span class="cnt" data-n="{m.group(1)}" style="min-width:{len(m.group(1))}ch">{m.group(1)}</span>{e(m.group(2))}' if m else e(v)
        out.append(f'<div><span class="st-ic">{ic(STAT_ICONS[k], 30, "currentColor", 1.6)}</span><b>{num}</b><span>{label}</span></div>')
    return "".join(out)


def works_block():
    """Наши работы: тёмная плашка, слева фото, справа список проектов; наведение меняет фото."""
    media = "".join(f'<img src="{img(p)}" alt="{e(t)}: {e(d)}" loading="lazy"{" class=on" if i == 0 else ""}>' for i, (t, d, p) in enumerate(PROJECTS))
    rows = "".join(f'<li><a href="/raboty/" data-i="{i}"{" class=on" if i == 0 else ""}><img class="wl-th" src="{img(p, True)}" alt="" loading="lazy">'
                   f'<span class="wl-n">{i + 1:02d}</span><span class="wl-t"><b>{e(t)}</b><span>{e(d)}</span></span><span class="wl-a">{ARR}</span></a></li>'
                   for i, (t, d, p) in enumerate(PROJECTS))
    return f'''<section id="works" class="wrap sec"><div class="works rv"><div class="works-media" aria-hidden="true">{media}</div>
<div class="works-r"><span class="eyebrow">Портфолио</span><h2 class="h2">Наши работы</h2><p class="works-lead">Выполненные проекты: какие решения выбрали заказчики, как организовали свет и что вошло в монтаж.</p>
<ol class="works-list">{rows}</ol><a class="btn" href="/raboty/">Смотреть все проекты {ARR}</a></div></div></section>'''


# Логотип-надпись «Центро+» (файл заказчика). Цвет — currentColor: белый на тёмном;
# на белой шапке CSS заливает его исходным градиентом #wmG (определён в шапке).
WORDMARK_D = "M393.41 109.44C393.09 108.26 393.23 6.37 393.55 6.05C393.98 5.62 406.02 5.62 406.45 6.05C406.66 6.26 406.75 7.81 406.75 11.43C406.75 17.47 406.69 17.40 409.37 14.56C410.37 13.50 411.67 12.29 412.24 11.88C412.82 11.46 413.59 10.89 413.96 10.59C414.53 10.14 415.20 9.74 417.93 8.28C418.51 7.96 422.13 6.67 423.62 6.24C427.77 5.05 435.58 4.56 439.88 5.23C444.19 5.90 449.71 7.51 451.34 8.58C451.69 8.81 452.14 9.00 452.33 9.00C452.53 9.00 452.97 9.22 453.32 9.50C453.67 9.78 454.07 10.00 454.21 10.00C454.35 10.00 454.61 10.14 454.79 10.31C454.98 10.49 455.63 10.95 456.25 11.35C460.21 13.90 464.02 17.95 467.19 22.98C467.51 23.47 467.82 24.04 467.90 24.25C467.97 24.46 468.16 24.85 468.31 25.12C468.46 25.40 468.66 25.79 468.75 26.00C468.84 26.21 469.07 26.66 469.25 27.00C469.77 27.96 471.00 31.56 471.01 32.12C471.02 32.40 471.19 33.08 471.39 33.62C472.62 36.97 472.67 49.82 471.48 53.58C471.21 54.40 471.00 55.30 471.00 55.60C471.00 55.89 470.84 56.43 470.65 56.80C470.45 57.16 470.22 57.84 470.12 58.30C469.89 59.39 469.03 61.46 468.46 62.29C468.21 62.65 468.00 63.08 468.00 63.24C468.00 63.60 465.23 67.74 463.90 69.38C462.30 71.34 459.08 74.42 457.62 75.39C456.89 75.87 456.16 76.43 455.99 76.63C455.83 76.84 455.56 77.00 455.41 77.01C455.25 77.01 454.84 77.23 454.50 77.50C454.16 77.77 453.71 77.99 453.50 78.00C453.29 78.01 452.84 78.23 452.50 78.50C452.16 78.77 451.71 78.99 451.50 79.00C451.29 79.01 450.84 79.23 450.50 79.50C450.16 79.77 449.68 79.99 449.44 79.99C449.20 80.00 448.58 80.22 448.07 80.50C447.55 80.78 446.87 81.00 446.56 81.00C446.24 81.00 445.57 81.17 445.07 81.38C442.30 82.54 432.51 83.12 428.25 82.38C423.54 81.56 421.63 80.96 418.12 79.22C414.39 77.37 412.48 75.99 409.69 73.15C408.49 71.92 407.44 70.97 407.37 71.05C407.29 71.12 407.24 79.64 407.25 89.97C407.25 100.30 407.19 109.03 407.10 109.38L406.95 110.00L400.25 110.00L393.56 110.00L393.41 109.44ZM68.74 99.24C68.26 98.76 68.24 98.45 68.26 90.62C68.27 86.15 68.21 82.38 68.12 82.25C68.02 82.09 56.10 82.00 33.99 82.00L0.00 82.00L0.00 43.88L0.00 5.75L6.72 5.75C12.05 5.75 13.50 5.82 13.72 6.09C13.92 6.33 14.02 15.21 14.06 38.15L14.12 69.88L34.45 69.94C48.15 69.98 54.94 69.92 55.26 69.74C55.74 69.49 55.75 68.87 55.81 37.68L55.88 5.88L62.50 5.88L69.12 5.88L69.19 37.61C69.23 59.25 69.34 69.44 69.51 69.61C69.67 69.77 72.04 69.92 75.57 70.00L81.38 70.12L81.44 84.54C81.50 97.40 81.46 99.00 81.11 99.36C80.43 100.04 69.44 99.94 68.74 99.24ZM134.13 82.24C132.34 81.97 130.45 81.59 129.93 81.38C129.41 81.17 128.74 81.00 128.43 81.00C128.13 81.00 127.59 80.85 127.23 80.66C126.88 80.48 126.26 80.25 125.86 80.15C125.46 80.06 124.79 79.82 124.38 79.63C123.96 79.44 122.81 78.92 121.81 78.48C120.82 78.04 120.00 77.59 120.00 77.49C120.00 77.38 119.69 77.17 119.31 77.02C116.62 75.94 110.57 70.61 108.34 67.35C106.87 65.20 105.00 62.23 105.00 62.04C105.00 61.95 104.79 61.42 104.53 60.88C103.52 58.75 103.00 57.47 103.00 57.12C103.00 56.92 102.79 56.10 102.53 55.31C100.69 49.63 100.57 40.07 102.26 33.00C102.79 30.77 103.32 29.08 103.64 28.57C103.84 28.27 104.00 27.87 104.00 27.69C104.00 27.50 104.22 26.91 104.50 26.37C104.78 25.84 105.00 25.32 105.00 25.22C105.00 25.02 107.04 21.64 107.62 20.88C110.82 16.66 113.18 14.20 115.54 12.63C116.14 12.23 116.85 11.71 117.12 11.47C117.40 11.24 118.30 10.69 119.12 10.25C119.95 9.81 120.73 9.35 120.86 9.23C120.99 9.10 121.25 9.00 121.43 9.00C121.62 9.00 122.07 8.80 122.44 8.56C123.73 7.71 128.38 6.22 131.88 5.54C134.83 4.96 142.71 4.79 145.38 5.25C148.36 5.77 150.51 6.24 150.93 6.45C151.17 6.57 151.90 6.81 152.55 6.97C153.86 7.28 158.60 9.53 160.00 10.49C160.21 10.63 160.93 11.11 161.61 11.55C164.27 13.29 168.27 17.33 169.88 19.90C170.29 20.56 170.81 21.39 171.03 21.74C173.50 25.66 175.46 30.69 176.16 34.88C176.34 35.98 176.60 37.44 176.73 38.12C177.10 40.05 177.07 47.31 176.69 47.83C176.40 48.22 174.19 48.26 145.75 48.31L115.12 48.38L115.04 49.36C114.97 50.32 115.61 52.82 116.50 55.00C116.75 55.62 117.02 56.29 117.10 56.50C117.59 57.81 120.09 61.24 121.67 62.78C123.47 64.52 126.74 67.00 127.25 67.01C127.46 67.01 127.91 67.23 128.25 67.50C128.59 67.77 128.99 67.99 129.12 67.99C129.26 68.00 129.82 68.21 130.38 68.48C135.57 70.96 144.90 71.40 151.48 69.47C152.36 69.21 153.26 69.00 153.48 68.99C153.70 68.99 154.16 68.77 154.50 68.50C154.84 68.23 155.29 68.01 155.50 68.00C155.71 67.99 156.16 67.77 156.50 67.50C156.84 67.23 157.29 67.01 157.50 67.00C157.71 67.00 158.55 66.49 159.37 65.87C160.19 65.26 160.92 64.75 161.00 64.75C161.07 64.75 161.84 64.07 162.71 63.25C163.59 62.42 164.40 61.75 164.52 61.75C164.64 61.75 165.31 62.45 166.03 63.31C166.74 64.17 167.40 64.93 167.51 65.00C167.87 65.24 172.00 70.30 172.00 70.50C172.00 70.61 171.06 71.59 169.91 72.68C167.28 75.17 164.73 76.95 161.75 78.39C160.99 78.76 160.15 79.17 159.88 79.32C158.53 80.02 156.68 80.66 154.73 81.10C153.96 81.28 153.20 81.50 153.04 81.60C151.43 82.60 139.33 83.00 134.13 82.24ZM528.98 82.64C528.91 82.57 527.61 82.34 526.11 82.12C524.61 81.91 523.15 81.62 522.88 81.49C522.60 81.36 521.86 81.15 521.23 81.01C520.61 80.88 519.76 80.60 519.36 80.39C518.96 80.18 518.47 80.00 518.28 80.00C517.97 80.00 517.45 79.79 515.25 78.77C514.21 78.28 513.13 77.68 513.00 77.51C512.93 77.42 512.31 77.03 511.62 76.64C510.94 76.25 510.21 75.77 510.00 75.59C509.79 75.41 508.75 74.57 507.68 73.73C505.06 71.67 500.00 65.82 500.00 64.86C500.00 64.70 499.83 64.42 499.63 64.25C499.43 64.09 499.11 63.65 498.93 63.29C498.74 62.92 498.48 62.40 498.33 62.12C494.86 55.42 493.19 44.92 494.53 38.12C494.66 37.44 494.88 36.04 495.01 35.03C495.14 34.01 495.35 33.06 495.47 32.90C495.59 32.75 495.81 32.12 495.96 31.50C496.33 29.93 497.07 27.93 497.58 27.16C497.81 26.81 498.00 26.37 498.01 26.20C498.01 26.02 498.23 25.59 498.50 25.25C498.77 24.91 498.99 24.48 498.99 24.29C499.00 24.11 499.70 22.93 500.54 21.67C503.48 17.32 509.44 11.94 513.62 9.88C514.04 9.68 514.54 9.41 514.75 9.29C519.25 6.68 525.41 5.22 532.62 5.07C537.63 4.96 539.38 5.08 542.88 5.76C550.15 7.19 557.90 11.32 562.96 16.46C564.34 17.86 567.58 22.09 568.02 23.07C568.16 23.38 568.60 24.19 569.01 24.88C569.42 25.56 569.82 26.29 569.90 26.50C569.97 26.71 570.24 27.38 570.49 28.00C571.55 30.61 571.75 31.25 572.34 33.62C573.55 38.58 573.77 45.71 572.88 51.12C572.36 54.31 570.83 59.52 570.24 60.11C570.11 60.24 570.00 60.52 569.99 60.74C569.99 60.95 569.77 61.41 569.50 61.75C569.23 62.09 569.01 62.52 569.01 62.70C569.00 63.07 566.34 67.10 565.02 68.74C562.23 72.20 555.05 78.00 553.56 78.00C553.43 78.00 553.12 78.22 552.88 78.50C552.63 78.78 552.21 79.00 551.95 79.00C551.69 79.00 551.06 79.22 550.55 79.48C549.25 80.17 547.10 81.00 546.65 81.00C546.44 81.00 545.74 81.18 545.09 81.40C542.89 82.15 539.18 82.58 534.12 82.68C531.36 82.73 529.05 82.72 528.98 82.64ZM207.30 81.70C206.84 81.24 206.86 6.42 207.33 6.04C207.73 5.71 220.46 5.61 220.78 5.93C220.90 6.05 221.03 13.29 221.06 22.01L221.12 37.88L242.49 37.94C254.23 37.97 263.94 37.91 264.06 37.79C264.18 37.67 264.26 30.57 264.26 22.01C264.24 10.67 264.32 6.35 264.53 6.09C264.91 5.63 277.48 5.58 277.95 6.05C278.39 6.49 278.39 81.26 277.95 81.70C277.56 82.09 265.45 82.13 264.73 81.74C264.25 81.48 264.24 81.11 264.26 65.95C264.26 57.41 264.18 50.33 264.06 50.21C263.94 50.09 254.23 50.03 242.49 50.06L221.12 50.12L221.00 66.00L220.88 81.88L214.24 81.94C209.29 81.99 207.53 81.93 207.30 81.70ZM329.17 81.83C329.07 81.74 329.00 67.41 329.00 49.99C329.00 23.34 328.95 18.27 328.65 18.02C328.40 17.82 324.64 17.74 314.90 17.76C307.53 17.77 301.38 17.71 301.25 17.62C300.93 17.43 300.91 6.08 301.23 5.89C301.70 5.59 370.06 5.74 370.41 6.03C370.83 6.38 370.90 16.49 370.49 17.27C370.24 17.74 369.82 17.75 356.79 17.75C346.67 17.75 343.28 17.82 343.05 18.05C342.82 18.28 342.75 25.72 342.75 50.02C342.75 78.67 342.71 81.71 342.35 81.85C341.81 82.06 329.37 82.04 329.17 81.83ZM437.50 70.25C444.27 69.08 450.25 65.44 453.46 60.52C453.96 59.75 454.44 59.07 454.52 59.00C454.98 58.60 456.72 54.66 457.36 52.56C459.11 46.81 458.69 37.08 456.49 32.62C456.22 32.08 456.00 31.55 456.00 31.46C456.00 30.33 451.79 24.69 449.71 23.03C447.33 21.14 445.67 20.00 445.29 20.00C445.08 20.00 444.74 19.84 444.52 19.64C444.05 19.22 442.39 18.58 440.50 18.10C439.74 17.91 438.79 17.63 438.38 17.48C437.96 17.33 435.82 17.15 433.62 17.07C427.41 16.86 423.17 18.03 418.00 21.39C416.45 22.39 412.00 26.72 412.00 27.22C412.00 27.36 411.84 27.63 411.64 27.83C411.12 28.34 409.56 31.24 408.95 32.80C406.31 39.58 406.58 50.24 409.54 56.03C409.79 56.53 410.00 57.11 410.00 57.31C410.00 57.51 410.23 57.88 410.50 58.12C410.77 58.37 411.00 58.72 411.00 58.90C411.00 59.92 415.42 64.53 418.39 66.61C421.11 68.51 425.02 69.88 429.75 70.59C431.47 70.85 434.93 70.70 437.50 70.25ZM538.60 70.35C539.85 70.13 541.47 69.74 542.19 69.48C545.29 68.35 546.40 67.87 546.88 67.48C547.15 67.25 547.94 66.74 548.62 66.35C552.40 64.18 556.95 57.98 558.04 53.55C558.19 52.90 558.42 52.25 558.54 52.10C558.86 51.68 559.50 46.17 559.50 43.75C559.50 39.47 558.72 35.14 557.46 32.35C557.21 31.78 557.00 31.14 557.00 30.92C557.00 30.71 556.90 30.47 556.77 30.39C556.65 30.31 556.19 29.60 555.75 28.81C554.47 26.53 552.14 23.88 550.19 22.50C549.53 22.04 549.00 21.58 549.00 21.47C549.00 21.37 548.76 21.21 548.47 21.12C548.19 21.03 547.57 20.69 547.10 20.37C545.93 19.58 542.69 18.25 540.88 17.83C533.38 16.06 526.63 17.01 520.00 20.77C519.00 21.34 516.73 23.23 515.36 24.65C513.97 26.07 511.00 30.26 510.99 30.79C510.99 30.98 510.77 31.41 510.50 31.75C510.23 32.09 510.01 32.58 510.01 32.82C510.00 33.07 509.85 33.58 509.66 33.95C507.74 37.72 507.67 48.22 509.53 53.13C509.79 53.82 510.00 54.55 510.00 54.76C510.00 54.97 510.15 55.36 510.34 55.63C510.53 55.90 510.76 56.38 510.86 56.70C511.23 57.88 515.72 64.00 516.22 64.00C516.31 64.00 516.91 64.49 517.56 65.10C518.21 65.70 519.25 66.45 519.87 66.75C520.49 67.05 521.06 67.39 521.13 67.51C521.53 68.16 526.44 69.86 528.99 70.24C530.01 70.40 530.91 70.57 530.97 70.64C531.24 70.91 536.53 70.71 538.60 70.35ZM626.17 62.84C626.08 62.74 626.00 57.01 626.00 50.10C626.00 42.08 625.91 37.47 625.75 37.38C625.62 37.29 619.84 37.23 612.91 37.24C602.40 37.26 600.27 37.20 600.03 36.91C599.82 36.66 599.76 35.03 599.81 31.34L599.88 26.12L612.88 26.00L625.88 25.88L625.94 12.94L626.00 0.00L632.00 0.00L638.00 0.00L638.00 12.70C638.00 22.24 638.07 25.47 638.30 25.70C638.53 25.93 641.72 26.00 651.16 26.00C659.69 26.00 663.77 26.08 663.88 26.26C664.22 26.82 664.06 36.81 663.71 37.03C663.52 37.15 657.78 37.24 650.95 37.25C641.29 37.25 638.48 37.32 638.33 37.56C638.22 37.73 638.07 43.50 638.00 50.38L637.88 62.88L632.11 62.94C628.94 62.98 626.27 62.93 626.17 62.84ZM163.58 37.96C164.03 37.25 162.49 31.46 161.46 29.96C161.21 29.60 161.00 29.18 161.00 29.04C161.00 28.64 158.63 25.22 157.58 24.11C156.40 22.85 153.39 20.45 152.38 19.96C151.96 19.76 151.40 19.48 151.12 19.34C150.85 19.20 150.24 18.89 149.77 18.66C146.56 17.04 141.89 16.37 136.62 16.78C133.15 17.05 128.60 18.35 127.12 19.49C126.66 19.85 126.15 20.16 124.88 20.87C122.52 22.17 119.18 26.05 117.30 29.65C115.75 32.64 114.51 37.68 115.17 38.33C115.26 38.43 126.13 38.47 139.33 38.44C161.38 38.38 163.34 38.34 163.58 37.96Z"


def wordmark(grad=False):
    defs = ('<defs><linearGradient id="wmG" x1="0" y1="55" x2="665" y2="55" gradientUnits="userSpaceOnUse">'
            '<stop/><stop offset=".456" stop-color="#414141"/><stop offset="1" stop-color="#4D4D4D"/></linearGradient></defs>') if grad else ""
    return (f'<b class="wm"><svg viewBox="0 0 665 110" role="img" aria-label="{e(S["name"])}">{defs}'
            f'<path fill="currentColor" fill-rule="evenodd" d="{WORDMARK_D}"/></svg></b>')


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
<a class="logo" href="/">{LOGO_SVG}<span>{wordmark(True)}<small>натяжные потолки</small></span></a>
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
<div><a class="logo" href="/">{LOGO_SVG}<span>{wordmark()}<small>натяжные потолки</small></span></a><p style="color:#BFB3A8;max-width:260px">Натяжные потолки и освещение в Москве и Московской области</p></div>
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
<svg class="calc-arc" aria-hidden="true"><path class="sh"/><path class="gl"/><path class="ln"/></svg>
<div class="calc-l"><span class="eyebrow">{eyebrow}</span><h2 class="h2" style="max-width:520px">{title}</h2>
<p>Укажите площадь, полотно и профиль. После замера смета фиксируется в договоре и не меняется.</p>
<div style="display:flex;flex-wrap:wrap;align-items:center;gap:22px;margin-top:6px"><a href="#" data-cb class="btn">Получить точную смету {ARR}</a>
<span class="calc-sum"><small>Ориентировочно</small><b>—</b></span></div></div>
<div class="calc-f"><div><label for="c-area-{canvas}">Площадь помещения <b class="area-out">18 м²</b></label><input id="c-area-{canvas}" type="range" name="area" min="4" max="120" step="1" value="18"></div>
<div><span class="lbl">Тип полотна</span><div class="chips" style="margin-top:10px">{chips}</div></div>
<div class="row2"><div><label for="c-prof-{canvas}">Профиль</label><select id="c-prof-{canvas}" name="profile" style="margin-top:8px">{opts}</select></div>
<div><span class="lbl">Светильники, шт</span><div class="num" data-k="lamps" style="margin-top:8px"><button type="button" data-d="-1" aria-label="Меньше">−</button><output>4</output><button type="button" data-d="1" aria-label="Больше">+</button></div></div></div>
<p class="calc-note"></p><p class="calc-from">от 25 000 ₽</p></div></div></section>'''


def catalog_cards(types):
    return "".join(f'<a class="ccard" href="/katalog/{t["slug"]}/"><img src="{img(t["photos"][0], True)}" alt="{e(t["name"])}" loading="lazy">'
                   f'<div><b>{e(t["short"])} {ARR}</b><span>{e(t["card"])}</span></div></a>' for t in types)


GEO_SHAPES = json.load(open(os.path.join(ROOT, "geo_shapes.json"), encoding="utf-8"))
PIN_IC = "M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11zM12 12.3a2.3 2.3 0 1 0 0-4.6 2.3 2.3 0 0 0 0 4.6z"
CAR_IC = "M5 16h14M6.5 16v2.5M17.5 16v2.5M4 16v-3.5l2-5h12l2 5V16M4 12.5h16M7.5 13.8h.01M16.5 13.8h.01"
CLOCK_IC = "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM12 7.5V12l3 2"


def geo_svg():
    """Карта: реальные границы области и Москвы (OSM), город-хаб и все города; подсказка — в main.js."""
    W, PAD, cs = 800, 16, 0.563
    xs = [x for x, y in GEO_SHAPES["mo"]]
    ys = [y for x, y in GEO_SHAPES["mo"]]
    lon0, lat1 = min(xs), max(ys)
    k = (W - 2 * PAD) / ((max(xs) - lon0) * cs)
    H = round((lat1 - min(ys)) * k + 2 * PAD)
    P = lambda lo, la: ((lo - lon0) * cs * k + PAD, (lat1 - la) * k + PAD)
    d = lambda ring: "M" + "L".join("%.1f %.1f" % P(lo, la) for lo, la in ring) + "Z"
    mo = d(GEO_SHAPES["mo"])
    msk = "".join(d(r) for r in GEO_SHAPES["moscow"])
    cx, cy = P(37.62, 55.75)
    HUB_R = 27
    lines, pts = "", ""
    for i, (lo, la, n, big) in enumerate(c for c in GEO if c[2] != "Москва"):
        x, y = P(lo, la)
        if ((x - cx) ** 2 + (y - cy) ** 2) ** .5 < HUB_R + 7:
            continue  # under the Moscow badge: covered by Moscow itself
        if big:
            # мягкая дуга от Москвы к крупному городу
            mx, my = (cx + x) / 2, (cy + y) / 2
            dx, dy = x - cx, y - cy
            qx, qy = mx - dy * 0.18, my + dx * 0.18
            lines += f'<path class="ln" pathLength="1" data-i="{i}" d="M{cx:.1f} {cy:.1f}Q{qx:.1f} {qy:.1f} {x:.1f} {y:.1f}"/>'
        r = 4.2 if big else 3
        west = x < cx - 4
        lbl = (f'<text x="{x - 9 if west else x + 9:.1f}" y="{y - 7:.1f}"{" text-anchor=end" if west else ""}>{e(n)}</text>') if big else ""
        pts += (f'<g class="ct{" big" if big else ""}" data-i="{i}" data-n="{e(n)}" tabindex="0" role="button" aria-label="{e(n)}: выезд на замер бесплатно">'
                f'<circle class="h" cx="{x:.1f}" cy="{y:.1f}" r="{r * 3.2:.1f}"/><circle class="c" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>{lbl}</g>')
    hub = (f'<g class="hub"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="120" fill="url(#gHub)"/>'
           f'<circle class="ring r2" cx="{cx:.1f}" cy="{cy:.1f}" r="74"/><circle class="ring r1" cx="{cx:.1f}" cy="{cy:.1f}" r="46"/>'
           f'<circle class="core" cx="{cx:.1f}" cy="{cy:.1f}" r="{HUB_R}"/><text x="{cx:.1f}" y="{cy + 4.5:.1f}" text-anchor="middle">Москва</text></g>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Карта: Москва и Московская область, города, где мы работаем">'
            f'<defs><radialGradient id="gHub"><stop offset="0" stop-color="#FFB948" stop-opacity=".38"/><stop offset=".55" stop-color="#F3D3B4" stop-opacity=".10"/><stop offset="1" stop-color="#F3D3B4" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="gPt"><stop offset="0" stop-color="#FFC56A" stop-opacity=".55"/><stop offset="1" stop-color="#FFC56A" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="gLn" x1="0" x2="1"><stop offset="0" stop-color="#FFB948" stop-opacity=".7"/><stop offset="1" stop-color="#F3D3B4" stop-opacity=".25"/></linearGradient></defs>'
            f'<path class="mo-glow" d="{mo}"/><path class="mo" d="{mo}"/><path class="msk" d="{msk}"/>'
            f'<g class="lns">{lines}</g>{hub}<g class="cts">{pts}</g></svg>')


def geo_block():
    m = re.match(r"(\d+)(.*)", GEO_CITIES)
    return f'''<section id="geo" class="wrap sec"><div class="geo">
<div class="geo-l"><span class="eyebrow">География работ</span>
<h2 class="h2">Устанавливаем потолки по всей <em>Москве и Подмосковью</em></h2>
<p>Выезжаем на замер, помогаем подобрать решение и выполняем монтаж в Москве и городах Московской области.</p>
<div class="geo-nums"><div><span class="gi">{ic(PIN_IC, 22, "currentColor", 1.6)}</span><span><b><span class="cnt" data-n="{m.group(1)}" style="min-width:{len(m.group(1))}ch">{m.group(1)}</span>{e(m.group(2))}</b><small>городов обслуживания</small></span></div>
<div><span class="gi">{ic(CAR_IC, 22, "currentColor", 1.6)}</span><span><b>0 ₽</b><small>выезд на замер</small></span></div></div>
<a href="#" data-cb class="btn">Проверить возможность замера {ARR}</a></div>
<div class="geo-map">{geo_svg()}<div class="geo-tip" role="status" aria-live="polite"><b></b><span>{ic(CAR_IC, 16, "currentColor", 1.6)}Выезд на замер — 0 ₽</span><span>{ic(CLOCK_IC, 16, "currentColor", 1.6)}Монтаж от 1 дня</span></div></div>
</div></section>'''

def faq_block():
    items = "".join(f'<details><summary>{e(q)}<i aria-hidden="true">{CHEV}</i></summary><p>{e(a)}</p></details>' for q, a in FAQ)
    left, right = items.split("</details>")[:-1][0::2], items.split("</details>")[:-1][1::2]
    col = lambda l: '<div style="display:flex;flex-direction:column;gap:12px">' + "".join(x + "</details>" for x in l) + "</div>"
    return f'''<section id="faq" class="wrap sec"><span class="eyebrow">FAQ</span><h2 class="h2" style="margin-top:12px">Вопросы, которые задают нам чаще всего</h2>
<div class="faq">{col(left)}{col(right)}</div></section>'''


def articles_block(title="Полезные статьи", items=None):
    items = ARTICLES[:4] if items is None else items
    cards = "".join(f'<a class="art" href="/stati/{a["slug"]}/"><img src="{img(a["img"], True)}" alt="" loading="lazy"><div><b>{e(a["title"])}</b><p>{e(a["sub"])}</p><span>Читать статью →</span></div></a>' for a in items)
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
    slides = "".join(f'<img {"src" if i == 0 else "data-src"}="{img(n)}" alt="Натяжной потолок с подсветкой" {"fetchpriority=high" if i == 0 else ""}{" class=on" if i == 0 else ""}>' for i, n in enumerate(HERO))
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
    stats = stats_html()
    steps = "".join(f'<li><span class="n">{i + 1:02d}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, (t, d) in enumerate(STEPS))
    mq = "".join(f'<img src="{img(n, True)}" alt="" loading="lazy">' for n in MARQUEE)
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
<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between;margin-bottom:28px"><div><span class="eyebrow">Преимущества</span><h2 class="h2" style="margin-top:12px">Почему выбирают {S["name"]}</h2></div><p class="lead" style="max-width:480px">Работаем по Москве и области с 2010 года. Делаем аккуратно, по договору и с понятной сметой.</p></div>
<div class="why-grid">{"".join(cells)}</div><div class="stats">{stats}</div></section>
{geo_block()}
{works_block()}
<section class="wrap sec"><div class="about rv"><img src="{img("about")}" alt="" loading="lazy"><div class="about-in"><div class="about-top"><div style="display:flex;flex-direction:column;gap:12px"><span class="eyebrow" style="color:var(--accent)">О компании</span><h2 class="h2" style="max-width:640px">{S["name"]} — натяжные потолки под ключ с {S["years"]} лет опыта</h2></div>
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
    body += f'<section class="wrap sec"><div class="g4">{catalog_cards(TYPES)}</div></section>' + calc_block() + faq_block() + articles_block() + cta_block()
    page("/katalog/", f"Каталог натяжных потолков — {S['name']}", "Все виды натяжных потолков: матовые, глянцевые, сатиновые, тканевые, с подсветкой, теневые, парящие, бесщелевые и световые линии.", body)


def type_page(t):
    cv = [c for c in CANVASES if t["canvas"] in c["t"]]
    cards = "".join(f'<div class="pcard">{"<span class=tag>" + c["tag"] + "</span>" if c["tag"] else ""}<b>{c["n"]}</b><span class="pr">{c["p"]} <small>₽/м²</small></span>'
                    f'<dl><dt>Производитель</dt><dd>{c["c"]}</dd><dt>Толщина</dt><dd>{c["th"]}</dd><dt>Ширина</dt><dd>{c["w"]}</dd><dt>Гарантия</dt><dd>{c["g"]}</dd></dl></div>' for c in cv)
    advs = "".join(f'<div class="rv"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in t["adv"])
    gal = "".join(f'<a href="{img(p)}"><img src="{img(p, True)}" alt="{e(t["name"])} — фото объекта" loading="lazy"></a>' for p in t["photos"])
    pts = "".join(f"<li>{e(x)}</li>" for x in t["points"])
    others = [o for o in TYPES if o["slug"] != t["slug"]][:4]
    body = f'''<section class="phero"><img class="bg" src="{img(t.get("hero", t["photos"][0]))}" alt=""><div class="wrap"><nav class="crumbs"><a href="/">Главная</a> / <a href="/katalog/">Каталог</a> / {e(t["short"])}</nav>
<h1 class="h1" style="font-size:clamp(34px,4.4vw,54px)">{e(t["name"])}</h1><p>{e(t["intro"])}</p><ul class="feat-list">{pts}</ul>
<div class="hero-btns"><a href="#" data-cb class="btn">Заказать {ARR}</a><a href="#calc" class="btn btn-ghost">Рассчитать стоимость</a></div></div></section>
{calc_block(t["canvas"], "Рассчитайте стоимость", e(t["short"]))}
<section class="wrap sec"><h2 class="h2">Натяжные потолки: цена за 1 м²</h2><p class="lead" style="margin-top:10px">Используем только сертифицированные полотна, разрешённые для жилых помещений.</p>{"<div class=price-g>" + cards + "</div>" if cards else ""}</section>
<section class="wrap sec"><h2 class="h2">Преимущества: {e(t["short"].lower())}</h2><div class="advs">{advs}</div></section>
<section class="wrap sec"><h2 class="h2">Фото наших объектов</h2><div class="gallery">{gal}</div></section>
<section class="wrap sec"><h2 class="h2">Другие решения</h2><div class="g4" style="margin-top:28px">{catalog_cards(others)}</div></section>
{faq_block()}
{articles_block()}
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
    allp = WORKS_NEW + sorted(({p for t in TYPES for p in t["photos"]} | set(MARQUEE) | set(WORKS_EXTRA)) - set(WORKS_NEW))
    gal = "".join(f'<a href="{img(p)}"><img src="{img(p, True)}" alt="Наш объект" loading="lazy"></a>' for p in allp)
    body = phero("Наши работы", "Фотографии объектов, которые мы сделали в Москве и области: квартиры, дома, санузлы и коммерческие помещения.", "4638", [("Главная", "/"), ("Наши работы", "")])
    body += f'<section class="wrap sec"><h2 class="h2">Фотогалерея объектов</h2><div class="gallery">{gal}</div></section>'
    body += f'<section class="wrap sec"><div style="display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end;justify-content:space-between"><h2 class="h2">Установим любой вид натяжного потолка</h2><p class="lead" style="max-width:460px">Расскажем об особенностях каждого варианта, чтобы вы сделали свой выбор.</p></div><div class="tabs" role="tablist" aria-label="Виды потолков">{tabs}</div>{panels}</section>'
    body += faq_block() + articles_block() + cta_block()
    page("/raboty/", f"Наши работы — фото натяжных потолков | {S['name']}", "Фото выполненных работ: теневые, парящие, матовые потолки, световые линии и подсветка в Москве и области.", body)


def promos():
    cards = "".join(f'<div class="promo {c} rv"><span class="big">{b}</span><b>{e(t)}</b><p>{e(d)}</p><a href="#" data-cb class="btn">Хочу также</a></div>' for b, t, d, c in PROMOS)
    body = phero("Акции", "Лучшие спецпредложения — установите натяжные потолки с выгодой.", "4589", [("Главная", "/"), ("Акции", "")])
    body += f'<section class="wrap sec"><div class="promos">{cards}</div><p class="lead" style="margin-top:20px;font-size:14px">Условия акций уточняйте у менеджера. Акции не суммируются, если не указано иное.</p></section>' + calc_block() + faq_block() + articles_block() + cta_block()
    page("/akcii/", f"Акции на натяжные потолки — {S['name']}", "Скидки новосёлам и пенсионерам, светильники в подарок, рассрочка 0%, скидка в день замера.", body)


def about():
    stats = stats_html()
    advs = "".join(f'<div class="rv"><b>{t}</b><p>{d}</p></div>' for t, d, p in WHY[:4])
    body = phero(f"О компании {S['name']}", "Натяжные потолки под ключ в Москве и Московской области. Уют. Качество. Надёжность.", "4608", [("Главная", "/"), ("О компании", "")])
    body += f'''<section class="wrap sec split"><div class="split-t" style="max-width:520px;flex-basis:420px"><h2 class="h2">Делаем потолки, которые создают атмосферу</h2>
<p class="lead">Мы занимаемся натяжными потолками больше {S["years"].rstrip("+")} лет. За это время сделали более {S["works"].rstrip("+")} объектов — от небольших санузлов до загородных домов со сложными световыми сценариями.</p>
<p class="lead">Начинаем с бесплатной консультации и замера, подбираем полотно, профиль и освещение, фиксируем смету в договоре. Монтируем чисто — с пылесборником — и сдаём работу с гарантией.</p>
<p class="lead">Работаем только с сертифицированными материалами от проверенных производителей.</p></div>
<div class="split-c" style="display:grid;grid-template-columns:1fr 1fr;gap:14px"><img src="{img("4576")}" alt="" style="border-radius:16px;aspect-ratio:3/4;object-fit:cover;width:100%"><img src="{img("4661")}" alt="" style="border-radius:16px;aspect-ratio:3/4;object-fit:cover;width:100%;margin-top:40px"></div></section>
<section class="wrap sec"><div class="stats" style="border:0;margin:0">{stats}</div></section>
<section class="wrap sec"><h2 class="h2">Наши принципы</h2><div class="advs">{advs}</div></section>'''
    body += contacts_block() + faq_block() + articles_block() + cta_block()
    page("/o-kompanii/", f"О компании — {S['name']}", f"{S['name']}: натяжные потолки в Москве и области, {S['years']} лет опыта, {S['works']} выполненных работ, гарантия {S['warranty']}.", body)


def contacts():
    body = phero("Контакты", f"{S['address']}. {S['hours_calls']}.", "4628", [("Главная", "/"), ("Контакты", "")]) + contacts_block() + faq_block() + articles_block() + cta_block()
    page("/kontakty/", f"Контакты — {S['name']}", f"Телефон {S['phone']}, адрес: {S['address']}. WhatsApp и Telegram.", body)


def articles():
    body = phero("Статьи", "Полезное о натяжных потолках: как выбрать, что учесть при ремонте и что делать в непредвиденных ситуациях.", "4620", [("Главная", "/"), ("Статьи", "")])
    cards = "".join(f'<a class="art" href="/stati/{a["slug"]}/"><img src="{img(a["img"], True)}" alt="" loading="lazy"><div><b>{e(a["title"])}</b><p>{e(a["sub"])}</p><span>Читать статью →</span></div></a>' for a in ARTICLES)
    body += f'<section class="wrap sec"><div class="arts" style="margin:0">{cards}</div></section>' + faq_block() + cta_block()
    page("/stati/", f"Статьи о натяжных потолках — {S['name']}", "Полезные статьи о натяжных потолках.", body)
    for n, a in enumerate(ARTICLES):
        parts = ""
        for kind, val in a["body"]:
            if kind == "ul":
                parts += "<ul>" + "".join(f"<li>{e(x)}</li>" for x in val) + "</ul>"
            elif kind == "img":
                ph, alt = a["photos"][val]
                parts += f'<img src="{img(ph)}" alt="{e(alt)}" loading="lazy" width="1200" height="800">'
            else:
                parts += f"<{kind}>{e(val)}</{kind}>"
        if a.get("faq"):
            parts += '<h2>Частые вопросы</h2><div class="afaq">' + "".join(f'<details><summary>{e(q)}<i aria-hidden="true">{CHEV}</i></summary><p>{e(t)}</p></details>' for q, t in a["faq"]) + "</div>"
        if a.get("cta"):
            lk = f'<a class="link-arrow" href="{a["link"][1]}">{e(a["link"][0])} {ARR}</a>' if a.get("link") else ""
            parts += f'<div class="acta"><h2>{e(a["cta"][0])}</h2><p>{e(a["cta"][1])}</p><div class="acta-r"><a class="btn" href="#" data-cb>Получить консультацию {ARR}</a>{lk}</div></div>'
        else:
            parts += f'<p><a class="btn" href="#" data-cb>Задать вопрос мастеру {ARR}</a></p>'
        b = phero(e(a["title"]), e(a["sub"]), a["img"], [("Главная", "/"), ("Статьи", "/stati/"), (a["title"], "")])
        b += f'<section class="wrap sec"><article class="prose">{parts}</article></section>'
        others = [ARTICLES[(n + k) % len(ARTICLES)] for k in range(1, 4)]
        b += articles_block("Другие статьи", others) + cta_block()
        page(f"/stati/{a['slug']}/", a.get("meta_title") or f"{a['title']} — {S['name']}", a["sub"], b)


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
