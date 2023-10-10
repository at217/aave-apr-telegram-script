from web3 import Web3
import json
import time 
from telegram import Bot
import asyncio

#Arbitrum key
arbitrum_key='https://arb-mainnet.g.alchemy.com/v2/L5nnpNcPv0Bbf8roQPfiL-6kvqq_li_Z'

#Create a Web3 instance
node_connect = Web3(Web3.HTTPProvider(arbitrum_key))

#check connection
print(node_connect.is_connected())

#Load Contract Address 
aave_pool_contractadd=node_connect.to_checksum_address('0x794a61358D6845594F94dc1DB02A252b5b4814aD')
aave_lend=node_connect.to_checksum_address('0x625E7708f30cA75bfd92586e17077590C60eb4cD')
aave_stable_borrow=node_connect.to_checksum_address('0x307ffe186F84a3bc2613D1eA417A5737D69A7007')
aave_var_borrow=node_connect.to_checksum_address('0xFCCf3cAbbe80101232d343252614b6A3eE81C989')

#Load Json ABI
with open(r'C:\Users\at147\Coding\Get Apr Python\aave-apr-telegram-script\Aave_pool.json') as file:
    aave_pool_abi=json.load(file)
with open(r'C:\Users\at147\Coding\Get Apr Python\aave-apr-telegram-script\aave_lend.json') as file2:
    aave_lend_abi=json.load(file2)
with open(r'C:\Users\at147\Coding\Get Apr Python\aave-apr-telegram-script\aave_stable_borrow.json') as file3:
    aave_stable_borrow_abi=json.load(file3)
with open(r'C:\Users\at147\Coding\Get Apr Python\aave-apr-telegram-script\aave_var_borrow.json') as file4:
    aave_var_borrow_abi=json.load(file4)

#Initialize the contract Objects
contract = node_connect.eth.contract(address=aave_pool_contractadd, abi=aave_pool_abi)
contract_l=node_connect.eth.contract(address=aave_lend, abi=aave_lend_abi)
contract_sb=node_connect.eth.contract(address=aave_stable_borrow, abi= aave_stable_borrow_abi)
contract_vb=node_connect.eth.contract(address=aave_var_borrow, abi=aave_var_borrow_abi)

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

#Call Read Function
def getLiquidity():

    lent=contract_l.functions.totalSupply().call()
    stable_borrow=contract_sb.functions.totalSupply().call()
    var_borrow=contract_vb.functions.totalSupply().call()
    net_liq=(lent-stable_borrow-var_borrow)/10**12
    net_liq=round(net_liq,2)
    return net_liq

async def sendTelegram(rate,liq,message):
    bot = Bot(token="6320196512:AAF8oxhA80R7FJ9QUd6EuqUbuPEhi66Swkk")
    await bot.send_message(chat_id="-1001971375873", text=f"{rate}%,${liq}M,{message}") 

SLEEPTIME=60
LOOPCOUNT=0
notify=30

async def main():
    global LOOPCOUNT, SLEEPTIME
    while True:
        rounded_apy_=getAPY()
        liquidity=getLiquidity()

        if liquidity<2.5:
            LOOPCOUNT=0
            await sendTelegram(rounded_apy_,liquidity,message='insufficient liq please investigate')
            SLEEPTIME=20
        else:
            LOOPCOUNT+=1
            if LOOPCOUNT%notify==0:
                await sendTelegram(rounded_apy_,liquidity,message='sufficient liq')

            SLEEPTIME=60

        await asyncio.sleep(SLEEPTIME)   

if __name__ == "__main__":
    asyncio.run(main())



