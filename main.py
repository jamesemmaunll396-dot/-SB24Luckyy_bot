
import logging
import os
from urllib.parse import quote

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ------------------------------------------------------------
# FOOTBALL NEWS HUB
# No football API key or news API key required.
#
# Required Render Environment variable:
# BOT_TOKEN
#
# Start command:
# python main.py
# ------------------------------------------------------------

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("football_news_hub")


WELCOME_TEXT = (
    "Welcome to Football News Hub! ⚽\n\n"
    "Find football news, league coverage, match schedules and team updates "
    "using the menu below.\n\n"
    "Choose a category to get started."
)


ABOUT_TEXT = (
    "ℹ️ ABOUT FOOTBALL NEWS HUB\n\n"
    "Football News Hub is an independent football information bot. "
    "It is not an official account of FIFA, UEFA, any football club, league "
    "or news publisher.\n\n"
    "This simple version provides links to external football news and "
    "competition websites. It does not fetch live scores or reproduce "
    "third-party articles.\n\n"
    "External websites and their content belong to their respective owners."
)


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------

MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "📰 Latest Football News",
            callback_data="news"
        ),
        InlineKeyboardButton(
            "📅 Match Updates",
            callback_data="matches"
        ),
    ],
    [
        InlineKeyboardButton(
            "🏆 League News",
            callback_data="leagues"
        ),
        InlineKeyboardButton(
            "🔄 Transfer News",
            callback_data="transfers"
        ),
    ],
    [
        InlineKeyboardButton(
            "🌍 International Football",
            callback_data="international"
        ),
        InlineKeyboardButton(
            "👥 Team News",
            callback_data="teams"
        ),
    ],
    [
        InlineKeyboardButton(
            "ℹ️ About & Sources",
            callback_data="about"
        ),
    ],
])


BACK_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "⬅️ Back to Menu",
            callback_data="menu"
        )
    ]
])


# ------------------------------------------------------------
# FOOTBALL NEWS SOURCES
# ------------------------------------------------------------

NEWS_LINKS = [
    (
        "BBC Sport Football",
        "https://www.bbc.com/sport/football"
    ),
    (
        "Sky Sports Football",
        "https://www.skysports.com/football"
    ),
    (
        "ESPN Soccer",
        "https://www.espn.com/soccer/"
    ),
]


# ------------------------------------------------------------
# MATCH UPDATES
# ------------------------------------------------------------

MATCH_LINKS = [
    (
        "Premier League Fixtures",
        "https://www.premierleague.com/fixtures"
    ),
    (
        "UEFA Fixtures",
        "https://www.uefa.com/uefachampionsleague/fixtures/"
    ),
    (
        "ESPN Soccer Scores",
        "https://www.espn.com/soccer/scoreboard"
    ),
]


# ------------------------------------------------------------
# FOOTBALL LEAGUES
# ------------------------------------------------------------

LEAGUE_LINKS = [
    (
        "Premier League",
        "https://www.premierleague.com/"
    ),
    (
        "La Liga",
        "https://www.laliga.com/en-GB"
    ),
    (
        "Bundesliga",
        "https://www.bundesliga.com/en/bundesliga"
    ),
    (
        "Serie A",
        "https://www.legaseriea.it/en"
    ),
    (
        "Ligue 1",
        "https://www.ligue1.com/"
    ),
    (
        "UEFA Champions League",
        "https://www.uefa.com/uefachampionsleague/"
    ),
]


# ------------------------------------------------------------
# TRANSFER NEWS
# ------------------------------------------------------------

TRANSFER_LINKS = [
    (
        "BBC Sport Transfers",
        "https://www.bbc.com/sport/football/transfers"
    ),
    (
        "Sky Sports Transfers",
        "https://www.skysports.com/transfer"
    ),
    (
        "ESPN Soccer News",
        "https://www.espn.com/soccer/"
    ),
]


# ------------------------------------------------------------
# INTERNATIONAL FOOTBALL
# ------------------------------------------------------------

INTERNATIONAL_LINKS = [
    (
        "FIFA",
        "https://www.fifa.com/"
    ),
    (
        "CAF",
        "https://www.cafonline.com/"
    ),
    (
        "UEFA",
        "https://www.uefa.com/"
    ),
    (
        "CONCACAF",
        "https://www.concacaf.com/"
    ),
]


# ------------------------------------------------------------
# CREATE LINK BUTTONS
# ------------------------------------------------------------

def links_menu(items):

    rows = [
        [
            InlineKeyboardButton(
                label,
                url=url
            )
        ]
        for label, url in items
    ]

    rows.append([
        InlineKeyboardButton(
            "⬅️ Back to Menu",
            callback_data="menu"
        )
    ])

    return InlineKeyboardMarkup(rows)


# ------------------------------------------------------------
# START COMMAND
# ------------------------------------------------------------

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    context.user_data.pop("waiting_for_team", None)

    if update.message:

        await update.message.reply_text(
            WELCOME_TEXT,
            reply_markup=MAIN_MENU
        )

        logger.info(
            "User %s started the bot",
            update.effective_user.id
        )


# ------------------------------------------------------------
# HELP COMMAND
# ------------------------------------------------------------

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message:

        await update.message.reply_text(
            "How to use Football News Hub ⚽\n\n"
            "1. Send /start to open the menu.\n"
            "2. Choose a football category.\n"
            "3. Select a source to open its website.\n\n"
            "Use /about to learn about this bot.",
            reply_markup=MAIN_MENU
        )


# ------------------------------------------------------------
# ABOUT COMMAND
# ------------------------------------------------------------

async def about_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message:

        await update.message.reply_text(
            ABOUT_TEXT,
            reply_markup=BACK_MENU,
            disable_web_page_preview=True
        )


# ------------------------------------------------------------
# INLINE BUTTON HANDLER
# ------------------------------------------------------------

async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if not query:
        return

    await query.answer()

    choice = query.data

    context.user_data.pop("waiting_for_team", None)

    if choice == "menu":

        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=MAIN_MENU
        )

    elif choice == "news":

        await query.edit_message_text(
            "📰 LATEST FOOTBALL NEWS\n\n"
            "Choose a publisher to read its latest football coverage. "
            "This bot opens the original websites rather than copying articles.",
            reply_markup=links_menu(NEWS_LINKS),
            disable_web_page_preview=True
        )

    elif choice == "matches":

        await query.edit_message_text(
            "📅 MATCH UPDATES\n\n"
            "Choose a source to check fixtures, match schedules and scores. "
            "Match information is displayed on the linked website.",
            reply_markup=links_menu(MATCH_LINKS),
            disable_web_page_preview=True
        )

    elif choice == "leagues":

        await query.edit_message_text(
            "🏆 LEAGUE NEWS\n\n"
            "Choose a competition website for league news and updates.",
            reply_markup=links_menu(LEAGUE_LINKS),
            disable_web_page_preview=True
        )

    elif choice == "transfers":

        await query.edit_message_text(
            "🔄 TRANSFER NEWS\n\n"
            "Choose a football publisher to read transfer coverage "
            "and reports.",
            reply_markup=links_menu(TRANSFER_LINKS),
            disable_web_page_preview=True
        )

    elif choice == "international":

        await query.edit_message_text(
            "🌍 INTERNATIONAL FOOTBALL\n\n"
            "Choose a football governing body for international "
            "competition news and announcements.",
            reply_markup=links_menu(INTERNATIONAL_LINKS),
            disable_web_page_preview=True
        )

    elif choice == "teams":

        context.user_data["waiting_for_team"] = True

        await query.edit_message_text(
            "👥 TEAM NEWS\n\n"
            "Send the name of a club or national team. "
            "I will prepare a link to search for its latest football news.",
            reply_markup=BACK_MENU
        )

    elif choice == "about":

        await query.edit_message_text(
            ABOUT_TEXT,
            reply_markup=BACK_MENU,
            disable_web_page_preview=True
        )

    else:

        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=MAIN_MENU
        )


# ------------------------------------------------------------
# TEAM NEWS SEARCH
# ------------------------------------------------------------

async def handle_team_name(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message or not update.message.text:
        return

    if not context.user_data.get("waiting_for_team"):

        await update.message.reply_text(
            "Send /start to open the football menu.",
            reply_markup=MAIN_MENU
        )

        return

    team_name = update.message.text.strip()[:80]

    context.user_data.pop("waiting_for_team", None)

    if not team_name:

        await update.message.reply_text(
            "Please send a team name.",
            reply_markup=MAIN_MENU
        )

        return

    search_url = (
        "https://news.google.com/search?q="
        + quote(f"{team_name} football")
        + "&hl=en-GB&gl=GB&ceid=GB:en"
    )

    await update.message.reply_text(
        f"👥 TEAM NEWS: {team_name}\n\n"
        "Use the button below to find football news about this team.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "Search Team News",
                    url=search_url
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Back to Menu",
                    callback_data="menu"
                )
            ],
        ]),
        disable_web_page_preview=True
    )


# ------------------------------------------------------------
# ERROR HANDLER
# ------------------------------------------------------------

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    error = context.error

    if error:

        logger.error(
            "Bot update error: %s",
            error,
            exc_info=(
                type(error),
                error,
                error.__traceback__
            )
        )


# ------------------------------------------------------------
# MAIN APPLICATION
# ------------------------------------------------------------

def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN is missing. Add your BotFather token "
            "in Render > Environment. Do not put it directly in this file."
        )

    logger.info("Starting Football News Hub bot")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CommandHandler("about", about_command)
    )

    application.add_handler(
        CallbackQueryHandler(menu_callback)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_team_name
        )
    )

    application.add_error_handler(error_handler)

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=False
    )


# ------------------------------------------------------------
# RUN BOT
# ------------------------------------------------------------

if __name__ == "__main__":

    main()
