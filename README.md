# centro-plus.ru

Статический сайт «Центр Плюс — натяжные потолки».

- `data.py` — все данные: контакты, цены (пока черновые), тексты, акции, FAQ, статьи.
- `src/` — стили, скрипты, фото. `build.py` собирает сайт в `dist/`.
- Пуш в `main` → Timeweb App Platform (Москва) сам собирает сайт (`python3 build.py`)
  и выкладывает `dist/`. GitHub Actions только проверяет, что сборка проходит.
- Настройки приложения App Platform — репозиторий `Ad-Reach/infra` (Terraform).

Локально: `python3 build.py && python3 -m http.server -d dist`.
