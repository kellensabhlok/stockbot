
import requests
from bs4 import BeautifulSoup


def institutional_ownership(stockname):

    link = "https://fintel.io/so/us/{}".format(stockname)
    request_object = requests.get(link)
    html_text = request_object.text
    soup = BeautifulSoup(html_text, 'html.parser')

    # grab class table from the html
    table = soup.find('table', {'class': 'table'})

    # find where it says "institutional Shares" in table and take the next sibling
    institutional_shares = table.find('td', text="Institutional Shares (Long)").next_sibling
    # turn institutional_shares into a string
    institutional_shares = str(institutional_shares)
    # remove the first 4 characters
    institutional_shares = institutional_shares[4:]

    # find '\n' and remove everything after it
    institutional_shares = institutional_shares.split('(ex')[0]

    # replace '\n' with "shares"
    institutional_shares = institutional_shares.replace('\n', ' shares')
    return institutional_shares