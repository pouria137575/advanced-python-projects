import requests
from bs4 import BeautifulSoup

def extract_restaurant_data(url="https://takhfifan.com/tehran/restaurants-cafes"):
    """Fetches restaurant data from the provided URL and returns a list of dictionaries.

    Args:
        url (str, optional): The URL of the restaurant listing page. Defaults to "https://takhfifan.com/tehran/restaurants-cafes".

    Returns:
        list: A list of dictionaries containing restaurant names and ratings.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []  # Return empty list on error

    soup = BeautifulSoup(response.text, 'html.parser')

    # Improved restaurant name extraction (assuming consistency within class)
    restaurant_elements = soup.find_all("p", class_="vendor-card-box__title-text")
    restaurants = [element.text.strip() for element in restaurant_elements]

    # Improved rating extraction (assuming consistency within class)
    rating_elements = soup.find_all("p", class_="rate-badge__rate-value")
    ratings = [element.text.strip() for element in rating_elements]

    # Ensure data lengths match and create restaurant data
    if len(restaurants) == len(ratings):
        restaurant_data = [{'name': name, 'rating': rating} for name, rating in zip(restaurants, ratings)]
    else:
        print("Warning: Mismatched number of restaurants and ratings. Returning empty data.")
        restaurant_data = []

    return restaurant_data

if __name__ == "__main__":
    restaurants = extract_restaurant_data()
    if restaurants:
        for restaurant in restaurants:
            print(f"Restaurant: {restaurant['name']}, Rating: {restaurant['rating']}")
    else:
        print("No restaurant data found.")
