from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def xd():
    if request.method == 'POST':
        try:
            empresa = {"":{}}

            HEADERS = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Accept":"*/*",
                "Keep-Alive": "300",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            }

            iterator = [
                'Nombre',
                'Mercado',
                'Pais',
                'Sector',
                'SubSector',
                'Num_Empleados',
                'Precio',
                'Hora',
                'Historia',
                'BPA',
                'PER',
                'BETA',
                'Ingresos_Totales_TTM',
                'Ingresos_Totales_Ejercicio',
                'Beneficio_Neto_TTM',
                'Beneficio_Neto_Ejercicio',
                'Valor_total_Activos',
                'Valor_total_Pasivos',
                'URL'
            ]

            emp = request.form['emp']

            url = requests.get("https://es.finance.yahoo.com/lookup?s="+emp, headers=HEADERS)
            soup = BeautifulSoup(url.text)
            e = soup.find("td", class_="data-col0").text
            
            empresa[e] = {}

            url = requests.get("https://es.finance.yahoo.com/quote/"+e+"/profile?p="+e, headers=HEADERS)
            soup = BeautifulSoup(url.text)

            itera = 0

            bloque_perfil = soup.find("div", attrs={"data-test":"qsp-profile"})

            #Company name
            empresa[e][iterator[itera]] = bloque_perfil.find("h3").text
            itera += 1

            #Marketplace
            empresa[e][iterator[itera]] = soup.find("div", class_="C($tertiaryColor)").text.split("-")[0]
            itera += 1

            #Country
            empresa[e][iterator[itera]] = str(soup.find("div", attrs={"data-test":"qsp-profile"}).find("p")).split("<br/>")[-3]
            itera+=1

            #Sector, SubSector and Employees count
            for j in soup.find_all("span", class_="Fw(600)"):
                empresa[e][iterator[itera]] = j.text
                itera+=1
                
            #Price
            empresa[e][iterator[itera]] = soup.find("fin-streamer", class_="Fw(b)", attrs={"data-symbol" : e}).text
            itera+=1

            #Time
            empresa[e][iterator[itera]] = str(datetime.now())
            itera+=1

            #History
            empresa[e][iterator[itera]] = soup.find("p", class_="Mt(15px)").text
            itera += 1

            url = requests.get("https://es.finance.yahoo.com/quote/"+e+"?p="+e, headers=HEADERS)
            soup = BeautifulSoup(url.text)

            #Getting PER, BPA, BETA
            empresa[e][iterator[itera]] = soup.find("td", class_="Ta(end)", attrs={"data-test" : "PE_RATIO-value"}).text
            itera+=1

            empresa[e][iterator[itera]] = soup.find("td", class_="Ta(end)", attrs={"data-test" : "EPS_RATIO-value"}).text
            itera+=1

            empresa[e][iterator[itera]] = soup.find("td", class_="Ta(end)", attrs={"data-test" : "BETA_5Y-value"}).text
            itera+=1

            url = requests.get("https://es.finance.yahoo.com/quote/"+e+"/financials?p="+e, headers=HEADERS)
            soup = BeautifulSoup(url.text)

            #Getting Total Income TTM and Last income
            counter = 0
            for i in soup.find("div", {"title":"Ingresos totales"}).parent.parent.find_all("span"):
                if(i.text != "Ingresos totales" and counter != 2):
                    empresa[e][iterator[itera]] = i.text
                    itera+=1
                    counter+=1
                    
            #Getting Net profit TTM and Last income
            counter = 0
            for i in soup.find("div", {"title":"Ingresos netos"}).parent.parent.find_all("span"):
                if(i.text != "Ingresos netos" and counter != 2):
                    empresa[e][iterator[itera]] = i.text
                    itera+=1
                    counter+=1
                    
            url = requests.get("https://es.finance.yahoo.com/quote/"+e+"/balance-sheet?p="+e, headers=HEADERS)
            soup = BeautifulSoup(url.text)

            counter = 0
            #Getting Total Actives, total Pasive.
            for i in soup.find("div", {"title":"Activos totales"}).parent.parent.find_all("span"):
                if(i.text != "Activos totales" and counter != 1):
                    empresa[e][iterator[itera]] = i.text
                    itera+=1
                    counter+=1
            counter = 0
            for i in soup.find("div", {"title":"Pasivo total"}).parent.parent.find_all("span"):
                if(i.text != "Pasivo total" and counter != 1):
                    empresa[e][iterator[itera]] = i.text
                    itera+=1
                    counter+=1
            counter = 0

            link = "https://www.bing.com/images/search?q=logo"+empresa[e]["Nombre"].split(",")[0]+"+&form=HDRSC3&first=1&tsc=ImageHoverTitle&cw=1443&ch=952"
            url = requests.get(link, headers=HEADERS)
            soup = BeautifulSoup(url.text)
            empresa[e][iterator[itera]] = soup.find("ul", class_="dgControl_list").find("img")["src"]
            itera += 1

        except:
            return render_template('/index.html', error=True)
        return render_template('/data.html', empresa=empresa[e]) 

    if request.method == 'GET':
        return render_template('/index.html', error=False)

    return render_template('/index.html', error=False)

if __name__=='__main__':
    app.run(debug=True)