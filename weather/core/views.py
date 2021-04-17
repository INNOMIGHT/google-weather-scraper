from django.http import HttpResponse
from django.shortcuts import render
import requests


def get_html_content(city):

    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 " \
                 "Safari/537.36 "
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(' ', '+')
    html_content = session.get('https://www.google.com/search?q=weather+in+'+city).text

    return html_content


def home(request):
    weather_data = None
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_content = get_html_content(city)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        print(html_content)

        weather_data = dict()

        weather_data['region'] = soup.find("div", attrs={"class": "wob_loc mfMhoc"}).text
        weather_data['daytime'] = soup.find("div", attrs={"id": "wob_dcp"}).text
        weather_data['weather_stat'] = soup.find("span", attrs={"id": "wob_dc"}).text
        weather_data['temperature'] = soup.find("span", attrs={"class": "wob_t"}).text

    return render(request, 'core/home.html', {'weather': weather_data})
