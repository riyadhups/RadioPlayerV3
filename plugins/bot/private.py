"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import Config
from utils import USERNAME, mp
from pyrogram import Client, filters, emoji
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

msg=Config.msg
ADMINS=Config.ADMINS
CHAT_ID=Config.CHAT_ID
playlist=Config.playlist
LOG_GROUP=Config.LOG_GROUP

HOME_TEXT = "👋🏻 **Hi [{}](tg://user?id={})**,\n\nI'm **Radio Player V3.0** \nKanalda və Qrupda 7x24 fasiləsiz Radio / Musiqi / YouTube Canlı Oynaya bilər. @TheThagiyevv tərəfindən  hazırlanmışdır 😉!"
HELP_TEXT = """
💡 --**Ayarlamaq**--:

\u2022 Əlavə Et.Admin hüquqları ilə qrupunuza bot və istifadəçi hesabını əlavə edin
\u2022 Qrupunuzda səsli söhbətə başlayın və vc-yə qoşulmadıqda botu yenidən başla.
\u2022 Cavab olaraq /play [mahnı adı] və ya /play istifadə edin
💡 --**Common Commands**--:

\u2022 `/help` - bütün əmrlər üçün yardım göstərir
\u2022 `/song` - mahnı [mahnı adı] - mahnını audio kimi endirin
\u2022 `/current` - idarəetmə ilə cari treki göstərir
\u2022 `/playlist` - cari və növbəli pleylistini göstərir

💡 --**Admin Əmirləri**--:

\u2022 `/radio` - radio axını başladın
\u2022 `/stopradio` - radio axını dayandırın
\u2022 `/skip` - skip current music
\u2022 `/join` - səsli söhbətə qoşulun
\u2022 `/leave` - səsli söhbəti tərk edin
\u2022 `/stop` - musiqi çalmağı dayandırın
\u2022 `/ses` - səs həcmi (0-200)
\u2022 `/replay` - əvvəldən oynayın
\u2022 `/clean` - istifadə olunmamış xam faylları silin
\u2022 `/pause` - musiqi oxumağa fasilə verin
\u2022 `/resume` - musiqi oxumağa davam edin
\u2022 `/mute` - səssizə atar
\u2022 `/unmute` - səsi açar 
\u2022 `/restart` - botu yeniden başlat 
\u2022 `/setvar` - ...

© **Powered By** : 
**@TheThagiyevv | @RiyaddSup** 👑
"""


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.from_user.id not in Config.ADMINS and query.data != "help":
        await query.answer(
            "Sizə İcazə Verilmir! 🤣",
            show_alert=True
            )
        return

    if query.data.lower() == "replay":
        group_call = mp.group_call
        if not playlist:
            await query.answer("⛔️ Boş Playlist !", show_alert=True)
            return
        group_call.restart_playout()
        if not playlist:
            pl = f"{emoji.NO_ENTRY} **Boş Playlist!**"
        else:
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer(" 😁 Təkrarlanır !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏸", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "pause":
        if not playlist:
            await query.answer("⛔️ Boş Playlist !", show_alert=True)
            return
        else:
            mp.group_call.pause_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("⏸ Yayım dayandırıldı  !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("▶️", callback_data="resume"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "resume":   
        if not playlist:
            await query.answer("⛔️ Boş Playlist !", show_alert=True)
            return
        else:
            mp.group_call.resume_playout()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("▶️ Yenidən Davam edir !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏸", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "skip":   
        if not playlist:
            await query.answer("⛔️ Boş Playlist !", show_alert=True)
            return
        else:
            await mp.skip_current_playing()
            pl = f"{emoji.PLAY_BUTTON} **Playlist**:\n" + "\n".join([
                f"**{i}**. **{x[1]}**\n  - **Requested By:** {x[4]}"
                for i, x in enumerate(playlist)
                ])
        try:
            await query.answer("⏩ Uğurla Dəyişilir !", show_alert=True)
            await query.edit_message_text(f"{pl}",
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔄", callback_data="replay"),
                                InlineKeyboardButton("⏸", callback_data="pause"),
                                InlineKeyboardButton("⏩", callback_data="skip")
                            ],
                        ]
                    )
                )
        except MessageNotModified:
            pass

    elif query.data.lower() == "help":
        buttons = [
            [
                InlineKeyboardButton("Mahnılar Axtarın", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("🇦🇿 Rəsmi Kanal", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/RiyaddSup"),
            ],
            [
                InlineKeyboardButton("Daha Çox Botlar", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("Mənbə kodu", url="https://github.com/Riyaddzr/RadioPlayeV"),
            ],
            [
                InlineKeyboardButton("Evə Qayıt", callback_data="home"),
                InlineKeyboardButton("Menyü Bağla", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HELP_TEXT,
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "home":
        buttons = [
            [
                InlineKeyboardButton("Mahnılar Axtarın", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("🇦🇿Rəsmi Kanal", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/RiyaddSup"),
            ],
            [
                InlineKeyboardButton("Daha çox Botlar", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("mənbə kodu", url="https://github.com/riyadds/musics"),
            ],
            [
                InlineKeyboardButton("❔ Necə Kömək edə Bilərəm ❔", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await query.edit_message_text(
                HOME_TEXT.format(query.from_user.first_name, query.from_user.id),
                reply_markup=reply_markup
            )
        except MessageNotModified:
            pass

    elif query.data.lower() == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            pass

    await query.answer()



@Client.on_message(filters.command(["start", f"start@{USERNAME}"]))
async def start(client, message):
    buttons = [
            [
                InlineKeyboardButton("Mahnı Axtarın", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("🇦🇿Rəsmi Kanal", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/RiyaddSup"),
            ],
            [
                InlineKeyboardButton("Daha çox Botlar", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("Mənbə kodu", url="https://github.com/getdanasencani/hzrideyl"),
            ],
            [
                InlineKeyboardButton("❔ Necə Kömək Edə Bilərəm ❔", callback_data="help"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    m=await message.reply_photo(photo="https://images.app.goo.gl/uZrfqvgS2EQ1vUZ38", caption=HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await mp.delete(m)
    await mp.delete(message)


@Client.on_message(filters.command(["help", f"help@{USERNAME}"]))
async def help(client, message):
    buttons = [
            [
                InlineKeyboardButton("Mahnı Axtarın", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("🇦🇿 Rəsmi Kanal", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("SUPPORT", url="https://t.me/RiyaddSup"),
            ],
            [
                InlineKeyboardButton("Daha çox Botlar", url="https://t.me/RiyaddBlog"),
                InlineKeyboardButton("SOURCE CODE", url="https://github.com/grtddbalam/hzdddyldehele"),
            ],
            [
                InlineKeyboardButton("Evə Qayıt", callback_data="home"),
                InlineKeyboardButton("Menyü Bağla", callback_data="close"),
            ]
            ]
    reply_markup = InlineKeyboardMarkup(buttons)
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_photo(photo="https://images.app.goo.gl/uZrfqvgS2EQ1vUZ38", caption=HELP_TEXT, reply_markup=reply_markup)
    await mp.delete(message)


@Client.on_message(filters.command(["setvar", f"setvar@{USERNAME}"]) & filters.user(ADMINS) & (filters.chat(CHAT_ID) | filters.private | filters.chat(LOG_GROUP)))
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        k=await message.reply_text(
            text="❗ *Heroku Tətbiqi Tapılmadı* !** \n__Heroku Bu Əmrə Aşağıdakı Heroku lazımdır  Quraşdırılmalı :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @AsmSupport !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        await mp.delete(k)
        await mp.delete(message)
        return
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            k=await message.reply_text("❗ **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001313215676`")
            await mp.delete(k)
            await mp.delete(message)
            return
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"❗ **Dəyər Müəyyən edilməyib, Beləliklə, Silinir `{var}` Dəyişən !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"🗑 **Uğurla Silindi `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"🤷‍♂️ **Adlandırılmış dəyişən `{var}` Tapılmadı, Heç nə Dəyişilmədi !**")
            return
        if var in config:
            m=await message.reply_text(f"⚠️ **Dəyişən Artıq Tapılıb, Beləki redoktor dəyəri`{value}` !**")
        else:
            m=await message.reply_text(f"⚠️ **Dəyişən tapılmadı, ona görə də yeni Var kimi təyin olunur! !**")
        await asyncio.sleep(2)
        await m.edit(f"✅ **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
        await mp.delete(m)
        await mp.delete(message)
        return
    else:
        k=await message.reply_text("❗ **Siz heç bir dəyişən təqdim etməmisiniz, düzgün formata əməl etməlisiniz !** \n\nFor Example: \n• `/setvar CHAT_ID=-1001313215676` to change or set CHAT var. \n• `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.")
        await mp.delete(k)
        await mp.delete(message)
