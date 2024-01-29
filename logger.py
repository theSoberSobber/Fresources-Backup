def log(level, key, *values):
    indentation = '\t' * level
    formatted_values = ', '.join(map(str, values))
    formatted_log = f"{indentation}=> {key}: {formatted_values}"
    print(formatted_log)