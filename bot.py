import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки из переменных окружения
TOKEN = os.environ.get('TOKEN')
YOUR_CHAT_ID = os.environ.get('YOUR_CHAT_ID')

# Полное меню из 15 блюд
menu = {
    "coffee": {
        "name": "☕️ Кофе/чай",
        "desc": "Ароматный кофе без сахара или мягкий и греющий душу чай для моей королевы",
        "price": 1
    },
    "sandwich": {
        "name": "🥪 Бутерброд",
        "desc": "Неоспоримая классика: просто, вкусно, быстро",
        "price": 5
    },
    "tuna": {
        "name": "🥑 Бутерброд с тунцом и авокадо",
        "desc": "Хрустящий тост с неповторимым вкусом авокадо и тунца! То что надо для начала дня",
        "price": 10
    },
    "salmon": {
        "name": "🐟 Бутерброд с красной рыбой",
        "desc": "Дорого богато: все лучшее для дамы сердца великого шеф-повара...",
        "price": 15
    },
    "scramble": {
        "name": "🥚 Скрэмбл",
        "desc": "Нежнейший сливочный омлет в сочетании со всем, что найдется в холодильнике",
        "price": 10
    },
    "pancakes": {
        "name": "🥞 Блины",
        "desc": "Кручу-верчу обворожить кулинарными способностями хочу! Начинка для блинов за отдельную цену...)",
        "price": 20
    },
    "porridge": {
        "name": "🥣 Манная каша!!!",
        "desc": "Невозможно было оставить без внимания это грандиозное блюдо! Фирменный рецепт специально для Вас, моя любовь!",
        "price": 1
    },
    "cutlets": {
        "name": "🍽 Рубленные котлеты с гарниром",
        "desc": "Простой, но очень вкусный рецепт! Всеми любимые котлеты с нежным и утонченным вкусом, отличный выбор!",
        "price": 15
    },
    "cheeseburger": {
        "name": "🍔 Двойной чизбургер",
        "desc": "Шеф-повар не сильно одобряет.... Но как будто и Биг спэшл охото!",
        "price": 15
    },
    "cake": {
        "name": "🍰 Торт",
        "desc": "Иногда можно и сладенькое попробовать! Вашему вниманию авторский чизкейк с разнообразием ягод и начинок",
        "price": 20
    },
    "pie": {
        "name": "🥧 Пирог",
        "desc": "Ну мёёёёёёд! И хруст безе и всё причастное соответственно. Начинка на Ваш выбор!",
        "price": 20
    },
    "curry": {
        "name": "🍛 Карри",
        "desc": "Тушеная курочка с овощами - что может быть лучше? Только курочка с карри!",
        "price": 15
    },
    "dumplings": {
        "name": "🥟 Пельмешки",
        "desc": "Ну тут без комментариев, зай... Просто, вкусно и неповторимо. По всем стандартам ГОСТ - со сметаной",
        "price": 7
    },
    "teriyaki": {
        "name": "🍗 Курочка терияки",
        "desc": "Отличный рецепт для разнообразия кухни. Разнообразь свое вкусовое предпочтение кисло-сладким вкусом курочки",
        "price": 15
    },
    "lasagna": {
        "name": "🧀 Лазанья",
        "desc": "Ну это ЛЕГЕНДА! Наша фирменная! Блюдо, при котором шеф-повар уступает свое место на поприще кулинарии и становится подмастерьем великого мастера",
        "price": 20
    }
}

compliments = [
    "Зая, ты — мое самое сладкое настроение! 🍯",
    "Зая, без тебя даже солнце не такое яркое. 🌞➡️🌚",
    "Зая, ты — мой личный магнит, который притягивает счастье. 🧲💘",
    "Зая, с тобой даже дождь превращается в романтику. ☔️💕",
    "Зая, ты — мой единственный повод для улыбки с утра. 😌🌅",
    "Ты — самое красивое солнце в моей галактике! ☀️",
    "С тобой даже обычный день становится волшебным. ✨",
    "Твой смех — мой самый любимый звук. 😊",
    "Ты вдохновляешь меня каждый день. 💫",
    "Как же повезло вселенной, что ты в ней есть! 🌌",
    "Ты словно утренний кофе — бодришь и согреваешь. ☕️",
    "Рядом с тобой время останавливается. ⏳",
    "Ты — мой личный антистресс. 💆‍♂️💖",
    "Твой взгляд заряжает меня на весь день. 🔋",
    "Ты — воплощение нежности и силы одновременно. 🌸💪"
]

user_cart = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение с меню"""
    menu_items = list(menu.items())
    keyboard = []
    
    # Создаем кнопки меню (2 в ряд)
    for i in range(0, len(menu_items), 2):
        row = []
        for j in range(i, min(i+2, len(menu_items))):
            item = menu_items[j]
            row.append(InlineKeyboardButton(
                f"{item[1]['name']} 💋 {item[1]['price']}",
                callback_data=item[0]
            ))
        keyboard.append(row)
    
    # Кнопка корзины
    user_id = update.effective_user.id
    cart_text = "🛒 Корзина пуста"
    if user_id in user_cart and user_cart[user_id]["items"]:
        cart_text = f"🛒 Корзина ({len(user_cart[user_id]['items'])}) 💋 {user_cart[user_id]['total_kisses']}"
    
    keyboard.append([InlineKeyboardButton(cart_text, callback_data="cart")])
    
    await update.message.reply_text(
        "💝 Привет, Зая! Выбери, что я приготовлю сегодня:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "cart":
        await show_cart(query, context)
        return
    if query.data == "checkout":
        await checkout(query, context)
        return
    if query.data == "back":
        await start(update, context)
        return
    
    if user_id not in user_cart:
        user_cart[user_id] = {"items": [], "total_kisses": 0}
    
    dish = menu[query.data]
    user_cart[user_id]["items"].append(dish["name"])
    user_cart[user_id]["total_kisses"] += dish["price"]
    
    await query.edit_message_text(
        text=f"✅ Добавлено: {dish['name']}\n{dish['desc']}\nЦена: 💋 {dish['price']}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Корзина", callback_data="cart")],
            [InlineKeyboardButton("📋 Меню", callback_data="back")]
        ])
    )

async def show_cart(query, context):
    """Показ корзины"""
    user_id = query.from_user.id
    if user_id not in user_cart or not user_cart[user_id]["items"]:
        text = "🛒 Корзина пуста!"
    else:
        items = "\n".join(f"• {item}" for item in user_cart[user_id]["items"])
        text = f"🛒 Твой заказ:\n{items}\n\nВсего: 💋 {user_cart[user_id]['total_kisses']} поцелуев"
    
    buttons = [
        [InlineKeyboardButton("✅ Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton("📋 Меню", callback_data="back")]
    ]
    
    await query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def checkout(query, context):
    """Оформление заказа"""
    user_id = query.from_user.id
    if user_id in user_cart and user_cart[user_id]["items"]:
        # Отправка уведомления вам
        order = ", ".join(user_cart[user_id]["items"])
        total = user_cart[user_id]["total_kisses"]
        await context.bot.send_message(
            chat_id=YOUR_CHAT_ID,
            text=f"💌 Новый заказ от @{query.from_user.username}!\nБлюда: {order}\nСумма: 💋 {total} поцелуев"
        )
        
        # Ответ пользователю
        await query.edit_message_text(
            text=f"{random.choice(compliments)}\nСпасибо за заказ, Зая! Оплата: 💋 {total} поцелуев! Готовлю с любовью! ❤️"
        )
        user_cart[user_id] = {"items": [], "total_kisses": 0}

def main():
    """Запуск бота"""
    port = int(os.environ.get('PORT', 5000))
    
    app = Application.builder() \
        .token(TOKEN) \
        .read_timeout(30) \
        .write_timeout(30) \
        .build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_query))

    # Для Render
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        secret_token='RENDER_SECRET',
        webhook_url=f"https://your-app-name.onrender.com/{TOKEN}"
    )

if __name__ == "__main__":
    main()