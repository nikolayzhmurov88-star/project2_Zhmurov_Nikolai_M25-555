#!/usr/bin/env python3
from src.primitive_db import engine


def main():
    
    print('DB project is running!')
    engine.welcome()



# Вызываем ее только при запуске модуля как программы
if __name__ == "__main__":
    main()