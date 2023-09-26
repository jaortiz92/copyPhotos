from typing import Dict


class Menu():

    @classmethod
    def init_app(cls) -> int:
        flag = True
        while flag:
            selected: str = input(
                '¿Que desea extrer?\n\t1. Fotos de excel\n\t2. Fotos de carpeta\n')
            if selected == '1':
                function_selected: int = 1
                flag = False
            elif selected == '2':
                function_selected: int = 2
                flag = False
            else:
                print('Valor ingresado no valido')

        return function_selected

    @classmethod
    def filter_search(cls) -> Dict[str, str]:
        '''
        Preguntar al usuario desde que fecha quiere trabajar el reporte, y tambien si quiere un solo cliente o todos

        Parametros:
            df -> DataFrame con la información del excel
            line -> str con el nombre de la linea que se esta trabajando

        return
            Dict[str, str]:
                date : Value date
                client : Value customer
        '''
        cls.date = input(
            'Introduzca la fecha dasde la cual quiere generar la copia (YYYY-MM-DD): ')
        flag = True
        select = '0'
        while select not in ['1', '2'] or flag:
            flag = False
            print('Filtrar:\n1. Por Cliente\n2. Todo')
            select = input()
            if select == '1':
                cls.client = input('Ingrese el nombre del cliente: ')
            elif select == '2':
                cls.client = None
        return {
            'date': cls.date,
            'client': cls.client
        }


    @classmethod
    def filter_by(cls) -> str:
        flag = True
        while flag:
            selected: str = input(
                '¿Por cual metodo quiere filtrar?\n\t1. TEMPORADA\n\t2. DESCRIPCION\n')
            if selected == '1':
                function_selected: str = 'TEMPORADA'
                flag = False
            elif selected == '2':
                function_selected: str = 'DESCRIPCION'
                flag = False
            else:
                print('Valor ingresado no valido')

        return function_selected
    
    