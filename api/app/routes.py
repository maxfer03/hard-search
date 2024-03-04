from app import app
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
import utils
import re
import time



@app.route('/')
def index():
    # Home route that returns a string
    return '''Harware search - Conurbano/caba
    
    NOTAS:
    Algunas páginas no tienen el precio listado:
    - ashir.com.ar
    - pcarts.com

    TODO:
    - Alltek
    - Diamond Computacion
 
    '''

@app.route('/search', methods=['GET'])
def search(): 
    # Get the query parameter from the URL
    query = request.args.get('query', '')
    # If no query provided, return an error
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    #query = query.replace(' ', '%20')
    
    # List of pages to search
    pages = [
        {
            'name': 'Full H4rd',
            'location': 'Microcentro, CABA',
            'base_url': "https://www.fullh4rd.com.ar",
            'suffix': f'/cat/search/{query}',
        },
        {
            'name': 'Ether Gaming',
            'location': 'San Miguel',
            'base_url': f"https://ethergaming.com.ar",
            'suffix': f'/?s={query}&post_type=product'
        },
        {
            'name': 'Rocket Hard',
            'location': 'Merlo',
            'base_url': f"https://www.rockethard.com.ar",
            'suffix': f'/buscar/?q={query}'
        },
        # Commenting xt-pc for now, unsafe site
        # {
        #     'name': 'xt-pc',
        #     'location': 'Microcentro, CABA',
        #     'base_url': f"https://www.xt-pc.com.ar",
        #     'suffix': f'/cat/search/{query}'
        # },
        {
            'name': 'Gaming City',
            'location': 'San Miguel',
            'base_url': f"https://www.tienda.gamingcity.com.ar",
            'suffix': f'/{query}'
        },
        {
            'name': 'HyperGAMING',
            'location': 'Saavedra, CABA',
            'base_url': f"https://www.hypergaming.com.ar",
            'suffix': f'/buscar/?q={query}'
        },
        {
            'name': 'Gezatek',
            'location': 'Almagro, CABA',
            'base_url': f"https://www.gezatek.com.ar",
            'suffix': f'/tienda/?busqueda={query}'
        },
        {
            'name': 'Gauss Online',
            'location': 'Monte Castro / Velez Sarsfield, CABA',
            'base_url': f"https://www.gaussonline.com.ar",
            'suffix': f'/{query}'
        },
        {
            'name': 'Insumos Acuario',
            'location': 'Colegiales, CABA',
            'base_url': f"https://www.insumosacuario.com.ar",
            'suffix': f'/buscar/?q={query}'
        },
        {
            'name': 'MLX',
            'location': 'Saavedra / Nuñez, CABA',
            'base_url': f"https://mlx.com.ar",
            'suffix': f'/?s={query}&post_type=product&dgwt_wcas=1'
        },
        {
            'name': 'MEXX',
            'location': 'Caballito, CABA',
            'base_url': f"https://www.mexx.com.ar",
            'suffix': f'/buscar/?p={query}'
        },
        {
            'name': 'Katech',
            'location': 'Lanus',
            'base_url': f"https://katech.com.ar",
            'suffix': f'/?s={query}&post_type=product&dgwt_wcas=1'
        },
        
        
    ]
    

    def get_page_data(page, idx):
      print(idx, 'scraping at', page['name'])
      final_data = {}
      def base_scrape(url, parse_function):
        try:
          response = requests.get(url, timeout=5)
        except requests.exceptions.ReadTimeout:
            return 'Timeout', 408
        

        if response.status_code != 200:     
            print(f"Failed to fetch data at  {page['name']}")
            return 'Failed to fetch data', 500
        soup = BeautifulSoup(response.content, 'html.parser')
      
        data = parse_function(soup)
      
        return data



      if idx == 0 or idx == 3:
        #Full h4rd | xt-pc
        def parse_site0 (soup):
          card_class =  "product-list"
          price_class = 'price'
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('div', class_=price_class).text.split(' ')[0]
            title = item.find('h3').text
            prodUrl = page['base_url']+item.find('a', href=True)['href']
          except AttributeError:
            price = 0
            title = "No Product Found"

          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",
          }
        final_data = base_scrape(page['base_url']+page['suffix'], parse_site0)
      elif idx == 1:
        #Ether Gaming
        def parse_site1(soup):
          card_class =  "product-type-simple"
          price_class = 'price-box'
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)

          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('div', class_=price_class).text.split(' ')[0]
            title = item.find('h2').text
            prodUrl = item.find('a', href=True)['href']
          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",

          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site1)

      elif idx == 2:
        #Rocket Hard
        def parse_site2(soup):
          card_class =  "prod-cat"
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('b').text
            title = item.find('h4').text
            prodUrl = item.find('a', href=True)['href']
          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",
          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site2)
      elif idx == 4 or idx== 7:
        #Gaming City | Gauss Online
        def parse_site4(soup):
          card_class = "ui-search-layout__item"
          price_class = 'ui-search-item__group ui-search-item__group--price ui-search-item__group--price-grid-container shops__items-group'
          listing_items = soup.find_all('li', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('div', class_=price_class).text
            title = item.find('h2').text
            prodUrl = item.find('a', href=True)['href']

          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",
          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site4)

      elif idx == 5:
        #HyperGAMING
        def parse_site5(soup):
          card_class =  "prod-cat"
          title_class = 'card-title'
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('b').text
            title = item.find('h4', class_=title_class).text
            prodUrl = item.find('a', href=True)['href']

          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",

          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site5)
      elif idx == 6:
        #Gezatek
        def parse_site6(soup):
          card_class = "product"
          price_class = 'precio_web'
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('h3', class_=price_class).text
            title = item.find('h2').text
            prodUrl = page['base_url']+item.find('a', href=True)['href']

          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",
          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site6)

      elif idx == 8:
        #Insumos Acuario
        def parse_site8(soup):
          card_class = "listado-"
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('b').text
            title = item.find('h4').text
            prodUrl = item.find('a', href=True)['href']

          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",
          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site8)
      elif idx == 9:
        #MLX
        def parse_site9(soup):
          card_class = "product"
          price_class = "woocommerce-Price-amount"
          listing_items = soup.find_all('article', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          item = utils.checkForQuery(query, listing_items)
          try:
            price = item.find('span', class_=price_class).text
            title = item.find('h2').text
            prodUrl = item.find('a', href=True)['href']

          except AttributeError:
            price = 0
            title = "No Product Found / Price not Specified"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",
          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site9)
      elif idx == 10:
        #MEXX
        def parse_site10(soup):
          card_class = "card-ecommerce"
          title_class = "card-title"
          listing_items = soup.find_all('div', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)

          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('b').text
            title = item.find('h4', class_=title_class).text
            prodUrl = item.find('a', href=True)['href']
          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",

          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site10)
      elif idx == 11:
        #Katech
        def parse_site11(soup):
          card_class = "product"
          price_class = "price"
          listing_items = soup.find_all('article', class_=card_class)
          listing_items = utils.excludeCombos(listing_items)
          try:
            item = utils.checkForQuery(query, listing_items)
            price = item.find('p', class_=price_class).text
            title = item.find('h2').text
            prodUrl = item.find('a', href=True)['href']

          except AttributeError:
            price = 0
            title = "No Product Found"
          return {
            'prod': utils.formatTitle(title),
            'price': utils.formatPrice(price),
            'prodUrl': prodUrl if 'prodUrl' in locals() else "",

          }
        final_data = base_scrape(page['base_url']+page['suffix'],parse_site11)
      
      if type(final_data) is tuple:
        return {
          'name': page['name'],
          'price': 0,
          'error': final_data[0]
        }
      return {
         'name': page['name'],
         'location': page['location'],
         'prod': final_data['prod'] if final_data and 'prod' in final_data else "No Product Found",
         'prodUrl': final_data['prodUrl'] if final_data and 'prodUrl' in final_data else "",
         'price': final_data['price']
      }

    searchResults = []
    for idx, page in enumerate(pages):  
      searchResults.append(get_page_data(page, idx))


                    
    notFoundShops = list(filter(lambda x: x['price'] == 0, searchResults))
    searchResults[:] = [d for d in searchResults if d['price'] != 0]
    finalResults = sorted(searchResults, key=lambda d: d['price'])

    final = {
      'found' : finalResults,
      'not_found': notFoundShops
    }
    return jsonify(final)

