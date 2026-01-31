# Публикация RaceBuff в репозиторий GitHub

Репозиторий: **[github.com/froseeee/Racebuff](https://github.com/froseeee/Racebuff)**.

## Подготовка к выгрузке (чеклист)

- [ ] В исходниках везде RaceBuff; пакет переименован в `racebuff` (без упоминаний TinyPedal, кроме блока «оригинал» в `racebuff/const_app.py` и README).
- [ ] `racebuff/const_app.py`: `REPO_NAME = "froseeee/Racebuff"` (или ваш логин/репо).
- [ ] Собран exe: `python freeze_py2exe.py -c -y` → папка `dist/RaceBuff/`.
- [ ] Папка `dist/` в `.gitignore` — в репо не попадает.
- [ ] Коммит и пуш: `git add .` → `git commit -m "..."` → `git push origin main`.
- [ ] Релиз: см. [RELEASE.md](RELEASE.md).

## 1. Репозиторий уже настроен

В **`racebuff/const_app.py`** указано: `REPO_NAME = "froseeee/Racebuff"`. Ссылки в приложении (меню, окно «О программе») ведут на этот репозиторий.

## 2. Привяжите проект и запушьте

В корне проекта выполните:

```bash
git remote remove origin
git remote add origin https://github.com/froseeee/Racebuff.git
git branch -M main
git push -u origin main
```

Если используете SSH:

```bash
git remote add origin git@github.com:froseeee/Racebuff.git
```

## 3. Submodules

В проекте есть submodules (pyLMUSharedMemory, pyRfactor2SharedMemory). При клонировании репозитория:

```bash
git clone --recursive https://github.com/froseeee/Racebuff.git
cd Racebuff
git submodule update --init
```

## 4. Релизы (Releases)

**Подробная инструкция:** см. **[RELEASE.md](RELEASE.md)** — что архивировать, как создать релиз.

Кратко: соберите exe (`python freeze_py2exe.py -c -y`), заархивируйте папку **dist/RaceBuff** целиком, в [Releases](https://github.com/froseeee/Racebuff/releases) создайте новый релиз (tag, например `v1.0.0`), прикрепите zip и опубликуйте. **В релиз достаточно один архив с папкой RaceBuff из dist.**
