import flet as ft
from logit import log


class HomePage:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.col = []
        self.create_ui()

    def on_search(self, e) -> None:
        ...

    def create_ui(self) -> None:
        self.create_directory_ui()
        self.create_search_ui()
        self.finalize_ui()

    def create_directory_ui(self) -> None:
        # self.row.append(ft.Text("Enter Directory:"))
        self.col.append(
            ft.Container(
                ft.TextField(
                    label="Location",
                    hint_text="src/",
                    hint_style=ft.TextStyle(weight=ft.FontWeight.W_100),
                    icon=ft.icons.FOLDER_OUTLINED,
                    width=250,
                    height=50,
                    on_submit=self.on_search,
                ),
                padding=ft.Padding(0, 50, 0, 0),
            )
        )

    def create_search_ui(self) -> None:
        self.col.append(
            ft.Container(ft.OutlinedButton("Search", on_click=self.on_search))
        )

    def finalize_ui(self) -> None:
        row = ft.Row([ft.Column(self.col)], alignment=ft.MainAxisAlignment.CENTER)
        self.page.add(row)
