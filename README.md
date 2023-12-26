# Wpbf

It is a python script to brute force against the WordPress login form.


## Installation

```
git clone https://github.com/ret2x-tools/wp-brute-force.git
pip install -r requirements.txt
```


## Usage

```
root@parrot:~$ python3 Wpbf.py -h
usage: Wpbf.py [-h] [-u URL] [-l USERNAME] [-L USER FILE] [-P PASS FILE] [-t THREADS]

Wordpress Login Brute Force

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  target url (e.g. http://www.wpsite.com)
  -l USERNAME        username
  -L USER FILE       user_file.txt
  -P PASS FILE       pass_file.txt
  -t THREADS         default 5

Examples: 
Wpbf.py -u http://www.wpsite.com -l admin -P passfile.txt
Wpbf.py -u http://www.wpsite.com -L userfile.txt -P passfile.txt
```
