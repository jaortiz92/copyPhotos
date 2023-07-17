from cProfile import run
import os
import shutil

PATH_ORIGIN = 'Fotos'
PATH_DESTINY = 'Data'

def run():
    counter = 0
    for brand in os.listdir(PATH_ORIGIN):
        for dir_brand in os.listdir(f'{PATH_ORIGIN}/{brand}'):
            for file in os.listdir(f'{PATH_ORIGIN}/{brand}/{dir_brand}'):
                src = f'{PATH_ORIGIN}/{brand}/{dir_brand}/{file}'
                dst = f'{PATH_DESTINY}/{file[:-4]}_{dir_brand}.jpg'
                print(src)
                shutil.move(src, dst)
                counter += 1
    print(f'Proceso terminado, se movieron {counter} archivos')


if __name__ == '__main__':
    run()