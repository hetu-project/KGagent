# KGagent
do something from instructions to agent output by raw and resort graph data

## example code review

1. User Query Proposal: A user submits a query.
Multi-Agent Analysis: Multiple agents work together to understand the user's intent, which in this case is identified as a "code review."
2. Parallel Processing:
One agent retrieves the user's configuration for code review from a Dgraph database.
Simultaneously, another agent processes the query and analyzes the results.
The agents then combine the user's configuration (e.g., style check, security check, performance check) with the query results to determine the final review configuration.
3. Data Storage: The query and the final configuration are saved in a graph database like Neo4j.
4. Query Execution:
If privacy is required, the query is processed using a private LLM running in a trusted execution environment (TEE).
If privacy is not a concern, the query is handled via APIs provided by OpenAI, DeepSeek, or Anthropic.
5. Quick Testing(Option):
If the content is executable (e.g., code or a testable idea), a canvas is created to run the code or idea in a free and available TEE environment for quick testing.
6. Result Handling:
The results are returned to the user and saved in the graph database.
Concurrently, another agent updates the user's contributor points, while another agent tracks the user's coding style and language preferences.

