import re
import aiofiles
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery
from aiogram.types import Message
from config import GROUP_IDS, ADMIN_ID
from main import bot
import keyboards.keyboard as kb
import datetime

router = Router()


class Register(StatesGroup):
    send = State()
    delete = State()


def new_user(uid):
    with open("users.txt", "a") as f:
        f.write(str(uid) + "\n")


def get_russian_weekday(date):
    days = ['Понедельник', 'Вторник', 'Среда',
            'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    return days[date.weekday()]


async def create_sheduler(s):
    schedule = s.split('\n')
    week_type = s.split('\n')[-1]
    today = datetime.date.today()
    current_week_start = today - datetime.timedelta(days=today.weekday())

    if week_type.lower() == 'следующая':
        start_date = current_week_start + datetime.timedelta(weeks=1)
    else:
        start_date = current_week_start

    result = []
    for i in range(7):
        day_date = start_date + datetime.timedelta(days=i)
        day_name = get_russian_weekday(day_date)
        people = schedule[i].split()

        result.append(
            f"📅 {day_name} {day_date.strftime('%d.%m.%Y')}\n"
            f"👥 {' '.join(people) if people else '🎉 Свободно'}"
        )

    # Выводим результат
    result_s = "\n" + f"✨ РАСПИСАНИЕ НА НЕДЕЛЮ ✨" + "\n"
    result_s += "═══════════" + "\n\n"
    result_s += "\n\n".join(result)
    result_s += "\n\n" + "✅ Готово! Хорошей недели! 😊" + "\n"
    async with aiofiles.open('rasp.txt', 'w', encoding='utf-8') as file:
        await file.write(result_s)
    return result_s


@router.message(Command("schedule"))  # F.text
async def message_with_text(message: Message):
    print(message.chat.id, message.from_user.id, 'schedule')
    if message.chat.id in GROUP_IDS:
        try:
            async with aiofiles.open('rasp.txt', 'r', encoding='utf-8') as file:
                rasp = await file.read()
            await message.answer(rasp, reply_markup=await kb.user_keyboard())
        except FileNotFoundError:
            await message.answer("Файл с расписанием отсутствует", reply_markup=await kb.user_keyboard())
        except Exception as e:
            await message.answer(f"Ошибка: {str(e)}", reply_markup=await kb.user_keyboard())


@router.message(Command("end"))  # F.text
async def update(message: Message):
    if message.chat.id in GROUP_IDS:
        param = message.text.split()
        if len(param) == 2:
            date_l = re.findall('[0-9]{2}\.[0-9]{1,2}\.[0-9]{4}', param[1])
            if len(date_l):
                date_l = list(map(int, date_l[0].split('.')))
                today = datetime.date.today()
                future = datetime.date(date_l[2], date_l[1], date_l[0])
                diff = int((future - today).days)
                if diff > 0:
                    await message.answer('До конца работы осталось' + str(diff) + ' дней.',
                                         reply_markup=await kb.user_keyboard())
                else:
                    await bot.send_photo(message.chat.id, caption='Уже прошло ' + str(
                        abs(diff)) + ' дней с окончания работы.\nТеперь добби свободен.',
                                         photo=FSInputFile(r"data//dobbi.png"), reply_markup=await kb.user_keyboard())
            else:
                await message.answer('Неверный формат, я не понимаю.\nПример: /end 01.01.2019',
                                     reply_markup=await kb.user_keyboard())
        else:
            await message.answer('Неверный формат, я не понимаю.\nПример: /end 01.01.2019',
                                 reply_markup=await kb.user_keyboard())


@router.message(Command("start"))  # F.text
async def message_with_text(message: Message):
    print(message.from_user.id, message.chat.id, message.text)
    new_user(message.from_user.id)
    if message.from_user.id in ADMIN_ID and message.chat.id not in GROUP_IDS:
        m = await message.answer("Добро пожаловать в наш Бот",
                                 reply_markup=await kb.start_keyboard())
    elif message.chat.id in GROUP_IDS:
        m = await message.answer("Добро пожаловать!\nЕсть команда /help",
                                 reply_markup=await kb.user_keyboard())
    else:
        await message.answer('Вход рубль, выход два')


@router.callback_query()
async def handle_callback_query(callback: CallbackQuery, state: FSMContext):
    print('query.data router', callback.data)
    print(callback.from_user.id, callback.message.chat.id)

    query = callback.data
    if callback.message.chat.id in GROUP_IDS:
        if 'rasp' in query:
            try:
                async with aiofiles.open('rasp.txt', 'r', encoding='utf-8') as file:
                    rasp = await file.read()
                await callback.message.answer(rasp, reply_markup=await kb.user_keyboard())
            except FileNotFoundError:
                await callback.message.answer("Файл с расписанием отсутствует", reply_markup=await kb.user_keyboard())
            except Exception as e:
                await callback.message.answer(f"Ошибка: {str(e)}", reply_markup=await kb.user_keyboard())

    if callback.from_user.id in ADMIN_ID and callback.message.chat.id not in GROUP_IDS:
        if 'new' in query:
            await state.set_state(Register.send)
            await callback.message.answer("Введите расписание:", reply_markup=await kb.back_keyboard())
        # elif "send" in query:
        #     async with aiofiles.open('rasp.txt', 'r', encoding='utf-8') as file:
        #         rasp = await file.read()
        #     for group_id in GROUP_IDS:
        #         await bot.send_message(group_id, rasp)
        elif 'rasp' in query:
            try:
                async with aiofiles.open('rasp.txt', 'r', encoding='utf-8') as file:
                    rasp = await file.read()
                await callback.message.answer(rasp, reply_markup=await kb.start_keyboard())
            except FileNotFoundError:
                await callback.message.answer("Файл с расписанием отстуствует")
                if callback.from_user.id in ADMIN_ID:
                    await state.set_state(Register.send)
                    await callback.message.answer("Введите расписание:", reply_markup=await kb.back_keyboard())
            except Exception as e:
                await callback.message.answer(f"Ошибка: {str(e)}", reply_markup=await kb.start_keyboard())
        elif "back" in query:
            await callback.message.answer("Добро пожаловать в наш Бот", reply_markup=await kb.start_keyboard())
            await state.clear()
        elif "del" in query:
            await callback.message.answer("Введите id:", reply_markup=await kb.back_keyboard())
            await state.set_state(Register.delete)


@router.message(Register.send)
async def auth_phone(message: Message, state: FSMContext):
    sheduler = await create_sheduler(message.text)
    for group_id in GROUP_IDS:
        m = await bot.send_message(group_id, sheduler, reply_markup=await kb.user_keyboard())
        print(m.message_id)

    await message.answer('Расписание создано', reply_markup=await kb.start_keyboard())
    await state.clear()


@router.message(Register.delete)
async def auth_phone(message: Message, state: FSMContext):
    await bot.delete_message(chat_id=GROUP_IDS[0], message_id=message.text)
    await message.answer('Сообщение удалено', reply_markup=await kb.start_keyboard())
    await state.clear()


# 592538405,

@router.message(Command("help"))  # F.text
async def message_with_text(message: Message):
    if message.chat.id in GROUP_IDS:

        mes = """
        🤖 <b>Доступные команды бота</b> 🤖

        1. <b>/help</b> 🆘  
           <i>Показать список всех команд</i>  
           ➤ Пример: <code>/help</code>

        2. <b>/schedule</b> 📅  
           <i>Получить расписание на текущую неделю</i>  
           ➤ Пример: <code>/schedule</code>

        3. <b>/end</b> ⏳  
           <i>Узнать количество дней до указанной даты</i>  
           ➤ Формат: <code>ДД.ММ.ГГГГ</code>  
           ➤ Пример: <code>/end 22.02.2024</code>
        """
        m = await message.answer(mes, parse_mode='html', reply_markup=await kb.user_keyboard())
        print(m.message_id)
    else:
        await message.answer('Вход рубль, выход два')

#
# @router.message(F.text)  # F.text
# async def message_with_text(message: Message):
#     if message.from_user.id in ADMIN_ID and message.chat.id not in GROUP_IDS:
#         m = await message.answer("Добро пожаловать в наш Бот",
#                                  reply_markup=await kb.start_keyboard())
#     elif message.chat.id in GROUP_IDS:
#         m = await message.answer("Добро пожаловать!\nЕсть команда /help",
#                                  reply_markup=await kb.user_keyboard())
#     else:
#         await message.answer('Вход рубль, выход два')