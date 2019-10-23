import requests

number_pages = 2500

region = "52"
departement = "044"
commune = "44162"
reseau = "044000138_044"

sess = requests.session()

sess.get("https://orobnat.sante.gouv.fr/orobnat/afficherPage.do?methode=menu&usd=AEP&idRegion=%s" % region)

for i in range(number_pages):
    resp = sess.post("https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do",
                     headers={
                         "Origin": "https://orobnat.sante.gouv.fr",
                         "Content-Type": "application/x-www-form-urlencoded",
                         "User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
                         "Referer": "https://orobnat.sante.gouv.fr/orobnat/rechercherResultatQualite.do",
                     },
                     data={
                         "methode": "rechercher",
                         "idRegion": region,
                         "usd": "AEP",
                         "departement": departement,
                         "communeDepartement": commune,
                         "reseau": reseau,
                         "posPLV": i,
                     })

    if resp.status_code != 200:
        print("FAILURE (i = %d)", i)
        continue

    with open("html/%d.html" % i, "w") as f:
        f.write(resp.text)

    print(i)
