""" Real Estate GUI. Some print statements from
    development have been included in this code. The House class is
    in a separate file and imported but could just as easily have
    been written in this file.
"""
from tkinter import *
import tkinter
from House import *

class RealEstatePanel:
    
    def __init__(self, parent):
        """ Sets up the overall GUI.  Note the use of float('inf')
            This is Python for infinity and could be replaced by a
            suitably large number.   
        """ 
        self.price_ranges_values = [("any price", float('inf')),
                         ("<$100K", 100000.0),
                         ("<$200K", 200000.0),
                         ("<$300K", 300000.0),
                         ("<$400K", 400000.0)]
        self.num_bedrooms_values = [("any bedrooms",-1),
                           ("1 bedroom",  1),
                           ("2 bedrooms", 2),
                           ("3 bedrooms", 3),
                           ("4 bedrooms", 4)]
        self.parent = parent
        self.count = 0
        self.houses = []

        self.price_choice = float('inf') # Could be replaced by a large number
        self.bedroom_choice = -1
        self.make_list()

        self.current_house = 0
        self.current_house_index = 0
        
        self.search_frame = Frame(self.parent)
        self.search_label = Label(self.search_frame, text = "Search for: ")
        self.search_label.pack()
        self.view_houses_frame = Frame(self.parent)
  

        self.has_black = True
        try:
            self.no_house = PhotoImage(file="images/black.gif")
        except IOError:
            self.has_black = False

        # Calls to set up GUI for search options
        self.construct_search_options(self.search_frame)
        self.construct_view_houses_frame(self.view_houses_frame)


        #self.SearchFrame.form(left=0, right='%50', top=0)
        self.search_frame.pack(fill="both", expand="yes", side=LEFT)
        self.view_houses_frame.pack(fill="both", expand="yes", side=RIGHT)


    def make_list(self):
        """ Reads in from a file to create a ist of House objects.
        """
        i = 0;  
        file_name = "houseList.txt";
        try:
            my_file = open(file_name, 'r')
        except IOError:
            print ('cannot open', file_name)
        else:
            lines = my_file.readlines()
            for line in lines:
                line = line.replace('\n','')
                house_info = line.split(';')
                print("found the image file");
                #print (house_info)
                street_number = house_info[0]
                street = house_info[1]
                suburb = house_info[2]
                town = house_info[3]
                land_sq_metres = float(house_info[4])
                #print(house_info[5])
                num_bedrooms = int(house_info[5])
                retail_value = float(house_info[6])
                sale_price = float(house_info[7])
                image_name = house_info[8]
                print("made a new listing")
                self.houses += [House(street_number,street,suburb,
                                           town, land_sq_metres,num_bedrooms,
                                           retail_value,sale_price,image_name)]
                self.houses[self.count].presentation() # to the shell
                self.count +=1
        
        self.house_index_list = range(self.count) # The index numbers of the houses meeting the current criteria

        
    def sel_price(self):
        self.price_choice = self.price_ranges_values[self.var_price.get()][1]
 #       print(self.price_choice)

    def sel_bedrooms(self):
        self.bedroom_choice = self.num_bedrooms_values[self.var_bedrooms.get()][1]
 #       print (self.bedroom_choice)


    def search_houses(self):
        """ Empties self.house_index_list and then builds up this list with
            the index numbers of houses meeting the new criteria.
        """
        self.house_index_list = [] 
        for i in range(len(self.houses)):
 #           print (i, self.price_choice, house.asking_price,self.bedroom_choice, house.num_bedrooms)
            if  self.price_choice >= self.houses[i].asking_price and (self.bedroom_choice == self.houses[i].num_bedrooms
                                                           or self.bedroom_choice == -1) :
                self.house_index_list += [i]
        self.entry_widget.delete(0, END)
        self.entry_widget.insert(0,str(len(self.house_index_list)) + " houses found")
        print(self.house_index_list)
        if len(self.house_index_list)>0:
            self.current_house = self.house_index_list[0]
            self.current_house_index = 0
            self.update_house()
        else:
            self.view_canvas.delete(ALL)
            if self.has_black:
                self.view_canvas.create_image(100, 100, image = self.no_house)
            self.street_label["text"] = ''
            self.suburb_label["text"] = ''
            self.town_label["text"] = ''
            self.bedrooms_label["text"] = ''
            self.rateable_value_label["text"] = ''
            self.asking_price_label["text"] = ''         
            self.index_entry.delete(0, END)
            self.index_entry.insert(0, '')

    def reset(self):
        """ Resets the GUI to display all houses and indicate that it is
            doing so with the radio buttons.
        """
        self.price_choice = float('inf')
        self.bedroom_choice = -1
        self.var_price.set(0)
        self.var_bedrooms.set(0)
        self.search_houses()

    def construct_search_options(self, parent):
        """ Sets up and displays the Radiobuttons for searching by price
            and searching by number of bedrooms, as well as the search
            now button, the Entry saying how many have been found and the reset button.
        """
        self.price_ranges = []
        self.var_price = IntVar()
        for i in range(len(self.price_ranges_values)):
            self.price_ranges += [Radiobutton(parent, text = self.price_ranges_values[i][0],
                                      variable=self.var_price, value=i,
                                      command=self.sel_price)]
            
            self.price_ranges[i].pack( anchor = W )


        seperator = Label(parent, text="-------------------")
        seperator.pack(anchor = W )


        self.bedrooms = []
        self.var_bedrooms = IntVar()
        for i in range(len(self.num_bedrooms_values)):
            self.bedrooms += [Radiobutton(parent, text = self.num_bedrooms_values[i][0],
                                      variable=self.var_bedrooms, value=i,
                                      command=self.sel_bedrooms)]
            
            self.bedrooms[i].pack( anchor = W ) 

        
        search_button = Button(parent, text="Search Now", command=self.search_houses)
        search_button.pack(anchor = W)

        self.entry_widget = Entry(parent)
        self.entry_widget["width"] = 15
        self.entry_widget.pack(anchor = W)

        reset_button = Button(parent, text="Reset", command=self.reset)
        reset_button.pack(anchor = W)

    def construct_view_houses_frame(self, parent):
        """ Sets up the GUI components that show information about a particular house.
        """
        house = self.houses[self.current_house]
        street_number = str(house.street_number)
        street = house.street
        suburb = house.suburb
        town = house.town
        
        self.street_label = Label(parent, text=street_number + " " + street)
        self.suburb_label = Label(parent, text=suburb)
        self.town_label = Label(parent, text=town)

        self.street_label.pack()
        self.suburb_label.pack()
        self.town_label.pack()

        self.photo_file = house.photo_file

        self.view_canvas = Canvas(parent, width = 200, height = 200, bg = 'yellow')
        
        #self.house_photo = Label(parent,image=photo_file)
        #self.house_photo.image = house_photo 
        
        self.view_canvas.create_image(100, 100, image = self.photo_file)
        self.view_canvas.pack()

        self.bedrooms_label = Label(parent, text=str(house.num_bedrooms) + " bedrooms")
        self.rateable_value_label = Label(parent, text= "Rateable value: $" + str(house.r_v))
        self.asking_price_label = Label(parent, text= "Asking price: $" + str(house.asking_price))

        self.bedrooms_label.pack()
        self.rateable_value_label.pack()
        self.asking_price_label.pack()
        
        scroll_frame = LabelFrame(parent)
        self.construct_scroll_frame(scroll_frame)
        scroll_frame.pack()

    def construct_scroll_frame(self, parent):
        """ Sets up the GUI components that allow the user to scroll
            between houses.
        """
        self.left_icon = PhotoImage(file="images/leftArrow.gif")
        self.right_icon = PhotoImage(file="images/rightArrow.gif")
    
        self.left_button = Button(parent, image=self.left_icon, command=self.scroll_left)
        self.right_button = Button(parent, image=self.right_icon, command=self.scroll_right)
        self.index_entry = Entry(parent)
        self.index_entry["width"] = 1
        self.index_entry.insert(0, self.current_house)

        self.right_button.pack(side=RIGHT)
        self.index_entry.pack(side=RIGHT)
        self.left_button.pack(side=RIGHT)

    def update_house(self):
        """ Reconfigures the widgets of the view_houses_frame to
            display the details of the current house.
        """
        house = self.houses[self.current_house]
        street_number = str(house.street_number)
        street = house.street
        suburb = house.suburb
        town = house.town
        self.street_label["text"] = street_number + " " + street
        self.suburb_label["text"] = suburb
        self.town_label["text"] = town
        
        self.photo_file = house.photo_file
        self.view_canvas.delete(ALL)
        if house.has_image:
            self.view_canvas.create_image(100, 100, image = self.photo_file)

        self.bedrooms_label["text"] = str(house.num_bedrooms) + " bedrooms"
        self.rateable_value_label["text"] = "Rateable value: $" + str(house.r_v)
        self.asking_price_label["text"] = "Asking price: $" + str(house.asking_price)

        self.index_entry.delete(0, END)
        self.index_entry.insert(0, self.current_house)
        
    def scroll_left(self):
        """ Decrements the current house index. If we have
            reached the beginning of self.house_index_list it is
            set to the last position of the self.house_index_list.
        """
        if len(self.house_index_list) > 0:
            self.current_house_index -= 1

            if self.current_house_index < 0:
                self.current_house_index = len(self.house_index_list) - 1
            self.current_house = self.house_index_list[self.current_house_index]
            self.update_house()
            
    def scroll_right(self):
        """ Increments the current house index. If we have
            reached the end of self.house_index_list it is
            set to zero
        """
        if len(self.house_index_list) > 0:
            self.current_house_index += 1

            if self.current_house_index >= len(self.house_index_list):
                self.current_house_index = 0
            self.current_house = self.house_index_list[self.current_house_index]
            self.update_house()
        
if __name__ == '__main__':
    root = Tk()
    RealEstatePanel(root)
    root.wm_title("Real Estate")
    root.mainloop()

    
