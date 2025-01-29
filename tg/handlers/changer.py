import asyncio
import random
from aiogram import Router, Bot, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from tg.models import TelegramUser
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async

router = Router()

