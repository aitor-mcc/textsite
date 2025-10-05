import sympy 
 
def encrypt(key,text): 
    #encrypts text and saves it as array 
    new_text = [] 
    for i in range(len(text)): 
        new_char = pow(ord(text[i]),key[0],key[1]) 
        new_text.append(new_char) 
 
    return new_text 
 
def decrypt(key,text): 
    #text must be stored in an array 

    new_text = "" 
    for i in range(len(text)): 
        new_char = pow(int(text[i]),key[0],key[1]) 
        new_text += chr(new_char) 
 
    return new_text 
 
 
def generate_keys():#random public and private key generation 
    #ideally we would increase the range for these, but for testing efficiency I have let these be relatively small 
    p = sympy.randprime(1,1000) 
    q = sympy.randprime(1,1000) 
     
    n = p*q #this is the modulus 
    phi_n = (p-1)*(q-1)#euler totient function 
    e = 65537#public exponent 
    d = modInverse(e,phi_n)#private exponent 
    public_key = [e,n] 
    private_key = [d,n] 
 
    return [public_key,private_key] 
 
 
def modInverse(num, mod): #modular multiplicar inverse where e*d = 1 mod(n) 
    for X in range(1, mod): 
        if (((num % mod) * (X % mod)) % mod == 1): 
            return X 
    return -1 
 
 
def list_to_str(list): 
    string = "" 
    for i in list: 
        string += str(i) 
        string += "," 
 
    return string 
 
def str_to_list(string): 
    li = [] 
    char = "" 
    for i in string: 
        if i != ",": 
            char += i 
        else: 
            li.append(char) 
            char = "" 
 
    return li 
 
 
#for sending messages through asgi  
js_script = """ 
<script> 
      const chatSocket = new WebSocket("ws://" + window.location.host + "/"); 
      chatSocket.onopen = function (e) { 
 
        console.log("The connection was setup successfully !"); 
      }; 
      chatSocket.onclose = function (e) { 
        console.log("Something unexpected happened !"); 
      }; 
      document.querySelector("#id_message_send_input").focus(); 
      document.querySelector("#id_message_send_input").onkeyup = function (e) { 
        if (e.keyCode == 13) { 
          document.querySelector("#id_message_send_button").click(); 
        } 
      }; 
      document.querySelector("#id_message_send_button").onclick = function (e) { 
        var messageInput = document.querySelector( 
          "#id_message_send_input" 
        ).value; 
        chatSocket.send(JSON.stringify({ message: messageInput, username : "{{request.user.username}}"})); 
      }; 
      chatSocket.onmessage = function (e) { 
        const data = JSON.parse(e.data); 
        /*var div = document.createElement("div"); 
        div.innerHTML = data.username + " : " + data.message; 
        document.querySelector("#id_message_send_input").value = ""; 
        document.querySelector("#id_chat_item_container").appendChild(div);*/ 
        location.reload() 
      }; 
</script> 
"""