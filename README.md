<h1 align="center">🎫 Totelepep.mu Ticket Checker</h1>

<p align="center">
  A sleek, dark-themed desktop GUI to check <strong>Totelepep.mu (totelepep.mu)</strong> betting ticket statuses — built with <strong>PySide6</strong>.
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/platform-Windows-blue?style=flat-square">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-yellow?style=flat-square">
  <img alt="Framework" src="https://img.shields.io/badge/GUI-PySide6-7c5cff?style=flat-square">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green?style=flat-square">
</p>

---

<h2>📸 Preview</h2>

<p align="center">
  <em>Paste a ticket number, hit Search, and get a color-coded table of every leg — green for wins, red for losses, yellow for pending.</em>
</p>

<table align="center">
  <tr>
    <td align="center"><b>Status Header</b></td>
    <td align="center"><b>Leg-by-Leg Table</b></td>
  </tr>
  <tr>
    <td>Shows overall ticket status (WINNER / LOSER / UNDECIDED), booking ref, and booking date at a glance.</td>
    <td>Every match is broken down with time, cleaned-up match name, market, pick, odds, and result — each row tinted by outcome.</td>
  </tr>
</table>

---

<h2>✨ Features</h2>

<ul>
  <li>🔍 <strong>Instant lookup</strong> — paste any Totelepep.mu ticket number and search with one click (or hit Enter)</li>
  <li>🎨 <strong>Color-coded results</strong> — WIN (green), LOSS (red), and PENDING/UND (yellow) rows are visually distinct</li>
  <li>🧾 <strong>Full leg breakdown</strong> — time, match, market, pick, and odds for every selection on the ticket</li>
  <li>🌙 <strong>Dark theme UI</strong> — clean, modern, easy on the eyes</li>
  <li>⚡ <strong>Non-blocking requests</strong> — API calls run on a background thread so the UI never freezes</li>
  <li>🧠 <strong>Smart name cleanup</strong> — raw competition strings are parsed into readable "Country / League / Team v Team" format</li>
</ul>

---

<img width="886" height="752" alt="image" src="https://github.com/user-attachments/assets/216d1022-cdcb-445c-b102-a07d2b7fb4e9" />

---

<h2>🛠️ Tech Stack</h2>

<table>
  <tr><th>Component</th><th>Library</th></tr>
  <tr><td>GUI Framework</td><td><a href="https://doc.qt.io/qtforpython/">PySide6</a></td></tr>
  <tr><td>HTTP Requests</td><td><a href="https://docs.python-requests.org/">requests</a></td></tr>
  <tr><td>Threading</td><td>PySide6 <code>QThread</code> (built-in)</td></tr>
</table>

---

<h2>📦 Installation</h2>

<h3>1. Clone the repository</h3>

<pre><code>git clone https://github.com/YashvirGaming/Totelepep.mu-Ticket-Checker.git
cd Totelepep.mu-Ticket-Checker
</code></pre>

<h3>2. Install dependencies</h3>

<pre><code>pip install -r requirements.txt
</code></pre>

<p><strong>requirements.txt</strong></p>

<pre><code>PySide6
requests
</code></pre>

<h3>3. Run the app</h3>

<pre><code>python ticket_checker.py
</code></pre>

---

<h2>🚀 Usage</h2>

<ol>
  <li>Launch the app</li>
  <li>Paste your ticket number into the input box (e.g. <code>AAD-6411128</code>)</li>
  <li>Click <strong>Search</strong> or press <kbd>Enter</kbd></li>
  <li>View the overall status and a full color-coded table of every leg on the ticket</li>
</ol>

---

<h2>📁 Project Structure</h2>

<pre><code>Totelepep.mu-ticket-checker/
├── ticket_checker.py     # Main application (GUI + logic)
├── requirements.txt      # Python dependencies
└── README.md             # You are here
</code></pre>

---

<h2>🔌 API Reference</h2>

<p>This app talks directly to Totelepep.mu's internal ticket-status endpoint:</p>

<table>
  <tr><th>Field</th><th>Value</th></tr>
  <tr><td>Endpoint</td><td><code>POST https://www.totelepep.mu/WebApi/GetTicketStatus</code></td></tr>
  <tr><td>Content-Type</td><td><code>application/x-www-form-urlencoded; charset=UTF-8</code></td></tr>
  <tr><td>Payload</td><td><code>TicketNumber={TICKET_ID}</code></td></tr>
</table>

<p><strong>Sample response fields used:</strong></p>

<table>
  <tr><th>JSON Path</th><th>Displayed As</th></tr>
  <tr><td><code>transaction.status</code></td><td>Overall ticket status header</td></tr>
  <tr><td><code>transaction.bookingRef</code></td><td>Reference label</td></tr>
  <tr><td><code>transaction.bookingDate</code></td><td>Booked date label</td></tr>
  <tr><td><code>transaction.bets[].competitionName</code></td><td>Match column (cleaned + outcome parsed)</td></tr>
  <tr><td><code>transaction.bets[].marketCode</code></td><td>Market column</td></tr>
  <tr><td><code>transaction.bets[].optionName</code></td><td>Pick column</td></tr>
  <tr><td><code>transaction.bets[].optionOdd</code></td><td>Odds column</td></tr>
  <tr><td><code>transaction.bets[].betTime</code></td><td>Time column</td></tr>
</table>

---

<h2>🎨 Color Legend</h2>

<table>
  <tr>
    <td>🟩</td><td><strong>WIN</strong></td><td>Leg won</td>
  </tr>
  <tr>
    <td>🟥</td><td><strong>LOS</strong></td><td>Leg lost</td>
  </tr>
  <tr>
    <td>🟨</td><td><strong>UND</strong></td><td>Leg undecided / pending</td>
  </tr>
</table>

---

<h2>🗺️ Roadmap</h2>

<ul>
  <li>[ ] Summary row (total won / lost / pending count)</li>
  <li>[ ] Export results to CSV</li>
  <li>[ ] Auto-refresh for pending tickets</li>
  <li>[ ] Multi-ticket batch lookup from a text file</li>
  <li>[ ] Light theme toggle</li>
</ul>

---

<h2>⚠️ Disclaimer</h2>

<p>
This tool queries a third-party public-facing API and is intended for personal, informational use only —
checking the status of your own betting tickets. It is not affiliated with or endorsed by Totelepep.mu.
Use responsibly and in accordance with the website's terms of service.
</p>

---

<h2>📄 License</h2>

<p>Distributed under the MIT License. See <code>LICENSE</code> for more information.</p>

---

<p align="center">Built with 🖤 using PySide6</p>
