from web3 import Web3
import json
import time 
from telegram import Bot
import asyncio

#Arbitrum key
arbitrum_key='USE YOUR API KEY'

#Create a Web3 instance
node_connect = Web3(Web3.HTTPProvider(arbitrum_key))

#check connection
print(node_connect.is_connected())

#Load Contract Address 
aave_pool_contractadd=node_connect.to_checksum_address('0x794a61358D6845594F94dc1DB02A252b5b4814aD')

#Load Json ABI
with open('Aave_pool.json') as file:
    aave_pool_abi=json.load(file)

#Initialize the contract Object
contract = node_connect.eth.contract(address=aave_pool_contractadd, abi=aave_pool_abi)

#Call Read Function
def getAPY():
    USDC_contract_add=node_connect.to_checksum_address('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8')
    reserve_data=contract.functions.getReserveData(USDC_contract_add).call()

    Rays=reserve_data[2]
    PRECISION=10**27
    SECONDS_YEAR=24*3600*365
    APY=(((1+(Rays/PRECISION/SECONDS_YEAR))**SECONDS_YEAR)-1)*100
    rounded_apy=round(APY,1)

    return rounded_apy

async def sendTelegram(rate):
    bot = Bot(token="USE YOUR TG BOT TOKEN")
    await bot.send_message(chat_id="USE YOUR CHANNEL ID", text=f"{rate}%") 

async def main():
    while True:
        rounded_apy_=getAPY()
        await sendTelegram(rounded_apy_)
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())



