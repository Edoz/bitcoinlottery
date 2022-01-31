# donate

In the improbable event that you win, you can donate some BTC to 1Bu8LY9iue1W2weR3AcpkgnRkqzs4aa7n5

# bitcoinlottery - the free to play lottery

This is a python script that tries to find the private key of a (list of) bitcoin addresses, giving you ownership of the corresponding bitcoin wallet and its bitcoins if it succeeds.

The probabiliy of success on every attempt is 1 in 2^256, so you will never ever win this lottery.

But, you could be insanely lucky on any one attempt, and the script runs several hundred attempts per second.

This script is orders of magnitude faster than various websites running the same concept. It only checks against legacy BTC addresses (those that start with 1) because it's much less computationally intensive, giving you more attempts per second.

# usage

Download 'bitcoin_lottery.py' and 'addresses.txt', run `python bitcoin_lottery.py 1`, change 1 to the number of cores you want to use.

Run the `python process_addresses.py` in conjunction with the latest list of addresses in TSV format from https://bitcointalk.org/index.php?topic=5254914.0 or other source to generate an updated 'addresses.txt' file, removing by default all non-legacy addresses and all addresses with less than 300,000 satoshis in them.

If Fortuna willing you find a key, it'll save it to text file "found.txt".

Godspeed, brother.
