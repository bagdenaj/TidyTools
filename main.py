from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from jnius import autoclass
from kivy.logger import Logger

from kivy.utils import platform

# if platform == 'android':
#     from jnius import autoclass, cast
#     JS = autoclass('java.lang.String')
#     Intent = autoclass('android.content.Intent')
#     PythonActivity = autoclass('org.kivy.android.PythonActivity')
#     currentActivity = cast('android.app.Activity', PythonActivity.mActivity)

KV = '''
<ManufacturesSelect>:
    id: manufacture_select
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        pos_hint:{'y': 0.85}

        BoxLayout:
            size_hint_y: None
            height: self.minimum_height

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_field
                hint_text: 'Search for Manufacturer'
                on_text: 
                    root.set_manf_list(self.text)

    RecycleView:
        pos_hint:{'center_y': 0.4}

        MDList:
            id: manufacture

    BoxLayout:
        id: tool_select

<ToolSelect>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        pos_hint:{'y': 0.75}
        
        BoxLayout:
            size_hint_y: None
            height: self.minimum_height

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_tool
                hint_text: 'Search for tool'
                on_text: 
                    root.set_tools_list(self.text)

    RecycleView:
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}

        MDList:
            id: tools
    

'''

manufactures = [
    "Stihl",
    "Obi",
    "ABUS",
    "Bosch",
    "HYMER"
]

tools = [
    "Kettensäge",
    "Presslufthammer",
    "Schleifgerät",
    "Nagel"
]


def set_schedule(title):
    try:
        System = autoclass ('java.lang.System')
        Intent = autoclass('android.content.Intent')
        intent = Intent()
        Calendar = autoclass('java.util.Calendar')
        calendar = Calendar.getInstance()
        calendar.setTimeInMillis(System.currentTimeMillis())
        intent.setType("vnd.android.cursor.item/event")
        intent.putExtra(Events.TITLE, title)
        intent.putExtra(Events.RRULE, "FREQ=WEEKLY;BYDAY=MO;COUNT=3")
        intent.putExtra("title", "A Test Event from android app")
        intent.setAction(intent.ACTION_INSERT)
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        PythonActivity.mActivity.startActivity(intent)
    except Exception as err:
            Logger.exception(err)

class ManufacturesSelect(Screen):
    def __init__(self, **kwargs) -> None:
        super(ManufacturesSelect, self).__init__(**kwargs)

    def add_toolselect(self):
        try:
            toolselect = ToolSelect()
            self.ids.tool_select.add_widget(toolselect)
        except Exception as err:
            Logger.exception(err)

    def pressed(self, value):
        try:
            self.ids.manufacture.clear_widgets()
            self.ids.search_field.text = value.text + " "
            self.add_toolselect()
        except Exception as err:
            Logger.exception(err)


    def set_manf_list(self, text=" "):
        try:
            self.ids.tool_select.clear_widgets()
            self.ids.manufacture.clear_widgets()
            for man in manufactures:
                if text.casefold() in man.casefold():
                    self.ids.manufacture.add_widget(
                        OneLineListItem(text=man,on_press=self.pressed)
                    )
        except Exception as err:
            Logger.exception(err)

class ToolSelect(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super(ToolSelect, self).__init__(**kwargs)

    def pressed(self, value):
        try:
            self.ids.tools.clear_widgets()
            self.ids.search_tool.text = value.text + " "
            # need to somehow disable set_list() after here
            set_schedule(value.text)
        except Exception as err:
            Logger.exception(err)



    def set_tools_list(self, text=" "):
        try:
            self.ids.tools.clear_widgets()
            for tool in tools:
                if text.casefold() in tool.casefold():
                    self.ids.tools.add_widget(
                        OneLineListItem(text=tool,on_press=self.pressed)
                    )
        except Exception as err:
            Logger.exception(err)


class Test(MDApp):
    def build(self):
        Logger.info("Building app")
        Builder.load_string(KV)
        
        self.screen = ManufacturesSelect(name="manufacture_select")
        Logger.info("Screen instanciated")
        return self.screen

    def on_start(self):
        Logger.info("On_start")
        self.screen.set_manf_list()

Test().run()