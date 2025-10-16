import csv
import sys
import os



print('Instructions for uploading image links for the Tutor Bios page on Canvas:\n')
print('1. Navigate to Files on the CCC-Tutorial Center Canvas, then click Switch to Old Files Page.')
print('2. Next, click on the specific folder of portraits you need (Coordinator Portraits, Humanities Portraits, STEM Portraits).')
print('* Make sure that all new tutors\' portraits have already been uploaded onto Canvas in the right folder, with their full name as the name of the image file *')
print('3. Lastly, hit Ctrl-s, and save as Webpage, Complete. This will save the webpage as an html file.')

option = 0
image_links = {} 

while True:
    print('\n------------------------------------------------')
    option = input('Options: 1) Upload images 2) Move onto next step\n')
    if option == '1':
        print('\nHTML files in current folder:')
        for x in os.listdir():
            if x.endswith('.html'):
                print(x)

        print('------------------------------------------------')
        file_path= input('Name of file: ')
        # Using complete HTML downloaded from Canvas file page
        file = open(file_path, 'r') 

        for line in file:
            words = line.strip().split()
            for word in words:
                for i in range(58):
                    word += ' '
                # Get link 
                if word[0:58] == 'url(&quot;https://scccd.instructure.com/images/thumbnails/':
                    link = word[58:66]
                    link.strip()
                # Get name 
                if word[0:26] == 'class=\"ef-name-col__text\">':
                    name = word[26:]
                    end_index = name.find('.')
                    name = name[:end_index]
                    name.strip()
                    image_links[name] = link 
        print('\nCurrent links:')
        for image in image_links:
            print(image,': ',image_links[image])
    elif option == '2':
        break

option = 0
print('Instructions for uploading responses from the Tutor Bio Info form:\n')
print('1. You got it')

while True:
    print('\n------------------------------------------------')
    option = input('Options: 1) Upload responses 2) Done\n')
    if option == '1':
        print('\nCSV files in current folder:')
        for x in os.listdir():
            if x.endswith('.csv'):
                print(x)

        print('------------------------------------------------')
        file_path = input('Name of file: ')
        file = open(file_path, 'r') 
        additions = open('additions.csv', 'w')

        additions.write('name#image_url#quote#about_me_items#experience#education\n')

        reader = csv.reader(file);
        for row in reader:
            # skip first row
            if row[0] == 'Timestamp': continue;

            # get name
            name = row[1]
            trimmed_name = name.replace(' ', '')

            # get image 
            image_url = image_links[trimmed_name]

            # get quote 
            quote = row[7] 
            # erase quote chars bc omg people cannot be trusted w them
            quote = quote.replace('“', '')
            quote = quote.replace('”', '')
            quote = quote.replace('\"', '')

        

            # get about_me_items
            about_me_items = row[4] + '|' + row[5] + '|' + row[6] 

            # get experience
            experience = row[2]

            # get education
            education = row[3]


            additions.write(name + '#' + image_url + '#' + quote + '#' + about_me_items + '#' + experience + '#' + education + '\n')
    elif option == '2':
        break 
print('New entries have been uploaded to additions.csv!')

