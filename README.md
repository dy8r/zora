## About
This script optimizes your ~~sybil activities on~~ interactions with Zora<br />
Performs a mint of an NFT on zora.co on any of supported chains (zora, base, op, arb) on any number of your accounts<br />
Has customizable wait time setting and a randomizer

## Prerequisites 
- Download and install Python https://kinsta.com/knowledgebase/install-python/
- Install required libraries Mac, Linux - `pip3 install -r requirements.txt`, Windows - `pip install requirements.txt`
- Add your private keys to `pks.txt`. Each key should be on a new line

## Settings and starting a script
Run the script by navigating to the project dir and executing `python3 main.py` (if you're on Mac or Linux) or `python main.py` (if you're on Windows)<br />
You will be prompted with several input requests. (the console will say something and you will type your answer in it and press enter)<br />
You will see the following prompts:
1) __How many wallets out of X__ - X is the number of private keys you have in your pks.txt file. Enter a number of how many wallets you want a mint performed on.
2) __Randomize?__ - type `y` or `n` (yes or no). No - (say you want to mint on 3 of your 10 wallets) - it will mint on wallets 1, 2, 3. Yes - it will select three random wallets (i.e. 4, 7, 8)
3) __Mint link__ - enter a mint link to zora. It should look like this https://zora.co/collect/zora:0xC94AcD65b6965370eBEf0a2AdCDAD5B4362dD671/9
4) __input time in seconds before deadline (0 if mint now)__ - how long do you want your mint to take? <br />- 0 if you want to mint immediately (useful when it's a fast mint).<br />- 600 (600 seconds = 10 minutes), for example, is a good number when you want to mint right now, but don't want to make your wallets look sybil. In the case of three wallets, the script will uniformly generate sleep times for each wallet in a way that average sleep time is about 600/3 (but are uniformly distributed +-50% from it) and their sum does never exceed 600s. So, sleep times will be something like (2 minutes, 4 minutes, 3 minutes) in this case

No support for proxies right now (you don't need them, you're interacting with RPCs)<br />
No support for customization of # of mints per account (can be added easily though, I might add it if I see any use case for it)<br />
No support for non-free mints (I am working on it)<br />
No support for mints outside zora.co (I am working on it)
