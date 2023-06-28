contract_address = "0x15F4272460062b835Ba0abBf7A5E407F3EF425d3"
token_id = 1
my_mnemonic = "sorok tysach obezyan v jopy sunuly banan"
amount = 0.1

from web3 import Web3

from thirdweb import abi

w3 = Web3(Web3.HTTPProvider("https://polygon.rpc.thirdweb.com"))

print(f"gas price: {w3.eth.gas_price} BNB")  # кол-во Wei за единицу газа
print(f"current block number: {w3.eth.block_number}")
print(f"number of current chain is {w3.eth.chain_id}") 

w3.eth.account.enable_unaudited_hdwallet_features()
account = w3.eth.account.from_mnemonic(my_mnemonic)

contract = w3.eth.contract(contract_address, abi=abi)
owner = contract.functions.ownerOf(token_id).call()

def build_txn(
  *,
  web3: Web3,
  from_address: str,
  to_address: str, 
  amount: float,
) -> dict[str, int | str]:
    gas_price = web3.eth.gas_price

    txn = {  
        'chainId': web3.eth.chain_id,
        'from': from_address,
        'to': from_address,
        'value': int(Web3.toWei(amount, 'ether')),
        'nonce': web3.eth.getTransactionCount(from_address), 
        'gasPrice': web3.eth.gas_price,
        }
    gas = web3.eth.estimate_gas(txn)
    
    nonce = web3.eth.getTransactionCount(from_address)

    txn = {
      'chainId': web3.eth.chain_id,
      'from': from_address,
      'to': to_address,
      'value': int(Web3.toWei(amount, 'ether')),
      'nonce': nonce, 
      'gasPrice': gas_price,
      'gas': gas,
    }
    return txn


transaction = build_txn(
  web3=w3,
  from_address=account.address,
  to_address=owner,
  amount=amount,
)

signed_txn = w3.eth.account.sign_transaction(transaction, account.key)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

print(f"https://polygonscan.com/tx/{txn_hash.hex()}")