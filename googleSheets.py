import gspread
import config


def write(values) -> bool:
    try:
        if type(values) != list:
            raise Exception("Data Issue")
        gc = gspread.service_account(filename='service_account.json')
        sh = gc.open(config.SHEETS_NAME)

        # values = ['Wert 1', 'Wert 2', 'Wert 3']

        last_row = len(sh.sheet1.get_all_values()) + 1
        last_row
        sh.sheet1.insert_row(values, index=last_row)
        print("Added following Data: " + str(values))
        return True
    except Exception as e:
        print("Exception - googleSheets - write - " + str(e))
        return False
