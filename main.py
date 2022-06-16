from jnius import autoclass, cast
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem

# from kivy.utils import platform

# if platform == 'android':
#     from jnius import autoclass, cast
#     JS = autoclass('java.lang.String')
#     Intent = autoclass('android.content.Intent')
#     PythonActivity = autoclass('org.kivy.android.PythonActivity')
#     currentActivity = cast('android.app.Activity', PythonActivity.mActivity)

KV = """
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


"""

manufactures = ["Stihl", "Obi", "ABUS", "Bosch", "HYMER"]

tools = ["Kettensäge", "Presslufthammer", "Schleifgerät", "Nagel"]


# def set_schedule(self, tool):
#     try:
#         Intent = autoclass("android.content.Intent")
#         Calendar = autoclass("java.util.Calendar")
#         CalendarContract = autoclass("android.provider.CalendarContract")
#         Events = autoclass("android.provider.CalendarContract$Events")
#         self.intent = Intent()

#         self.begin_time = Calendar.getInstance()
#         self.end_time = Calendar.getInstance()
#         self.begin_time.set(2022, 5, 13, 7, 30)
#         self.end_time.set(2022, 5, 13, 13, 30)

#         self.intent.setData(Events.CONTENT_URI)
#         self.intent.putExtra(Events.TITLE, tool)
#         Logger.info(f"begin_time: {self.begin_time.getTime()}")
#         Logger.info(f"end_time: {self.end_time.getTime()}")
#         self.intent.putExtra(
#             CalendarContract.EXTRA_EVENT_BEGIN_TIME,
#             str(self.begin_time.getTimeInMillis()),
#         )
#         self.intent.putExtra(
#             CalendarContract.EXTRA_EVENT_END_TIME,
#             str(self.end_time.getTimeInMillis()),
#         )
#         self.intent.putExtra("description", "Some description")
#         self.intent.putExtra("rrule", "FREQ=WEEKLY;BYDAY=MO;COUNT=3")
#         Logger.info(f"intent: {self.intent}")
#         Logger.info(f"intent uri: {self.intent.toUri(0)}")
#         try:
#             Logger.info(
#                 f"intent extra: {self.intent.getStringArrayListExtra('description')}"
#             )
#         except Exception:
#             pass
#         try:
#             Logger.info(
#                 f"intent.getExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME): "
#                 f"{self.intent.getExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME)}"
#             )
#             Logger.info(
#                 f"intent.getExtra(CalendarContract.EXTRA_EVENT_END_TIME): "
#                 f"{self.intent.getExtra(CalendarContract.EXTRA_EVENT_END_TIME)}"
#             )
#             Logger.info(
#                 f"intent.getExtra('title'): {self.intent.getStringExtra('title')}"
#             )
#             Logger.info(
#                 f"intent.getExtra('rrule'): {self.intent.getStringExtra('rrule')}"
#             )
#         except Exception:
#             pass
#         self.intent.setAction(Intent.ACTION_INSERT)

#         PythonActivity = autoclass("org.kivy.android.PythonActivity")
#         currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
#         currentActivity.startActivity(self.intent)

#         # Tell the Python garbage collector this will not be reused
#         self.intent = None
#         self.begin_time = None
#         self.end_time = None
#     except Exception as err:
#         Logger.exception(err)


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
                        OneLineListItem(text=man, on_press=self.pressed)
                    )
        except Exception as err:
            Logger.exception(err)


class ToolSelect(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super(ToolSelect, self).__init__(**kwargs)

    def set_schedule(self, tool):
        try:
            Intent = autoclass("android.content.Intent")
            Calendar = autoclass("java.util.Calendar")
            CalendarContract = autoclass("android.provider.CalendarContract")
            Events = autoclass("android.provider.CalendarContract$Events")
            self.intent = Intent()

            self.begin_time = Calendar.getInstance()
            self.end_time = Calendar.getInstance()
            self.begin_time.set(2022, 5, 13, 7, 30)
            self.end_time.set(2022, 5, 13, 13, 30)

            self.intent.setData(Events.CONTENT_URI)
            self.intent.putExtra(Events.TITLE, tool)
            Logger.info(f"begin_time: {self.begin_time.getTime()}")
            Logger.info(f"end_time: {self.end_time.getTime()}")
            self.intent.putExtra(
                CalendarContract.EXTRA_EVENT_BEGIN_TIME,
                str(self.begin_time.getTimeInMillis()),
            )
            self.intent.putExtra(
                CalendarContract.EXTRA_EVENT_END_TIME,
                str(self.end_time.getTimeInMillis()),
            )
            self.intent.putExtra(Events.Description, "Some description")
            self.intent.putExtra(Events.RRULE, "FREQ=WEEKLY;BYDAY=MO;COUNT=3")
            Logger.info(f"intent: {self.intent}")
            Logger.info(f"intent uri: {self.intent.toUri(0)}")
            try:
                Logger.info(
                    f"intent extra: "
                    f"{self.intent.getStringArrayListExtra('description')}"
                )
            except Exception:
                pass
            try:
                Logger.info(
                    f"intent.getExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME): "
                    f"{self.intent.getExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME)}"
                )
                Logger.info(
                    f"intent.getExtra(CalendarContract.EXTRA_EVENT_END_TIME): "
                    f"{self.intent.getExtra(CalendarContract.EXTRA_EVENT_END_TIME)}"
                )
                Logger.info(
                    f"intent.getExtra('title'): {self.intent.getStringExtra('title')}"
                )
                Logger.info(
                    f"intent.getExtra('rrule'): {self.intent.getStringExtra('rrule')}"
                )
            except Exception:
                pass
            self.intent.setAction(Intent.ACTION_INSERT)

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            currentActivity = cast("android.app.Activity", PythonActivity.mActivity)
            currentActivity.startActivity(self.intent)

            # Tell the Python garbage collector this will not be reused
            self.intent = None
            self.begin_time = None
            self.end_time = None
        except Exception as err:
            Logger.exception(err)

    def pressed(self, value):
        try:
            self.ids.tools.clear_widgets()
            self.ids.search_tool.text = value.text + " "
            # need to somehow disable set_list() after here
            Logger.info(value.text)
            self.set_schedule(value.text)
        except Exception as err:
            Logger.exception(err)

    def set_tools_list(self, text=" "):
        try:
            self.ids.tools.clear_widgets()
            for tool in tools:
                if text.casefold() in tool.casefold():
                    self.ids.tools.add_widget(
                        OneLineListItem(text=tool, on_press=self.pressed)
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
