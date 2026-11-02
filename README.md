# DebitLens

Finds every recurring payment in a bank statement, decodes the merchant, flags price hikes, trial conversions and charges after the service stopped being used, and shows the correct way to cancel. Synthetic data only.

hackFront India - Problem: "The Auto Debits Nobody Can Find". Team FALCON.

## Run the dashboard
Open frontend/index.html in a browser. No install needed.

## What the dashboard does
- Generates 12 months of synthetic statements (seeded, repeatable)
- Decodes bank text with a hand-built alias table plus fuzzy matching and a confidence score
- Detects recurring payments with irregular dates, rejects irregular merchants (Swiggy, Uber)
- Flags: price increase, trial converted to paid, charges after inactivity
- Per-mechanism cancellation guides (UPI AutoPay, card e-mandate, NACH, App Store, direct billing)
- Annual view and a payment graph; "Export Cypher" produces the Neo4j load script

## Neo4j (optional backend)
1. Open the dashboard, Payment Graph, click "Export Cypher", paste the output into data/graph.cypher
2. cd backend && pip install -r requirements.txt
3. Set NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
4. uvicorn app:app --reload, then POST /load and GET /graph/Netflix

The backend was written but the dashboard does not call it yet; the dashboard graph is built in the browser.

## Disclosure
AI tools (Claude) were used to help write code and documents. All financial data is synthetic.
