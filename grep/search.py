import flet as ft
from pathlib import Path
from logit import log


class FileContainer:
    FONT_FAMILY = "Hack NF"

    def __init__(
        self, file_path: Path, btn_col: list, substring: str, on_file_select: callable
    ) -> None:
        self.path = file_path
        self.btn_col = btn_col
        self.substring = substring
        self.on_file_select = on_file_select
        self.create_ui()

    def process_line_with_substring(self, line: str) -> str:
        splitted = line.split(self.substring)
        splitted_arr = (" " * len(sub) for sub in splitted)
        inserted_arr = [spaces + self.substring for spaces in splitted_arr]
        inserted_arr.pop()

        return "".join(inserted_arr)

    def get_substring_text(self) -> ft.Text:
        text = ""
        for line in self.path.read_text().splitlines():
            text += self.process_line_with_substring(line) + "\n"

        return ft.Text(text, color="yellow", font_family=FileContainer.FONT_FAMILY)

    def create_ui(self) -> None:
        self.btn_col.append(
            ft.Container(
                ft.ElevatedButton(
                    self.path.name, width=120, on_click=self.on_file_select
                )
            )
        )
        self.container = ft.Stack(
            [
                ft.Container(
                    ft.Text(
                        self.path.read_text(), font_family=FileContainer.FONT_FAMILY
                    ),
                ),
                ft.Container(self.get_substring_text()),
            ],
        )


class SearchPage:
    def __init__(self, page: ft.Page, data: dict[str, str]) -> None:
        self.page = page
        self.col = []
        self.files: list[FileContainer] = []
        self.btn_col = []
        self.location = Path(data["location"])
        self.substring = data["substring"]
        self.current_file_index = 0
        self.search()
        self.create_ui()

    def on_file_select(self, e) -> None:
        for index, btn in enumerate(self.btn_col):
            if btn.content.text == e.control.text:
                self.current_file_index = index

        self.page.clean()
        self.finalize_ui()

    def search(self):
        for file in self.location.rglob("*.py"):
            if self.substring not in file.read_text():
                continue
            self.files.append(
                FileContainer(file, self.btn_col, self.substring, self.on_file_select)
            )

        for file in self.files:
            self.col.append(file.container)

    def set_window_dimensions(self):
        self.page.window_width = 1100
        self.page.window_height = 600

    def create_ui(self) -> None:
        self.set_window_dimensions()

        self.finalize_ui()

    def finalize_ui(self) -> None:
        self.row = ft.Row(
            [
                ft.Column(
                    self.btn_col,
                    scroll=ft.ScrollMode.AUTO,
                    height=self.page.window_height,
                ),
                ft.Column(
                    [self.col[self.current_file_index]],
                    height=self.page.window_height,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.page.add(self.row)
