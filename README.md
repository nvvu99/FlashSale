# Flashsale Scraper

This projects used (Scrapy)[https://scrapy.org/] to scrape the flashsale products from (tiki.vn)[https://tiki.vn] and (sendo.vn)[https://sendo.vn]

# Run this project
* Clone this project:
```
git clone https://github.com/nvvu99/FlashSale.git
```
* `cd` to `FlashSale` and install requirements:
```
cd FlashSale
pip install -r requirements.txt
```
* Start Scrapy
```
scrapy crawl
```
* The scraped data will be stored at two file `category.json` and `product.json`

# Project demo
The demo of this project is at the folder Demo. Create a folder named `Product` and run the file `flashsale.exe`.

# Sample scraped data
* Product
``` json
{
  "product_id": "tiki54550261", 
  "name": "Quạt USB mini Cho Điện Thoại iPhone NS 5600", 
  "image": "https://salt.tikicdn.com/cache/280x280/ts/product/19/f4/47/f5d14f10c8bfb4ba9dbe39c83fe1db5a.jpg", 
  "category_id": 1882, 
  "url": "https://tiki.vn/quat-usb-mini-cho-dien-thoai-iphone-ns-5600-p16217211.html?spid=54550261", "origin_price": 105000, 
  "discount_price": 15000, 
  "quantity": 8, 
  "remain": 8, 
  "start_time": 1589821200, 
  "end_time": 1590944399, 
  "rating": 0, 
  "review": 0
}
```
* Category
``` json
{
  "category_id": 1882, 
  "category_name": "Điện Gia Dụng"
}
```