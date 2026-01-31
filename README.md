# RaceBuff

**RaceBuff** — свободный оверлей телеметрии для гоночных симуляторов с **полной поддержкой iRacing** и поддержкой rFactor 2 / Le Mans Ultimate.

---

## Возможности

- **Полная поддержка iRacing** — все виджеты работают без плагинов: Relative, Standings, Timing, Tyres, Brake, Fuel, Session, Weather, Radar, Delta Best и др.
- **Русский и английский** — переключение языка в настройках.
- **rFactor 2 и Le Mans Ultimate** — через плагин Shared Memory или встроенный API (LMU).
- **Гибкая настройка** — позиции виджетов, темы, сохранение раскладок в JSON.

---

## Быстрый старт

1. Скачайте [последний релиз](https://github.com/froseeee/Racebuff/releases) или клонируйте репозиторий.
2. Запустите приложение из папки **racebuff** (см. ниже).
3. В настройках выберите **API телеметрии → iRacing** (или LMU / rFactor 2).
4. Запустите симулятор; оверлей появится на треке.

Подробная инструкция — в [racebuff/README.md](racebuff/README.md).

---

## Структура репозитория

| Папка | Описание |
|-------|----------|
| **racebuff/** | Основное приложение RaceBuff (Python): оверлей, виджеты, адаптеры iRacing / LMU / rF2. |
| **src/** | Дополнительный нативный оверлей (C++/DirectX) — опционально. |

**Рекомендуемый способ использования:** запуск из **racebuff** (`python run.py` или собранный `racebuff.exe`).

---

## Поддерживаемые симуляторы

| Симулятор | Требования | Windows | Linux |
|-----------|------------|:-------:|:-----:|
| **iRacing** | Плагин не нужен | Да | Нет |
| **Le Mans Ultimate (LMU)** | Плагин не нужен (встроенный API) или rF2 Shared Memory Map | Да | Да (с плагином) |
| **rFactor 2** | Плагин rF2 Shared Memory Map | Да | Да |

- **iRacing** — полная поддержка через официальный SDK (`pyirsdk`). В настройках: **API телеметрии → iRacing**.
- **Le Mans Ultimate** — встроенная поддержка без плагина (Windows) или через плагин rF2 Shared Memory (Windows/Linux). В настройках: **API телеметрии → Le Mans Ultimate**.
- **rFactor 2** — через плагин [rF2 Shared Memory Map](https://github.com/TinyPedal/TinyPedal/wiki). В настройках: **API телеметрии → rFactor 2**.

Режим отображения игры: **Borderless** или **Windowed** (Fullscreen не поддерживается).

---

## iRacing — что поддерживается

- **Relative / Standings** — позиции, гэпы, классы, пит-лейн, порядок отрисовки.
- **Timing** — текущий/последний/лучший круг, оценка круга, время до лидера.
- **Session** — тип сессии, флаги (green/yellow/blue), пит-открыт, температура трека и воздуха.
- **Lap** — прогресс круга, дистанция, длина трека, круги до лидера/до впереди идущего.
- **Vehicle** — топливо, бак, пит-стопы, имена пилотов/машин, классы, позиции.
- **Tyre** — температура (поверхность/внутренняя/каркас), износ.
- **Brake** — баланс, давление и температура по колёсам.
- **Engine / Inputs / Wheel** — передачи, RPM, педали, руль, углы скольжения.
- **Switch** — фары, зажигание, ограничитель скорости.

Данные берутся из официального iRacing SDK через `pyirsdk`; многоместо поддерживается (CarIdx*).

---

## Требования

- **Windows** — для iRacing и LMU без плагина. rFactor 2 и LMU (legacy) с плагином — также **Linux**.
- Режим отображения игры: **Borderless** или **Windowed** (не Fullscreen).
- Для iRacing: `pip install pyirsdk` (уже в `requirements.txt` в racebuff).
- Для rFactor 2 / LMU (с плагином): установите [rF2 Shared Memory Map Plugin](https://github.com/TinyPedal/TinyPedal/wiki); подмодули pyRfactor2SharedMemory и pyLMUSharedMemory включены в репозиторий.

---

## Лицензия и благодарности

- **RaceBuff** распространяется под [GNU GPL v3+](LICENSE).
- Оверлей основан на [TinyPedal](https://github.com/TinyPedal/TinyPedal); благодарности оригинальным авторам — в [racebuff/README.md](racebuff/README.md).

---

**Репозиторий:** [github.com/froseeee/Racebuff](https://github.com/froseeee/Racebuff)
