def process_line_with_substring(substring, line: str) -> str:
    splitted = line.split(substring)
    splitted_arr = (" " * len(sub) for sub in splitted)
    inserted_arr = [spaces + substring for spaces in splitted_arr]
    inserted_arr.pop()
    return "".join(inserted_arr)


print(process_line_with_substring("run", "not found"))
