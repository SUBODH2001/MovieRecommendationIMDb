import requests
from bs4 import BeautifulSoup
import pandas as pd 
import gspread
from datetime import datetime
import schedule, time

class Movies(object):
    
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        }

    def recommend(self, genres = None, year_start = None, year_end = None, keywords = None):
        name, year, time, rating = '', '', '', ''
        if not (genres or year_start or year_end or keywords):
            url = "https://www.imdb.com/search/title/?title_type=feature&sort=moviemeter,asc&num_votes=100000,"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_most_popular(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif genres and not ( year_start or year_end or keywords):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_geners_filter(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif year_start and not ( genres or year_end or keywords):
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={year_start}-01-01,&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_year_filter(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")


        elif year_end and not ( genres or year_start or keywords):
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=,{year_end}-12-31&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_year_filter(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif  keywords and not (year_end or genres or year_start):
            url = f"https://www.imdb.com/search/title/?title_type=feature&sort=num_votes,desc&keywords="
            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_keywords_filter(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")


        elif genres and year_start and not ( year_end or keywords):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&release_date={year_start}-01-01,&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif genres and year_end and not ( year_start or keywords):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&release_date=,{year_end}-12-31&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif genres and keywords and not ( year_start or year_end):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&sort=num_votes,desc&keywords="

            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif year_start and year_end and not ( genres or keywords):
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={year_start}-01-01,{year_end}-12-31&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_year_filter(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        elif year_start and keywords and not ( genres or year_end):
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={year_start}-01-01,&sort=num_votes,desc&keywords="

            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        
        elif year_end and keywords and not ( genres or year_start):
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date=,{year_end}-01-01&sort=num_votes,desc&keywords="

            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")
        
        elif year_end and keywords and genres and not ( year_start):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&release_date=,{year_end}-12-31&sort=num_votes,desc&keywords="

            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")
            
        elif year_start and keywords and genres and not ( year_end):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&release_date={year_start}-12-31,&sort=num_votes,desc&keywords="
            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")
        
        elif year_start and keywords and year_end  and not ( genres):
            url = f"https://www.imdb.com/search/title/?title_type=feature&release_date={year_start}-01-01,{year_end}-12-31&sort=num_votes,desc&keywords="
            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")
        
        elif year_start and genres and year_end  and not ( keywords ):
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&release_date={year_start}-01-01,{year_end}-12-31&sort=num_votes,desc"
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")

        else:
            url = f"https://www.imdb.com/search/title/?title_type=feature&genres={genres}&release_date={year_start}-01-01,{year_end}-12-31&sort=num_votes,desc&keywords="
            while keywords:
                keyword = keywords.pop()
                url+=keyword
                if keywords:
                    url+=","
            try:
                response = requests.get(url, headers = self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                n = 5
                for movie in soup.find('div', class_ = "ipc-page-grid__item ipc-page-grid__item--span-2").find("ul").find_all("li"):
                    name = " ".join(movie.find("h3").text.split()[1:])
                    spanlist = movie.find("div").find("div").find("div").find("div").find_all("span")
                    year = spanlist[0].text
                    time = spanlist[1].text
                    rating = spanlist[2].text
                    reviews = spanlist[3].text[:spanlist[3].text.index(")")+1]
                    n-=1
                    self.update_dashboard_all_filters(name, year, time, rating, reviews)
                    if n == 0:
                        break
            except Exception as e:
                print(f"Link not working, Please come afte some time, Error is {e}")


    def update_dashboard_most_popular(self, name, year, time, rating, reviews):
        try:
            sh = gc.open_by_key("1r4iebbTwoqOTpoGoM1CZU34ijgvJEElLPgK9MJ9TpEA")
            sheet = sh.worksheet("DataSheet")
            current_date = datetime.now().date()
            current_date_str = current_date.strftime('%Y-%m-%d')
            values = [current_date_str ,name, year, time, rating, reviews]
            sheet.append_row(values=values, table_range="B:F") 
        except Exception as e:
            print(f"Wasn't able to add to sheet might be some error: {e}")


    def update_dashboard_year_filter(self, name, year, time, rating, reviews):
        try:
            sh = gc.open_by_key("1r4iebbTwoqOTpoGoM1CZU34ijgvJEElLPgK9MJ9TpEA")
            sheet = sh.worksheet("DataSheet")
            current_date = datetime.now().date()
            current_date_str = current_date.strftime('%Y-%m-%d')
            values = [current_date_str ,name, year, time, rating, reviews]
            sheet.append_row(values=values, table_range="I:N")             
        except Exception as e:
            print(f"Wasn't able to add to sheet might be some error: {e}")

    def update_dashboard_geners_filter(self, name, year, time, rating, reviews):
        try:
            sh = gc.open_by_key("1r4iebbTwoqOTpoGoM1CZU34ijgvJEElLPgK9MJ9TpEA")
            sheet = sh.worksheet("DataSheet")
            current_date = datetime.now().date()
            current_date_str = current_date.strftime('%Y-%m-%d')
            values = [current_date_str ,name, year, time, rating, reviews]
            sheet.append_row(values=values, table_range="Q:V")             
        except Exception as e:
            print(f"Wasn't able to add to sheet might be some error: {e}")

    def update_dashboard_keywords_filter(self, name, year, time, rating, reviews):
        try:
            sh = gc.open_by_key("1r4iebbTwoqOTpoGoM1CZU34ijgvJEElLPgK9MJ9TpEA")
            sheet = sh.worksheet("DataSheet")
            current_date = datetime.now().date()
            current_date_str = current_date.strftime('%Y-%m-%d')
            values = [current_date_str ,name, year, time, rating, reviews]
            sheet.append_row(values=values, table_range="Y:AD")             
        except Exception as e:
            print(f"Wasn't able to add to sheet might be some error: {e}")
    
    def update_dashboard_all_filters(self, name, year, time, rating, reviews):
        try:
            sh = gc.open_by_key("1r4iebbTwoqOTpoGoM1CZU34ijgvJEElLPgK9MJ9TpEA")
            sheet = sh.worksheet("DataSheet")
            current_date = datetime.now().date()
            current_date_str = current_date.strftime('%Y-%m-%d')
            values = [current_date_str ,name, year, time, rating, reviews]
            sheet.append_row(values=values, table_range="AG:Al")             
        except Exception as e:
            print(f"Wasn't able to add to sheet might be some error: {e}")

def scheduling():
    Subodh =  Movies()
    try: 
        Subodh.recommend()
    except Exception as e:
        print(e)
    try: 
        Subodh.recommend(year_start=2014, year_end=2020)
    except Exception as e:
        print(e)
    try: 
        Subodh.recommend(genres="Action")
    except Exception as e:
        print(e)
    try: 
        Subodh.recommend(keywords= ["suspense", "kidnapping"])
    except Exception as e:
        print(e)
    try: 
        Subodh.recommend(year_start=2014, year_end=2018, genres="Action", keywords= ["suspense", "kidnapping"])
    except Exception as e:
        print(e)


schedule.every(1).days.do(scheduling)

while True:
    schedule.run_pending()
    time.sleep(100)

#year_start= 1999, year_end=2001, genres="comedy", keywords=["cult-film"]