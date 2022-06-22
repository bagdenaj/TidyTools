import requests
from jnius import autoclass, cast
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.screen import MDScreen

KV = """
<ManufacturesSelect>:
    id: manufacture_select
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            spacing: dp(5)
            padding: dp(20)
            pos_hint:{'y': 0.9}

            MDBoxLayout:
                size_hint_y: None
                height: self.minimum_height

                MDIconButton:
                    icon: 'magnify'

                MDTextField:
                    id: search_field
                    hint_text: 'Search for Manufacturer'
                    on_text:
                        root.set_manf_list(self.text)

        MDScrollViewRefreshLayout:

            MDList:
                id: manufacture

        MDBoxLayout:
            id: tool_select

<ToolSelect>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        pos_hint:{'y': 0.75}

        MDBoxLayout:
            size_hint_y: None
            height: self.minimum_height

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_tool
                hint_text: 'Search for tool'
                on_text:
                    root.set_tools_list(self.text)

        MDScrollViewRefreshLayout:
            pos_hint:{'center_x': 0.5, 'center_y': 0.3}

            MDList:
                id: tools

        MDRectangleFlatButton:
            pos_hint:{'center_x': 0.5, 'center_y': 0.1}
            text: "Set schedules"
            theme_text_color: "Custom"
            text_color: 1, 0, 0, 1
            line_color: 0, 0, 1, 1
            on_release:
                root.set_tool_schedule(search_tool.text)

"""


def get_tools():
    response = requests.get("http://127.0.0.1:8000/get_tools")
    return response.json()


def get_manufactures():
    response = requests.get("http://127.0.0.1:8000/get_manufactures")
    return response.json()


def set_schedule(tool):
    if platform == "android":
        Intent = autoclass("android.content.Intent")
        Calendar = autoclass("java.util.Calendar")
        CalendarContract = autoclass("android.provider.CalendarContract")
        Events = autoclass("android.provider.CalendarContract$Events")
        JS = autoclass("java.lang.String")
        intent = Intent()

        date = Calendar.getInstance()
        date.set(2022, 5, 26, 7, 30)

        intent.setData(Events.CONTENT_URI)
        intent.putExtra(Events.TITLE, JS(tool))

        intent.putExtra(CalendarContract.EXTRA_EVENT_ALL_DAY, JS("true"))
        intent.putExtra(
            CalendarContract.EXTRA_EVENT_BEGIN_TIME,
            JS(str(date.getTimeInMillis())),
        )
        intent.putExtra(
            CalendarContract.EXTRA_EVENT_END_TIME,
            JS(str(date.getTimeInMillis())),
        )

        intent.putExtra(Events.DESCRIPTION, JS("Some description"))
        intent.putExtra(Events.RRULE, JS("FREQ=WEEKLY;BYDAY=MO;COUNT=3"))
        intent.setAction(Intent.ACTION_INSERT)

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
        currentActivity.startActivity(intent)
    if platform == "win":
        print(f"Now exporting {tool}")


class ManufacturesSelect(MDScreen):
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
            for man in get_manufactures():
                if text.casefold() in man[0].casefold():
                    self.ids.manufacture.add_widget(
                        OneLineListItem(text=man[0], on_press=self.pressed)
                    )
        except Exception as err:
            Logger.exception(err)


class ToolSelect(MDBoxLayout):
    def __init__(self, **kwargs) -> None:
        super(ToolSelect, self).__init__(**kwargs)

    def pressed(self, value):
        try:
            self.ids.tools.clear_widgets()
            self.ids.search_tool.text = value.text + " "
            # need to somehow disable set_list() after here
            # set_schedule(value.text)
        except Exception as err:
            Logger.exception(err)

    def set_tool_schedule(self, tool):
        set_schedule(tool)

    def set_tools_list(self, text=" "):
        try:
            self.ids.tools.clear_widgets()
            for tool in get_tools():
                if text.casefold() in tool[0].casefold():
                    self.ids.tools.add_widget(
                        OneLineListItem(text=tool[0], on_press=self.pressed)
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