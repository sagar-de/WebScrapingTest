import os
from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup

quotes=[]
base_url_wongnai = 'https://www.wongnai.com/restaurants?categories=59&regions=9681'
req = Request(
    base_url_wongnai,
    headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

bsh = BeautifulSoup(webpage, 'html.parser')
base_wongnai_detail_url = bsh.findAll('a', attrs={'class': 'sc-10ino0a-13 dKFLtJ'})
base_wongnai_detail_url_list = []
wongnai_base_url = "https://wongnai.com/"

Cafe_Name=[]
Cafe_Category =[]
Cafe_img=[]
Cafe_Price=[]

for url in base_wongnai_detail_url:
    base_wongnai_detail_url_list.append(wongnai_base_url + url['href'])

for restaurent_url in base_wongnai_detail_url_list:
    req = Request(
        restaurent_url,
        headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    bsh = BeautifulSoup(webpage, 'html.parser')
    '''cafe name'''
    cafe_name = bsh.find('h1', attrs={'data-track-id': "business-cover-header-title"})
    Cafe_Name.append(cafe_name.text)
    print("cafe name: ",Cafe_Name)
    '''cafe_image'''
    cafe_image = bsh.findAll('img', attrs={'data-track-id': "business-photo"})
    for image in cafe_image:
        Cafe_img.append(image['src'])
    '''cafe_price'''
    cafe_price_range = bsh.find('span', attrs={'class': "sc-1kh6w3g-1"})
    Cafe_Price.append(cafe_price_range.text)
    '''cafe category'''
    cafe_cat = bsh.find('a', attrs={'data-track-id': "business-cover-categories"})
    Cafe_Category.append(cafe_cat.text)
    print("cafe_cat: ",Cafe_Category)
    ####Parse View All Url
    cafe_detail_url = bsh.findAll('a', attrs={'class': 'sc-10ak5zj-0 gyjqEZ sc-1365huc-2 gKiAgG'})
    tag = 'menu'
    Product_Name=[]
    product_price=[]
    Product_img=[]
    for url in cafe_detail_url:
        menu_url = url['href']
        if menu_url.find('menu'):
            complete_url = 'https://www.wongnai.com/' + menu_url
            req = Request(complete_url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            bsh = BeautifulSoup(webpage, 'html.parser')

            '''product name'''
            try:
                product_name = bsh.findAll('div', attrs={'class': "ricb8s-2 gySlrN"})
                for pro_name in product_name:
                    if pro_name.text == None:
                        print("Product Name Not Found")
                        Product_Name.append(pro_name.text)
            except Exception as e:
                print(e)

            '''product_price'''
            try:
                product_price = bsh.findAll('div', attrs={'class': "ricb8s-6 dmTbmp"})
                for price in product_price:
                    if price.text == None:
                        print("Price not found")
                        product_price.append(price.text.replace("THB", ""))
            except Exception as e:
                print(e)

            '''Recomnded user'''
            try:
                recmonded_product = bsh.findAll('img', attrs={'class': "mnqwk5-1 LSoWc"})
                recmonded_product_href = bsh.findAll('div', attrs={'class': '_21btc6ycbuwmnmRpkhCZGl mnqwk5-1 LSoWc'})

                for href in recmonded_product_href:
                    if href.find('a')['href'] == None:
                        print("Product Url Not found")
                    print(href.find('a')['href'])
            except Exception as e:
                print(e)

            try:
                for prod in recmonded_product:
                    if prod['src'] == None or prod['title'] == None:
                        print("Source and title of recommended product not found")
                    src = prod['src']
                    title = prod['title']
                    print("recomended :" + src + "  " + title)

                '''product_photo'''
                product_photo = bsh.findAll('div', attrs={'class': "sc-1xmxu10-0 hwQWQt _2tANtL-R5DV884KIYx7G_s"})
                for image in product_photo:
                    if image.find('img')['src'] == None:
                        print("Source not found for recommended product")
                        Product_img.append(image.find('img')['src'])
            except Exception as e:
                print(e)


# Writing The Information to CSV
restaurent_df = pd.DataFrame({'Cafe Name': Cafe_Name,
'Cafe Category/ Type of Food': Cafe_Category,
'Product Name': Product_Name,
'Product Price': product_price,
'Product Photo': Product_img
})
print(restaurent_df.info())
restaurent_df.to_csv(os.getcwd() +'/restaurent_data.csv')