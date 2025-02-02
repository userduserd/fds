import asyncio
import random
from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from tg.models import TelegramUser, Invoice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.filters import Command, CommandObject

from tg.text import admin_text

router = Router()


class InvoiceAmountState(StatesGroup):
    awaiting_amount = State()


@router.callback_query(F.data.startswith("accept_inv_"))
async def accept_inv(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    invoice = await sync_to_async(Invoice.objects.get)(id=data[2])
    await state.update_data(invoice_id=invoice.id)
    await call.message.answer("Введите сумму:")
    await state.set_state(InvoiceAmountState.awaiting_amount)


@router.message(InvoiceAmountState.awaiting_amount)
async def invoice_amount(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        invoice_id = data.get("invoice_id")
        invoice = await sync_to_async(Invoice.objects.get)(id=invoice_id)
        amount = int(msg.text)
        if invoice.amount == amount:
            invoice.amount = amount
            invoice.is_complete = True
            invoice.save()
            await msg.answer(f"Платеж принят {amount} Т")
            await state.clear()
        else:
            await msg.answer("Платеж не совпадает, примите инвойс заново!")
            await state.clear()
    except Exception as e:
        print(e)


class IdState(StatesGroup):
    awaiting_id = State()
    awaiting_desc = State()
    awaiting_photo = State()
    chat_with_admin = State()

@router.message(Command("start"))
async def start(msg: Message, command: CommandObject, state: FSMContext):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=msg.from_user.id)
    user.first_name = msg.from_user.first_name
    user.last_name = msg.from_user.last_name
    user.username = msg.from_user.username
    user.save()
    if not user.is_exchanger:
        await msg.answer("Введите ID заявки:")
        await state.set_state(IdState.awaiting_id)
        await state.update_data(user_id=user.user_id)


@router.message(IdState.awaiting_id)
async def awaiting_id(msg: Message, state: FSMContext):
    try:
        invoice = await sync_to_async(Invoice.objects.get)(uniq_id=msg.text)
        await msg.answer(f"Напишите свой вопрос поддержке по заявке {invoice.uniq_id}")
        await state.update_data(uniq=invoice.uniq_id)
        await state.set_state(IdState.awaiting_desc)
    except Exception as e:
        await msg.answer("Не похоже на ID заявки, попробуйте еще раз.")


@router.message(IdState.awaiting_desc)
async def awaiting_desc(msg: Message, state: FSMContext):
    if msg.text:
        data = await state.get_data()
        uniq = data.get("uniq")
        await msg.answer(f"Прикрепите чек или скриншот по заявке {uniq}:")
        await state.update_data(desc=msg.text)
        await state.set_state(IdState.awaiting_photo)
    else:
        await msg.answer("Не пытайтесь сломать меня!")


@router.message(IdState.awaiting_photo)
async def awaiting_photo(msg: Message, state: FSMContext, bot: Bot):
    if msg.photo or msg.document:
        data = await state.get_data()
        client_id = data.get("user_id")
        uniq_id = data.get("uniq")
        invoice = await sync_to_async(Invoice.objects.get)(uniq_id=uniq_id)
        description = data.get("desc")
        admin = await sync_to_async(TelegramUser.objects.filter)(is_admin=True)
        admin = admin.first()
        await msg.forward(admin.user_id)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Ответить", callback_data=f"answer_to_{client_id}"))
        await bot.send_message(chat_id=admin.user_id, text=admin_text.format(
            client_id=client_id, bot=invoice.bot_user, uniq_id=uniq_id, desc=description), reply_markup=builder.as_markup())
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Завершить")]], resize_keyboard=True)
        await msg.answer("Переводим на оператора...", reply_markup=keyboard)
        await state.set_state(IdState.chat_with_admin)
    else:
        await msg.answer(f"Прикрепите чек или скриншот отправки:")


@router.message(IdState.chat_with_admin)
async def chat_with_admin(msg: Message, state: FSMContext, bot: Bot):
    if msg.text == "❌ Завершить":
        await msg.answer("Чат завершен")
        await state.clear()
    else:
        data = await state.get_data()
        client_id = data.get("user_id")
        uniq_id = data.get("uniq")
        invoice = await sync_to_async(Invoice.objects.get)(uniq_id=uniq_id)
        description = data.get("desc")
        admin = await sync_to_async(TelegramUser.objects.filter)(is_admin=True)
        admin = admin.first()
        await msg.forward(admin.user_id)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Ответить", callback_data=f"answer_to_{client_id}"))
        await bot.send_message(chat_id=admin.user_id, text=admin_text.format(
            client_id=client_id, bot=invoice.bot_user, uniq_id=uniq_id, desc=description),
                               reply_markup=builder.as_markup())


class AdminAnswer(StatesGroup):
    awaiting_text = State()


@router.callback_query(F.data.startswith("answer_to_"))
async def answer_to_client(call: CallbackQuery, state: FSMContext):
    data = call.data.split("_")
    client_id = data[2]
    await state.set_state(AdminAnswer.awaiting_text)
    await state.update_data(client_id=client_id)
    await state.set_state(AdminAnswer.awaiting_text)
    await call.answer("Введите текст для клиента")


@router.message(AdminAnswer.awaiting_text)
async def awaiting_text(msg: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    client_id = data.get("client_id")
    await bot.send_message(text=msg.text, chat_id=client_id)
    await msg.answer(f"Отправлено сообщение: {msg.text}")
