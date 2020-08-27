#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# Rgoding, 2020-Aug-17, Created File
# Rgoding, 2020-Aug-18, Created Save function
# Rgoding, 2020-Aug-19, Created Add and delete function
# Rgoding, 2020-Aug-26, Added Exception Handling
# Rgoding, 2020-Aug-26, Modified the permanent data to store as binary data

#------------------------------------------#
#Import pickle module
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
strID = ''      #CD Inventory ID
strTitle = ''   #CD Title
stArtist = ''   #CD Artist


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def add_inventorydata(ID, Title, Artist, table):
         """Function to take adding inventory data and append it to table

       Args:
            ID: CD Inventory ID 
            Title: CD Title
            Artist: CD Artist's Name
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
         """Structured Error Handling if CD ID is not an integer"""
         try:
            
             intID = int(ID)
             dicRow = {'ID': intID, 'Title': Title, 'Artist': Artist}
             table.append(dicRow)
         except Exception as e:
             print('That is not an integer')
             print(e)
             
    
    @staticmethod
    def delete_file(ID, table):
        
        """Function to delete CD Inventory Entry from Table

        Reads the rows in table and if row ID matches user input, that
        row and entry is removed from table

        Args:
            ID: CD Inventory ID to be deleted, input by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        
        
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
   

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        objFile = open(file_name, 'ab')
        data = pickle.load(objFile)
        pickle.dump(data, objFile)
        
       
    @staticmethod
    def write_file(file_name, table):
         """Function to Save the data to CDInventory.txt file
                
        Opens the strFileName to write to, then looks at 1stTbl and saves each
        row

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """ 
         objFile = open(file_name,'wb')
         pickle.dump(table, objFile)
         objFile.close()
                
        

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def add_inventory():
        """Add Inventory to CDInventory.txt

        Args:
            None

        Returns:
            strID, strTitle, stArtist for data processing function to handle

        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        DataProcessor.add_inventorydata(strID,strTitle,stArtist,lstTbl) 
   

# 1. When program starts, read in the currently saved Inventory
# Add Error exceptions to display error instead of closing program
try:
    FileProcessor.read_file(strFileName, lstTbl)
except:
    print("No text file found in local folder, please create CDInventory.txt")


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        #Add Error handling if file is not created
        try:
            if strYesNo.lower() == 'yes':
                print('reloading...')
                FileProcessor.read_file(strFileName, lstTbl)
                IO.show_inventory(lstTbl)
        except:
            print("CDInventory.txt does not exist in local directory")
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        IO.add_inventory()
        # 3.3.2 Add item to the table
        
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove, with error exception added
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
            DataProcessor.delete_file(intIDDel,lstTbl)
            IO.show_inventory(lstTbl)
        except:
            print("That is not an integer!")
    
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
           FileProcessor.write_file(strFileName,lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




