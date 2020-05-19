from djitellopy import Tello
import time
import threading
import pandas as pd

class DataTello:
    
    def __init__(self):
        # Inicia objeto de controle do Tello
        self.tello = Tello()
        
        # Array onde será armazenado a lista de dados coletado pelo Tello
        self.__data = []
        self.__array = []

        # Tempo de voo em mili segundos
        self.tempoVoo = 420000

        '''
        ___Padrão para nome dos arquivos das tabelas___
        Onde x é o nº da tabela e y a quantidade de tempo em segundos do voo
        
        1. Para a janela fechada e porta fechada: x_tudoFechado_y.csv
        2. Para a janela aberta e porta aberta: x_janelaPortaAberta_y.csv
        3. Para a janela e porta aberta, com ventilador ligado na direção do drone: x_janelaPortaAbertaVentilador_y.csv
        '''

        # Padrão de nome
        self.nomeArquivo = '2_tudoFechado_420'
        self.__df = pd.DataFrame(columns=['timestamp', 'pitch', 'roll', 
                                          'yaw', 'vgx', 'vgy', 'vgz', 
                                          'templ', 'temph', 'tof', 
                                          'height',  'battery',  'barometer', 
                                          'time', 'agx', 'agy',  'agz'])
    '''
        self.__startCollector = False
        self.__endProgram = False
        threadCollector = threading.Thread(target=self.dataCollector, args=())
        threadCollector.daemon = False
        threadCollector.start()

    def dataCollector(self):
        while True:
            if self.__startCollector:
                self.__data.append(self.tello.get_states())

            if  self.__endProgram:
                for item in self.__data:
                    timestamp = int(round(time.time() * 1000))         # Cria timestamp no momento que recebe os dados
                    self.__df.loc[len(self.__df)] = [timestamp, item[1],  item[3], item[5], item[7], 
                                    item[9],   item[11], item[13], item[15], item[17], item[19], 
                                    item[21],    item[23], item[25], item[27], item[29], item[31]] # Adiciona os novos valores em uma nova linha do DataFrame

                self.__df.to_csv('{}.csv'.format(self.nomeArquivo))

                break            
    '''           

    def fly(self):
        #
        self.tello.connect()
        self.tello.takeoff()
        timestampInicial = int(round(time.time() * 1000))
        timestampFinal = timestampInicial

        while ((timestampFinal - timestampInicial) < self.tempoVoo):
            try:
                timestampFinal = int(round(time.time() * 1000))         # Cria timestamp no momento que recebe os dados
                self.__data.append(self.tello.get_states())
                if (not len(self.__data) % 20 == 0):
                    self.tello.send_command_without_return('command')
            except KeyboardInterrupt:
                print ('\n . . .\n')
                self.tello.end()  
                break

        self.tello.land()
        self.tello.end()

        for item in self.__data:
            timestamp = int(round(time.time() * 1000))         # Cria timestamp no momento que recebe os dados
            self.__df.loc[len(self.__df)] = [timestamp, item[1],  item[3], item[5], item[7], 
                            item[9],   item[11], item[13], item[15], item[17], item[19], 
                            item[21],    item[23], item[25], item[27], item[29], item[31]] # Adiciona os novos valores em uma nova linha do DataFrame

        self.__df.to_csv('{}.csv'.format(self.nomeArquivo))

    def stop(self):
        self.tello.end()

        

    def run(self):
        self.tello.connect()
        self.tello.takeoff()
        tempo1 = self.tello.get_flight_time()
        tempo1 = tempo1[0:(len(tempo1)-1)]
        #time.sleep(3)
        bateria = self.tello.get_battery()
        tempo2 = self.tello.get_flight_time()
        tempo2 = tempo2[0:(len(tempo2)-1)]
        
        print('Nivel da bateria é: {}'.format(str(bateria)))
        
        print('Tempo de início foi {}'.format(str(tempo1)))
        print('Tempo de término foi de {}'.format(str(tempo2)))
        
        while ((int(tempo2) - int(tempo1)) < 10):
            print('Nivel da bateria é: ' + str(bateria))
            self.__array.append(self.tello.get_attitude())
            self.__data.append(self.tello.get_states())    
            tempo2 = self.tello.get_flight_time()
            tempo2 = tempo2[0:(len(tempo2)-1)]

        self.tello.land()
        self.tello.end()
        print(self.__array)
        print(self.__data)


def main():
    dataTello = DataTello()
    dataTello.fly()
    #dataTello.stop()

if __name__ == "__main__":
    main() 