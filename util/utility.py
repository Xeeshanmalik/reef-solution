import pandas as pd
import numpy as np
import codecs
import requests
import json

class Util:

    @staticmethod
    def write_html(output, df):
        # Format the frame output to html

        with codecs.open(output, 'w', encoding='utf8') as file_handle:
            file_handle.write('<html>')
            file_handle.write('<body align=center>')
            file_handle.write(df)
            file_handle.write('</body>')
            file_handle.write('</html>')

    @staticmethod
    def convert_to_html(name, project, time, output):
        # Combine all dimensions in tabular form

        df = pd.DataFrame(columns=name, index=project)
        df = df.fillna('')
        np.fill_diagonal(df.values, time)
        for column in df:
            df[column] = df[column].str.encode('utf-8')
        Util.write_html(output, df.to_html())
        return df

    @staticmethod
    def api_call(URL, headers, string):
        # Get Project and User Data using API Call

        response = requests.get(URL, headers=headers)
        response = response.content
        data = json.loads(response)[string]
        return data