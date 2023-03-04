import flet as ft
from pathlib import Path
from logit import log


class FileContainer:
    def __init__(self, file_path: Path, btn_col: list, substring: str) -> None:
        self.path = file_path
        self.btn_col = btn_col
        self.substring = substring
        self.create_ui()

    def process_line_with_substring(self, line) -> str:
        founded = ""
        new_line = ""
        prev_i = 0
        for i, char in enumerate(line):
            founded += char
            if i == line.index(self.substring, prev_i):
                prev_i = i
                new_line += " " * (len(founded) + len(self.substring) * 2)
                new_line += self.substring
                founded = ""

        return new_line

    def get_substring_text(self) -> ft.Text:
        text = ""
        for line in self.path.read_text().splitlines():
            if self.substring not in line:
                text += "\n"
                continue

            text += self.process_line_with_substring(line) + "\n"

        return ft.Text(text, color="yellow", weight=ft.FontWeight.BOLD)

    def create_ui(self) -> None:
        self.btn_col.append(ft.Container(ft.ElevatedButton(self.path.name)))
        self.container = ft.Stack(
            [
                ft.Container(ft.Text(self.path.read_text(), selectable=True)),
                ft.Container(self.get_substring_text()),
            ]
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

    def search(self):
        for file in self.location.rglob("*.py"):
            self.files.append(FileContainer(file, self.btn_col, self.substring))

        for file in self.files:
            self.col.append(file.container)

    def set_window_dimensions(self):
        self.page.window_width = 1100
        self.page.window_height = 600

    def create_ui(self) -> None:
        self.set_window_dimensions()
        self.col.append(ft.Text("Test"))
        self.finalize_ui()

    def finalize_ui(self) -> None:
        row = ft.Row(
            [
                ft.Column(self.btn_col, scroll=ft.ScrollMode.ALWAYS),
                self.col[self.current_file_index],
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.page.add(row)
