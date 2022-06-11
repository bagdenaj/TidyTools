from turtle import onclick, onrelease
from unicodedata import name
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen, ScreenManager

KV = '''
<ManufacturesSelect>
    id: manufacture_select
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        pos_hint:{'center_x': 0.5, 'y': 0.85}

        BoxLayout:
            size_hint_y: None
            height: self.minimum_height

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: 
                    root.set_list(self.text)

    RecycleView:
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}

        MDList:
            id: container

<ToolSelect>
    id: tool_select

'''

manufactureres = [
    "Stihl",
    "Obi",
    "ABUS",
    "Bosch",
    "HYMER"
]


class ManufacturesSelect(Screen):
    def __init__(self, **kwargs) -> None:
        super(ManufacturesSelect, self).__init__(**kwargs)

    def pressed(self, value):
        print(value.text)


    def set_list(self, text=" "):
        self.ids.container.clear_widgets()
        for man in manufactureres:
            if text.casefold() in man.casefold():
                self.ids.container.add_widget(
                    OneLineListItem(text=man,on_press=self.pressed)
                )

class ToolSelect(Screen):
    pass


class Test(MDApp):
    def build(self):
        Builder.load_string(KV)
        
        self.screen = ManufacturesSelect(name="manufacture_select")
        return self.screen

    def on_start(self):
        self.screen.set_list()

Test().run()