with open('arquivoaaa.txt','w',encoding='utf-8') as file:
    while True:
        try:
            line = input()

            print(line,file=file)
        except EOFError:
            break
            