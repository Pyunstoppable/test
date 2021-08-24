import asyncio

def run_server(host,port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


di = {}

class ClientServerProtocol(asyncio.Protocol):
    def __init__(self) -> None:
        di = {}
        super().__init__()
    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        #print(f'connection {self.peername}')
        self.transport = transport
    
    def process_data(self,data):
        diata = data

        #print(f'connection {self.peername}')               
        #print('сервак получил:', data)            

        # put
        if data[:3] == 'put':
            try:
                #print('Подан ключ', data.split(' ')[1] , type(data.split(' ')[1]))
                if data.split(' ')[1] not in di.keys():
                    #di.update({data.split(' ')[1]:[(float((data.split(' ')[2])),int(data.split(' ')[3]))]})
                    di[data.split(' ')[1]] = ([(float((data.split(' ')[2])),int(data.split(' ')[3]))])
                    #print('ключа нет', {data.split(' ')[1]:[(float((data.split(' ')[2])),int(data.split(' ')[3]))]})
                else:
                    for i in di[data.split(' ')[1]]:
                        if int(data.split(' ')[3]) in i:
                            di[data.split(' ')[1]].remove(i)
                    di[data.split(' ')[1]].append((float((data.split(' ')[2])),int(data.split(' ')[3])))
                    #print('Ключ есть', ((float((data.split(' ')[2])),int(data.split(' ')[3]))))
                data = 'ok\n\n'
                   
            except Exception as er:
                data = 'error\nwrong command\n\n'
        #print('Словарь: ', di)
        # get
        if data == 'get *\n':
            #print('Запрос по всем ключам')
            data = 'ok\n'
            for key, value in di.items():    
                for i in (value):        
                    data += (key + ' ' + str(i[0]) + ' ' + str(i[1]) + '\n')
            data += '\n'
            #print(data)
        elif data[:3] == 'get' and data[:3] != 'get *\n':
                #print('Запрос по одному ключу')
            
                if len(data.split(' ')) != 2:
                    data = 'error\nwrong command\n\n'
                                
                elif str(data.split(' ')[1].replace('\n','')) not in di:
                    #print('Словарь: ', di)
                    #print(len(str(data.split(' ')[1].replace('\n',''))))
                    for i in str(data.split(' ')[1].replace('\n','')):
                        #print('символ',i, 'кон симв')
                        data = 'ok\n\n'

                else:
                    #print('Ключ найден')
                    data2 = str(data.split(' ')[1].replace('\n',''))
                    data = 'ok\n'
                    for key, value in di.items():
                        if key == data2 :
                            for i in (value):        
                                data += (key + ' ' + str(i[0]) + ' ' + str(i[1]) + '\n')
                    data += '\n'
                    #print(data)
                    
             
        return data
    
    def data_received(self, data):
        resp = self.process_data(data.decode())

        self.transport.write(resp.encode())
        #print('сервак возвращает:', (resp.encode()))


