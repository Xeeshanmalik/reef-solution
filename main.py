import argparse
import pandas as pd
import numpy as np
from ConfigParser import SafeConfigParser
import requests
import simplejson as json
import codecs


def write_html(output, df):

    # Format the frame output to html

    with codecs.open(output, 'w', encoding='utf8') as file_handle:
        file_handle.write('<html>')
        file_handle.write('<body align=center>')
        file_handle.write(df)
        file_handle.write('</body>')
        file_handle.write('</html>')


def convert_to_html(name, project, time, output):

    # Combine all dimensions in tabular form

    df = pd.DataFrame(columns=name, index=project)
    df = df.fillna('')
    np.fill_diagonal(df.values,time)
    for column in df:
        df[column] = df[column].str.encode('utf-8')
    write_html(output, df.to_html())
    return df


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Reef Technologies")
    parser.add_argument('--output', nargs='?', type=str,
                        default='output/output.html', help="printing output in an html file")

    # Reading Keys From The Config File

    config = SafeConfigParser()
    config.read('config.ini')
    AUTH_KEY = config.get('reef','Auth-Token')
    APP_TOKEN= config.get('reef','App-Token')
    PROJECT_URL = config.get('reef', 'PROJECT_URL')
    USER_URL = config.get('reef', 'USER_URL')

    # Get Project and User Data using API Call

    headers={'App-Token': APP_TOKEN, 'Auth-Token': AUTH_KEY}
    project_response = requests.get(PROJECT_URL, headers=headers)
    project_response = project_response.content
    project_data = json.loads(project_response)["projects"]
    user_response = requests.get(USER_URL, headers=headers)
    user_response = user_response.content
    user_data = json.loads(user_response)["users"]

    # Loading Required output to seperate Lists

    name, project, time = [], [], []

    for user, proj in zip(user_data,project_data):
        name.append(user['name'])
        project.append(proj['name'])
        time.append(user['last_activity'])

    args = parser.parse_args()

    # Saving the desired output in HTML Format

    output = convert_to_html(name, project, time, args.output)

    print("Output Saved in HTML at", args.output)