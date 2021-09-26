import random, pickle, sys, numpy as np

text = """
Выберите дальнейшее действие:
1. Загрузить игру;
2. Начать новую игру;
3. Выйти из игры.
"""
text2 = """
Выберите дальнейшее действие:
1. Открыть клетку;
2. Поставить/убрать флажок;
3. Сохранить игру;
4. Загрузить игру (Текущая игра не будет сохранена);
5. Начать новую игру;
6. Выйти в меню;
7. Выйти из игры.
"""
text3 = """
Выберите дальнейшее действие:
1. Поставить флажок;
2. Убрать флажок;
3. Вернуться назад.
"""

print("Добро пожаловать в игру САПЁР!!!\nВаша цель открыть всё поле не подорвавшись на мине! Удачи!")

def main():
    greating = input(text)
    while greating not in ['1', '2', '3']:
        print("Введите корректные значения!!!")
        greating = input(text)
    if greating == "1":
        continue_game()
    elif greating == "2":
        new_game()
    else:
        sys.exit()

def respawn(h, w, bombs):
    # Создание поля
    field = np.full((w, h), 0)

    # Расстановка бомб
    n = [x for x in range(h * w)]
    random.shuffle(n)
    bombs_numbers = list()
    for x in range(bombs):
        bombs_numbers.append([n[x] // h, n[x] % w])
    for x in bombs_numbers:
        field[x[0], x[1]] = -1

    # Перебор клеток для установки количества бомб вокруг
    s = ((0, 0), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1))

    for y in range(h):
        for x in range(w):
            if field[y, x] != -1:
                for x1, y1 in s:
                    new_x = x + x1
                    new_y = y + y1

                    if 0 <= new_x < w and 0 <= new_y < h and field[new_y, new_x] == -1:
                        field[y, x] += 1

    return bombs_numbers, field

def ninput():
    w = int(input("Введите ширину поля (минимальная 5): "))
    h = int(input("Введите высоту поля (минимальная 5): "))
    bombs = int(input("Введите количество бомб на поле, не превосходящее произведение высоты на ширину делённое пополам: "))
    while w < 5 or h < 5 or bombs > w*h//2:
        print("Введите корректные значения!!!")
        w = int(input("Введите ширину поля (минимальная 5): "))
        h = int(input("Введите высоту поля (минимальная 5): "))
        bombs = int(input("Введите количество бомб на поле, не превосходящее произведение высоты на ширину делённое пополам: "))
    return w, h, bombs

def new_game():
    w, h, bombs = ninput()

    #Создание поля
    field = np.full((w,h), 0)

    #Расстановка бомб
    n = [x for x in range(h*w)]
    random.shuffle(n)
    bombs_numbers = list()
    for x in range(bombs):
        bombs_numbers.append([n[x]//h, n[x]%w])
    for x in bombs_numbers:
        field[x[0],x[1]] = -1

    #Перебор клеток для установки количества бомб вокруг
    s = ((0,0), (0,1), (0,-1), (1,0), (1,1), (1,-1), (-1,0), (-1,1), (-1,-1))

    for y in range(h):
        for x in range(w):
            if field[y,x] != -1:
                for x1, y1 in s:
                    new_x = x + x1
                    new_y = y + y1

                    if 0 <= new_x < w and 0 <= new_y < h and field[new_y, new_x] == -1:
                        field[y,x] += 1

    hidden_field = np.full((w, h), "X")
    flags = []
    opened = []
    win = h * w - bombs
    first_try = 1

    play(w, h, bombs, win, first_try, bombs_numbers, field, hidden_field, flags, opened)

def continue_game():
    load_file = input("Введите название игры, которую вы хотите загрузить:")
    try:
        with open(load_file+".txt", "r") as file_1:
            w = int(file_1.readline())
            h = int(file_1.readline())
            bombs = int(file_1.readline())
            win = int(file_1.readline())
            first_try = int(file_1.readline())

        with open(load_file+".dat", "rb") as file_2:
            bombs_numbers = pickle.load(file_2)
            field = pickle.load(file_2)
            hidden_field = pickle.load(file_2)
            flags = pickle.load(file_2)
            opened = pickle.load(file_2)

        print("c1")
        play(w, h, bombs, win, first_try, bombs_numbers, field, hidden_field, flags, opened)
    except FileNotFoundError:
        print("Сохранение с данным названием не было найдено.")
        main()

def saving_game(w, h, bombs, win, first_try, bombs_numbers, field, hidden_field, flags, opened):
    title = input("Введите название игры, под которым вы хотите её сохранить:")
    with open(title+".txt", "w") as file_1:
        for x in [w, h, bombs, win, first_try]:
            file_1.write(str(x) + "\n")

    with open(title+".dat", "wb") as file_2:
        for x in [bombs_numbers, field, hidden_field, flags, opened]:
            pickle.dump(x, file_2)

def play(w, h, bombs, win, first_try, bombs_numbers, field, hidden_field, flags, opened):
    field = np.array(field)
    hidden_field = np.array(hidden_field)
    while True:
        print(hidden_field)
        guess = input(text2)
        while guess not in ["1", "2", "3", "4", "5", "6"]:
            print("Введите корректные значения!!!")
            guess = input(text2)

        if guess == "1":
            check = input("Введите координаты клетки через пробел, которую хотите открыть. Координаты верхней левой клетки равны 0 и 0: ")
            check = check.split()
            check_x = int(check[0])
            check_y = int(check[1])
            while first_try and field[check_y, check_x] == -1:
                bombs_numbers, field = respawn(h, w, bombs)
            first_try = 0
            if [check_y, check_x] not in opened:
                opened.append([check_y, check_x])
                if field[check_y, check_x] == -1:
                    hidden_field[check_y, check_x] = -1
                    print(field)
                    print("Увы, вы проиграли.")
                    main()
                elif win == len(opened):
                    hidden_field[check_y, check_x] = field[check_y, check_x]
                    print(field)
                    print("Ура! Вы победили!")
                    main()
                else:
                    hidden_field[check_y, check_x] = field[check_y, check_x]
            else:
                print("Вы уже открыли эту клетку!")

        elif guess == "2":
            guess_choice = input(text3)
            while guess_choice not in ["1", "2", "3"]:
                print("Введите корректные значения!!!")
                guess_choice = input(text3)
            if guess_choice == "1":
                check_box = input("Введите координаты клетки через пробел, куда хотите поставить флажок. Координаты верхней левой клетки равны 0 и 0: ")
                check_box = check_box.split()
                check_box_x = int(check_box[0])
                check_box_y = int(check_box[1])
                if [check_box_y, check_box_x] not in opened and [check_box_y, check_box_x] not in flags:
                    flags.append([check_box_y, check_box_x])
                    hidden_field[check_box_y, check_box_x] = "M"
                else:
                    print("Данная клетка открыта или в ней уже стоит флажок!")
            if guess_choice == "2":
                check_box = input("Введите координаты клетки через пробел, откуда хотите убрать флажок. Координаты верхней левой клетки равны 0 и 0: ")
                check_box = check_box.split()
                check_box_x = int(check_box[0])
                check_box_y = int(check_box[1])
                if [check_box_y, check_box_x] in flags and [check_box_y, check_box_x] not in opened:
                    flags.remove([check_box_y, check_box_x])
                    hidden_field[check_box_y, check_box_x] = "X"
                else:
                    print("Данная клетка открыта или в ней нет флажка!")

        elif guess == "3":
            saving_game(w, h, bombs, win, first_try, bombs_numbers, field, hidden_field, flags, opened)

        elif guess == "4":
            continue_game()

        elif guess == "5":
            new_game()

        elif guess == "6":
            main()

        else:
            sys.exit()

main()