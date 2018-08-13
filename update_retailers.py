import sqlite3
import csv
import openpyxl
import datetime
import os
from settings import DATABASE

def update(update_list, cur, retailer_table, retailer_str, template):
	output_wb = openpyxl.load_workbook(walmart_template)
	output_sheet = output_wb.active
	output_ix = 6

	quantity_query = """SELECT item_sku, item_inv, manufacturer_id, description, merchant_sku, upc, quantity
						FROM {} JOIN {} ON item_sku = vendor_sku
						WHERE item_inv != quantity AND status != "Discontinued" """
	status_query = """SELECT item_sku, item_inv, manufacturer_id, description, merchant_sku, upc, quantity
						FROM {} JOIN {} ON item_sku = vendor_sku
						WHERE item_inv != 0 and (status = "Unavailable" or status = "Discontinued") """
	
	for inventory in ["star_inventory", "sbw_inventory"]: 
		qty_query = cur.execute(quantity_query.format(inventory, retailer_table)).fetchall()
		stat_query = cur.execute(status_query.format(inventory, retailer_table)).fetchall()
		full_query = qty_query + stat_query

		for item in full_query:
			output_sheet['A' + str(output_ix)] = "IN"
			output_sheet['B' + str(output_ix)] = item[0]
			
			if item[1] == 0:
				output_sheet['C' + str(output_ix)] = "No"
				status = "Unavailable"
			else:
				output_sheet['C' + str(output_ix)] = "Yes"
				status = "Available"
			
			output_sheet['D' + str(output_ix)] = item[1]
			output_sheet['H' + str(output_ix)] = item[2]
			output_sheet['I' + str(output_ix)] = item[3]
			output_sheet['W' + str(output_ix)] = item[4]
			output_sheet['X' + str(output_ix)] = retailer_str
			output_sheet['Y' + str(output_ix)] = item[5]

			output_ix += 1

			cur.execute("UPDATE {} SET quantity = ? WHERE vendor_sku = ?".format(
				retailer_table), (item[1], item[0]))
			cur.execute("UPDATE {} SET status = ? WHERE vendor_sku = ?".format(
				retailer_table), (status, item[0]))
			update_list.append("{}: {} ---> {} [{}]".format(
				item[0], item[6], item[1], status))

	today = datetime.date.today().strftime("%m-%d-%Y")
	name = "{} INV. {}.xlsx".format(retailer_str, today)
	print(str(output_ix - 6) + " SKUs updated.")
	path = os.path.join(dir_path, name)

	return output_wb, path
	output_wb.save(os.path.join(dir_path, name))

if __name__ == '__main__':
	walmart_template = "Files/Warehouse InventoryTemplate - Walmart Canada.xlsx"
	bestbuy_template = "Files/Warehouse InventoryTemplate - BestBuyCA.xlsx"
	source_template = "Files/Warehouse InventoryTemplate - The Source"

	update_list = []

	dir_path = os.path.join(os.getcwd(), 'Update Sheets')
	os.makedirs(dir_path, exist_ok=True)

	db = DATABASE

	conn = sqlite3.connect(db)
	cur = conn.cursor()

	print("Generating inventory update sheets...")
	print('Walmart:')
	walmart_updated, walmart_path = update(update_list, cur, "walmart",
										"WALMARTCA", walmart_template)
	print("BestBuy:")
	bestbuy_updated, bestbuy_path = update(update_list, cur, "bestbuy",
										"BESTBUYCA", bestbuy_template)
	print("The Source:")
	source_updated, source_path = update(update_list, cur, "source",
										"THESOURCE", source_template)
	
	print("UPDATES:")
	for update in update_list:
		print(update)

	answer = input("Save update sheets? [y/n]")
	if answer == 'y':
		walmart_updated.save(walmart_path)
		bestbuy_updated.save(bestbuy_path)
		source_updated.save(source_path)

	answer = input("Commit changes to db? [y/n]")
	if answer == 'y':
		conn.commit()
		print("Updates committed.")
		cur.close()
		conn.close()
	else:
		cur.close()
		conn.close()





