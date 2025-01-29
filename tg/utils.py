from .models import Invoice
from asgiref.sync import sync_to_async
from .text import invoice_changer_text
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def invoice_checker(bot):
    while True:
        invoices = await sync_to_async(Invoice.objects.filter)(new_invoice=True)
        if invoices:
            builder = InlineKeyboardBuilder()
            for invoice in invoices:
                text = invoice_changer_text.format(uniq=invoice.uniq_id, req=invoice.req.req, amount=invoice.amount,
                                                   bank_name=invoice.req.name)
                builder.add(InlineKeyboardButton(text="Принять", callback_data=f"accept_inv_{invoice.id}"))
                await bot.send_message(chat_id=invoice.req.user.user_id, text=text)
                invoice.new_invoice = False
                invoice.save()