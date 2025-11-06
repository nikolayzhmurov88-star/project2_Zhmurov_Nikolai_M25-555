import prompt

def welcome():
    print("\nПервая попытка запустить проект!")
    print("\n*** \\<command> exit - выйти из программы")
    print("\n*** \\<command> help - справочная информация")
    while True:
        try:
            cmd = prompt.string("\nВведите команду: ").strip()
            if cmd == "exit":
                print("\nВыход из программы.")
                break
            elif cmd == "help":
                print("\n*** \\<command> exit - выйти из программы")
                print("\n*** \\<command> help - справочная информация")
            else:
                print(f"\nНеверная команда: {cmd}")
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break