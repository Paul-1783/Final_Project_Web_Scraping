import errno
import operator
import os
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

url = "https://www.imdb.com/chart/top/"
page = requests.get(url)
if page.status_code == 200:
    soup = BeautifulSoup(page.text, "html.parser")

list_of_all_tagged_titles_with_dates = soup.find_all("td", class_="titleColumn")
list_of_film_titles = []
for elem in list_of_all_tagged_titles_with_dates:
    list_of_film_titles.append(str(elem).partition(">")[2].partition(">")[2].partition("<")[0])

list_of_dates = list(soup.find_all("span", class_="secondaryInfo"))
list_of_dates_untagged = []
for elem2 in list_of_dates:
    list_of_dates_untagged.append(str(elem2).partition(">")[2].partition("<")[0].replace("(", "").replace(")", ""))

images = soup.findAll('img')

try:
    os.mkdir("all_images")
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

list_of_image_paths = []

if len(images) != 0:
    for i, image in enumerate(images):
        try:
            image_link = image["src"]
            r = requests.get(image_link).content
            try:
                r = str(r, 'utf-8')
            except UnicodeDecodeError:
                image_path = f"all_images/images{i + 1}.jpg"
                list_of_image_paths.append(image_path)
                with open(image_path, "wb+") as f:
                    f.write(r)
        except OSError:
            print("img content not available.")

movies_and_their_date_of_appearance = dict(zip(list_of_film_titles, list_of_dates_untagged))
image_paths_and_date_of_appearance = dict(zip(list_of_image_paths, list_of_dates_untagged))


dict_of_dates_with_movie_numbers = {}
for k, v in movies_and_their_date_of_appearance.items():
    if v not in dict_of_dates_with_movie_numbers:
        dict_of_dates_with_movie_numbers[v] = 1
    else:
        dict_of_dates_with_movie_numbers[v] += 1

dict_of_best_years = dict(sorted(dict_of_dates_with_movie_numbers.items(), key=operator.itemgetter(1), reverse=True)[:10])


plt.figure(1)
plt.xlabel("Date of Appearance")
plt.ylabel("Number of Movies")
plt.bar(*zip(*dict_of_best_years.items()))


e = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
f = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
fig, ax = plt.subplots(figsize=(15, 15))
plt.setp(ax, xlabel='Date of Appearance')
plt.setp(ax, ylabel='Number of Movies')
for key, value in image_paths_and_date_of_appearance.items():
    ab = AnnotationBbox(OffsetImage(plt.imread(key), zoom=0.5), (float(value), float(dict_of_dates_with_movie_numbers[value])),
                        frameon=False)
    ax.add_artist(ab)
plt.scatter(e, f, alpha=0)

plt.show()
