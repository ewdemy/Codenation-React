import json
import requests
import hashlib

def decrypt(message,key):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    message = message.lower()
    decryptedMessage = ""

    for i in message:
        if(i in alphabet):
            iIndex = alphabet.index(i)
            decryptedMessage += alphabet[(iIndex - key) % len(alphabet)]
        else:
            decryptedMessage += i
    return decryptedMessage

#Token do usuário Codenation
myToken = ""


response = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=' + myToken)

data = json.loads(response.content)
dataJson = json.dumps(data)

file = open('answer.json','w')
file.write(dataJson)
file.close()

fileRead = open('answer.json','r')
data = json.loads(fileRead.read())
encoding = fileRead.encoding

decrypted = decrypt(data["cifrado"],data["numero_casas"])

data["decifrado"] = decrypted

hashFile = hashlib.sha1(decrypted.encode(encoding)).hexdigest()

data["resumo_criptografico"] = hashFile

dataJson = json.dumps(data)

file = open('answer.json','w')
file.write(dataJson)
file.close()

answer = {'answer': open('answer.json', 'rb')}
post = requests.post('https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=' + myToken, files=answer)

print(post.content)
print(post.text)











