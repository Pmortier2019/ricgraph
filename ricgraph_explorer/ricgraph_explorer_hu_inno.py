from fastapi import APIRouter, HTTPException
from ricgraph_explorer_graphdb import get_driver  # of andere db connectie
from neo4j import GraphDatabase

router = APIRouter()

@router.get("/publications/{title}")
def get_publication_by_title(title: str):
    query = """
    MATCH (p:RicgraphNode {category: 'research-output'})
    WHERE toLower(p.value) CONTAINS toLower($title)
    RETURN p LIMIT 10
    """
    with get_driver().session() as session:
        result = session.run(query, {"title": title})
        publications = [record["p"] for record in result]
        if not publications:
            raise HTTPException(status_code=404, detail="No publication found.")
        return [dict(pub) for pub in publications]
