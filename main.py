from datetime import date, datetime, timedelta
import pandas as pd
import requests

def nextDateIfSaturadyAndMonday(data: datetime):
    if data.weekday() == 5:
        return data + timedelta(days=2)
    if data.weekday() == 6:    
        return data + timedelta(days=1)
    return data

def main(event, prazoDias):
    startDate = date.today()
    endDate = date.today() + timedelta(days=prazoDias)

    url = "https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls"
    r = requests.get(url, verify=False)
    open('temp.xls', 'wb').write(r.content)
    feriadosNacionais = pd.read_excel('temp.xls')

    datasFeriados = feriadosNacionais['Data']
    datasFeriados.drop(datasFeriados.tail(9).index, inplace=True)

    feriadosAcimaHoje = [data for data in datasFeriados if data.date() >= startDate and data.date() <= endDate]

    datas = []
    for i in range(prazoDias+1):
        data = startDate + timedelta(days=i)
        if data.weekday() not in (5,6): # retirda o sabado e o domingo da data
            datas.append(data)

    if feriadosAcimaHoje:
        for feriado in feriadosAcimaHoje:        
            if feriado == endDate:
                if endDate.weekday() < 5:
                    endDate = endDate + timedelta(days=1)
                else:
                    endDate = nextDateIfSaturadyAndMonday(endDate)
                print(endDate.strftime('%d/%m/%Y'))
                break    

    if datas:
        for data in datas:
            if data == endDate:
                endDate = data
                print('Prox. data util: ', data)
                break
    
    return endDate
