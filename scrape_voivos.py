from VoivoModel import get_voivo_urls, scrape_voivo

for x in get_voivo_urls():
    scrape_voivo(x).write_to_file("wojewodztwa.csv")