import codecs
from bs4 import BeautifulSoup,NavigableString
from os import sys

path = sys.argv[1];
f = codecs.open(path, encoding='utf-8')
html = f.read()

# First element with matching body content
def content_first_match(tags, content):
    for tag in tags:
        if tag.string and tag.string.strip() == content:
            return tag
            
# Next sibling element that is not whitespace
def next_sibling_element(element):
    sibling = element.next_sibling
    # print(type(sibling))
    if type(sibling) is NavigableString:
        return next_sibling_element(sibling)
    else:
        return sibling

headers = ["Date", "Value date", "Name", "Amount EUR", "Amount orig", "Rate", "Location", "Reference"]
print(";".join(headers));
            
soup = BeautifulSoup(html, "html.parser")
for t in soup.find_all("div", class_="transaction"):
    for tHeader in t.find_all("div", class_="header"):
        childDivs = tHeader.find_all("div", recursive=False)
        date = childDivs[0].string.strip()
        name = childDivs[1].string.strip()
        amount = childDivs[2].string.strip()
        
        tRow = next_sibling_element(tHeader)
        def get_val(header):
            if(header):
                return next_sibling_element(header).string.strip()
            else:
                return ""
            
        ref = get_val(content_first_match(tRow.descendants, "Arkistointiviite"))
        location = get_val(content_first_match(tRow.descendants, "Sijainti"))
        valueDate = get_val(content_first_match(tRow.descendants, "Arvopäivä"))
        amountOrig = get_val(content_first_match(tRow.descendants, "Alkuperäinen summa"))
        rate = get_val(content_first_match(tRow.descendants, "Valuuttakurssi"))
    
        print(";".join([
                date, valueDate, name, amount, amountOrig, rate, location, ref
            ]));
        
    
