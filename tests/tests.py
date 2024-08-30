from fmpxx.financials import Financials
import os
import dotenv

dotenv.load_dotenv()

API_Key = os.getenv("FMP")



client = Financials(API_Key)
print(client.get_earnings_his('NVDA', period=1))