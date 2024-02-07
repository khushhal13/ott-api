# search_app/views.py
from django.shortcuts import render
import requests

def search(request):
    query = request.GET.get('q', '')

    if query:
        results = fetch_ott_results(query)
    else:
        results = []

    return render(request, 'search_app/search.html', {'query': query, 'results': results})

def fetch_ott_results(query):
    url = "https://ott-details.p.rapidapi.com/search"
    querystring = {"title": query, "page": "1"}
    headers = {
        "X-RapidAPI-Key": "f1c8b787c7msh7cdea8ef19142b3p10dd68jsn83ac75348439",
        "X-RapidAPI-Host": "ott-details.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        
        # Extract necessary details from the API response
        results = []
        for item in data.get('results', []):
            result = {
                'title': item.get('title', ''),        # Title
                'type': item.get('type', ''),          # Type
                'imageurl': item.get('imgurl', ''),  # Image URL
                'genre': item.get('genre', ''),        # Genre
                'released': item.get('released', ''),  # Released Date
                'synopsis': item.get('synopsis', ''),  # Synopsis
            }
            results.append(result)
            
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OTT API: {e}")
        return []
