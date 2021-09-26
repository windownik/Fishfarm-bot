
filename = 'modules/all_text.xlsx'


def read_admin():
    return 1111


def set_admin(admin):
    with open('modules/admin.txt', 'w', encoding='utf-8') as file:
        data = file.write(f'{admin}#\n')
    file.close()


def xsl_read():
    with open('modules/token.txt', 'r', encoding='utf-8') as file:
        data = file.read()
        file.close()
    return str(data)
