# centro-plus.ru

Статический сайт «Центр Плюс — натяжные потолки».

- `data.py` — все данные: контакты, цены (пока черновые), тексты, акции, FAQ, статьи.
- `src/` — стили, скрипты, фото. `build.py` собирает сайт в `dist/`.
- Пуш в `main` → GitHub Actions собирает сайт и выкладывает в `/var/www/centro-plus` на VDS.
  Секреты: `VDS_HOST`, `VDS_USER`, `VDS_PASSWORD`.
- Блок для Caddy: `deploy/Caddyfile.snippet`.

Локально: `python3 build.py && python3 -m http.server -d dist`.
