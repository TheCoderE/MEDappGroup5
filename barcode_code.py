from datetime import date
import csv
import kivy
from kivy.app import App
kivy.require('1.9.0')
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.app import App
from kivy.lang import Builder
from kivy_garden.zbarcam import ZBarCam
from kivy_garden.qrcode import QRCodeWidget

globvar = ''

Test = """
BoxLayout:
    orientation: 'vertical'
    ZBarCam:
        id: zbarcam
    Label:
        size_hint: None, None
        size: (self.texture_size[0], 50)
        text: app.get_barcodes([symbol.data.decode("utf-8") for symbol in zbarcam.symbols])
"""


class TestAPP(App):
    def build(self):
        return Builder.load_string(Test)

    def get_barcodes(self, barcodes):
        if len(barcodes) > 0:
            global globvar
            if barcodes [0] == '12345678':
                barcodes = globvar
                barcodes = '12345678'
                globvar = barcodes
                print(globvar)
            elif barcodes [0] == '11234567':
                barcodes = globvar
                b = '11234567'
                globvar = b
                print(globvar)
        return "barcodes"


if __name__ == '__main__':
    TestAPP().run()



# Code for creation of popup function with kivy


Config.set('graphics', 'resizable', True)


class PopupExample(App):

    def build(self):
        self.layout = GridLayout(cols=1000, padding=10)
        self.button = Button(text='Your medicine is expired \n '
                                  'For disposal please follow the instructions:\n click',)
        self.layout.add_widget(self.button)
        self.button.bind(on_press=self.onButtonPress)

        return self.layout



    def onButtonPress(self, button):
        layout = GridLayout(cols=1, padding=100)
        popupLabel = Label(text=medicines[barcode].how_disposal(), color= 'red')
        closeButton = Button(text="To close message, please click the x")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(title='Expiration warning', content=layout)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)



class PopupExample2(App):

    def build(self):
        self.layout = GridLayout(cols=1000, padding=10)
        self.button = Button(text='Your medicine is available.\n click',)
        self.layout.add_widget(self.button)
        self.button.bind(on_press=self.onButtonPress)

        return self.layout



    def onButtonPress(self, button):
        layout = GridLayout(cols=1, padding=100)
        popupLabel = Label(text='You have the medication at home', color= 'red')
        closeButton = Button(text="To close message, please click the x")

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        popup = Popup(title='Availability', content=layout)
        popup.open()
        closeButton.bind(on_press=popup.dismiss)



# Code for connection to csv file: takes the whole csv file and turns each line into a medicine object


data = {}

with open(r'c:\Users\sarah\PycharmProjects\pythonSummerSchool\Project\test2.csv', 'r') as fin:
    reader = csv.DictReader(fin)
    for record in reader:
        data[record['barcode']] = {k: v for k, v in record.items()}


# Code for Medicine class creation


class Medicine:
    def __init__(self, barcode, medicinename, quantity, expiry, disposal):
        self.barcode = barcode
        self.medicinename = medicinename
        self.quantity = quantity
        self.expiry = expiry
        self.disposal = disposal

    def __str__(self) -> str:
        return self.medicinename

    def __repr__(self) -> str:
        return f"Medicine({self.medicinename})"

    def get_barcode(self):
        return self.barcode

    def how_disposal(self):
        return self.disposal

# function to manually add a medicine if it is not in the digital medicine cabinet

def add_medicine (barcode_value):
        a_list = []
        a_list.append(barcode_value)
        print('Please type in the name of the newly added medicine, or press enter to skip.')
        answer_medicinename = input()
        a_list.append(answer_medicinename)
        print('Please type in the quantity you are buying right now, or press enter to skip.')
        answer_quantity = input()
        a_list.append(answer_quantity)
        print('Please type in the expiry date (YYYY-MM-DD) of the medicine you are buying right now, or press enter to skip.')
        answer_expiry = input()
        a_list.append(answer_expiry)
        print('Please type in the correct disposal of the medicine you are buying right now, or press enter to skip.')
        answer_disposal = input()
        a_list.append(answer_disposal)
        with open(r'c:\Users\sarah\PycharmProjects\pythonSummerSchool\Project\test2.csv', 'a', newline='') as f: # add own file path
            writer = csv.writer(f)
            writer.writerow(a_list)


# Code for checking the medicine cabinet and checking the expiration date, when expired it gives advise on how to dispose the medicine


def check_cabinet():
    #print('Do you have the medicine at home? Please enter the barcode of the medicine:')
    answer_barcode = globvar                    # checks inventory if barcode is already available
    if answer_barcode not in medicines:
        print('You don\'t have this medicine yet. You need to buy it. Would you like to add all information for this '
              'new medicine to your digital medicine cabinet now? (y/n)')
        answer_addition = input()               # and asks if you want to add the missing medicine to your cabinet
        while True:
            if answer_addition == "n":
                return
            elif answer_addition == "y":
                add_medicine(answer_barcode)
                return
            elif answer_addition == "42":
                print(
                    "This is the answer to the Ultimate Question of Life, the Universe, and Everything, "
                    "but in no way helpful here. Please type in whether you would like to add this new medicine now. (y/n)")
                answer_addition = input()
            else:
                print("Please type in whether you would like to add this new medicine now. (y/n)")
                answer_addition = input()

    if int(medicines[answer_barcode].quantity) < 1:         # checks whether the medicine is known but not in stock
        print('You don\'t have it anymore. You need to buy it.')
        return
    ex_date = medicines[answer_barcode].expiry          # checks expiration date
    today = str(date.today())
    if today > ex_date:
        PopupExample().run()            # link to Popup function to send a message if the medicine is expired
        return
    else:
        PopupExample2().run()
        print('The medicine is available and still usable.')




medicines = {}
for barcode, values in data.items():
    medicines[barcode] = Medicine(**values)



check_cabinet()

