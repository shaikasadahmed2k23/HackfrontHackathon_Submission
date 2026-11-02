import os
from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase

app = FastAPI(title="DebitLens API")

def driver():
    uri = os.getenv("NEO4J_URI")
    if not uri or not os.getenv("NEO4J_PASSWORD"):
        raise HTTPException(503, "Set NEO4J_URI and NEO4J_PASSWORD (and NEO4J_USER if not neo4j)")
    return GraphDatabase.driver(uri, auth=(os.getenv("NEO4J_USER", "neo4j"), os.environ["NEO4J_PASSWORD"]))

@app.post("/load")
def load():
    """Load data/graph.cypher (exported from the dashboard) into Neo4j."""
    text = open(os.path.join(os.path.dirname(__file__), "..", "data", "graph.cypher")).read()
    stmts = [s.strip() for s in text.split(";\n") if s.strip().rstrip(";")]
    with driver() as d, d.session() as s:
        for q in stmts:
            s.run(q.rstrip(";"))
    return {"statements_run": len(stmts)}

@app.get("/graph/{merchant}")
def merchant_graph(merchant: str):
    q = ("MATCH (m:Merchant {name:$n}) "
         "OPTIONAL MATCH (a:MerchantAlias)-[:DECODES_TO]->(m) "
         "OPTIONAL MATCH (d:Mandate)-[:PAYS]->(m) "
         "OPTIONAL MATCH (d)-[:VIA]->(k:Mechanism)-[:CANCEL_VIA]->(c:CancellationPath) "
         "RETURN m.name AS merchant, collect(DISTINCT a.text) AS aliases, "
         "collect(DISTINCT d.id) AS mandates, collect(DISTINCT k.name) AS mechanisms, "
         "collect(DISTINCT c.mechanism) AS cancel_paths")
    with driver() as d, d.session() as s:
        row = s.run(q, n=merchant).single()
    if not row:
        raise HTTPException(404, "Merchant not found")
    return dict(row)
