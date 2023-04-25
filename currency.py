from currency_converter import CurrencyConverter


def EURtoUSD(data: str):
    try:
        if "," in data:
            data = data.replace(",", ".")
        c = CurrencyConverter()
        data = round(c.convert(float(data), 'EUR', 'USD'), 2)
        print(str(data).replace(".", ","))
        return str(data).replace(".", ",")
    except Exception as e:
        print("Exception currency - EURtoUSD - " + str(e))
        raise(e)


if __name__ == '__main__':
    pass
