from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
import os
import re
import time
from pandas.core.frame import DataFrame
from pandas.core.series import Series
from re import Match
from .constants import Constants
from .utils import Utils
from .menu import Menu


class CopyPhotos():
    def __init__(self) -> None:
        self.select_function_to_use()

    def select_function_to_use(self) -> None:
        function_selected: int = Menu.init_app()
        if function_selected == 1:
            self.extraction_type: int = Menu.extraction_type()
            self.extract_from_excel()
        elif function_selected == 2:
            self.extract_from_folder()
        time.sleep(30)

    def extract_from_excel(self) -> None:
        '''
        Inicia el proceso de extraccion desde el archivo de excel
        '''

        self.photos = Utils.list_files(Constants.DIR_DATA)
        self.data = self.generate_data()
        # self.data = self.filter_data_to_work(self.data)
        if self.extraction_type:
            if self.data.shape[1] <= 3:
                print('El Archivo no contiene la columna NOMBRE')
            elif sum(self.data['NOMBRE'].isna()):
                print('La columna NOMBRE tiene valores nulos')
            else:
                self.data['NOMBRE'] = self.data['NOMBRE'].str.strip()
                self.init_copy()
        else:
            self.init_copy()

    def generate_data(self) -> DataFrame:
        '''
        Devuelve archivo con la data limpia para trabajar

        return:
            Vuelve excel en DataFrame, quita nulos y duplicados
        '''
        df = pd.read_excel(
            Constants.ORDER_FILE_NAME,
            dtype={
                'CLIENTE': str,
                'REFERENCIA': str,
                'COLOR': str,
                'NOMBRE': str
            }
        )

        df = df.drop_duplicates(
            ['CLIENTE', 'REFERENCIA', 'COLOR'], ignore_index=True)
        return df.dropna(subset=['CLIENTE', 'REFERENCIA'])

    def filter_data_to_work(self, df) -> DataFrame:
        '''
        Devuelve DataFrame con la informacion que el usuario quiere trabajar

        return:
            DataFrame
        '''
        flag = True
        while flag:
            user_info: Dict[str, str] = Menu.filter_search()
            df = df[df['LINEA'] == Constants.LINE]
            df = df[df['FECHA'] >= user_info['date']]
            if user_info['client']:
                df = df[df['CLIENTE'] == user_info['client']]
                print(df.shape)
            if df.shape[0] > 0:
                flag = False
            else:
                print('-' * 100)
                print('Filtros no generan información para copiar')
        return df.reset_index(drop=True)

    def init_copy(self):
        '''
        Inicia el proceso de copiado de imagenes y genera reporte de archivos
        no encotrados
        '''
        self.data['FILES'] = self.data[
            ['REFERENCIA', 'COLOR']
        ].apply(Utils.search, photos=self.photos, axis=1)

        Utils.info_no_math(self.data)

        self.create_dirs_and_copy_data()
        # Utils.pack_dirs()

        print('Archivos copiados correctamente')

    def create_dirs_and_copy_data(self):
        '''
        Crear directorios y pegar archivos

        Crear el directorio con el nombre del cliente y copia los archivos que tienen nombre en FILE

        Parametros:
        self.data -> DataFrame con la data que tiene la lista de los nombres de los archivos
        '''
        self.data = self.data[self.data['FILES'] != 'No'].copy()
        self.data.loc[:, 'CLIENTE'] = self.data['CLIENTE'].apply(
            lambda x: x.strip()
        )
        for client in list(np.unique(self.data['CLIENTE'])):
            dir_destination = Constants.DIR_OUT + '/{}'.format(client)
            try:
                os.mkdir(dir_destination)
            except:
                print('Carpeta ya existe: ', dir_destination)

            if self.extraction_type:
                with_name = 1
            else:
                self.data['NOMBRE'] = np.nan
                with_name = 0

            data_temp = self.data[self.data['CLIENTE'] == client].reset_index(
                drop=True
            )

            data_temp['NOMBRE_FOTOS'] = data_temp[
                ['FILES', 'NOMBRE']
            ].apply(
                Utils.copy_data,
                dir_destination=dir_destination,
                with_name=with_name,
                axis=1
            )

            if self.extraction_type:
                df = pd.DataFrame(columns=data_temp.columns)
                for index in data_temp.index:
                    for file in data_temp.loc[index, 'NOMBRE_FOTOS']:
                        temp = data_temp.loc[[index], :]
                        temp[['NOMBRE_FOTOS', 'ANCHO', 'LARGO']] = file
                        df = pd.concat(
                            [df, temp],
                            ignore_index=True
                        )
                Utils.save_table(df, client)

    def extract_from_folder(self) -> None:
        '''
        Inicia el proceso de extraccion desde el archivo de la carpeta
        '''
        files_df: DataFrame = self.generate_table_from_folder()
        references: DataFrame = self.generate_table_references()
        files_df = pd.merge(
            left=files_df,
            right=references,
            on='REFERENCIA',
            how='left'
        )

        not_marge: DataFrame = files_df[files_df['MARCA'].isna()]
        if len(not_marge) > 0:
            print(
                'Las siguientes referencias no tienen información en la tabla de referencias')
            print(not_marge['REFERENCIA'])
            files_df = files_df[~files_df['MARCA'].isna()]

        filter_by: str = Menu.filter_by()
        Utils.create_folders_by(files_df, 'GENERO', filter_by)

        files_df['RUTA_DESTINO'] = files_df[
            [filter_by, 'GENERO', 'ARCHIVO']
        ].apply(
            lambda x: '{}/{}/{}/{}/{}'.format(
                Constants.DIR_OUT, filter_by,
                x[0], x[1], x[2]
            ),
            axis=1
        )

        Utils.info_to_excel(files_df, filter_by)

        Utils.only_copy_data(
            files_df['RUTA_ORIGEN'],
            files_df['RUTA_DESTINO'],
        )

    def generate_table_from_folder(self) -> DataFrame:
        '''
        Devuelve DataFrame con la informacion de todos los archivos en la carpeta indicada

        return:
            DataFrame
        '''
        files: List[str] = os.listdir(Constants.DIR_DATA_FOLDER)
        values: List[Tuple[str]] = []
        for file in files:
            match_file: Match = re.search(
                r'_*(M?[0-9]+)_([0-9]*[A-Z]*).*', file)
            if match_file:
                values.append(
                    (match_file.group(1), match_file.group(2),
                     Constants.DIR_DATA_FOLDER + file, file)
                )
            else:
                print('Archivo {} no tiene el formato correcto'.format(file))
        return pd.DataFrame(
            values, columns=['REFERENCIA', 'COLOR', 'RUTA_ORIGEN', 'ARCHIVO']
        )

    def generate_table_references(self) -> DataFrame:
        '''
        Devuelve DataFrame con la informacion de todas las referencias

        return:
            DataFrame
        '''
        return pd.read_excel(
            Constants.REFERENCES_FILE_NAME,
            dtype={
                'REFERENCIA': str,
            }
        )
