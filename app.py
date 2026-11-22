from flask import Flask, request
app = Flask(__name__)
history = []

def ai_analyze(completed, pending, docs):
    summary = f"Completed: {completed}. Pending first: {pending}."
    missing = "Missing: No documents. Add docs / login details." if not docs else "Documents attached. No missing docs."
    if "urgent" in pending.lower() or "payment" in pending.lower() or "client" in pending.lower():
        priority = "🔴 HIGH PRIORITY - Do this first"
    else:
        priority = "🟡 MEDIUM PRIORITY"
    return summary, missing, priority

CSS = """
<style>
body{font-family:Arial;margin:0;background:linear-gradient(135deg,#667eea,#764ba2,#f093fb,#f5576c);min-height:100vh;padding:20px}
.nav{background:white;padding:15px 25px;border-radius:15px;display:flex;justify-content:space-between;align-items:center;max-width:900px;margin:auto;box-shadow:0 10px 30px rgba(0,0,0,0.2)}
.nav b{font-size:22px;color:#6d28d9}
.nav a{text-decoration:none;color:#6d28d9;font-weight:bold;margin-left:15px}
.hero{background:white;padding:30px;border-radius:20px;max-width:900px;margin:20px auto;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,0.2)}
.hero h1{font-size:38px;background:linear-gradient(90deg,#7c3aed,#db2777,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:5px}
.cards{display:flex;gap:15px;justify-content:center;flex-wrap:wrap;margin-top:20px}
.card{flex:1;min-width:180px;padding:20px;border-radius:15px;color:white}
.c1{background:linear-gradient(135deg,#6366f1,#a855f7)} .c2{background:linear-gradient(135deg,#ec4899,#f97316)} .c3{background:linear-gradient(135deg,#10b981,#06b6d4)}
.box{background:white;padding:25px;border-radius:20px;max-width:600px;margin:20px auto;box-shadow:0 10px 30px rgba(0,0,0,0.2)}
input,textarea,select{width:100%;padding:12px;margin:6px 0;border:2px solid #e5e7eb;border-radius:10px;box-sizing:border-box}
.btn{background:linear-gradient(90deg,#7c3aed,#db2777);color:white;padding:13px;width:100%;border:none;border-radius:12px;font-size:16px;font-weight:bold;cursor:pointer}
.btn2{background:linear-gradient(90deg,#059669,#06b6d4);color:white;padding:11px;border:none;border-radius:10px;cursor:pointer}
.tag{display:inline-block;padding:6px 12px;border-radius:20px;background:#fef3c7;font-weight:bold}
</style>
"""

NAV = """<div class='nav'><b>🚀 TransferTrail AI</b><div><a href='/'>🏠 Home</a><a href='/new'>✨ New Handover</a><a href='/history'>📋 History</a><a href='/about'>ℹ️ About</a></div></div>"""

@app.route('/')
def home():
    return CSS + NAV + """
    <div class='hero'>
    <div style='font-size:50px'>🤖✨</div>
    <h1>TransferTrail AI</h1>
    <p style='font-size:18px;color:#555'>Smart Work Handover System - Never Lose Work When Employee Leaves!</p>
    <div class='cards'>
    <div class='card c1'><h3>🧠 AI Summary</h3><p>Auto summary of completed & pending work</p></div>
    <div class='card c2'><h3>🎤 Voice Assistant</h3><p>Speak your question, AI will answer</p></div>
    <div class='card c3'><h3>⚡ Priority Check</h3><p>Detects Urgent, Client, Payment tasks</p></div>
    </div>
    <br><a href='/new'><button class='btn'>🚀 Start New Handover →</button></a>
    <br><br><a href='/history'>View All History →</a>
    </div>
    <p style='text-align:center;color:white'>Made for Smart Teams • AI Powered • 100% Free</p>
    """

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
        project = request.form['project']; from_emp = request.form['from_emp']; to_emp = request.form['to_emp']
        completed = request.form['completed']; pending = request.form['pending']; docs = request.form['docs']; question = request.form['question']
        summary, missing, priority = ai_analyze(completed, pending, docs)
        answer = f"Pending: {pending}" if "pending" in question.lower() else f"Completed: {completed}" if "completed" in question.lower() else f"From {from_emp} to {to_emp} - Project {project}"
        history.append(f"{project} | {from_emp} -> {to_emp} | {priority}")
        return CSS + NAV + f"""
        <div class='box'><h2 style='color:#7c3aed'>🎉 Handover Generated!</h2>
        <p><b>Project:</b> {project} | {from_emp} → {to_emp}</p>
        <p><span class='tag'>{priority}</span></p>
        <h3>🧠 AI Summary</h3><p>{summary}</p>
        <h3>⚠️ Missing Info</h3><p>{missing}</p>
        <h3>💬 AI Answer</h3><p>{answer}</p>
        <button class='btn2' onclick="speak()">🔊 Speak Summary</button>
        <br><br><a href='/new'>➕ New Handover</a> | <a href='/history'>📋 View History</a>
        <script>function speak(){{let u=new SpeechSynthesisUtterance("{summary} {priority}"); speechSynthesis.speak(u);}}</script>
        </div>"""
    return CSS + NAV + """
    <div class='box'><h2 style='color:#7c3aed'>✨ Create New Handover</h2>
    <form method="POST">
    🏢 Project Name: <input name="project" placeholder="Ex: Website Project" required>
    👤 From Employee: <input name="from_emp" placeholder="Ex: Rahul" required>
    👤 To Employee: <input name="to_emp" placeholder="Ex: Anu" required>
    ✅ Completed Tasks: <textarea name="completed" placeholder="Login page done"></textarea>
    ⏳ Pending Tasks: <textarea name="pending" placeholder="Urgent payment page for client"></textarea>
    📎 Documents / Links: <input name="docs" placeholder="Leave blank to test Missing">
    🤖 Ask AI: <input name="question" placeholder="What is pending?">
    <button type="button" class='btn2' onclick="startVoice()">🎤 Speak Question</button><br><br>
    <button class='btn'>✨ Generate AI Handover</button>
    </form>
    <script>function startVoice(){let r=new webkitSpeechRecognition(); r.onresult=function(e){document.querySelector('[name=question]').value=e.results[0][0].transcript}; r.start();}</script>
    </div>"""

@app.route('/history')
def hist():
    items = "".join([f"<div style='background:#f3f4f6;padding:12px;border-radius:10px;margin:8px 0'>📄 {h}</div>" for h in history]) or "<p>No handovers yet</p>"
    return CSS + NAV + f"<div class='box'><h2>📋 Handover History</h2>{items}<br><a href='/new'>➕ New Handover</a></div>"

@app.route('/about')
def about():
    return CSS + NAV + """<div class='box'><h2>ℹ️ About TransferTrail AI</h2><p>This app helps companies when an employee leaves or goes on leave. It creates AI summary, finds missing info, detects urgent tasks, and answers questions by voice.</p><p><b>Features:</b> AI Summary, Missing Check, Priority, Voice Assistant, History</p><p><b>Tech:</b> Python, Flask, HTML, CSS, JavaScript</p></div>"""

app.run(debug=True)