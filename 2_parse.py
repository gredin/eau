import pickle

from bs4 import BeautifulSoup

pages = []

for i in range(2500):
    with open("html/%d.html" % i, "r") as f:
        trs = []

        content = f.read()
        soup = BeautifulSoup(content, "html.parser")

        trs.append([str(td.string)
                    for td in soup.find(string="Date du prélèvement").find_parent("tr").find_all("td")])

        for tr in soup.find(string="Paramètres analytiques").find_parent("table").find_next_sibling("table").find_all("tr"):
            trs.append([str(td.string) for td in tr.find_all("td")])

        trs_dict = {}
        for tds in trs:
            trs_dict[tds[0]] = tds[1:]

        pages.append((i, trs_dict))

with open("pages.pickle", "wb") as f:
    pickle.dump(pages, f)
