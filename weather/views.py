from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchCityForm, ChangePreferenceForm
from .models import Pref, City
from .logic import main
from django.http import response
from django.contrib import messages


def home(request):
    title = 'Home'
    if request.method == 'POST':
        city_form = SearchCityForm(request.POST)
        if city_form.is_valid():
            # name of typed in city could be wrong at this point
            city = request.POST.get('city')
            c = City(city=city)
            d = City.objects.last()
            try:
                initial_data = main.General(city)
                d.delete()
                c.save()
                return response.HttpResponseRedirect('weather')
            except:
                initial_data = main.General(d.city)
                messages.warning(
                    request, f'The city you searched for could not be found. Please check your spelling')
                return response.HttpResponseRedirect('/')

        else:
            print('not valid')
            last_search = City.objects.last().city
            initial_data = main.General(last_search)

    else:
        print('NO POST')
        city_form = SearchCityForm()
        last_search = City.objects.last().city
        initial_data = main.General(last_search)

    context = {
        'city_form': city_form,
        'title': title,
    }
    return render(request, 'weather/home.html', context)


def weather(request):
    title = 'Weather'
    city_name = City.objects.last().city
    weather_data = main.General(city_name)
    max_wind = Pref.objects.last().max_wind
    min_temp = Pref.objects.last().min_temp
    country = weather_data.weather_data_list[0].country
    loc = weather_data.weather_data_list[0].city
    date_list = []
    for i in weather_data.dates:
        date_list.append(i.lstrip('0'))

    ########### FORM STUFF #################

    if request.method == 'POST' and 'city' in request.POST:
        city_form = SearchCityForm(request.POST)
        if city_form.is_valid():
            # name of typed in city could be wrong at this point
            city = request.POST.get('city')
            c = City(city=city)
            d = City.objects.last()
            try:
                initial_data = main.General(city)
                d.delete()
                c.save()
                return response.HttpResponseRedirect('/weather')
            except:
                initial_data = main.General(d.city)
                messages.warning(
                    request, f'The city you searched for could not be found. Please check your spelling')
                return response.HttpResponseRedirect('/weather')

        else:
            print('not valid')
            last_search = City.objects.last().city
            initial_data = main.General(last_search)

    else:
        print('NO POST')
        city_form = SearchCityForm()
        last_search = City.objects.last().city
        initial_data = main.General(last_search)

    ######### PREFERENCES FORMS ##################

    if request.method == 'POST' and 'max_wind' in request.POST:
        print('post')
        pref_form = ChangePreferenceForm(request.POST)
        if pref_form.is_valid():
            print('valid')
            max_wind = int(request.POST.get('max_wind'))
            min_temp = int(request.POST.get('min_temp'))
            if max_wind > 50 or max_wind < 0:
                messages.warning(
                    request, 'Wind Speed: Please enter a number between 0 and 50')
                if min_temp > 40 or min_temp < -20:
                    messages.warning(
                        request, 'Minimum Temperature: Please enter a number between -20 and 40')
                return response.HttpResponseRedirect('/weather')

            if min_temp > 40 or min_temp < -20:
                messages.warning(
                    request, f'Minimum Temperature: Please enter a number between -20 and 40')
                if max_wind > 50 or max_wind < 0:
                    messages.warning(
                        request, f'Wind Speed: Please enter a number between 0 and 50')
                return response.HttpResponseRedirect('/weather')

            p = Pref(max_wind=max_wind, min_temp=min_temp)
            d = Pref.objects.last()
            d.delete()
            p.save()
            messages.success(request, f'Your preferences have been updated')
            return response.HttpResponseRedirect('/weather')
        else:
            print('not valid')
    else:
        pref_form = ChangePreferenceForm()

    ######### END OF FORMS #################

    good_weather_list = []
    for i in weather_data.weather_data_list:
        if i.temp > min_temp and (i.wind_speed < max_wind) and i.dark == False and i.main != 'Rain' and i.main != 'Snow':
            good_weather_list.append(i)
    context = {
        'city': loc,
        'title': title,
        'country': country,
        'data': weather_data,
        'date_list': date_list,
        'max_wind': max_wind,
        'min_temp': min_temp,
        'good_weather_list': good_weather_list,

    }
    return render(request, 'weather/table.html', context)
