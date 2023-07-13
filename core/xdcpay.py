from web3 import Web3

# web3 = Web3(Web3.HTTPProvider("https://apothemxdcpayrpc.blocksscan.io/"))
web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

connect = lambda:web3.isConnected()

def pay(from_acc,to_acc,pk,amt):
    context = {"msg":"","done":False,"error":"","hash":"","url":"HTTP://127.0.0.1:7545"}
    try:
        if from_acc[:2] =='0x' and to_acc[:2] == '0x':
            address1 = web3.to_checksum_address(from_acc)
            address2 = web3.to_checksum_address(to_acc)
            print(address1,address2)
            balance = web3.eth.get_balance(address1)
            
            print(balance,amt)
            print("Balance : "+str(web3.from_wei(balance, 'ether'))+ " ETH")
            if balance<amt:
                context["error"] = "Not Enough Blance!"
            else:
                tx = {
                    'nonce':web3.eth.get_transaction_count(address1),
                    'to':address2,
                    'value':web3.to_wei(amt, 'ether'),
                    'gas':200000,
                    'gasPrice':web3.to_wei('50', 'gwei')
                }
                # signed = w3.eth.account.sign_transaction(transaction, pk)
                signd_tx = web3.eth.account.sign_transaction(tx,private_key=pk)

                # tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
                # tx = w3.eth.get_transaction(tx_hash)
                # assert tx["from"] == acct2.address

                tx_trans = web3.eth.send_raw_transaction(signd_tx.rawTransaction)
                hash_ = web3.to_hex(tx_trans)
                context["hash"] = hash_
                context['done'] = True
                context['url'] = f"https://explorer.apothem.network/txs/{hash_}"
                context['msg'] = "Transaction Successfull !!"

        else:
            context['error'] = "Not an Valid Address !!"
    except Exception as e:
        context['error'] = str(e)  
    return context

if __name__ == '__main__':
    c = pay("0xC2a0715bAED62D5fC27377E62E66840f47160b7b", "0x699280A805AB7b1EdE27267e78BEEf5304d3A101", "0xfa871c48c870f78d061cefa7a4cd546c3259befec9bfc01e0b69331f7d544c35", 10)
    print(c)