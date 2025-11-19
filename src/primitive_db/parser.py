
import re


def parse_insert(tokens):
    if len(tokens) < 4:
        raise ValueError("Неверный формат INSERT. Используйте: "
                         "insert into <table> values (...)") 

    if tokens[0].lower() != "insert" or tokens[1].lower() != "into":
        raise ValueError("Ожидалось: insert into <table> values (...)")

    table_name = tokens[2]
    remainder = " ".join(tokens[3:]).strip()

    match = re.match(r'values\s*\((.*)\)', remainder, re.IGNORECASE)
    if not match:
        raise ValueError("Используйте формат: values (val1, val2, ...)")

    raw_values = match.group(1)
    lexer = re.findall(r'"[^"]*"|[^,\s]+', raw_values)

    parsed_values = []
    for item in lexer:
        item = item.strip()
        if item.startswith('"') and item.endswith('"'):
            parsed_values.append(item[1:-1])
            continue
        if item.lower() == "true":
            parsed_values.append(True)
            continue
        if item.lower() == "false":
            parsed_values.append(False)
            continue
        try:
            parsed_values.append(int(item))
            continue
        except ValueError:
            pass
        try:
            parsed_values.append(float(item))
            continue
        except ValueError:
            pass
        parsed_values.append(item)

    return table_name, parsed_values


def parse_where_clause(where_tokens):
    """Превращает строку вида ['age', '=', '28'] в словарь {'age': 28}."""
    if len(where_tokens) != 3 or where_tokens[1] != "=":
        raise ValueError("Неверный формат условия WHERE. Используйте: column = value")
    key = where_tokens[0]
    val = where_tokens[2]

    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    elif val.lower() == "true":
        val = True
    elif val.lower() == "false":
        val = False
    else:
        try:
            val = int(val)
        except ValueError:
            try:
                val = float(val)
            except ValueError:
                pass
    return {key: val}


def parse_set_clause(set_tokens):
    """Превращает строку вида ['age', '=', '29'] в словарь {'age': 29}."""
    if len(set_tokens) != 3 or set_tokens[1] != "=":
        raise ValueError("Неверный формат SET. Используйте: column = value")
    key = set_tokens[0]
    val = set_tokens[2]

    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]
    elif val.lower() == "true":
        val = True
    elif val.lower() == "false":
        val = False
    else:
        try:
            val = int(val)
        except ValueError:
            try:
                val = float(val)
            except ValueError:
                pass

    return {key: val}   