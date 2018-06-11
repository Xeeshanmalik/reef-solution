import argparse
from ConfigParser import SafeConfigParser
from util.utility import Util


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

    project_data = Util.api_call(PROJECT_URL, headers, "projects")
    user_data = Util.api_call(USER_URL, headers,"users")

    # Loading Required output to seperate Lists

    name, project, time = [], [], []

    for user, proj in zip(user_data,project_data):
        name.append(user['name'])
        project.append(proj['name'])
        time.append(user['last_activity'])

    args = parser.parse_args()

    # Saving the desired output in HTML Format

    output = Util.convert_to_html(name, project, time, args.output)

    print("Output Saved in HTML at", args.output)