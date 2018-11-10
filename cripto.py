def crip(texto):
    crip = ""
    for c in texto:
        if(c.isalpha()):
            cod = ord(c)
            cod += 3
            crip += chr(cod)
        else:
            crip += c

    return "".join(reversed(crip))


def decrip(texto):
    decrip = ""
    for c in texto:
        if(c.isalpha()):
            cod = ord(c)
            cod -= 3
            decrip += chr(cod)
        else:
            decrip += c

    return "".join(reversed(decrip))
