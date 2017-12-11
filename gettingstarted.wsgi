def main():
    my_file = open("some.txt", w)
    print("Имя файла: ", my_file.name)
    print("Идет запись в файл...")
    print("2 + 2 * 2 = ", 2 + 2 * 2)
    print("Файл закрыт: ", my_file.closed)
    

if __name__ == '__main__':
     main()
