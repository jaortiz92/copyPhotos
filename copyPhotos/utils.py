import os
import shutil
import re
from .constants import Constants


class Utils():

    @classmethod
    def list_files(cls, dir):
        '''
        Devuelve lista de path de todas las fotos que esten en el dir_data

        dir:
            Path de ruta de las fotos
        return:
            Lista con la ruta de todas las fotos
        '''
        data = []
        for list_dir in os.walk(dir):
            for file in list_dir[-1]:
                if '.' in file:
                    path_file = list_dir[0] + '\\' + file
                    data.append(path_file)
        return data

    @classmethod
    def copy_data(cls, list_files, dir_destination):
        '''Copiar archivos en la carpeta indicada

        Toma un lista de archivos y las pega en la carpeta indicada

        Parametros:
        list_files -> Lista con nombre de los archivos para copiar
        dir_destination -> Ruta donde se pegaran los archivos
        '''
        counter = 0
        for origin in list_files:
            shutil.copy(origin, dir_destination)
            file_name = os.path.basename(origin)
            name, extension = os.path.splitext(file_name)
            counter_name = '0' + str(counter) if len(str(counter)) == 1 else str(counter)
            new_name = name + '_' + counter_name + extension
            new_path_file = os.path.join(dir_destination, new_name)
            old_path_file = os.path.join(dir_destination, file_name)
            os.rename(old_path_file, new_path_file)
            counter += 1

    @classmethod
    def pack_dirs(cls):
        '''Comprimir carpetas

        Toma las carpetas de los cliente y las comprime

        Parametros:
        None
        '''
        regular = re.compile('.*\..+')
        for x in os.listdir(Constants.DIR_OUT):
            dir_file = Constants.DIR_OUT + x
            if not regular.match(dir_file) and dir_file not in ['File', 'Data']:
                shutil.make_archive(dir_file, 'zip', base_dir=dir_file)
                shutil.rmtree(dir_file)
                print(dir_file)

    @classmethod
    def search(cls, x, photos):
        '''Devuelve lista con el nombre de los diferentes nombres encontrados, si no encuentra devuelve "No"

        Crea expresion regular para buscar en la lista del directorio principal y va agregandolo a la list_join
        Parametros:

        x -> [str de la referencia, str del color]
        '''
        list_join = []

        if str(x[1]).isnumeric():
            regular_expression = '.*{}_0*{}.*'.format(x[0], x[1])
            regular_expression = re.compile(regular_expression)
        else:
            regular_expression = '.*{}_.*'.format(x[0])
            regular_expression = re.compile(regular_expression)
            
        for file in photos:
            if regular_expression.match(file):
                list_join.append(file)
        if len(list_join) == 0:
            list_join = 'No'
        return list_join

    @classmethod
    def info_no_math(self, data):
        '''
        Crear excel con la informacion que no se copio

        Toma los que no tiene nombre de archivo y lo guarda en un excel

        Parametros:
        data -> DataFrame con la data que tiene la lista de los nombres de los archivos
        '''
        df_without_data = data[data['FILES'] == 'No']
        df_without_data.to_excel(
            Constants.DIR_OUT + '/Archivos_sin_encontrar.xlsx',
            index=False
        )
