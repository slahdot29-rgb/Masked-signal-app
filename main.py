import os
import json
import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import StringProperty

# Android safe path
KEYS_FILE = os.path.join(App.get_running_app().user_data_dir, "keys.json")
key_unlocked = False

def load_keys():
    if not os.path.exists(KEYS_FILE):
        os.makedirs(os.path.dirname(KEYS_FILE), exist_ok=True) # create folder
        keys = {f"KEY{i:03d}": False for i in range(100, 110)}
        with open(KEYS_FILE, 'w') as f: json.dump(keys, f)
    with open(KEYS_FILE, 'r') as f: return json.load(f)

def use_key(key):
    keys = load_keys()
    key = key.strip() # remove spaces
    if key in keys and keys[key] == False:
        keys[key] = True
        with open(KEYS_FILE, 'w') as f: json.dump(keys, f)
        return True
    return False

def get_price(symbol):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, timeout=10, headers=headers)
        return r.json()['price']
    except:
        return "ERROR"

class KeyScreen(Screen):
    status = StringProperty("Enter One-Time Key")
    def check_key(self, key_input):
        global key_unlocked
        if use_key(key_input):
            key_unlocked = True
            self.status = "Unlocked! Key burned."
            self.manager.current = "main"
        else:
            self.status = "Invalid or Already Used Key"

class MainScreen(Screen):
    status_text = StringProperty("Ready")
    signal_text = StringProperty("No signal yet")
    def get_signal(self, symbol):
        if not key_unlocked:
            self.signal_text = "App locked. Enter key first."
            return
        self.status_text = f"Fetching {symbol}..."
        price = get_price(symbol)
        if price == "ERROR":
            self.status_text = "No internet / API error"
        else:
            self.signal_text = f"{symbol}\nPrice: ${price}\nSignal: MANUAL CHECK"
            self.status_text = "Price fetched ✓"

    def check_status(self):
        self.status_text = "Bot running ✓" if key_unlocked else "Enter key first"

class SignalApp(App):
    def build(self):
        Builder.load_file('main.kv')
        sm = ScreenManager()
        sm.add_widget(KeyScreen(name="key"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    SignalApp().run()