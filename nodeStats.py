from flask import Flask, render_template, request
import requests
from time import strftime, localtime

app = Flask(__name__)

urls = [
    'https://desocialworld.com/api/v1/node-info',
    'https://node.deso.org/api/v1/node-info',
    'https://desonode.rylees.net/api/v1/node-info',
    'https://nodeapi.nftz.me/api/v1/node-info',
    'https://bitclout.com/api/v1/node-info'
]

headers = {
    'Content-Type': 'application/json'
}

data = {}


@app.route('/')
def get_node_status():
    node_data = []
    for url in urls:
        response = requests.post(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            latest_header_timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime(data['DeSoStatus']['LatestHeaderTstampSecs']))
            latest_block_timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime(data['DeSoStatus']['LatestBlockTstampSecs']))
            node_info = {
                'url': url,
                'state': data['DeSoStatus']['State'],
                'latest_header_height': data['DeSoStatus']['LatestHeaderHeight'],
                'latest_header_timestamp': latest_header_timestamp,
                'latest_block_height': data['DeSoStatus']['LatestBlockHeight'],
                'latest_tx_index_height': data['DeSoStatus']['LatestTxIndexHeight'],
                'latest_block_timestamp': latest_block_timestamp
            }
            node_data.append(node_info)
        else:
            node_info = {
                'url': url,
                'error': f"Request failed with status code {response.status_code} - {response.text}"
            }
            node_data.append(node_info)

    return render_template('node_status.html', nodes=node_data)


if __name__ == '__main__':
    app.run()
