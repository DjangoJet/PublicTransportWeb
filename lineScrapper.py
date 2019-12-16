import bs4
# import pymongo
# import json
import requests

class getAllLine():
    def __init__(self,zditmURL):
        self.zditmURL = zditmURL
        self.getBS()
        

    def getBS(self):
        self.zditmHTML = requests.get(basicURL)
        self.zditmBS = bs4.BeautifulSoup(self.zditmHTML.text,'html.parser')
    
    def getLine(self,url):
        self.getLineStops(url)

    def getLines(self):
        for table in self.zditmBS.find_all('ul',{'class':'listalinii'}):
            for line in table:
                print(line.a.text + ': ' + line.a.attrs['href']+'\n')

    def getLineStops(self,lineURL):
        lineStopsBS = bs4.BeautifulSoup(requests.get(lineURL).text,'html.parser')
        
        #print left table 
        lineTableLeft = lineStopsBS.find('div',{'class':'trasywierszelewo'})
        tableLeft = lineTableLeft.find_all('tr',{'class': None})
        for table in tableLeft:
            czas = table.find('td',{'class': 'czas'})

            przystanek = table.find('td',{'class': 'przystanek'})
            try:
                if przystanek.a.find('span',{'class':'przystanekdod'}) == None:
                    try:
                        print(czas.text + ': ',end = '')
                    except:
                        pass
                    print(przystanek.text + ': ' + przystanek.a.attrs['href'])
            except:
                pass

        print('\n')

        #print left table 
        lineTableRight = lineStopsBS.find('div',{'class':'trasywierszeprawo'})
        tableRight = lineTableRight.find_all('tr',{'class': None})
        for table in tableRight:
            czas = table.find('td',{'class': 'czas'})

            przystanek = table.find('td',{'class': 'przystanek'})
            try:
                if przystanek.a.find('span',{'class':'przystanekdod'}) == None:
                    try:
                        print(czas.text + ': ',end = '')
                    except:
                        pass
                    print(przystanek.text + ': ' + przystanek.a.attrs['href'])
            except:
                pass

basicURL = "https://www.zditm.szczecin.pl/pl/pasazer/rozklady-jazdy,wedlug-linii"
abc = getAllLine(basicURL)
abc.getLine('https://www.zditm.szczecin.pl/pl/pasazer/rozklady-jazdy,linia,2')
