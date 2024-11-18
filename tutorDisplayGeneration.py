import csv
import sys

def get_last_name(full_name):
    # Extracts the last word of the name, assuming it's the last name
    return full_name.split()[-1]

def generate_row(name, image_url, quote, about_me_items, experience, education, mirror=False):
    about_me_list = "".join(f"<li>{item}</li>" for item in about_me_items)
    
    # Adjust the order of the columns based on the mirror parameter
    if mirror:
        return f"""
        <tr style="border: 2px solid lightblue;">
          <td>
            <div style="display: flex; justify-content: space-between; align-items: stretch;">
              <div style="width: 33.33%; padding: 20px; border-right: 2px solid lightblue; display: flex; flex-direction: column; justify-content: center;">
                <h3>About me:</h3>
                <ul>
                  {about_me_list}
                </ul>
              </div>
              <div style="width: 33.33%; padding: 20px; border-right: 2px solid lightblue; display: flex; flex-direction: column; justify-content: center;">
                <h3>Experience/Specialties:</h3>
                <p>{experience}</p>
                <h3>Education:</h3>
                <p>{education}</p>
              </div>
              <div style="width: 33.33%; padding: 20px; text-align: center; display: flex; flex-direction: column; justify-content: center;">
                <h2>{name}</h2>
                <img style="margin: auto;" src="https://scccd.instructure.com/courses/108747/files/{image_url}/preview" data-api-endpoint="https://scccd.instructure.com/api/v1/courses/108747/files/{image_url}" data-api-returntype="File" alt="{name}'s Headshot" width="240" height="320" />
                <p style="font-style: italic; text-align: center; padding: 20px;">"{quote}"</p>
              </div>
            </div>
          </td>
        </tr>
        """
    else:
        return f"""
        <tr style="border: 2px solid lightblue;">
          <td>
            <div style="display: flex; justify-content: space-between; align-items: stretch;">
              <div style="width: 33.33%; padding: 20px; text-align: center; border-right: 2px solid lightblue; display: flex; flex-direction: column; justify-content: center;">
                <h2>{name}</h2>
                <img style="margin: auto;" src="https://scccd.instructure.com/courses/108747/files/{image_url}/preview" data-api-endpoint="https://scccd.instructure.com/api/v1/courses/108747/files/{image_url}" data-api-returntype="File" alt="{name}'s Headshot" width="240" height="320" />
                <p style="font-style: italic; text-align: center; padding: 20px;">"{quote}"</p>
              </div>
              <div style="width: 33.33%; padding: 20px; border-right: 2px solid lightblue; display: flex; flex-direction: column; justify-content: center;">
                <h3>Experience/Specialties:</h3>
                <p>{experience}</p>
                <h3>Education:</h3>
                <p>{education}</p>
              </div>
              <div style="width: 33.33%; padding: 20px; display: flex; flex-direction: column; justify-content: center;">
                <h3>About me:</h3>
                <ul>
                  {about_me_list}
                </ul>
              </div>
            </div>
          </td>
        </tr>
        """

def generate_table(tutors):
    table_html = "<table style=\"width: 100%; border-collapse: collapse;\">\n<tbody>\n"
    for i, tutor in enumerate(tutors):
        # Alternate the mirror parameter based on whether the index is even or odd
        mirror = i % 2 == 1
        table_html += generate_row(
            tutor['name'], 
            tutor['image_url'], 
            tutor['quote'], 
            tutor['about_me_items'], 
            tutor['experience'], 
            tutor['education'], 
            mirror=mirror
        )
    table_html += "</tbody>\n</table>"
    return table_html


# def read_tutors_from_csv(file_path):
#     tutors = []
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             # Split 'about_me_items' by the "|" character to convert them into a list
#             row['about_me_items'] = row['about_me_items'].split('|')
#             tutors.append(row)
#     return tutors

# new function that reads tutors in the same format, but $#$ separated for all columns
def read_tutors_from_csv(file_path):
    tutors = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='#')
        for row in reader:
            # Split 'about_me_items' by the "|" character to convert them into a list
            row['about_me_items'] = row['about_me_items'].split('|')
            tutors.append(row)
    return tutors


def sort_tutors_by_last_name(tutors_input):
    # Sort tutors based on the last name, extracted using the get_last_name function
    return sorted(tutors_input, key=lambda tutor: get_last_name(tutor['name']))


def write_html_to_file(html_content, output_file_path):
    # Writes the generated HTML to a file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


# Load tutor data from the CSV file - example.csv if no command line arguments, otherwise the first command line argument
if len(sys.argv) == 1:
    file_path = 'example.csv'
else:
    file_path = sys.argv[1]

tutors = read_tutors_from_csv(file_path)
# Sort tutors by last name
tutors_sorted = sort_tutors_by_last_name(tutors)

# Generate the HTML table for the sorted list of tutors
html_table = generate_table(tutors_sorted)

# Add basic HTML structure
html_content = f"""
<h1>List of Tutors</h1>
{html_table}
"""

# output_file_path set from command line
if len(sys.argv) == 3:
    output_file_path = sys.argv[2]
else:
    output_file_path = 'tutors_list.html'
# Write the complete HTML content to a file
write_html_to_file(html_content, output_file_path)

# Print a success message
print('Success! HTML table generated and saved to ' + output_file_path)
