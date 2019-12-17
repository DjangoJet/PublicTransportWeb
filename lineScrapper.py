import bs4
import requests
from mongoengine import *
import datetime

class LineStop(EmbeddedDocument):
    title = StringField(required=True)
    time = StringField()
    url = StringField(required=True)

class Line(Document):
    number = StringField(required=True)
    url = StringField(required=True)
    leftTable = EmbeddedDocumentListField(LineStop, default=[])
    rightTable = EmbeddedDocumentListField(LineStop, default=[])
    published = DateTimeField(default=datetime.datetime.now)



class getAllLine():
    def __init__(self,zditmURL):
        self.zditmURL = zditmURL
        # connect('publictransportwebdb', host='localhost', port=27017)
        self.getBS()
        

    def getBS(self):
        self.zditmHTML = requests.get(basicURL)
        self.zditmBS = bs4.BeautifulSoup(self.zditmHTML.text,'html.parser')
    
    def getLine(self,url):
        self.getLineStops(url)

    def getLines(self):
        for table in self.zditmBS.find_all('ul',{'class':'listalinii'}):
            for line in table:
                linePost = Line(number=line.a.text, url=line.a.attrs['href'])
                linePost = self.getLineStops(line.a.attrs['href'],linePost)
                linePost.save()

    def getLineStops(self,lineURL,line):
        lineStopsBS = bs4.BeautifulSoup(requests.get('https://www.zditm.szczecin.pl/' + lineURL).text,'html.parser')
        
        #print left table 
        lineTableLeft = lineStopsBS.find('div',{'class':'trasywierszelewo'})
        tableLeft = lineTableLeft.find_all('tr',{'class': None})
        for table in tableLeft:
            time = table.find('td',{'class': 'czas'})
            busStop = table.find('td',{'class': 'przystanek'})

            timeDic = ''
            titleDic = ''
            urlDic = ''
            try:
                if busStop.a.find('span',{'class':'przystanekdod'}) == None:
                    try:
                        timeDic = time.text
                    except:
                        pass
                    titleDic = busStop.text
                    urlDic = busStop.a.attrs['href']
            except:
                pass
            if titleDic and urlDic:
                line.leftTable.create(title=titleDic, time=timeDic, url=urlDic)

        #print left table 
        lineTableRight = lineStopsBS.find('div',{'class':'trasywierszeprawo'})
        tableRight = lineTableRight.find_all('tr',{'class': None})
        for table in tableRight:
            time = table.find('td',{'class': 'czas'})
            busStop = table.find('td',{'class': 'przystanek'})

            timeDic = ''
            titleDic = ''
            urlDic = ''
            try:
                if busStop.a.find('span',{'class':'przystanekdod'}) == None:
                    try:
                        timeDic = time.text
                    except:
                        pass
                    titleDic = busStop.text
                    urlDic = busStop.a.attrs['href']
            except:
                pass
            if titleDic and urlDic:
                line.rightTable.create(title=titleDic, time=timeDic, url=urlDic)

        return line
basicURL = "https://www.zditm.szczecin.pl/pl/pasazer/rozklady-jazdy,wedlug-linii"
connect('publictransportwebdb', host='localhost', port=27017)
abc = getAllLine(basicURL)
abc.getLines()
# print('\n\n\n')
# abc.getLines()
# linePost = Line(number='1', url='pl/pasazer/rozklady-jazdy,linia,1')
# linePost = abc.getLineStops('pl/pasazer/rozklady-jazdy,linia,1',linePost)
# linePost.save()