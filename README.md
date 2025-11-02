## spotify_automation_tests

Spotify automated API tests

### Overview

This project demonstrates how to automate API testing for Spotify endpoints such as:
- Retrieving artist details
- Fetching top tracks
- Accessing album information
- Handling negative and edge cases

### Setup

1. Create a [Spotify Developer Account](https://developer.spotify.com/) and obtain your credentials (`CLIENT_ID` and `CLIENT_SECRET`).
2. Add a configuration file or set environment variables for your credentials e.g.:
   ```python
   CLIENT_ID = "xxxxxxxxxxxx"
   CLIENT_SECRET = "xxxxxxxxxx"

### Built with

- Python
- Pytest
- Playwright

### Notes

These tests use the Spotify Client Credentials Flow to obtain an access token.

All requests are made to the official [Spotify Web API](https://developer.spotify.com/documentation/web-api)

