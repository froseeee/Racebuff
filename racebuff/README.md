# RaceBuff — racing simulation overlay

**RaceBuff** is a Free and Open Source telemetry overlay application for racing simulation.

---

## Fork — оригинал / Original

**RaceBuff — это форк проекта TinyPedal.**  
**RaceBuff is a fork of TinyPedal.**

| | |
|---|--|
| **Оригинал / Original** | **[TinyPedal](https://github.com/TinyPedal/TinyPedal)** — [github.com/TinyPedal/TinyPedal](https://github.com/TinyPedal/TinyPedal) |
| **Автор оригинала / Original author** | **Xiang (S.Victor)** — основатель проекта, основная разработка, иконки TinyPedal / project founder, core development, TinyPedal icons |
| **Релизы оригинала** | [TinyPedal Releases](https://github.com/TinyPedal/TinyPedal/releases) |
| **Руководство пользователя** | [TinyPedal Wiki — User Guide](https://github.com/TinyPedal/TinyPedal/wiki/User-Guide) |
| **FAQ** | [TinyPedal Wiki — FAQ](https://github.com/TinyPedal/TinyPedal/wiki/Frequently-Asked-Questions) |

Все заслуги и ссылки принадлежат оригинальному проекту; рекомендуем поддерживать [TinyPedal](https://github.com/TinyPedal/TinyPedal).  
All credits and links belong to the original project; we encourage supporting [TinyPedal](https://github.com/TinyPedal/TinyPedal).

---

## What this fork adds / Что добавлено в форке

- **Full iRacing support** — all widgets work with iRacing: Relative, Standings, Timing, Tyres, Brake, Fuel, Session, Weather, Radar, Delta Best, etc. No plugin required. Choose iRacing in Config → Application → Telemetry API.  
  **Полная поддержка iRacing** — все виджеты работают с iRacing: Relative, Standings, Timing, шины, тормоза, топливо, сессия, погода, радар, Delta Best и др. Плагин не нужен. Выберите iRacing в Настройки → Приложение → API телеметрии.
- **Russian language** — Config → Application → Language → Русский. Menu, dialogs and About in Russian.  
  **Русский язык** — Настройки → Приложение → Язык → Русский. Меню, диалоги и «О программе» на русском.
- **Renamed app** to RaceBuff; About window credits original TinyPedal and this fork.  
  **Переименование** в RaceBuff; в окне «О программе» указаны оригинал TinyPedal и этот форк.
- No update checks against the original repository (you manage updates yourself).  
  Проверка обновлений оригинального репозитория отключена (обновления — на ваше усмотрение).

Otherwise RaceBuff follows TinyPedal: minimalist overlay, many widgets, rFactor 2 and Le Mans Ultimate support, Windows and Linux.

---

# English

## Requirements

| Supported API        | Requirement | Windows | Linux |
|----------------------|-------------|:-------:|:-----:|
| **iRacing**          | No plugin   | Yes     | No    |
| Le Mans Ultimate     | No plugin   | Yes     | No    |
| Le Mans Ultimate (legacy) | rF2 Shared Memory Map Plugin | Yes | Yes |
| rFactor 2            | rF2 Shared Memory Map Plugin | Yes | Yes |

- Game display: **Borderless** or **Windowed** (Fullscreen not supported).
- Do **not** install RaceBuff inside `Program Files` or the game folder.

Setup for rFactor 2 / Le Mans Ultimate (legacy) and plugin links: see [TinyPedal Wiki](https://github.com/TinyPedal/TinyPedal/wiki).

## Quick Start

1. Get the latest build from [Releases](https://github.com/froseeee/Racebuff/releases) (or build from source), extract to a folder, run `racebuff.exe` (or `python run.py`).
2. A tray icon appears. Right‑click for menu.
3. Start your sim; overlay shows when on track (auto‑hide when not). Toggle **Auto Hide** from the tray menu.
4. Use **Lock Overlay** to fix position; when unlocked, drag the overlay.
5. Enable/disable widgets in the main window. Open **Config** from the tray to change settings.
6. **Quit** from the tray or Overlay menu to exit.

**Language:** Config → Application → **Language** → English / Русский / system.

**iRacing:** Config → Application → **Telemetry API** → iRacing.

### iRacing — supported data

Relative/Standings (positions, gaps, classes), Timing (lap times, delta, time behind leader), Session (flags, track/air temp, pit open), Lap (progress, distance, laps behind), Vehicle (fuel, pit stops, driver/car names), Tyre (temps, wear), Brake (bias, pressure, temp), Engine/Inputs/Wheel (gear, RPM, pedals, slip angles), Switch (headlights, ignition). Data from official iRacing SDK via `pyirsdk`; multi-car (CarIdx*) supported.

## Run from source

### Dependencies

- Python 3.8–3.11
- PySide2 or PySide6 (`pip install PySide2` or `pip install PySide6`)
- psutil, pyLMUSharedMemory, pyRfactor2SharedMemory (see `requirements.txt`)
- For iRacing: `pyirsdk` (`pip install pyirsdk`)

From the project root:

```bash
pip install -r requirements.txt
python run.py
```

For PySide6:

```bash
python run.py --pyside 6
```

### Clone (with submodules)

```bash
git clone --recursive https://github.com/froseeee/Racebuff.git
cd Racebuff
git submodule update --init
```

## Build executable (Windows)

```bash
pip install py2exe
python freeze_py2exe.py
```

Output: `dist/RaceBuff/racebuff.exe` (and required folders). Run from inside `dist/RaceBuff`.

---

# Русский

## Требования

| Поддерживаемый API   | Требование | Windows | Linux |
|----------------------|------------|:-------:|:-----:|
| **iRacing**          | Плагин не нужен | Да   | Нет   |
| Le Mans Ultimate     | Плагин не нужен | Да   | Нет   |
| Le Mans Ultimate (legacy) | Плагин rF2 Shared Memory Map | Да | Да |
| rFactor 2            | Плагин rF2 Shared Memory Map | Да | Да |

- Режим отображения игры: **Borderless** или **Windowed** (Fullscreen не поддерживается).
- **Не** устанавливайте RaceBuff в `Program Files` или в папку игры.

Настройка rFactor 2 / Le Mans Ultimate (legacy) и ссылки на плагины: см. [TinyPedal Wiki](https://github.com/TinyPedal/TinyPedal/wiki).

## Быстрый старт

1. Скачайте последнюю сборку в [Releases](https://github.com/froseeee/Racebuff/releases) (или соберите из исходников), распакуйте в папку, запустите `racebuff.exe` (или `python run.py`).
2. В трее появится значок. Правый клик — меню.
3. Запустите симулятор; оверлей появится на треке (вне трека — скрывается). Включить/выключить **Автоскрытие** — в меню трея.
4. **Закрепить оверлей** — фиксирует позицию; когда откреплён — перетаскивайте окно.
5. Включать/выключать виджеты — в главном окне. **Настройки** — из меню трея.
6. **Выход** — из меню трея или Overlay.

**Язык:** Настройки → Приложение → **Язык** → English / Русский / system.

**iRacing:** Настройки → Приложение → **API телеметрии** → iRacing.

### iRacing — поддерживаемые данные

Relative/Standings (позиции, гэпы, классы), Timing (время круга, дельта, время до лидера), Session (флаги, температура трека/воздуха, пит открыт), Lap (прогресс, дистанция, круги до лидера), Vehicle (топливо, пит-стопы, имена пилотов/машин), Tyre (температуры, износ), Brake (баланс, давление, температура), Engine/Inputs/Wheel (передача, RPM, педали, углы скольжения), Switch (фары, зажигание). Данные из официального iRacing SDK через `pyirsdk`; многоместо (CarIdx*) поддерживается.

## Запуск из исходников

### Зависимости

- Python 3.8–3.11
- PySide2 или PySide6 (`pip install PySide2` или `pip install PySide6`)
- psutil, pyLMUSharedMemory, pyRfactor2SharedMemory (см. `requirements.txt`)
- Для iRacing: `pyirsdk` (`pip install pyirsdk`)

Из корня проекта:

```bash
pip install -r requirements.txt
python run.py
```

С PySide6:

```bash
python run.py --pyside 6
```

### Клонирование (с подмодулями)

```bash
git clone --recursive https://github.com/froseeee/Racebuff.git
cd Racebuff
git submodule update --init
```

## Сборка exe (Windows)

```bash
pip install py2exe
python freeze_py2exe.py
```

Результат: `dist/RaceBuff/racebuff.exe` (и нужные папки). Запускайте из папки `dist/RaceBuff`.

---

## Repository / Репозиторий

**Racebuff:** [github.com/froseeee/Racebuff](https://github.com/froseeee/Racebuff)

## License and credits / Лицензия и благодарности

- **RaceBuff** — свободное ПО под лицензией [GNU General Public License v3.0 или новее](LICENSE.txt).
- **TinyPedal** (оригинал): Copyright (C) 2022–2026 TinyPedal developers.  
  [Оригинальный репозиторий](https://github.com/TinyPedal/TinyPedal) · [Участники](https://github.com/TinyPedal/TinyPedal/blob/master/docs/contributors.md)
- Иконки и изображения: см. [images/CC-BY-SA-4.0.txt](images/CC-BY-SA-4.0.txt) и [docs/licenses/THIRDPARTYNOTICES.txt](docs/licenses/THIRDPARTYNOTICES.txt).

**RaceBuff — независимый форк; оригинальный проект TinyPedal и его авторы не несут ответственности за этот форк.**
