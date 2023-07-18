import pandas as pd
import numpy as np
import os
import re
from .constants import Constants
from .utils import Utils
from .menu import Menu


class CopyPhotos():
    def __init__(self) -> None:
        self.photos = Utils.list_files(Constants.DIR_DATA)
        self.data = self.generate_data()
        self.data = self.filter_data_to_work(self.data)
        self.init_copy()

    def generate_data(self):
        '''
        Devuelve archivo con la data limpia para trabajar

        return:
            Vuelve excel en DataFrame, quita nulos y duplicados
        '''
        df = pd.read_excel(Constants.ORDER_FILE_NAME)
        df = df.dropna(subset=['FECHA'])
        df = df.drop_duplicates(
            ['CLIENTE', 'REFERENCIA', 'COLOR'], ignore_index=True)
        df = df[['FECHA', 'CLIENTE', 'PEDIDO #', 'REFERENCIA', 'COLOR', 'LINEA']]
        return df

    def filter_data_to_work(self, df):
        '''
        Devuelve DataFrame con la informacion que el usuario quiere trabajar

        return:

        '''
        flag = True
        while flag:
            user_info = Menu().user_info
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
        Crear directorios y pagar archivos

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
                pass
            self.data[self.data['CLIENTE'] == client]['FILES'].apply(
                Utils.copy_data, dir_destination=dir_destination)
