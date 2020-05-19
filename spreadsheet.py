import xlsxwriter

TEMP_LISTING = "listing_to_post.xlsx"

def get_listing_data():
    workbook   = xlsxwriter.Workbook(TEMP_LISTING)
    workbook.close()
