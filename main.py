from web3 import Web3
import json as js
from requests.adapters import Retry
import requests
from web3.middleware import geth_poa_middleware
import time
import re
from random import shuffle, uniform

CHAIN_RPC = {
    'Arbitrum': 'https://1rpc.io/arb',
    'Optimism': 'https://1rpc.io/op',
    'Polygon' : 'https://1rpc.io/matic',
    'Zora'    : 'https://zora.rpc.thirdweb.com',      # https://zora.rpc.thirdweb.com | https://rpc.zora.energy | https://rpc.zerion.io/v1/zora
    'Ethereum': 'https://rpc.ankr.com/eth',
    'Base'    : 'https://rpc.ankr.com/base',
    'Nova'    : 'https://rpc.ankr.com/arbitrumnova',
    'zkSync'  : 'https://rpc.ankr.com/zksync_era',
    'Linea'   : 'https://1rpc.io/linea',
    'Blast'   : 'https://rpc.ankr.com/blast'
}

SCAN = {
    'Ethereum': 'https://etherscan.io/tx/',
    'Arbitrum': 'https://arbiscan.io/tx/',
    'Optimism': 'https://optimistic.etherscan.io/tx/',
    'Polygon': 'https://polygonscan.com/tx/',
    'Base': 'https://basescan.org/tx/',
    'Zora': 'https://explorer.zora.energy/tx/',
    'Nova': 'https://nova.arbiscan.io/tx/',
    'zkSync': 'https://era.zksync.network/tx/',
    'Linea': 'https://lineascan.build/tx/',
    'Blast': 'https://blastscan.io/tx/'
}

ADDRESS = {
    'Zora': Web3.to_checksum_address('0x04E2516A2c207E84a1839755675dfd8eF6302F0a'),
    'Base': Web3.to_checksum_address('0xff8b0f870ff56870dc5abd6cb3e6e89c8ba2e062'),
    'Optimism': Web3.to_checksum_address('0x3678862f04290E565cCA2EF163BAeb92Bb76790C'),
    'Arbitrum': Web3.to_checksum_address('0x1Cd1C1f3b8B779B50Db23155F2Cb244FCcA06B21'),
}

ZORA_GASPRICE_PRESCALE = 0.001

def get_web3(chain):
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        adapter = requests.adapters.HTTPAdapter(max_retries=retries)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # if self.proxy is not None:
        #     proxy_dick = {'https': 'http://' + self.proxy, 'http': 'http://' + self.proxy}
        #     session.proxies = proxy_dick
        return Web3(Web3.HTTPProvider(CHAIN_RPC[chain], request_kwargs={'timeout': 60}, session=session))

def get_scan(chain):
        return SCAN[chain]

def get_gas_price(chain, web3):
    if chain in ["Polygon", "Avax", 'Zora']:
        try:
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        except:
            pass

    if chain == 'Zora':
        return {'maxFeePerGas': Web3.to_wei(ZORA_GASPRICE_PRESCALE, 'gwei'), 'maxPriorityFeePerGas': Web3.to_wei(ZORA_GASPRICE_PRESCALE, 'gwei')}

    return {'maxFeePerGas': web3.eth.gas_price, 'maxPriorityFeePerGas': int(web3.eth.gas_price * 0.1)}



def send_transaction_and_wait(tx, message, private_key, web3, number, scan):
        signed_txn = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print('Sent a transaction')
        time.sleep(5)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=900, poll_latency=5)
        if tx_receipt.status == 1:
            print('The transaction was successfully mined')
        else:
            print("Transaction failed, I'm trying again")
            raise ValueError('')

        print(f'[{number}] {message} || {scan}{tx_hash.hex()}\n')
        return tx_hash

def mint_nft_zora(chain, web3, pk, number, scan, item_collection_number):
        quantity = 1
        contract = web3.eth.contract(address=Web3.to_checksum_address(nft_address), abi=abi_1155)
        fee = contract.functions.mintFee().call() * quantity
        dick = {
            'from': address_wallet,
            'value': fee,
            'nonce': web3.eth.get_transaction_count(address_wallet),
            **get_gas_price(chain, web3)
        }

        txn = contract.functions.mintWithRewards(
            ADDRESS[chain],
            item_collection_number,
            quantity,
            '0x000000000000000000000000' + address_wallet[2:],
            Web3.to_checksum_address('0xCC05E5454D8eC8F0873ECD6b2E3da945B39acA6C')
        ).build_transaction(dick)

        send_transaction_and_wait(txn, f'Mint {quantity} NFT on {chain}', pk, web3, number, scan)


def parse_url(url):
    match = re.search(r'collect/(.*?):(.*?)/(\d+)', url)
    if match:
        chain = match.group(1)
        address = match.group(2)
        number = match.group(3)
        return chain, address, number
    else:
        return None


if __name__ == '__main__':
    file = open('pks.txt', 'r')
    arr = file.readlines()
    file.close()
    pks = [i.replace('\n', '') for i in arr]
    n_of_w = input(f'How many wallets out of {len(pks)}\n')
    randomize = input('Randomize? y/n\n')
    if randomize in ['y', 'Y']:
        print('ok randomizing')
        shuffle(pks)

    mint_link = input('Mint link:\n') # https://zora.co/collect/zora:0xC94AcD65b6965370eBEf0a2AdCDAD5B4362dD671/9
    time_before_deadline = input('input time in seconds before dedaline (0 if mint now)\n')
    if not time_before_deadline.isdigit():
        raise ValueError('Invalid input. Time must be numeric.')
    else:
        if int(time_before_deadline) == 0:
             sleep_time = [0 for x in n_of_w]
             print('ok fast mint')
        else:
            sleep_time = []
            while True:
                sleep_time = []
                for _ in range(int(n_of_w)):
                    sleep_range = int(time_before_deadline) // int(n_of_w)
                    sleep_range_min = sleep_range - (sleep_range * 0.5)
                    sleep_range_max = sleep_range + (sleep_range * 0.5)
                    sleep_time.append(uniform(sleep_range_min, sleep_range_max))
                if sum(sleep_time) < int(time_before_deadline):
                    break
            print(f'Sleep time for each wallet: {sleep_time}')

    for number, private_key in enumerate(pks[:n_of_w]):
        ch, nft_address, mint_number = parse_url(mint_link)
        chain = ch.capitalize()
        abi_1155 = js.load(open('./abi/1155.txt'))
        web3 = get_web3(chain)
        scan = get_scan(chain)
        account = web3.eth.account.from_key(private_key)
        address_wallet = account.address
        print(f'Starting wallet {number}/{n_of_w} with address {address_wallet}\n')
        if chain in ['Zora', 'Base', 'Optimism', 'Arbitrum']:
            mint_nft_zora(chain, web3, private_key, number, scan, mint_number)
        else:
            print('Chain not supported')
        