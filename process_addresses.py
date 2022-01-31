import pandas as pd


def load_addresses(file='blockchair_bitcoin_addresses_and_balance_LATEST.tsv',discard_below_satoshi=300000):
    print('Loading large address file...')
    df = pd.read_csv(file,sep='\t')
    print('done')
    print('discarding low value addresses')
    df = df[df['balance'] > discard_below_satoshi]
    print('done')
    print('discarding addresses not starting with 1')
    df = df[df['address'].str.startswith('1')]
    print('done')
    return df

def download_from_loyce_club():
    import urllib.request
    from tqdm import tqdm
    class DownloadProgressBar(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)
    url = 'http://addresses.loyce.club/blockchair_bitcoin_addresses_and_balance_LATEST.tsv.gz'
    with DownloadProgressBar(unit='B', unit_scale=True,
                            miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename='blockchair_bitcoin_addresses_and_balance_LATEST.tsv.gz', reporthook=t.update_to)

def refresh_address_list(download=True):
    import gzip
    if download:
        download_from_loyce_club()
    with gzip.open('blockchair_bitcoin_addresses_and_balance_LATEST.tsv.gz') as f:
        load_addresses(file=f)['address'].to_csv('addresses.txt',header=False,index=False)

if __name__ == '__main__':
    '''df = load_addresses()
    print(df)
    df['address'].to_csv('blockchain_scraped_addresses.txt',header=False,index=False)'''
    refresh_addresses = input('Download list of addresses? Download size is about 1 GB. y/n')
    if refresh_addresses == 'y':
        refresh_address_list(True)
    else:
        refresh_address_list(False)
