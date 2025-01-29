import asyncio
import random
from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from tg.models import TelegramUser, Invoice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.filters import Command, CommandObject
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
        invoice.amount = amount
        invoice.is_complete = True
        invoice.save()
        await msg.answer(f"Платеж принят {amount} Т")
        await state.clear()
    except Exception as e:
        print(e)

@router.message(Command("start"))
async def start(msg: Message, command: CommandObject, edit=None):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=msg.from_user.id)
    user.first_name = msg.from_user.first_name
    user.last_name = msg.from_user.last_name
    user.username = msg.from_user.username
    user.save()