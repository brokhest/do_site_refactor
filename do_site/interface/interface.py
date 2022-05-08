from client import TodoClient, FileClient, ForumClient, LoginClient


def task_changes(token, task, name=None, desc=None, comp=None, cat=None):
    if name is None:
        name = task.get("title")
    if desc is None:
        desc = task.get("description")
    if comp is None:
        comp = task.get("completion")
    if cat is None:
        cat = task.get("category")
    if TodoClient.change_task(token, name, desc, comp, cat, task.get("pk")) == 1:
        print("Изменения применены успешно")
        return
    else:
        print("что-то пошло не так")
        return


def file_changes(token, file, name=None, permission=None, perm_to=None, keyword=None, public=None):
    if name is None:
        name = file.get("name")
    if permission is None:
        permission = file.get("permission")
    if perm_to is None:
        perm_to = file.get("permissioned_to_user")
    if public is None:
        public = file.get("public")
    if keyword is None:
        keyword = file.get("keyword")
    if FileClient.change_file(token, name, permission, perm_to, keyword, public, file.get("pk")) == 1:
        print("Изменения применены успешно")
        return
    else:
        print("что-то пошло не так")
        return


def login():
    while True:
        print("1.Войти в учетную запись \n2.Зарегистрироваться")
        a = input()
        if a == "1":
            print("Введите логин:")
            username = input()
            print("Введите пароль:")
            pwd = input()
            res = LoginClient.login(username, pwd)
            # res = LoginClient.login("interface", "123456")
            if res != 0:
                print("Вы успешно вошли")
                return res
            else:
                print("Логин или пароль введены неверно")
                continue
        elif a == "2":
            print("Введите логин:")
            username = input()
            print("Введите пароль:")
            pwd = input()
            res = LoginClient.register(username, pwd)
            if res != 0:
                print("Вы успешно зарегистрировались")
                return res
            else:
                print("Такой пользователь уже существует")
                continue
        else:
            print("Неверная команда")


def menu(token):
    while True:
        print("1.Просмотреть задачи\n2.Просмотреть файлы\n3.Просмотреть форум\nexit - выйти")
        a = input()
        if a == "exit":
            break
        elif a == "1":
            task_menu(token)
        elif a == "2":
            file_menu(token)
        elif a == "3":
            forum_menu(token)
        else:
            print("Недействительная команда")


def show_tasks(token):
    print("Ваши задачи:")
    i = 1
    tasks = TodoClient.get_tasks(token)
    if len(tasks) == 0:
        print("У вас ещё нет задач")
        return 0
    for task in tasks:
        print("Задача номер:", i)
        i += 1
        print("Название:", task.get("title"))
        print("Описание:", task.get('description'))
        status = "Незаконченно" if not task.get('completion') else "Законченно"
        print("Состояние:", status)
        cat = "Нет" if task.get("category") == "None" else task.get("category")
        print("Категория:", cat)
    return tasks


def add_task(token):
    print("Введите название задачи:")
    name = input()
    print("Введите описание задачи:")
    desc = input()
    if TodoClient.add_task(token, name, desc) == 1:
        print("Задача успешно добавлена")
        show_tasks(token)
        return
    else:
        print("упс, что-то пошло не так")
        return


def change_task(token):
    tasks = show_tasks(token)
    if tasks == 0:
        print("У вас ещё нет задач")
        return
    while True:
        print("Введите номер задачи, которую хотите обновить:")
        num = input()
        if not num or not (int(num)-1 > len(tasks) or int(num)-1 < len(tasks)):
            print("Введён неправильный номер задачи")
            continue
        else:
            print("Введите новое название (пустая строка - без изменений)")
            name = input()
            print("Введите новое описание (пустая строка - без изменений)")
            desc = input()
            print ("Введите новый статус +/- (пустая строка - без изменений)")
            comp = input()
            print ("Введите новую категорию (пустая строка - без изменений)")
            cat = input()
            if not name:
                name = None
            if not desc:
                desc = None
            if not comp:
                comp = None
            else:
                comp = True if comp == "+" else False
            if not cat:
                cat = None
            task_changes(token, tasks[int(num)-1], name, desc, comp, cat)
            return


def delete_task(token):
    tasks = show_tasks(token)
    if tasks == 0:
        print("У вас ещё нет задач")
        return
    while True:
        print("Введите номер задачи, которую хотите удалить:")
        num = input()
        if not (int(num)-1 > len(tasks) or int(num)-1 < len(tasks)):
            print("Введён неправильный номер задачи")
            continue
        else:
            TodoClient.delete_task(token, tasks[int(num)-1].get("pk"))
            print("Задача успешно удалена")
            return


def show_categories(token):
    cats = TodoClient.get_categories(token)
    if len(cats) == 0:
        print("У вас ещё нет категорий")
        return 0
    for cat in cats:
        print("Название категории:", cat.get("name"))
        print("Количество задач:", cat.get("Number of tasks"))
        print("\n")
    return cats


def show_category(token):
    cats = TodoClient.get_categories(token)
    if len(cats) == 0:
        print("У вас ещё нет категорий")
        return 0
    for cat in cats:
        print("Название категории:", cat.get("name"))
    print("Введите название категории:")
    name = input()
    data = TodoClient.get_category(token, name)
    if len(data) == 0:
        print("В этой категории ещё нет задач")
        return
    i = 1
    for task in data:
        print("Задача номер:", i)
        i += 1
        print("Название:", task.get("title"))
        print("Описание:", task.get('description'))
        status = "Незаконченно" if not task.get('completion') else "Законченно"
        print("Состояние:", status)
    return


def add_category(token):
    print("Введите название категории:")
    name = input()
    if TodoClient.add_category(token, name) == 1:
        print("Категория успешно добавлена")
        return
    else:
        print("Такое название категории уже есть")
        return


def change_category(token):
    cats = show_categories(token)
    print("Введите название категории, которое хотите поменять")
    name = input()
    print("Ввелите новое название")
    new_name = input()
    if TodoClient.change_category(token, new_name, name) == 1:
        print("Название успешно изменено")
        return
    else:
        print("Категория не найдена, или такое название уже существует")


def delete_category(token):
    cats = show_categories(token)
    print("Введите название категории, которую хотите удалить")
    name = input()
    if TodoClient.delete_category(token, name) == 1:
        print("Категория успешно удалена")
        return
    else:
        print("Категория не найдена")


def task_menu(token):
    print("Меню задач:")
    tasks = show_tasks(token)
    while True:
        a = input()
        if a == "help":
            print("Список команд:\n"
                  "show_t - показать список задач\n"
                  "add_t - добавить задачу\n"
                  "ch_t - обновить задачу\n"
                  "del_t - удалить задачу\n"
                  "show_c - показать список категорий\n"
                  "view_c - показать все задачи категории\n"
                  "add_c - добавить категорию\n"
                  "ch_c - изменить название категории\n"
                  "del_c - удалить категорию\n"
                  "back - назад")
        elif a.lower() == "show_t":
            tasks = show_tasks(token)
        elif a.lower() == "add_t":
            add_task(token)
        elif a.lower() == "ch_t":
            change_task(token)
        elif a.lower() == "del_t":
            delete_task(token)
        elif a.lower() == "show_c":
            show_categories(token)
        elif a.lower() == "view_c":
            show_category(token)
        elif a.lower() == "add_c":
            add_category(token)
        elif a.lower() == "ch_c":
            change_category(token)
        elif a.lower() == "del_c":
            delete_category(token)
        elif a.lower() == "back":
            return
        else:
            print("Неизвестная команда")


def show_files(token):
    files = FileClient.get_files(token)
    if len(files)==0:
        print("У вас нет загруженных файлов")
        return 0
    i = 1
    for file in files:
        print("Номер файла:",i)
        i+=1
        print("Название файла:", file.get("name"))
        print("Размер файла:", file.get("size"))
        perm = "Разрешен " if file.get("permission") else "Неразрешён "
        perm_to = "пользователю " if file.get("permissioned_to_user") else "по ключевому слову "
        if perm == "Неразрешён ":
            print(perm)
        else:
            print(perm, perm_to, file.get("keyword"))
        public = "Публичный" if file.get("public") else "Приватный"
        print("Состояние:", public)
    return files


def change_file(token):
    files = show_files(token)
    if files == 0:
        return
    while True:
        print("Введите номер файла, который вы хотите изменить")
        num = input()
        if not num or not (int(num) - 1 > len(files) or int(num) - 1 < len(files)):
            print("Введён неправильный номер фалйа")
            continue
        print("Введите новое название (пустая строка - без изменений)")
        name = input()
        if not name:
            name = None
        print("Введите новое разрешение +/- (пустая строка - без изменений)")
        permission = input()
        if (not permission and files[int(num)-1].get("permission")) or (permission == "+"):
            permission = True
            print("Файл будет разрешён \n1.пользователю \nили \n2.по слову")
            perm_to = input()
            if perm_to == "1":
                perm_to = True
                print("Введите логин пользователя")
                keyword = input()
            elif perm_to == "2":
                perm_to = False
                print("Введите ключевое слово")
                keyword = input()
            else:
                print("Неподходящий вариант")
                perm_to = None
                keyword = None
        else:
            permission = False
            perm_to = None
            keyword = None
        print("Введите новое состояние файла pr/pub (пустая строка - без изменений)")
        inp = input()
        public = True if inp == "pub" else False
        if not inp:
            public = None
        file_changes(token, files[int(num)-1], name, permission, perm_to, keyword, public)
        return


def delete_file(token):
    files = show_files(token)
    if len(files) == 0:
        return
    while True:
        print("Введите номер файла, который хотите удалить")
        num = input()
        if not num or not (int(num) - 1 > len(files) or int(num) - 1 < len(files)):
            print("Введён неправильный номер файла")
            continue
        if FileClient.delete_file(token, files[int(num)-1].get("pk")) == 1:
            print("Файл успешно удалён")
        else:
            print("Что-то пошло не так")
        return


def add_file(token):
    print("Введите полный путь файла")
    path = input()
    print("Введите статус файла pr/pub")
    inp = input()
    public = True if inp == "pub" else False
    if not inp:
        print("Неподходящий вариант")
        print("Меню файлов:")
        return
    if FileClient.add_file(token, path, public) == 1:
        print("Файл успешно добавлен")
    else:
        print("Что-то пошло не так")
    return


def file_menu(token):
    print("Меню файлов:")
    show_files(token)
    while True:
        a = input()
        if a == "help":
            print("Список команд:\n"
                  "show_f - показать список файлов\n"
                  "add_f - добавить файл\n"
                  "ch_f - обновить файл\n"
                  "del_f - удалить файл\n"
                  "back - назад")
        elif a.lower() == "show_f":
            show_files(token)
        elif a.lower() == "add_f":
            add_file(token)
        elif a.lower() == "ch_f":
            change_file(token)
        elif a.lower() == "del_f":
            delete_file(token)
        elif a.lower() == "back":
            return
        else:
            print("Неизвестная команда")


def show_forum(token):
    messages = ForumClient.get(token)
    if len(messages) == 0:
        print("На форуме ещё никто не писал")
        return 0
    for message in messages:
        print("Сообщение:", message.get("text"))
        print("Пользователь:", message.get("user"))
    return messages


def show_messages(token):
    messages = ForumClient.my_messages(token)
    if len(messages) == 0:
        print("У вас ещё нет сообщений")
        return 0
    i = 1
    for message in messages:
        print("Номер сообщения:",i)
        i+=1
        print("Сообщение:", message.get("text"))
    return messages


def add_message(token):
    print("Введите текст сообщения")
    text = input()
    if ForumClient.add_message(token, text) == 1:
        print("Сообщение успешно добавлено")
    else:
        print("Что-то пошло не так")
    return


def delete_message(token):
    messages = show_messages(token)
    if messages == 0:
        return
    while True:
        print("Введите номер сообщения, которое хотите удалить")
        num = input()
        if not num or not (int(num) - 1 > len(messages) or int(num) - 1 < len(messages)):
            print("Введён неправильный номер сообщения")
            continue
        if ForumClient.delete_message(token, messages[int(num)-1].get("pk")) == 1:
            print("Сообщение успещно удалён")
        else:
            print("Что-то пошло не так")
        return


def forum_menu(token):
    print("Форум:")
    show_forum(token)
    while True:
        a = input()
        if a == "help":
            print("Список команд:\n"
                  "show_f - показать форум\n"
                  "show_m - показать мои сообщения\n"
                  "add_m - добавить сообщение\n"
                  "del_m - удалить сообщение\n"
                  "back - назад")
        elif a.lower() == "show_f":
            show_forum(token)
        elif a.lower() == "show_m":
            show_messages(token)
        elif a.lower() == "add_m":
            add_message(token)
        elif a.lower() == "del_m":
            delete_message(token)
        elif a.lower() == "back":
            return
        else:
            print("Неизвестная команда")


if __name__ == '__main__':
    while True:
        token = login()
        menu(token)

