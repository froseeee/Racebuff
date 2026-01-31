# Релиз RaceBuff / Creating a Release

## Достаточно ли архива с папкой RaceBuff из dist?

**Да.** Для релиза достаточно заархивировать **целиком папку `dist/RaceBuff`**.

В архиве должна быть **одна папка** (например, `RaceBuff`), внутри неё:
- `racebuff.exe`
- `lib/`
- `platforms/`
- `docs/`
- `images/`
- `LICENSE.txt`
- `README.md`

Пользователь скачивает архив → распаковывает → заходит в папку `RaceBuff` → запускает `racebuff.exe`.

---

## Пошаговая подготовка к выгрузке

### 1. Закоммитить и отправить код (без dist)

Папка `dist/` в `.gitignore` — в репозиторий не попадёт. Пушим только исходники:

```bash
cd d:\RB\Racebuff\TinyPedalirae   # или путь к вашему клону RaceBuff
git add .
git status
git commit -m "RaceBuff: iRacing, Russian, README, release prep"
git push origin main
```

(Если `origin` ещё не настроен — см. [GITHUB_SETUP.md](GITHUB_SETUP.md).)

### 2. Собрать exe

```bash
cd d:\RB\Racebuff\TinyPedalirae   # или путь к вашему клону RaceBuff
C:\Py311\python.exe freeze_py2exe.py -c -y
```

Или свой Python: `python freeze_py2exe.py -c -y`

Результат: папка `dist/RaceBuff/` с `racebuff.exe` и всеми файлами.

### 3. Создать архив для релиза

**Вариант A — архив папки RaceBuff (рекомендуется)**

- Заархивировать **содержимое** папки `dist/RaceBuff` так, чтобы **в корне архива** была одна папка `RaceBuff`, а в ней — exe и папки.
- Или заархивировать саму папку `dist/RaceBuff`: тогда в архиве будет один элемент — папка `RaceBuff`.

Имя архива, например: `RaceBuff-v1.0.0-win64.zip`

**Вариант B — через PowerShell**

Из корня проекта:

```powershell
Compress-Archive -Path "dist\RaceBuff" -DestinationPath "RaceBuff-v1.0.0-win64.zip"
```

В итоге в `RaceBuff-v1.0.0-win64.zip` будет одна папка `RaceBuff` с exe и файлами.

### 4. Создать релиз на GitHub

1. Открыть [github.com/froseeee/Racebuff/releases](https://github.com/froseeee/Racebuff/releases).
2. **Create a new release**.
3. **Choose a tag:** например `v1.0.0` (создать новый tag).
4. **Release title:** например `RaceBuff v1.0.0`.
5. **Describe:** кратко, что в этой версии, например:
   - Fork TinyPedal, поддержка iRacing, русский язык.
   - Скачать: распаковать архив и запустить `RaceBuff/racebuff.exe`.
6. Прикрепить файл: перетащить **архив** (например `RaceBuff-v1.0.0-win64.zip`) в блок *Attach binaries*.
7. **Publish release**.

После этого ссылка на скачивание будет в разделе Releases.

---

## Кратко

| Шаг | Действие |
|-----|----------|
| 1 | `git add .` → `git commit` → `git push` (код без dist) |
| 2 | Собрать: `python freeze_py2exe.py -c -y` |
| 3 | Заархивировать папку **dist/RaceBuff** (в архиве — папка RaceBuff с exe и файлами) |
| 4 | Releases → Create new release → tag (v1.0.0) → прикрепить zip → Publish |

**В релиз достаточно один архив с папкой RaceBuff из dist.**
