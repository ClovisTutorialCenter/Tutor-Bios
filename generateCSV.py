import csv
import sys
import os

if len(sys.argv) != 3:
    print('Usage: python3 generateCSV.py <image links html file> <form responses csv file>')
    sys.exit(1)

image_links = {} 
file_path_1 = sys.argv[1]
file_path_2 = sys.argv[2]

file1 = open(file_path_1, 'r') 

for line in file1:
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

file2 = open(file_path_2, 'r') 
additions = open('additions.csv', 'w')

additions.write('name#image_url#quote#about_me_items#experience#education\n')

reader = csv.reader(file2);
for row in reader:
    # skip first row
    if row[0] == 'Timestamp': continue
    # get name
    name = row[1]
    trimmed_name = name.replace(' ', '')
    # get image 
    if not trimmed_name in image_links:
        continue
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

print('New entries have been uploaded to additions.csv!')
