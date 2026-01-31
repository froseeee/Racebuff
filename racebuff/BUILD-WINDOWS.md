# Сборка RaceBuff на Windows

## Требования

- **Python 3.9–3.11** (рекомендуется 3.11 с PySide6)
- Зависимости: PySide2 **или** PySide6, psutil, py2exe (для сборки .exe)

## Запуск из исходников

1. Клонировать репозиторий с подмодулями:
   ```bash
   git clone --recursive https://github.com/froseeee/Racebuff.git
   cd Racebuff
   ```

2. Установить зависимости (один из вариантов):
   - **Python 3.9 или 3.10:**  
     `pip install PySide2 psutil`
   - **Python 3.11:** (PySide2 недоступен)  
     `pip install PySide6 psutil`

3. Запуск:
   - С PySide2: `python run.py`
   - С PySide6: `python run.py --pyside 6`

## Сборка .exe (py2exe)

1. Установить зависимости и py2exe:
   ```bash
   pip install PySide6 psutil py2exe
   ```

2. Собрать исполняемый файл (без интерактивных вопросов):
   ```bash
   python freeze_py2exe.py -c -y
   ```
   - `-c` — очистить старую сборку перед сборкой  
   - `-y` — не спрашивать «удалить старую сборку?»

3. Результат:
   - **Папка:** `dist/RaceBuff/`
   - **Исполняемый файл:** `dist/RaceBuff/racebuff.exe`
   - Запускать нужно из папки `dist/RaceBuff` (рядом с `racebuff.exe` должны быть папки `lib`, `platforms`, `docs`, `images`).

## Проверка работоспособности

- **Из исходников:** после `python run.py` (или `python run.py --pyside 6`) в трее должен появиться значок RaceBuff; при запуске игры (iRacing / rFactor 2 / Le Mans Ultimate) в оконном или безрамочном режиме оверлей появится на треке.
- **Из .exe:** запустить `dist/RaceBuff/racebuff.exe` — поведение такое же.

Игру нужно запускать в режиме **Borderless** или **Windowed**; **Fullscreen** не поддерживается.
