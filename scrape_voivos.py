from VoivoModel import get_voivodeship_urls, scrape_voivodeship
from utils import write_to_file

for x in get_voivodeship_urls():
    write_to_file(scrape_voivodeship(x), "wojewodztwa.csv")
