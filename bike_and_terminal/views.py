from django.shortcuts import render
from .models import bike,terminal,distance,rent
from django.http import HttpResponse
from django.db import connection
import folium
import geocoder
import requests
import json
import itertools
import requests
from requests.exceptions import ConnectTimeout
from django.contrib.auth.decorators import login_required
from requests.adapters import HTTPAdapter, Retry

@login_required(login_url='/signin')
def show_loc(request):
    with connection.cursor() as cursor:
        cursor.execute("delete from bike_and_terminal_distance")
    m=folium.Map(location=[12.9716,77.5946],zoom_start=12)  
    feature_group = folium.FeatureGroup("To-From")  
    feature_group1 = folium.FeatureGroup("Terminals")
    with connection.cursor() as cursor:
        cursor.execute("select term_id from bike_and_terminal_terminal")
        t_id = cursor.fetchall()
        cursor.execute("select latitude from bike_and_terminal_terminal")
        lat = cursor.fetchall()
        cursor.execute("select longitude from bike_and_terminal_terminal")
        lon = cursor.fetchall()
        cursor.execute("select term_name from bike_and_terminal_terminal")
        name=cursor.fetchall()

    for (lat1,lon1,name1) in zip(lat, lon,name):
        lat2=lat1[0]
        lon2=lon1[0]
        name2=name1[0]
        feature_group1.add_child(folium.Marker([lat2,lon2],popup=folium.Popup(name2)))
        m.add_child(feature_group1)

    if request.method=='POST':
        with connection.cursor() as cursor:
            cursor.execute("delete from bike_and_terminal_distance")
        frm=request.POST['from']
        to=request.POST['to']
        location1=geocoder.osm(frm)
        location2=geocoder.osm(to)
        if (location1.lat is not None) and (location2.lat is not None):
            lat1=location1.lat
            lon1=location1.lng
            lat2=location2.lat
            lon2=location2.lng
            feature_group.add_child(folium.Marker([lat1,lon1],popup=str(frm), icon=folium.Icon(color='red')))
            feature_group.add_child(folium.Marker([lat2,lon2],popup=str(to), icon=folium.Icon(color='green')))
            m.add_child(feature_group)
            for (lat_1,lon_1,t_id1) in zip(lat, lon,t_id):
                retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
                lat_2=lat_1[0]
                lon_2=lon_1[0]
                t_id2=t_id1[0]
                s=requests.Session()
                s.mount('http://', HTTPAdapter(max_retries=retries))
                r = s.get(f"http://router.project-osrm.org/route/v1/driving/{lon_2},{lat_2};{lon1},{lat1}?overview=false", timeout=2)
                routes = json.loads(r.content)
                route_1 = routes.get("routes")[0]
                route_2 = route_1['legs']
                route_3 = route_2[0]
                startdistance = route_3['distance']
                r = s.get(f"http://router.project-osrm.org/route/v1/driving/{lon_2},{lat_2};{lon2},{lat2}?overview=false", timeout=2)
                routes = json.loads(r.content)
                route_1 = routes.get("routes")[0]
                route_2 = route_1['legs']
                route_3 = route_2[0]
                enddistance = route_3['distance']
                new_dist= distance(term_id_id=t_id2,startdistance=startdistance,enddistance=enddistance)
                new_dist.save()

    query_results = distance.objects.all()
    m = m._repr_html_()
    context = {'m': m,'query_results':query_results}
    return render(request, 'show_loc.html', context)

def rent_cal(request):
    current_user = request.user
    with connection.cursor() as cursor:
        cursor.execute("delete from bike_and_terminal_rent") 
    retries = Retry(total=5,
    backoff_factor=0.1,
    status_forcelist=[ 500, 502, 503, 504 ])
    if request.method=='POST':
        start=request.POST['startloc']
        end=request.POST['endloc']

        with connection.cursor() as cursor:
            cursor.execute(f"select latitude from bike_and_terminal_terminal where term_id = '{start}'")
            lat1 = cursor.fetchall()
            lat_1 = lat1[0]
            cursor.execute(f"select longitude from bike_and_terminal_terminal where term_id = '{start}'")
            lon1 = cursor.fetchall()
            lon_1 = lon1[0]
            cursor.execute(f"select latitude from bike_and_terminal_terminal where term_id = '{end}'")
            lat2 = cursor.fetchall()
            lat_2 = lat2[0]
            cursor.execute(f"select longitude from bike_and_terminal_terminal where term_id = '{end}'")
            lon2 = cursor.fetchall()
            lon_2 = lon2[0]

        s=requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=retries))
        r = s.get(f"http://router.project-osrm.org/route/v1/driving/{lon_2[0]},{lat_2[0]};{lon_1[0]},{lat_1[0]}?overview=false", timeout=2)
        routes = json.loads(r.content)
        route_1 = routes.get("routes")[0]
        route_2 = route_1['legs']
        route_3 = route_2[0]
        distance = route_3['distance']
        with connection.cursor() as cursor:
            cursor.execute(f"select bike_id from bike_and_terminal_bike where term_id_id = '{start}'")
            id=cursor.fetchall()

        for id1 in id:
            id_1=id1[0]
            with connection.cursor() as cursor:
                cursor.execute(f"select rent_cost from bike_and_terminal_bike where bike_id = '{id_1}' and rent_cost<=(select balance from user_auth where email = '{current_user}')")
                rent0=cursor.fetchall()
                rent1=rent0[0]
            rent_1=round((float(distance) * float(rent1[0]))/1000,2)
            new_rent= rent(bike_id_id=id_1,rent_cost=rent_1,fromt=start,tot=end)
            new_rent.save()
    query_results = rent.objects.all()

    context = {'dis':distance,'query_results':query_results} 
    return render(request, 'rent_cal.html',context)

def all_term(request):
    if request.method=='POST':
        query_results = terminal.objects.all()
        context= {'query_results':query_results}
        return render(request, 'all_term.html',context)
        

