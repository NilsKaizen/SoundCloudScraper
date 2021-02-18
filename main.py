from selenium import webdriver
import bs4
from requests_html import HTMLSession
import os

# new, top, mix, track and artist urls
top_url = "https://soundcloud.com/charts/top"
new_url = "https://soundcloud.com/charts/new"
track_url = "https://soundcloud.com/search/sounds?q="
artist_url = "https://soundcloud.com/search/people?q="
mix_url_end = "&filter.duration=epic"  # Look for songs that are 30 min or longer

# create the selenium browser
browser = webdriver.Chrome("YOUR_PATH_TO_CHROMEDRIVER")
browser.get("https://soundcloud.com")

# main menu
print()
print(">>> welcome to the Python Sound Cloud Scraper!")
print(">>> Explore the Top / New & Hot Charts for all Genres")
print(">>> Search for tracks, artists and mixes")
print()

while True:
    print(">>> Menu:")
    print(">>> 1 - Search for a track")
    print(">>> 2 - Search for an artists")
    print(">>> 3 - Search for a mix")
    print(">>> 4 - Top Charts")
    print(">>> 5 - New Charts")
    print(">>> 0 - Exit")
    print()
    try:
        choice = int(input(">>> Your choice (\"0\" to exit): "))
    except:
        print()
        print("ERROR: You should enter a number from 0 to 5")
        print()
        continue

    # Quit
    if choice == 0:
        browser.quit()
        break
    print()

    # Search for a Track
    if choice == 1:
        name = input(">>> Name of the Track: ")
        print()
        "%20".join(name.split(" "))  # Change all spaces in name with %20 because that's how url supports spaces
        browser.get(track_url + name)
        continue

    # Search for an Artist
    if choice == 2:
        name = input(">>> Name of the Artist: ")
        print()
        "%20".join(name.split(" "))  # Change all spaces in name with %20 because that's how url supports spaces
        browser.get(artist_url + name)
        continue

    # Search for a Mix
    if choice == 3:
        name = input(">>> Name of the Mix: ")
        print()
        "%20".join(name.split(" "))  # Change all spaces in name with %20 because that's how url supports spaces
        browser.get(track_url + name + mix_url_end)
        continue

    # Get the top 50 tracks for a genre
    if choice == 4:
        session = HTMLSession()
        r = session.get(top_url)

        if r.status_code == 200:

            links = r.html.find("a[href*=genre]")  # get all links in the page filter all links that have genre in it
            genres = [link.text for link in links[4:]]  # get all the names of genres
            urls = [str(link.absolute_links) for link in links[4:]]  # get the url of the genre

            for index, genre in enumerate(genres, 1):  # Sow the options to the user
                print(str(index) + ": " + genre)

            session.close()

            print()
            choice = input(">>> You choice (\"x\" to go back to main menu): ")
            print()

            while True:
                if choice == "x":
                    break
                else:
                    if int(choice) < len(genres) + 1:
                        choice = int(choice) - 1  # Because we started enumeration with 1

                        url = urls[choice].strip('{\'}')
                        r = session.get(url)
                        if r.status_code == 200:

                            links = r.html.find("h2")[3:]
                            tracks = [t.text for t in links]
                            tracks_urls = [u.find("a[itemprop]") for u in links]
                            tracks_urls = [str(u[0].absolute_links).strip('{\'}') for u in tracks_urls]
                            tracks_urls = tracks_urls

                            for index, track in enumerate(tracks, 1):
                                print(str(index) + ": " + track)
                            print()

                            session.close()
                            # Songs selection loop
                            i = True
                            while i:
                                choice = input(">>> Your choice (\"x\" to exit): ")
                                print()

                                if choice == "x":
                                    break
                                else:
                                    choice = int(choice) - 1  # Because we started enumeration with 1
                                print("Now playing: " + tracks[choice])
                                print()

                                browser.get(tracks_urls[choice])
                        else:
                            print()
                            print("ERROR: Genre page not found")
                            print()
                            break
                    else:
                        print()
                        print(f"ERROR Should enter an integer from 0 to {len(genres)} or \"x\"")
                        break
                        print()

    # Get new and hot tracks for genre
    if choice == 5:
        session = HTMLSession()
        r = session.get(new_url)

        if r.status_code == 200:

            links = r.html.find("a[href*=genre]")  # get all links in the page filter all links that have genre in it
            genres = [link.text for link in links[4:]]  # get all the names of genres
            urls = [str(link.absolute_links) for link in links[4:]]  # get the url of the genre

            for index, genre in enumerate(genres, 1):  # Sow the options to the user
                print(str(index) + ": " + genre)

            session.close()

            print()
            choice = input(">>> You choice (\"x\" to go back to main menu): ")
            print()

            while True:
                if choice == "x":
                    break
                else:
                    if int(choice) < len(genres) + 1:
                        choice = int(choice) - 1  # Because we started enumeration with 1

                        url = urls[choice].strip('{\'}')
                        r = session.get(url)
                        if r.status_code == 200:

                            links = r.html.find("h2")[3:]
                            tracks = [t.text for t in links]
                            tracks_urls = [u.find("a[itemprop]") for u in links]
                            tracks_urls = [str(u[0].absolute_links).strip('{\'}') for u in tracks_urls]
                            tracks_urls = tracks_urls

                            for index, track in enumerate(tracks, 1):
                                print(str(index) + ": " + track)
                            print()

                            session.close()
                            # Songs selection loop
                            i = True
                            while i:
                                choice = input(">>> Your choice (\"x\" to exit): ")
                                print()

                                if choice == "x":
                                    break
                                else:
                                    choice = int(choice) - 1  # Because we started enumeration with 1
                                print("Now playing: " + tracks[choice])
                                print()

                                browser.get(tracks_urls[choice])
                        else:
                            print()
                            print("ERROR: Genre page not found")
                            print()
                            break
                    else:
                        print()
                        print(f"ERROR Should enter an integer from 0 to {len(genres)} or \"x\"")
                        break
                        print()

        continue

print()
print("Good Bye !")
print()
