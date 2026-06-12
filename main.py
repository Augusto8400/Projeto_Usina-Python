from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from kivy.lang import Builder
Builder.load_file("rfid.kv")

from threading import Thread
import time

# ==========================================
# TROQUE PELOS UIDs DOS SEUS CARTÕES
# ==========================================

ELETRON_UID = "806837355043"
MUON_UID    = "405708210738"
QUARK_UID   = "94625137157"

# ==========================================
# TELAS
# ==========================================

class HomeScreen(Screen):
    pass

class EletronScreen(Screen):
    pass

class MuonScreen(Screen):
    pass

class QuarkScreen(Screen):
    pass


# ==========================================
# APP
# ==========================================

class RFIDApp(App):

    def build(self):

        self.sm = ScreenManager()

        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(EletronScreen(name="eletron"))
        self.sm.add_widget(MuonScreen(name="muon"))
        self.sm.add_widget(QuarkScreen(name="quark"))

        Thread(target=self.rfid_loop, daemon=True).start()

        return self.sm

    def trocar_tela(self, tela):
        self.sm.current = tela

    def processar_uid(self, uid):

        uid = str(uid)

        print("UID lido:", uid)

        if uid == ELETRON_UID:
            Clock.schedule_once(
                lambda dt: self.trocar_tela("eletron")
            )

        elif uid == MUON_UID:
            Clock.schedule_once(
                lambda dt: self.trocar_tela("muon")
            )

        elif uid == QUARK_UID:
            Clock.schedule_once(
                lambda dt: self.trocar_tela("quark")
            )

        else:
            Clock.schedule_once(
                lambda dt: self.trocar_tela("home")
            )

    def rfid_loop(self):

        # ==================================
        # EXEMPLO REAL COM MFRC522
        # ==================================

        from mfrc522 import SimpleMFRC522

        reader = SimpleMFRC522()

        while True:

            try:

                uid, text = reader.read()

                self.processar_uid(uid)

                time.sleep(1)

            except Exception as e:
                print("Erro RFID:", e)
                time.sleep(2)


# ==========================================
# EXECUÇÃO
# ==========================================

RFIDApp().run()