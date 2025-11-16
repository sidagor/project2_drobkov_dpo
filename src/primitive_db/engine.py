import prompt


def welcome():
    """Функция приветствия и игрового цикла"""
    print("Первая попытка запустить проект!")
    print("***")

    while True:
        print("<command> exit - выйти из программы")
        print("<command> help - справочная информация")

        command = prompt.string('Введите команду: ')

        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            print("Справочная информация:")
            print("- help - показать эту справку")
            print("- exit - выйти из программы")
        elif command:
            print(f"Неизвестная команда: {command}")
