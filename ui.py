import service
from utils import ResponseData, BadRequest
from typing import Union
from colorama import Fore
from dto import UserRegisterDTO


def print_response(response: Union[ResponseData, BadRequest]):
    color = Fore.GREEN if response.status_code == 200 else Fore.RED
    print(color + response.data + Fore.RESET)


# LOGIN & LOGOUT & REGISTER
def login():
    username = input(Fore.BLUE + '\nEnter your username: ')
    password = input('Enter your password: ' + Fore.RESET)
    response = service.login(username, password)
    print_response(response)


def login_for_blocking():
    username = input(Fore.BLUE + '\nEnter your username: ')
    password = input('Enter your password: ' + Fore.RESET)
    response = service.login_for_blocking(username, password)
    print_response(response)


def register():
    username = input(Fore.BLUE + '\nEnter your username: ')
    password = input('Enter your password: ' + Fore.RESET)
    dto: UserRegisterDTO = UserRegisterDTO(username, password)
    response = service.register(dto)
    print_response(response)


def logout():
    response = service.logout()
    print_response(response)


# CRUD
def todo_add():
    title = input(Fore.YELLOW + '\nEnter title : ' + Fore.RESET)
    response = service.todo_add(title)
    print_response(response)


def todo_delete():
    en_id = input(Fore.YELLOW + '\nEnter ID : ' + Fore.RESET)
    response = service.todo_delete(int(en_id))

    print_response(response)


def todo_update():
    en_id = input(Fore.YELLOW + '\nEnter ID : ' + Fore.RESET)
    title = input(Fore.YELLOW + '\nEnter title : ' + Fore.RESET)
    response = service.todo_update(int(en_id), str(title))

    print_response(response)


def todo_display(choice_):
    if choice_ == 1:
        response = service.display_todos_inc()
        print_response(response)
    elif choice_ == 2:
        response = service.display_todos_desc()
        print_response(response)
    elif choice_ == 3:
        response = service.display_todos_title_inc()
        print_response(response)
    elif choice_ == 4:
        response = service.display_todos_title_desc()
        print_response(response)
    else:
        print(Fore.RED + 'Invalid choice❌' + Fore.RESET)


# ADMIN
def block_user():
    en_id = input("\nEnter ID : ")
    response = service.block_user(int(en_id))
    print_response(response)


# INTERFACE
def menu():
    print(Fore.LIGHTCYAN_EX + '1. Login')
    print('2. Register')
    print('3. Blocking')
    print('4. Exit ' + Fore.RESET)
    return input(Fore.MAGENTA + 'Enter your choice...' + Fore.RESET)


if __name__ == '__main__':
    while True:

            choice = menu()
            if choice == '1':
                login()
                if service.session.check_session():
                    while True:
                        inner_choice = input(Fore.CYAN + "\n1. Create\n2. Update\n3. Delete\n4. Display\n"
                                                         "5. LogOut\nEnter your choice..." + Fore.RESET)
                        if inner_choice == '1':
                            todo_add()
                        elif inner_choice == '2':
                            todo_update()
                        elif inner_choice == '3':
                            todo_delete()
                        elif inner_choice == '4':
                            while True:
                                display_choice = input(
                                    Fore.CYAN + "1. Order by ID\n2. Prder by ID DESC\n3. Order by Title"
                                                "\n4. Order by Title DESC\n5. Back\n..." + Fore.RESET)

                                if display_choice == '1':
                                    todo_display(1)
                                elif display_choice == '2':
                                    todo_display(2)
                                elif display_choice == '3':
                                    todo_display(3)
                                elif display_choice == '4':
                                    todo_display(4)
                                elif display_choice == '5':
                                    break
                                else:
                                    print(Fore.RED + 'Invalid choice❌' + Fore.RESET)

                        elif inner_choice == '5':
                            logout()
                            break
                        else:
                            print(Fore.RED + 'Invalid choice❌' + Fore.RESET)

            elif choice == '2':
                register()

            elif choice == '3':
                login_for_blocking()
                if service.session.check_session():
                    block_user()
                service.session.session = None

            elif choice == '4':
                print(Fore.LIGHTGREEN_EX + "Thank you for using our services🫡" + Fore.RESET)
                quit()
            else:
                print(Fore.RED + 'Invalid choice❌' + Fore.RESET)

