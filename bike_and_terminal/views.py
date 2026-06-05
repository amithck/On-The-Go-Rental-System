from django.shortcuts import render
from .models import bike, terminal
from user.models import auth as UserProfile
import folium
import geocoder
import requests
from requests.adapters import HTTPAdapter, Retry
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def _create_osrm_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.1,
        status_forcelist=[500, 502, 503, 504],
    )
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session


def _fetch_route_distance(session, origin_lon, origin_lat, dest_lon, dest_lat, timeout=5):
    url = f'http://router.project-osrm.org/route/v1/driving/{origin_lon},{origin_lat};{dest_lon},{dest_lat}?overview=false'
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    routes = payload.get('routes')
    if not routes:
        raise ValueError('No route information available from OSRM service.')
    leg = routes[0].get('legs', [])[0]
    return leg.get('distance', 0)


@login_required(login_url='/signin')
def show_loc(request):
    m = folium.Map(location=[12.9716, 77.5946], zoom_start=12)
    feature_group = folium.FeatureGroup('To-From')
    feature_group1 = folium.FeatureGroup('Terminals')
    terminals = list(terminal.objects.all())

    for term in terminals:
        feature_group1.add_child(
            folium.Marker([float(term.latitude), float(term.longitude)], popup=folium.Popup(term.term_name))
        )
    m.add_child(feature_group1)

    error = None
    query_results = []
    if request.method == 'POST':
        frm = request.POST.get('from', '').strip()
        to = request.POST.get('to', '').strip()
        location1 = geocoder.osm(frm)
        location2 = geocoder.osm(to)
        if location1.lat is not None and location2.lat is not None:
            lat1 = location1.lat
            lon1 = location1.lng
            lat2 = location2.lat
            lon2 = location2.lng
            feature_group.add_child(
                folium.Marker([lat1, lon1], popup=str(frm), icon=folium.Icon(color='red'))
            )
            feature_group.add_child(
                folium.Marker([lat2, lon2], popup=str(to), icon=folium.Icon(color='green'))
            )
            m.add_child(feature_group)

            session = _create_osrm_session()
            for term in terminals:
                try:
                    start_distance = _fetch_route_distance(
                        session,
                        float(term.longitude),
                        float(term.latitude),
                        lon1,
                        lat1,
                    )
                    end_distance = _fetch_route_distance(
                        session,
                        float(term.longitude),
                        float(term.latitude),
                        lon2,
                        lat2,
                    )
                    query_results.append({
                        'term_id': term.term_id,
                        'term_name': term.term_name,
                        'startdistance': int(start_distance),
                        'enddistance': int(end_distance),
                        'no_of_bikes': term.no_of_bikes,
                    })
                except Exception as exc:
                    error = f'Unable to calculate route distances: {exc}'
        else:
            error = 'One or both provided locations could not be resolved. Please try valid addresses.'

    return render(request, 'show_loc.html', {
        'm': m._repr_html_(),
        'query_results': query_results,
        'error': error,
    })


@login_required(login_url='/signin')
def rent_cal(request):
    current_user = request.user
    error = None
    distance_value = None
    query_results = []
    rent_quotes = {}

    if request.method == 'POST':
        start = request.POST.get('startloc', '').strip()
        end = request.POST.get('endloc', '').strip()

        try:
            start_terminal = terminal.objects.get(term_id=start)
            end_terminal = terminal.objects.get(term_id=end)
            session = _create_osrm_session()
            distance_value = _fetch_route_distance(
                session,
                float(start_terminal.longitude),
                float(start_terminal.latitude),
                float(end_terminal.longitude),
                float(end_terminal.latitude),
            )
            user_balance = UserProfile.objects.filter(email=str(current_user)).values_list('balance', flat=True).first() or Decimal('0')
            available_bikes = bike.objects.filter(term_id=start_terminal, rent_cost__lte=user_balance)

            for available_bike in available_bikes:
                rent_cost = round((Decimal(distance_value) * Decimal(available_bike.rent_cost) / Decimal(1000)), 2)
                bike_id_str = str(available_bike.bike_id)
                quote = {
                    'bike_id': bike_id_str,
                    'bike_name': available_bike.bike_name,
                    'rent_cost': str(rent_cost),
                    'fromt': start,
                    'tot': end,
                }
                query_results.append(quote)
                rent_quotes[bike_id_str] = quote

            request.session['rent_quotes'] = rent_quotes
        except terminal.DoesNotExist:
            error = 'Selected terminal does not exist.'
        except Exception as exc:
            error = f'Cannot calculate rent quote: {exc}'

    return render(request, 'rent_cal.html', {
        'dis': distance_value,
        'query_results': query_results,
        'error': error,
    })


def all_term(request):
    query_results = terminal.objects.all()
    return render(request, 'all_term.html', {'query_results': query_results})
        

