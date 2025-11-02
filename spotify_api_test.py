import pytest
from playwright.sync_api import sync_playwright
import base64
from urllib.parse import urlencode

from config import *  # import CLIENT_ID, CLIENT_SECRET
from constants import *
from helpers import *


# --- FIXTURES ---


@pytest.fixture(scope="session")
def api_context():
    """Playwright API context fixture for HTTP requests."""
    playwright = sync_playwright().start()
    context = playwright.request.new_context()
    yield context
    playwright.stop()


@pytest.fixture(scope="session")
def spotify_token(api_context):

    # Create Basic Auth header for Spotify API
    client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("utf-8")
    client_creds_b64 = base64.b64encode(client_creds).decode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {client_creds_b64}"}

    response = api_context.post(TOKEN_URL, form={"grant_type": "client_credentials"}, headers=headers)

    print(f"\nResponse: {response}")
    print(f"Response body: {response.text()}")

    assert response.status == STATUS_OK
    token_data = response.json()
    return token_data["access_token"]


# --- TESTS ---


# ✅ POSITIVE TEST - get artist details
def test_get_artist_success(api_context, spotify_token):
    response = spotify_get(api_context, spotify_token, f"/v1/artists/{ARTIST_ID_VALID}")
    assert response.status == STATUS_OK
    data = response.json()
    assert data["id"] == ARTIST_ID_VALID
    assert "name" in data
    assert "genres" in data
    assert "images" in data
    assert isinstance(data["images"], list)
    assert isinstance(data["genres"], list)
    assert "popularity" in data
    print(f"Artist name: {data['name']}, popularity: {data['popularity']}")


# ❌ NEGATIVE TEST - get artist with invalid ID
def test_get_artist_invalid_id(api_context, spotify_token):
    response = spotify_get(api_context, spotify_token, f"/v1/artists/{ARTIST_ID_INVALID}")
    print(f"Response status: {response.status}")
    print(f"Response body: {response.text()}")
    assert response.status == STATUS_NOT_FOUND


# ✅ POSITIVE TEST - get artist's top 10 tracks
def test_get_artist_top_tracks(api_context, spotify_token):
    response = spotify_get(
        api_context, spotify_token, f"/v1/artists/{ARTIST_ID_VALID}/top-tracks", params={"country": "US"}
    )
    print(f"Response status: {response.status}")
    print(f"Response body: {response.text()}")
    assert response.status == STATUS_OK
    data = response.json()
    assert "tracks" in data
    assert isinstance(data["tracks"], list)
    assert len(data["tracks"]) <= TOP_TRACKS_MAX  # maximum tracks as per Spotify API
    print("\nTop tracks:")
    for i, track in enumerate(data["tracks"], 1):
        print(f"{i}. {track['name']}")

    # ❌ NEGATIVE TEST - get top tracks with non-existent artist


def test_get_top_tracks_invalid_artist(api_context, spotify_token):
    response = spotify_get(
        api_context, spotify_token, f"/v1/artists/{ARTIST_ID_INVALID}/top-tracks", params={"country": "US"}
    )
    print(f"Response status: {response.status}")
    print(f"Body: {response.text()}")
    assert response.status == STATUS_NOT_FOUND


# ✅ EDGE CASE TEST - get top tracks without country code
def test_get_top_tracks_missing_country(api_context, spotify_token):
    response = spotify_get(api_context, spotify_token, f"/v1/artists/{ARTIST_ID_VALID}/top-tracks")
    print(f"Response status: {response.status}")
    print(f"Body: {response.text()}")

    # API returns 200 and uses default market
    assert response.status == STATUS_OK, "API should use default market when country is not specified"
    data = response.json()
    assert "tracks" in data, "Response should contain tracks array"
    # Verify that we have some tracks
    assert len(data["tracks"]) > 0, "Expected some tracks even without specifying country"
    print("\nAvailable markets for first track:", data["tracks"][0].get("available_markets", []))


# ✅ POSITIVE TEST - get album details
def test_get_album_details_success(api_context, spotify_token):
    response = spotify_get(api_context, spotify_token, f"/v1/albums/{ALBUM_ID_VALID}", params={"market": "US"})
    print(f"Response status: {response.status}")
    print(f"Body: {response.text()}")
    assert response.status == STATUS_OK
    data = response.json()

    # Basic album information
    assert data["id"] == ALBUM_ID_VALID
    assert "name" in data
    assert "release_date" in data
    assert "total_tracks" in data
    assert "album_type" in data

    # Check artists and images
    assert "artists" in data and len(data["artists"]) > 0
    assert "images" in data and len(data["images"]) > 0
    assert isinstance(data["images"], list)
    assert isinstance(data["artists"], list)

    # Print details
    print(f"\nAlbum details:")
    print(f"Name: {data['name']}")
    print(f"Release date: {data['release_date']}")
    print(f"Total tracks: {data['total_tracks']}")
    print(f"Album type: {data['album_type']}")
    print(f"Artists: {', '.join(artist['name'] for artist in data['artists'])}")


# ❌ NEGATIVE TEST - get album with non-existent ID
def test_get_album_details_invalid_id(api_context, spotify_token):
    response = spotify_get(api_context, spotify_token, f"/v1/albums/{ALBUM_ID_INVALID}", params={"market": "US"})
    print(f"Response status: {response.status}")
    print(f"Body: {response.text()}")
    assert response.status == STATUS_NOT_FOUND
    data = response.json()
    assert "error" in data, "Response should contain error details"
