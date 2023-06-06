import pandas as pd
from fpdf import FPDF


class User:
    @staticmethod
    def user_number():
        number = int(input("Choose the product to buy: "))
        return number


class CsvFile:
    def __init__(self):
        self.file_path = 'storage.csv'
        self.data = pd.read_csv(self.file_path)

    def modify(self, number: int) -> dict:
        content_to_return = {}
        data = self.data
        for index, row in data.iterrows():
            if row["id"] == number:
                content_to_return['id'] = row["id"]
                content_to_return['name'] = row["name"]
                content_to_return['price'] = row["price"]
                data.at[index, 'in stock'] = row["in stock"] - 1

        data.to_csv(self.file_path, index=False)
        return content_to_return


class Counter:
    @staticmethod
    def load_receipt_count():
        with open("receipt_count.txt", "r") as file:
            return int(file.read())

    @staticmethod
    def save_receipt_count(receipt_count):
        with open("receipt_count.txt", "w") as file:
            file.write(str(receipt_count))


class Receipt:
    receipt_count = Counter.load_receipt_count()

    def create_pdf_receipt(self, product_id: str | int, product_name: str, price: float | int) -> None:
        receipt_count = self.receipt_count
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt N{receipt_count}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"ID: {product_id}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Name: {product_name}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {price}", ln=1)

        pdf.output("example.pdf")
        receipt_count += 1
        Counter.save_receipt_count(receipt_count)


if __name__ == "__main__":
    # print the products
    store = CsvFile()
    products = store.data
    print(products)
    # take input
    user_number = User.user_number()
    # modify the storage
    check = store.modify(user_number)
    # example {'id': 100, 'name': 'laptop sven 10', 'price': 999.0}
    # initialize the pdf print
    p_id = check['id']
    p_name = check['name']
    p_price = check['price']

    receipt = Receipt()
    receipt.create_pdf_receipt(p_id, p_name, p_price)
