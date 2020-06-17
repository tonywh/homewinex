import requests
import lxml.html as lh
#from recipe.apps.models import Ingredient

def main():

    # Read the data from the table in web page
    page = requests.get('http://www.brsquared.org/wine/CalcInfo/FruitDat.htm')
    doc = lh.fromstring(page.content)
    rows = doc.xpath('//body/table[2]//tr')

    # Convert data to a list of dictionaries
    headings = []
    table = []
    r = 0
    for row in rows:
        print(r)
        if r == 0:
            for c, col in enumerate( row ):
                name = col.text_content().strip()
                headings.append(name)
            r += 1
        else:
            if len(row) == len(headings):
                table.append({})
                for c, col in enumerate( row ):
                    value = col.text_content().strip()
                    table[r-1][headings[c]] = value
                r += 1
            else:
                print( f'Row {r} wrong length ({len(row)}) ')

    fruit = ''
    for row in table:
        # Store it if it's an average value for a fruit varity

        if row['Fruit'] == '':
            row['Fruit'] = fruit
            print('SPECIFIC: ', end='')
            print(row)
        else:
            fruit = row['Fruit']
            if row['Variety'] == '(average)' or row['Variety'] == '':
                print('AVERAGE:  ', end='')
                print(row)
            else:
                print('SPECIFIC: ', end='')
                print(row)

if __name__ == '__main__':
    main()
