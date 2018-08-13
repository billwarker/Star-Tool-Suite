import sqlite3
import openpyxl
import os
from bs4 import BeautifulSoup
import datetime
from Files.file_io import LeanDownloader, _convert_xml_to_xlsx
from settings import DOWNLOAD_DIR, STAR_PAYLOAD, SBW_PAYLOAD, CHROMEDRIVER, DATABASE, INVENTORY_DIR

def update_inventory(inventory_file, db, table):
	print('Updating inventory in database...')

	conn = sqlite3.connect(db)
	cur = conn.cursor()

	wb = openpyxl.load_workbook(inventory_file)
	sheet = wb.active

	added_skus = set()
	added_count = 0
	updated_skus = set()
	no_upc = set()

	for row in range(2, sheet.max_row + 1):

		item_num = sheet['A' + str(row)].value
		item_sku = sheet['B' + str(row)].value
		item_desc = sheet['C' + str(row)].value
		item_inv = int(sheet['E' + str(row)].value)
		item_upc = sheet['I' + str(row)].value
		item_info = (item_num, item_sku, item_desc, item_inv, item_upc)
		
		if item_upc == '':
			item_upc = str(0)
			no_upc.add(item_sku)

		try:
			cur.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?, ?, 0)",
				item_info)
			#conn.commit()
			print('Added', item_sku)
			added_skus.add(item_sku)
			print('Added {} to database.'.format(item_sku))
			added_skus.add(item_sku)
			added_count += 1

		except sqlite3.IntegrityError:
			cur.execute("SELECT item_inv FROM " + table + " WHERE item_sku = ?", (item_sku,))
			prev_inv = int(cur.fetchone()[0])
			cur.execute("UPDATE " + table + " SET item_inv = ?  WHERE item_sku = ?", (item_inv, item_sku))

			if prev_inv != item_inv:
				updated_skus.add("{} {} ---> {}".format(item_sku, prev_inv, item_inv))

	print('Updated.')
	print('SKUs added:', added_count)
	for sku in added_skus:
		print(sku)
	print("---")
	print('SKUs updated:', len(updated_skus))
	for sku in updated_skus:
		print(sku)

	conn.commit()
	cur.close()
	conn.close()

if __name__ == '__main__':
	os.makedirs(INVENTORY_DIR, exist_ok=True)
	
	name1 = "STAR Inventory {}".format(datetime.date.today().strftime("%m-%d-%Y"))
	name2 = "SBW Inventory {}".format(datetime.date.today().strftime("%m-%d-%Y"))
	
	downloader = LeanDownloader(CHROMEDRIVER)
	downloader.login(STAR_PAYLOAD)
	star_inventory = _convert_xml_to_xlsx(downloader.download_inventory(DOWNLOAD_DIR), name1, INVENTORY_DIR)

	downloader.logout()
	downloader.login(SBW_PAYLOAD)
	sbw_inventory = _convert_xml_to_xlsx(downloader.download_inventory(DOWNLOAD_DIR), name2, INVENTORY_DIR)
	downloader.close()

	update_inventory(star_inventory, DATABASE, "star_inventory")
	update_inventory(sbw_inventory, DATABASE, "sbw_inventory")
	

		

