import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
import aiohttp
import re

headers = {
        'authority': 'www.nic.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.nic.ru',
        'pragma': 'no-cache',
        'referer': 'https://www.nic.ru/whois/?searchWord=vk.com',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'x-client-fingerprint': '4238e7378b558ebfcb1cb9381c4b5685',
    }


async def mail_send(email_address, url):
    to_address = email_address
    subject = "Report"
    body = f"Найдено нарушение на сайте: {url}"
    message = MIMEMultipart()
    message["From"] = email_address
    message["To"] = to_address
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP(config.host, 587) as server:
        server.starttls()
        server.login(config.email_address, config.email_password)
        server.send_message(message)

    print("Письмо успешно отправлено!")


async def fetch(url, session, json):
    async with session.post(url, json=json) as response:
        return await response.json()


async def whoise_get(domen) -> None | str:
    json_data = {
        'searchWord': domen,
        'lang': 'ru',
    }
    url = "https://www.nic.ru/app/v1/get/whois"
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await fetch(url, session, json_data)
    if result.get("status") == "success":
        try:
            text = result["body"]["list"][0]["html"]
        except KeyError:
            domains: list[dict] = result["body"]["list"][0]["formatted"]
            for i in domains:
                if i.get("name") == "domain":
                    domain = i.get("value")
                    print(domain)
                    return domain
            return None
        pattern = r"Domain Name:\s+([\w.-]+)"

        match = re.search(pattern, text)

        if match:
            domain_name = match.group(1)
            print(domain_name)
            return domain_name
        else:
            return


asyncio.run(whoise_get("jut.su"))
