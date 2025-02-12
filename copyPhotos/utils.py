import os
import shutil
import re
from typing import List
from pandas.core.frame import DataFrame
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
    def copy_data(cls, x, dir_destination, with_name=0) -> None:
        '''Copiar archivos en la carpeta indicada

        Toma un lista de archivos y las pega en la carpeta indicada

        Parametros:
        list_files -> Lista con nombre de los archivos para copiar
        dir_destination -> Ruta donde se pegaran los archivos
        '''
        counter = 0
        names = []
        for origin in x[0]:
            shutil.copy(origin, dir_destination)
            file_name = os.path.basename(origin)
            name, extension = os.path.splitext(file_name)
            counter_name = '0' + \
                str(counter) if len(str(counter)) == 1 else str(counter)
            if with_name:
                name = x[1] + '_' + name
                new_name = name + '_' + counter_name + extension
            new_path_file = os.path.join(dir_destination, new_name)
            old_path_file = os.path.join(dir_destination, file_name)
            names.append(new_name)
            try:
                os.rename(old_path_file, new_path_file)
            except:
                pass
            counter += 1
        return names

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

        regular_expression_lookbook = '.*ookbook.*{}.*'.format(x[0])
        regular_expression_lookbook = re.compile(regular_expression_lookbook)
        regular_expression_conceito = '.*ceito.*{}.*'.format(x[0])
        regular_expression_conceito = re.compile(regular_expression_conceito)

        for file in photos:
            if (
                regular_expression.match(file) or
                regular_expression_lookbook.match(file) or
                regular_expression_conceito.match(file)
            ):
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

    @classmethod
    def save_table(self, data, name):
        '''
        Crear excel con la informacion que se copio

        Toma los que tiene nombre de archivo y lo guarda en un excel

        Parametros:
        df -> DataFrame con la data que tiene la lista de los nombres de los archivos
        name -> Nombre para guardar el archivo
        '''
        data.to_excel(
            Constants.DIR_OUT + '/' + name + '.xlsx',
            index=False
        )

    @classmethod
    def create_folders_by(
        self, df: DataFrame, gender_column: str, column_to_job: str
    ) -> None:
        '''
        Crear carpetas segun el tipo de filtrado
        '''
        main_path: str = Constants.DIR_OUT + '/{}'.format(column_to_job)
        if not column_to_job in os.listdir(Constants.DIR_OUT):
            os.mkdir(main_path)

        df = df.copy()
        df.drop_duplicates(
            [column_to_job, gender_column],
            inplace=True,
            ignore_index=True
        )

        for i in df.index:
            dir_column_to_job: str = main_path + \
                '/{}'.format(df.loc[i, column_to_job])
            dir_column_to_job_with_gender: str = dir_column_to_job + \
                '/{}'.format(df.loc[i, gender_column])
            if not df.loc[i, column_to_job] in os.listdir(main_path):
                os.mkdir(dir_column_to_job)
            if not df.loc[i, gender_column] in os.listdir(dir_column_to_job):
                os.mkdir(dir_column_to_job_with_gender)

    @classmethod
    def only_copy_data(
        cls, list_files: List[str], list_destination: List[str]
    ) -> None:
        '''Copiar archivos en la carpeta indicada
        '''

        for origin, destination in zip(list_files, list_destination):
            shutil.copy(origin, destination)

    @classmethod
    def info_to_excel(self, data: DataFrame, filter_by: str):
        '''
        Crear excel con la informacion de cada archivo
        '''
        data.to_excel(
            Constants.DIR_OUT +
            '/Archivos_pegados_de_carpeta_{}.xlsx'.format(filter_by),
            index=False
        )
