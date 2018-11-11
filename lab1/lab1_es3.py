"""
@author = Paolo Grasso
"""
import json
import datetime


class Discography():

    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.changed = 0
        print("Loading discography...")

        with open(self.filename, 'r') as infile:
            self.data = json.load(infile)

        print("Welcome to your discography")
        self.options = ['search', 'insert', 'print_all', 'exit', 'quit']

    def run(self):

        while True:
            inp = input('\nWhat do you want to do?\n - search\n'
            ' - insert\n - print_all\n - exit\n-> ')
            inp = inp.split()

            if inp[0] not in self.options:
                print("Invalid command")

            if inp[0] == 'exit' or inp == 'quit':
                if self.changed:
                    self.saveData()
                print("Quitting program...")
                break

            if inp[0] == 'print_all':
                self.printData()

            if inp[0] == 'insert':

                if not (self.checkDisk(inp[2])):
                    self.insertData(inp[1],inp[2],inp[3],inp[4])

                else:

                    while True:
                        up=input("Do you want to update data about %s? "
                        "(y/n)\n-> " % inp[2])

                        if up == 'y' or up == 'Y':
                            self.updateData(inp[1], inp[2], inp[3], inp[4])
                            break

                        elif up == 'n' or up == 'N':
                            break


            if inp[0] == 'search':
                #print(inp[1])
                #if isinstance(inp[1], int):
                #   print(int)
                self.search(inp[1])

    def search(self, arg):
        self.arg = arg
        k = 0

        for d in self.data['album_list']:

            if (d['artist'] == self.arg or d['title'] == self.arg):
                #print(self.data['album_list'][k])
                print(json.dumps(self.data['album_list'][k], indent=4))

            k += 1

        try:
            self.arg=int(self.arg)
            k = 0

            for d in self.data['album_list']:

                if (d['publication_year'] == self.arg or
                    d['total_tracks'] == self.arg):
                    #print(self.data['album_list'][k])
                    print(json.dumps(self.data['album_list'][k], indent=4))

                k += 1

        except:
            pass

    def printData(self):
        print("Printing discography...")
        print("\n --- START ---\n")
        print(json.dumps(self.data, indent=4))
        print("\n --- END --- \n")

    def saveData(self):
        print("Saving data to file...")
        with open(self.filename, 'w') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False)
        print("Complete\a")

    def checkDisk(self, disk):
        self.disk = disk
        #if any(d['title']==self.disk for d in self.data['album_list']):
        k = 0

        for d in self.data['album_list']:

            if d['title'] == self.disk:
                print("Disk %s is already present in the discography"
                    %self.disk)
                self.list_n = k
                return 1

            k += 1

        return 0

    def updateData(self, artist, title, year, tracks):
        self.artist = artist
        self.title = title

        try:
            self.publication_year = int(year)
            self.total_tracks = int(tracks)
            print("Updating data...")
            self.data['album_list'][self.list_n].update({"artist": self.artist,
                "title": self.title, "publication_year": self.publication_year,
                "total_tracks": self.total_tracks})
            self.changed = 1
            self.updateTime()

        except:
            print("Invalid format for year or number of tracks")

    def insertData(self, artist, title, year, tracks):

        self.artist = artist
        self.title = title

        try:
            self.publication_year = int(year)
            self.total_tracks = int(tracks)
            print("Adding data...")
            self.data['album_list'].append({"artist": self.artist,
                "title": self.title, "publication_year": self.publication_year,
                "total_tracks": self.total_tracks})
            self.changed = 1
            self.updateTime()

        except:
            print("Invalid format for year or number of tracks")

    def updateTime(self):
        self.data.update({"last_update":
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})


if __name__ == '__main__':

    mydisco = Discography('discography.json')
    mydisco.run()
