# 📅 Телеграм-бот расписания

Бот для автоматического оповещения о графике работы сотрудников на неделю/месяц.

## ✨ Возможности
- Отправка расписания на текущую и следующую неделю
- Автоматическое форматирование в читаемый вид с датами
- Поддержка групповых чатов (рассылка)
- Удобное управление через файл `rasp.txt`

## 🛠 Установка
1. Склонируйте репозиторий:
```bash
git clone https://github.com/tg-bot-work-schedule.git
cd tg-bot-work-schedule
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файлы конфигурации:
```bash
cp .env.example .env
cp rasp.example.txt rasp.txt
```

4. ⚙ Конфигурация 
##### Файл .env

```ini
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=123456789  # ID администратора
GROUP_IDS=-10012345, -678901234  # ID чатов через запятую
```

##### Формат файла rasp.txt
```ini
Иванов А.А. Петров Б.Б.
Сидоров В.В. Кузнецов Г.Г.
Иванов А.А. Петров Б.Б.
Сидоров В.В. Кузнецов Г.Г.
Иванов А.А. Петров Б.Б.
Сидоров В.В. Кузнецов Г.Г.
Иванов А.А. Петров Б.Б.
Следующая
```

5. 🐳 Запуск через Docker 
##### Соберите образ:

```bash
docker-compose build
```
##### Запустите контейнер:
```bash
docker-compose up -d
```

Пример вывода:
```
✨ РАСПИСАНИЕ НА НЕДЕЛЮ ✨
═══════════

📅 Понедельник 14.04.2025
👥 Иванов А.А. Петров Б.Б.

📅 Вторник 15.04.2025
👥 Сидоров В.В. Кузнецов Г.Г.
...
✅ Готово! Хорошей недели! 😊
```
