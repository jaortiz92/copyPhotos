class Menu():
    def __init__(self) -> None:
        self.user_info = self.start()

    def start(self):
        '''
        Preguntar al usuario desde que fecha quiere trabajar el reporte, y tambien si quiere un solo cliente o todos

        Parametros:
            df -> DataFrame con la información del excel
            line -> str con el nombre de la linea que se esta trabajando
        '''
        self.date = input(
            'Introduzca la fecha dasde la cual quiere generar la copia (YYYY-MM-DD): ')
        flag = True
        select = '0'
        while select not in ['1', '2'] or flag:
            flag = False
            print('Filtrar:\n1. Por Cliente\n2. Todo')
            select = input()
            if select == '1':
                self.client = input('Ingrese el nombre del cliente: ')
            elif select == '2':
                self.client = None
        return {
            'date': self.date,
            'client': self.client
        }
