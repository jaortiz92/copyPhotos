
import pandas as pd
import numpy as np
import os
import shutil
import re


dir_data = './Data'
dir_file = './File'
dir_out = './out'
data_dir = []


def list_files():
    '''Devuelve lista de path de todas las fotos que esten en el dir_data
    '''
    data_dir = []
    for list_dir in os.walk(dir_data):
        for file in list_dir[-1]:
            if '.' in file:
                path_file = list_dir[0] + '\\' + file
                data_dir.append(path_file)
    return data_dir


data_dir = list_files()


def clean_inicial_data():
    '''Devuelve archivo con la data limpia para trabajar

    Vuelve excel en DataFrame, quita nulos y duplicados'''
    file_name = f'{dir_file}/{os.listdir(dir_file)[0]}'
    df = pd.read_excel(file_name)
    df = df.dropna(subset=['FECHA'])
    df = df.drop_duplicates(['FECHA', 'CLIENTE', 'PEDIDO #',
                            'REFERENCIA', 'COLOR', 'LINEA'], ignore_index=True)
    df = df[['FECHA', 'CLIENTE', 'PEDIDO #', 'REFERENCIA', 'COLOR', 'LINEA']]
    return df


def filter_data(df, line):
    '''Devuelve DataFrame con la informacion que el usuario quiere trabajar

    Preguntar al usuario desde que fecha quiere trabajar el reporte, y tambien si quiere un solo cliente o todos

    Parametros:
    df -> DataFrame con la información del excel
    line -> str con el nombre de la linea que se esta trabajando
    '''
    date = input(
        'Introduzca la fecha dasde la cual quiere generar la copia (YYYY-MM-DD): ')
    df = df[df['FECHA'] >= date]
    df = df[df['LINEA'] == line]
    flag = True
    select = '0'
    while select not in ['1', '2'] or flag:
        flag = False
        print('Filtrar:\n1. Por Cliente\n2. Todo')
        select = input()
        if select == '1':
            flag1 = True
            while flag1:
                client = input('Ingrese el nombre del cliente: ')
                if client in list(df['CLIENTE'].values):
                    flag1 = False
                    df = df[df['CLIENTE'] == client]
                else:
                    print('Cliente no encontrado, intentelo de nuevo')
        elif select == '2':
            pass
    return df.reset_index()


def search(x):
    '''Devuelve lista con el nombre de los diferentes nombres encontrados, si no encuentra devuelve "No"

    Crea expresion regular para buscar en la lista del directorio principal y va agregandolo a la list_join
    Parametros:

    x -> [str de la referencia, str del color]
    '''
    list_join = []
    if str(x[1]).upper() == 'SURTIDO':
        regular_expression = '.*{}_.*'.format(x[0])
        regular_expression = re.compile(regular_expression)
    else:
        regular_expression = '.*{}_0*{}.*'.format(x[0], x[1])
        regular_expression = re.compile(regular_expression)
    for file in data_dir:
        if regular_expression.match(file):
            list_join.append(file)
    if len(list_join) == 0:
        list_join = 'No'
    print(list_join)
    return list_join


def copy_data(list_files, dir_destination):
    '''Copiar archivos en la carpeta indicada

    Toma un lista de archivos y las pega en la carpeta indicada

    Parametros:
    list_files -> Lista con nombre de los archivos para copiar
    dir_destination -> Ruta donde se pegaran los archivos
    '''
    for origin in list_files:
        shutil.copy(origin, dir_destination)


def info_no_math(df_for_job):
    '''Crear excel con la informacion que no se copio

    Toma los que no tiene nombre de archivo y lo guarda en un excel

    Parametros:
    df_for_job -> DataFrame con la data que tiene la lista de los nombres de los archivos
    '''
    df_without_data = df_for_job[df_for_job['FILES'] == 'No']
    df_without_data = df_without_data.drop(columns=['index'])
    df_without_data.to_excel('Archivos_sin_encontrar.xlsx', index=False)


def create_dirs_and_copy_data(df_for_job):
    '''Crear directorios y pagar archivos

    Crear el directorio con el nombre del cliente y copia los archivos que tienen nombre en FILE

    Parametros:
    df_for_job -> DataFrame con la data que tiene la lista de los nombres de los archivos
    '''
    df_for_job = df_for_job[df_for_job['FILES'] != 'No'].copy()
    df_for_job.loc[:, 'CLIENTE'] = df_for_job['CLIENTE'].apply(
        lambda x: x.strip())
    for client in list(np.unique(df_for_job['CLIENTE'])):
        dir_destination = './{}'.format(client)
        try:
            os.mkdir(dir_destination)
        except:
            pass
        df_for_job[df_for_job['CLIENTE'] == client]['FILES'].apply(
            copy_data, dir_destination=dir_destination)


def pack_dirs():
    '''Comprimir carpetas

    Toma las carpetas de los cliente y las comprime

    Parametros:
    None
    '''
    regular = re.compile('.*\..+')
    for x in os.listdir():
        if not regular.match(x) and x not in ['File', 'Data']:
            shutil.make_archive(x, 'zip', base_dir=x)
            shutil.rmtree(x)
            print(x)


def main():
    df = clean_inicial_data()
    df = filter_data(df, 'GRUPO KYLY')
    df['FILES'] = df[['REFERENCIA', 'COLOR']].apply(search, axis=1)
    info_no_math(df)
    create_dirs_and_copy_data(df)
    # pack_dirs()
    print('Archivos copiados correctamente')


if __name__ == '__main__':
    main()
