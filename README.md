# centro-plus.ru

Статический сайт «Центр Плюс — натяжные потолки».

- `data.py` — все данные: контакты, цены (пока черновые), тексты, акции, FAQ, статьи.
- `src/` — стили, скрипты, фото. `build.py` собирает сайт в `dist/`.
- Пуш в `main` → GitHub Actions собирает сайт и публикует `dist/` в ветку `site`
  → Timeweb App Platform (Амстердам) автоматически выкладывает её.
- Настройки приложения App Platform — репозиторий `Ad-Reach/infra` (Terraform).

Локально: `python3 build.py && python3 -m http.server -d dist`.
