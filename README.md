# centro-plus.ru

Статический сайт «Центр Плюс — натяжные потолки».

- `data.py` — все данные: контакты, цены (пока черновые), тексты, акции, FAQ, статьи.
- `src/` — стили, скрипты, фото. `build.py` собирает сайт в `dist/`.
- Пуш в `main` → GitHub Actions собирает сайт и выкладывает релиз в `/srv/centro-plus/releases/<sha>`
  на VDS (31.77.10.198) под пользователем `deploy`, затем переключает симлинк `/srv/centro-plus/current`.
  Секрет: `DEPLOY_SSH_KEY` (приватный ключ пользователя deploy). Отпечатки сервера — `deploy/known_hosts`.
- Блок для Caddy: `deploy/Caddyfile.snippet`.

Локально: `python3 build.py && python3 -m http.server -d dist`.
