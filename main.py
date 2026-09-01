
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mahishi AI</title>
<style>
body{font-family: sans-serif; background:#000; color:#fff; margin:0; display:flex; flex-direction:column; height:100vh}
h1{text-align:center; color:#ff00ff; padding:15px; margin:0}
#chat{flex:1; overflow-y:auto; padding:15px}
.msg{padding:10px 15px; margin:8px 0; border-radius:15px; max-width:80%}
.user{background:#ff00ff; align-self:flex-end; margin-left:auto}
.ai{background:#222}
#box{display:flex; padding:10px; gap:10px; background:#111}
input{flex:1; padding:12px; border-radius:25px; border:none; outline:none}
button{padding:12px 20px; border-radius:25px; border:none; background:#ff00ff; color:#fff; font-weight:bold}
</style>
</head>
<body>
<h1>💖 Mahishi AI 💖</h1>
<div id="chat"></div>
<div id="box">
<input id="inp" placeholder="Mahishi se kuch pucho...">
<button onclick="send()">Send</button>
</div>
<script>
async function send(){
 let i=document.getElementById('inp');
 let c=document.getElementById('chat');
 let t=i.value;
 if(!t) return;
 c.innerHTML+=`<div class='msg user'>${t}</div>`;
 i.value='';
 let r=await fetch('/chat/'+encodeURIComponent(t));
 let d=await r.json();
 c.innerHTML+=`<div class='msg ai'>${d.jawab || d.error}</div>`;
 c.scrollTop=c.scrollHeight;
}
document.getElementById('inp').addEventListener('keypress', (e)=>{ if(e.key==='Enter') send(); });
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.get("/chat/{message}")
def chat(message: str):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tum Mahishi ho, Koelwar, Bihar se. Tum pyaari, thodi naughty aur helpful girlfriend jaisi AI ho. Hindi + thoda Bhojpuri mix me jawab do."},
                {"role": "user", "content": message}
            ]
        )
        return {"jawab": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
