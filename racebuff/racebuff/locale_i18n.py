#  RaceBuff is an open-source overlay application for racing simulation.
#  Copyright (C) 2026 RaceBuff developers, see contributors.md file
#
#  This file is part of RaceBuff.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Locale / i18n support (English, Russian).
"""

# English key -> Russian translation (only strings that have Russian translation)
TRANSLATIONS = {
    # Main / single instance
    "RaceBuff is already running.\n\nOnly one instance may be run at a time.\nCheck system tray for hidden icon.": (
        "RaceBuff уже запущен.\n\n"
        "Одновременно может работать только один экземпляр.\n"
        "Проверьте значок в системном трее."
    ),
    # Menu - overlay
    "Lock Overlay": "Закрепить оверлей",
    "Auto Hide": "Автоскрытие",
    "Grid Move": "Перемещение по сетке",
    "VR Compatibility": "Режим VR",
    "Reload": "Перезагрузить",
    # Menu - reset
    "Reset Data": "Сброс данных",
    "Delta Best": "Delta Best",
    "Energy Delta": "Energy Delta",
    "Fuel Delta": "Fuel Delta",
    "Consumption History": "История расхода",
    "Sector Best": "Sector Best",
    "Track Map": "Карта трека",
    # Menu - config
    "Config": "Настройки",
    "Quit": "Выход",
    "Application": "Приложение",
    "Compatibility": "Совместимость",
    "Notification": "Уведомления",
    "Units": "Единицы измерения",
    "Global Font Override": "Шрифт по умолчанию",
    "User Path": "Пути",
    "Open Folder": "Открыть папку",
    # About
    "About": "О программе",
    "About {app_name}": "О программе {app_name}",
    "Contributors": "Участники",
    "License": "Лицензия",
    "Third-Party Notices": "Сторонние компоненты",
    "Close": "Закрыть",
    "Reset Options": "Сбросить настройки",
    "Reset to Default": "Сбросить по умолчанию",
    "Error": "Ошибка",
    "Apply": "Применить",
    "Save": "Сохранить",
    "Cancel": "Отмена",
    "Reset": "Сброс",
    # Reset data dialogs
    "Reset {data_type}": "Сброс {data_type}",
    "Cannot reset data while on track.": "Нельзя сбрасывать данные во время заезда.",
    "No {data_type} data found.<br><br>You can only reset data from active session.": (
        "Данные «{data_type}» не найдены.<br><br>"
        "Сброс возможен только для текущей сессии."
    ),
    "Reset <b>{data_type}</b> data for<br><b>{filename}</b> ?<br><br>This cannot be undone!": (
        "Сбросить данные <b>{data_type}</b> для<br><b>{filename}</b>?<br><br>"
        "Это действие нельзя отменить!"
    ),
    "This cannot be undone!": "Это действие нельзя отменить!",
    "{data_type} data has been reset for<br><b>{filename}</b>": (
        "Данные {data_type} сброшены для<br><b>{filename}</b>"
    ),
    # Config dialogs
    "Cannot open folder:<br><b>{filepath}</b>": "Не удалось открыть папку:<br><b>{filepath}</b>",
    "Reset all <b>{key_name}</b> options to default?<br><br>Changes are only saved after clicking Apply or Save Button.": (
        "Сбросить все параметры <b>{key_name}</b>?<br><br>"
        "Изменения сохраняются только после нажатия «Применить» или «Сохранить»."
    ),
    "Invalid {value_type} for <b>{option_name}</b> option.<br><br>Changes are not saved.": (
        "Недопустимое значение {value_type} для <b>{option_name}</b>.<br><br>"
        "Изменения не сохранены."
    ),
    # Metadata
    "Metadata Info": "Сведения о метаданных",
    "Show Map": "Показать карту",
    "Hide Map": "Скрыть карту",
    # Menu bar titles
    "Overlay": "Оверлей",
    "API": "API",
    "Config": "Настройки",
    "Tools": "Инструменты",
    "Window": "Окно",
    "Help": "Справка",
    # API menu
    "Remember API Selection from Preset": "Запоминать API из пресета",
    "Enable Legacy API Selection": "Включить выбор устаревшего API",
    "Options": "Параметры",
    "Restart API": "Перезапустить API",
    "Legacy API": "Устаревший API",
    "Enable <b>Legacy API</b> selection and restart <b>RaceBuff</b>?": "Включить выбор <b>устаревшего API</b> и перезапустить <b>RaceBuff</b>?",
    "Disable <b>Legacy API</b> selection and restart <b>RaceBuff</b>?": "Отключить выбор <b>устаревшего API</b> и перезапустить <b>RaceBuff</b>?",
    # Tools menu
    "Fuel Calculator": "Калькулятор топлива",
    "Driver Stats Viewer": "Статистика пилотов",
    "Track Map Viewer": "Просмотр карты трека",
    "Heatmap Editor": "Редактор тепловой карты",
    "Brake Editor": "Редактор тормозов",
    "Tyre Compound Editor": "Редактор составов шин",
    "Vehicle Brand Editor": "Редактор марок авто",
    "Vehicle Class Editor": "Редактор классов авто",
    "Track Info Editor": "Редактор информации о треке",
    "Track Notes Editor": "Редактор заметок о треке",
    # Window menu
    "Show at Startup": "Показывать при запуске",
    "Minimize to Tray": "Сворачивать в трей",
    "Remember Position": "Запоминать позицию",
    "Remember Size": "Запоминать размер",
    "Restart RaceBuff": "Перезапустить RaceBuff",
    # Help menu
    "User Guide": "Руководство пользователя",
    "FAQ": "Частые вопросы",
    "Show Log": "Показать лог",
    "Check for Updates": "Проверить обновления",
    # Tabs
    "Widget": "Виджеты",
    "Module": "Модули",
    "Preset": "Пресеты",
    "Spectate": "Наблюдение",
    "Pacenotes": "Пейс-ноты",
    "Hotkey": "Горячие клавиши",
    # Preset view
    "Refresh": "Обновить",
    "Transfer": "Перенос",
    "New Preset": "Новый пресет",
    "Auto Load Primary Preset": "Автозагрузка основного пресета",
    "Lock Preset": "Закрепить пресет",
    "Unlock Preset": "Снять блокировку пресета",
    "Duplicate": "Дублировать",
    "Rename": "Переименовать",
    "Delete": "Удалить",
    "Duplicate Preset": "Дублировать пресет",
    "Rename Preset": "Переименовать пресет",
    "Delete Preset": "Удалить пресет",
    "Lock <b>{filename}</b> preset?<br><br>Changes to locked preset will not be saved.": (
        "Закрепить пресет <b>{filename}</b>?<br><br>Изменения закреплённого пресета не будут сохраняться."
    ),
    "Unlock <b>{filename}</b> preset?": "Снять блокировку пресета <b>{filename}</b>?",
    "Delete <b>{filename}</b> preset permanently?<br><br>This cannot be undone!": (
        "Удалить пресет <b>{filename}</b> навсегда?<br><br>Это действие нельзя отменить!"
    ),
    "Confirm": "Подтверждение",
    "Yes": "Да",
    "No": "Нет",
    "Set Primary for Class": "Сделать основным для класса",
    "Clear Primary Tag": "Снять основной тег",
    "Enter a new preset name": "Введите имя нового пресета",
    "Invalid preset name.": "Недопустимое имя пресета.",
    "Preset already exists.": "Пресет с таким именем уже существует.",
    "Create new default preset": "Создать новый пресет по умолчанию",
    # Status bar / DPI
    "Config Telemetry API": "Настройка API телеметрии",
    "Toggle Window Color Theme": "Переключить тему оформления",
    "Toggle High DPI Scaling": "Переключить масштабирование DPI",
    "High DPI Scaling": "Масштабирование DPI",
    "Enable <b>High DPI Scaling</b> and restart <b>RaceBuff</b>?<br><br><b>Window</b> and <b>Overlay</b> size and position will be auto-scaled according to system DPI scaling setting.": (
        "Включить <b>масштабирование DPI</b> и перезапустить <b>RaceBuff</b>?<br><br>Размер и позиция <b>окна</b> и <b>оверлея</b> будут масштабироваться по настройкам системы."
    ),
    "Disable <b>High DPI Scaling</b> and restart <b>RaceBuff</b>?<br><br><b>Window</b> and <b>Overlay</b> size and position will not be scaled under high DPI screen resolution.": (
        "Отключить <b>масштабирование DPI</b> и перезапустить <b>RaceBuff</b>?<br><br>Размер и позиция <b>окна</b> и <b>оверлея</b> не будут масштабироваться на экранах с высоким DPI."
    ),
    # Config option names (format_option_name output)
    "Language": "Язык",
    "Show At Startup": "Показывать при запуске",
    "Minimize To Tray": "Сворачивать в трей",
    "Remember Position": "Запоминать позицию",
    "Remember Size": "Запоминать размер",
    "Enable High Dpi Scaling": "Масштабирование DPI",
    "Enable Auto Load Preset": "Автозагрузка пресета",
    "Enable Global Hotkey": "Глобальные горячие клавиши",
    "Show Confirmation For Batch Toggle": "Подтверждение массового переключения",
    "Check For Updates On Startup": "Проверять обновления при запуске",
    "Window Color Theme": "Тема оформления",
    "Api Name": "API телеметрии",
    "Enable Api Selection From Preset": "Выбор API из пресета",
    "Enable Legacy Api Selection": "Устаревший API",
    # Module/Widget list
    "Enable All": "Включить все",
    "Disable All": "Выключить все",
    "Enabled: <b>{n}/{total}</b>": "Включено: <b>{n}/{total}</b>",
    "Loaded: <b>{preset}</b>": "Загружен: <b>{preset}</b>",
    " (locked)": " (заблокирован)",
    "Spectating: <b>Disabled</b>": "Наблюдение: <b>Выкл</b>",
    "Spectating: <b>{name}</b>": "Наблюдение: <b>{name}</b>",
    "Spectate": "Наблюдение",
    "Refresh": "Обновить",
    "Enabled": "Вкл",
    "Disabled": "Выкл",
    "ON": "ВКЛ",
    "OFF": "ВЫКЛ",
    "Enable all widgets?": "Включить все виджеты?",
    "Disable all widgets?": "Выключить все виджеты?",
    "Enable all modules?": "Включить все модули?",
    "Disable all modules?": "Выключить все модули?",
    # Status bar
    "API: {api} ({status})": "Телеметрия: {api} ({status})",
    "UI: Dark": "Интерфейс: Тёмная",
    "UI: Light": "Интерфейс: Светлая",
    "Scale: Auto": "Масштаб: Авто",
    "Scale: Off": "Масштаб: Выкл",
    "Load Map": "Загрузить карту",
    "Zoom:": "Масштаб:",
    "Position:": "Позиция:",
    "Nodes:": "Узлы:",
    "Clear all key bindings?<br><br>This cannot be undone!": "Сбросить все привязки клавиш?<br><br>Это действие нельзя отменить!",
    "<b>Save changes before continue?</b>": "<b>Сохранить изменения перед продолжением?</b>",
    "Dark": "Тёмная",
    "Light": "Светлая",
    "Auto": "Авто",
    "Off": "Выкл",
    # Widget names (format_module_name output)
    "Battery": "Батарея",
    "Brake Bias": "Баланс тормозов",
    "Brake Performance": "Эффективность тормозов",
    "Brake Pressure": "Давление тормозов",
    "Brake Temperature": "Температура тормозов",
    "Brake Wear": "Износ тормозов",
    "Cruise": "Круиз",
    "Damage": "Повреждения",
    "Deltabest": "Дельта лучшего",
    "Deltabest Extended": "Дельта лучшего (расш.)",
    "Differential": "Дифференциал",
    "DRS": "DRS",
    "Electric Motor": "Электромотор",
    "Elevation": "Высота",
    "Engine": "Двигатель",
    "Flag": "Флаги",
    "Force": "Перегрузки",
    "Friction Circle": "Круг сцепления",
    "Fuel": "Топливо",
    "Fuel Energy Saver": "Энергия/топливо",
    "Gear": "Передача",
    "Heading": "Курс",
    "Instrument": "Приборы",
    "Lap Time History": "История кругов",
    "Laps And Position": "Круги и позиция",
    "Navigation": "Навигация",
    "P2P": "P2P",
    "Pace Notes": "Пейс-ноты",
    "Pedal": "Педали",
    "Pit Stop Estimate": "Оценка пит-стопа",
    "Radar": "Радар",
    "Rake Angle": "Угол диффузора",
    "Relative": "Относительно",
    "Relative Finish Order": "Порядок финиша",
    "Ride Height": "Дорожный просвет",
    "Rivals": "Соперники",
    "Roll Angle": "Крен",
    "RPM LED": "Светодиоды RPM",
    "Sectors": "Секторы",
    "Session": "Сессия",
    "Slip Ratio": "Проскальзывание",
    "Speedometer": "Спидометр",
    "Standings": "Позиции",
    "Steering": "Руль",
    "Steering Wheel": "Руль (виджет)",
    "Stint History": "История стинтов",
    "Suspension Force": "Усилие подвески",
    "Suspension Position": "Положение подвески",
    "Suspension Travel": "Ход подвески",
    "System Performance": "Нагрузка системы",
    "Timing": "Время",
    "Track Map": "Карта трека",
    "Track Notes": "Заметки о треке",
    "Trailing": "След",
    "Tyre Carcass": "Каркас шины",
    "Tyre Inner Layer": "Внутренний слой шины",
    "Tyre Load": "Нагрузка на шину",
    "Tyre Pressure": "Давление в шинах",
    "Tyre Temperature": "Температура шин",
    "Tyre Wear": "Износ шин",
    "Virtual Energy": "Виртуальная энергия",
    "Weather": "Погода",
    "Weather Forecast": "Прогноз погоды",
    "Weight Distribution": "Распределение веса",
    "Wheel Camber": "Развал колёс",
    "Wheel Toe": "Схождение колёс",
    # Widget context menu
    "Center Horizontally": "По центру по горизонтали",
    "Center Vertically": "По центру по вертикали",
    # Batch / common dialogs
    "Last Offset:": "Последнее смещение:",
    "Last Scale:": "Последний масштаб:",
    "Column:": "Столбец:",
    "Find:": "Найти:",
    "Replace:": "Заменить:",
    "Replace": "Заменить",
    "Invalid name.": "Недопустимое имя.",
    "Batch Offset": "Смещение",
    "Batch Replace": "Замена",
    # Config / font
    "Font Name": "Шрифт",
    "Font Size Addend": "Добавка к размеру шрифта",
    "Font Weight": "Насыщенность шрифта",
    # Preset
    "No preset selected.\nPlease select a preset to continue.": "Пресет не выбран.\nВыберите пресет и повторите.",
    # Preset transfer
    "To:": "В:",
    "No destination preset selected or found.": "Пресет назначения не выбран или не найден.",
    "No preset setting selected.<br><br>Select at least one setting and try again.": "Не выбрана ни одна настройка.<br><br>Выберите хотя бы одну и повторите.",
    "No option type selected.<br><br>Select at least one option type and try again.": "Не выбран тип опции.<br><br>Выберите хотя бы один тип и повторите.",
    "Transfer Completed": "Перенос завершён",
    "None": "Нет",
    # Track map
    "Track Map Name": "Имя карты трека",
    # Track notes editor
    "Hide Map": "Скрыть карту",
    "Show Map": "Показать карту",
    "Open Pace Notes": "Открыть пейс-ноты",
    "Open Track Notes": "Открыть заметки о треке",
    "New Pace Notes": "Новые пейс-ноты",
    "New Track Notes": "Новые заметки о треке",
    "From Map": "С карты",
    "From Telemetry": "Из телеметрии",
    "Highlight on Map": "Подсветить на карте",
    "Set from Map": "Установить с карты",
    "Set from Telemetry": "Установить из телеметрии",
    "Insert Row Above": "Вставить строку выше",
    "Insert Row Below": "Вставить строку ниже",
    "Delete Rows": "Удалить строки",
    "Ok": "ОК",
    "Saved": "Сохранено",
    "No data selected.": "Данные не выбраны.",
    "Nothing to save.": "Нечего сохранять.",
    "Notes saved at:<br><b>{filename}</b>": "Заметки сохранены:<br><b>{filename}</b>",
    "Set from Telemetry": "Установить из телеметрии",
    # Vehicle editors
    "RF2 Rest API": "RF2 Rest API",
    "LMU Rest API (Primary)": "LMU Rest API (основной)",
    "LMU Rest API (Alternative)": "LMU Rest API (альтернативный)",
    "JSON file": "Файл JSON",
    "Data Imported": "Данные импортированы",
    "Vehicle brand data imported.": "Данные марок авто импортированы.",
    # Pace notes view
    "Sound File Path:": "Путь к звуку:",
    "Sound Format:": "Формат звука:",
    "Global Offset:": "Глобальное смещение:",
    "Max Duration:": "Макс. длительность:",
    "Max Queue:": "Макс. очередь:",
    "Playback Volume: 0%": "Громкость воспроизведения: 0%",
    "Playback Volume: {volume}%": "Громкость воспроизведения: {volume}%",
    # Notification bar
    "Preset Locked": "Пресет заблокирован",
    "Spectate Mode Enabled": "Режим наблюдения включён",
    "Pace Notes Playback Enabled": "Воспроизведение пейс-нотов включено",
    "Global Hotkey Enabled": "Глобальные горячие клавиши включены",
    "View Updates On GitHub": "Обновления на GitHub",
    "Dismiss": "Закрыть",
    "Checking For Updates...": "Проверка обновлений...",
    # Log
    "Copy": "Копировать",
    "Copied all log to Clipboard.": "Лог скопирован в буфер обмена.",
    # Hotkey
    "Clear All": "Очистить всё",
    "Clear": "Очистить",
    # Heatmap
    "Cannot delete built-in heatmap preset.": "Нельзя удалить встроенный пресет тепловой карты.",
    "Invalid preset name.": "Недопустимое имя пресета.",
    "Preset already exists.": "Пресет с таким именем уже существует.",
    "Enter a new preset name": "Введите имя нового пресета",
    # Fuel calculator
    "Hide History": "Скрыть историю",
    "Show History": "Показать историю",
    "Load Live": "Загрузить из сессии",
    "Load File": "Загрузить файл",
    "Add Selected Data": "Добавить выбранные данные",
    "Lap Time:": "Время круга:",
    "Tank Capacity:": "Ёмкость бака:",
    "Fuel Ratio:": "Доля топлива:",
    "Fuel Consumption:": "Расход топлива:",
    "Energy Consumption:": "Расход энергии:",
    "Race Minutes:": "Минут гонки:",
    "Race Laps:": "Кругов гонки:",
    "Formation/Rolling:": "Формирование/прокатка:",
    "Average Pit Seconds:": "Среднее время пит-стопа (с):",
    "Total Pit Stops:": "Всего пит-стопов:",
    "Total Laps:": "Всего кругов:",
    "Total Minutes:": "Всего минут:",
    "Max Stint Laps:": "Макс. кругов стинта:",
    "Max Stint Minutes:": "Макс. минут стинта:",
    "One Less Pit Stop:": "На один пит-стоп меньше:",
    "Average Refilling:": "Средняя дозаправка:",
    "Starting Tyre Tread:": "Начальная глубина протектора:",
    "Lifespan Laps:": "Кругов до износа:",
    "Tread Wear Per Lap:": "Износ за круг:",
    "Lifespan Minutes:": "Минут до износа:",
    "Tread Wear Per Stint:": "Износ за стинт:",
    "Lifespan Stints:": "Стинтов до износа:",
    # Driver stats
    "No data found.": "Данные не найдены.",
    "No lap time found.": "Время круга не найдено.",
    "Remove Vehicle": "Удалить автомобиль",
    "Reset Lap Time": "Сбросить время круга",
}


def current_language() -> str:
    """Return current UI language: 'en', 'ru', or 'system'."""
    try:
        from .setting import cfg
        val = cfg.application.get("language", "system")
    except Exception:
        return "en"
    if val == "Русский":
        return "ru"
    if val == "English":
        return "en"
    return "system"


def tr(text_en: str, **format_kwargs) -> str:
    """Return translated string for current language. Falls back to English."""
    lang = current_language()
    if lang == "system":
        try:
            from PySide2.QtCore import QLocale
            if QLocale.system().language() == QLocale.Russian:
                lang = "ru"
            else:
                lang = "en"
        except Exception:  # Qt not available or other
            lang = "en"
    if lang != "ru":
        return text_en.format(**format_kwargs) if format_kwargs else text_en
    translated = TRANSLATIONS.get(text_en.strip())
    if translated is None:
        return text_en.format(**format_kwargs) if format_kwargs else text_en
    if format_kwargs:
        try:
            return translated.format(**format_kwargs)
        except KeyError:
            pass
    return translated
