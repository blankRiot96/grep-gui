import flet as ft
from grep.extra import RichText
from grep.homepage import HomePage


class App:
    def window_properties(self) -> None:
        self.page.title = "Grep GUI"
        self.page.window_width = 500
        self.page.window_height = 300

    def run(self, page: ft.Page) -> None:
        self.page = page
        self.window_properties()
        self.home_page = HomePage(page)

        # rt = RichText(
        #     "<style title_large>Hello</style> <c blue><bg blue_50>world</bg></c>, "
        #     "<f Courier>how</f> are <b>you</b> doing <c green_300><i>to</i>day</c>?",
        # )
        # page.add(rt)


def main() -> None:
    app = App()
    ft.app(target=app.run)
