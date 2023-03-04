import flet as ft
from logit import log
from grep.search import SearchPage


class HomePage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.col = []
        self.create_ui()

    def on_search(self, e) -> None:
        if not self.substring_field.value or not self.location_field.value:
            return
        self.page.clean()
        self.search_page = SearchPage(
            self.page,
            {
                "location": self.location_field.value,
                "substring": self.substring_field.value,
            },
        )

    def create_ui(self) -> None:
        self.create_directory_ui()
        self.create_search_ui()
        self.finalize_ui()

    def create_directory_ui(self) -> None:
        # self.row.append(ft.Text("Enter Directory:"))
        self.location_field = ft.TextField(
            value="D:/d/p/logit/",
            label="Location",
            hint_text="src/",
            hint_style=ft.TextStyle(weight=ft.FontWeight.W_100),
            icon=ft.icons.FOLDER_OUTLINED,
            width=250,
            height=50,
            on_submit=self.on_search,
        )
        self.col.append(
            ft.Container(
                self.location_field,
                padding=ft.Padding(0, 20, 0, 0),
            )
        )

    def create_search_ui(self) -> None:
        self.substring_field = ft.TextField(
            label="Substring",
            value="run",
            hint_text="potato",
            hint_style=ft.TextStyle(weight=ft.FontWeight.W_100),
            icon=ft.icons.TEXT_FORMAT_OUTLINED,
            width=250,
            height=50,
            on_submit=self.on_search,
        )
        self.col.append(
            ft.Container(
                self.substring_field,
                padding=ft.Padding(0, 20, 0, 0),
            )
        )
        self.col.append(
            ft.Container(
                ft.OutlinedButton("Search", on_click=self.on_search),
                padding=ft.Padding(0, 20, 0, 0),
            )
        )

    def finalize_ui(self) -> None:
        row = ft.Row([ft.Column(self.col)], alignment=ft.MainAxisAlignment.CENTER)
        self.page.add(row)
