def store_code_snippet(user_id, code):
    """存储代码片段到 Neo4j"""
    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run(
                """
                MERGE (u:User {id: $user_id})
                MERGE (c:CodeSnippet {code: $code})
                MERGE (u)-[:SUBMITTED]->(c)
                """,
                user_id=user_id,
                code=code,
            )
        )


def store_review(user_id, code, review_result):
    """存储审查结果到 Neo4j"""
    with driver.session() as session:
        session.execute_write(
            lambda tx: tx.run(
                """
                MERGE (u:User {id: $user_id})
                MERGE (c:CodeSnippet {code: $code})
                MERGE (r:CodeReview {result: $review_result})
                MERGE (u)-[:SUBMITTED]->(c)
                MERGE (c)-[:REVIEWED_BY]->(r)
                MERGE (u)-[:HAS_REVIEW]->(r)
                """,
                user_id=user_id,
                code=code,
                review_result=review_result,
            )
        )

