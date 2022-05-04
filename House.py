""" support class for House data
"""

from tkinter import *
class House:

    def __init__(self, street_number, street, suburb, town, land_sq_meters,
                 num_bedrooms, r_v, asking_price, image_name):
        self.street_number = street_number
        self.street = street
        self.suburb = suburb;
        self.town = town
        self.land_sq_meters = land_sq_meters
        self.num_bedrooms = num_bedrooms
        self.r_v = r_v
        self.asking_price = asking_price
        self.image_name = image_name
        self.sold = False

        try:
            self.photo_file = PhotoImage(file = self.image_name)
            print(type(self.photo_file))
        except IOError:
            self.has_image = False
        else:
            self.has_image = True
        
    def presentation(self):
        """ presents info in shell - useful for development purposes"""
        print("** Listing **")
        info = "{}, {}, {}, {}".format(self.street_number,
                                       self.street, self.suburb, self.town)
        print(info)
        print("Number of bedrooms: " + str(self.num_bedrooms))
        print("Land area: " + str(self.land_sq_meters))
        print("Rateable value " + str(self.r_v))
        print("Asking price " + str(self.asking_price))
        if (self.sold):
            print("SOLD")
        else:
            print("For Sale")
        print("**************")
