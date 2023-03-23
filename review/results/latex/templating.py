def build_template(template, dest, replacements):
    with open(template, 'r') as ffrom, open(dest, 'w') as fto:
        str = ffrom.read()
        for key in replacements:
            str = str.replace('{{' + key + '}}', replacements[key])
        fto.write(str)
    return str