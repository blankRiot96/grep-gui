import re

import flet
import flet as ft


class RichText(ft.Row):

    TAG_TO_ATTRIBUTE = {
        # tag: attribute, reference_function, default
        "b": (
            "weight",
            lambda v: RichText._get_value(flet.FontWeight, v),
            flet.FontWeight.BOLD,
        ),
        "c": ("color", lambda v: RichText._get_value(flet.colors, v), None),
        "f": ("font_family", lambda v: v, None),
        "i": ("italic", None, True),
        "bg": ("bgcolor", lambda v: RichText._get_value(flet.colors, v), None),
        "size": ("size", float, None),
        "style": ("style", lambda v: RichText._get_value(flet.TextThemeStyle, v), None),
        "w": ("weight", lambda v: RichText._get_value(flet.FontWeight, v), None),
    }

    def __init__(self, text, *args, break_into_words=True, **kwargs):
        super().__init__(
            *args,
            wrap=kwargs.pop("wrap", True),
            spacing=kwargs.pop("spacing", 0),
            run_spacing=kwargs.pop("run_spacing", 0),
            vertical_alignment=kwargs.pop(
                "vertical_alignment", ft.CrossAxisAlignment.BASELINE
            ),
            **kwargs,
        )

        self.controls = self._get_spans(text, break_into_words)

    def _get_spans(self, text: str, break_into_words: bool):
        spans = []
        style_stacks = {}
        for span in self._tokenizer(text, break_into_words):
            if "text" in span:
                active_styles = {
                    attribute: style_stack[-1]
                    for attribute, style_stack in style_stacks.items()
                    if style_stack
                }
                spans.append(ft.Text(span["text"], **active_styles))

            elif "start_tag" in span:
                tag = span["start_tag"]
                if not tag in self.TAG_TO_ATTRIBUTE:
                    raise RuntimeError(f"Unknown tag: {tag}")
                attribute, reference_function, default = self.TAG_TO_ATTRIBUTE[tag]
                value = default
                if span["param"]:
                    if reference_function:
                        value = reference_function(span["param"])
                style_stack = style_stacks.setdefault(attribute, [])
                style_stack.append(value)

            elif "end_tag" in span:
                tag = span["end_tag"]
                attribute = self.TAG_TO_ATTRIBUTE[tag][0]
                style_stack = style_stacks[attribute]
                if not style_stack:
                    raise RuntimeError(f'Mismatched end tag: {span["end_tag"]}')
                style_stack.pop()
        return spans

    def _tokenizer(self, text: str, break_into_words: bool):
        start = 0
        matchers_break_into_words = (
            r"(?P<text>[^<\s]+)",  # Plain text, no whitespace
            r"(?P<text>\s+)",  # Whitespace
            r"<(?P<start_tag>\w+)\s?(?P<param>[^>]+)?>",  # Start tag
            r"</(?P<end_tag>\w+)>",  # End tag
        )
        matchers_do_not_break_into_words = (
            r"(?P<text>[^<]+)",  # Plain text
            r"<(?P<start_tag>\w+)\s?(?P<param>[^>]+)?>",  # Start tag
            r"</(?P<end_tag>\w+)>",  # End tag
        )

        matchers = (
            matchers_break_into_words
            if break_into_words
            else matchers_do_not_break_into_words
        )

        while start < len(text):
            for matcher in matchers:
                match = re.match(matcher, text[start:])
                if match:
                    start += match.span()[1]
                    yield match.groupdict(default="")
                    break
            else:
                raise RuntimeError(
                    f"Something broken with {text}, starting at {text[start:]}"
                )

    @staticmethod
    def _get_value(reference, value):
        if not value:
            return

        if hasattr(reference, value.upper()):
            return getattr(reference, value.upper())
        elif hasattr(reference, f"{value.upper()}_500"):
            return getattr(reference, f"{value.upper()}_500")
        else:
            raise RuntimeError(f"Unknown value of type {reference}: {value}")
