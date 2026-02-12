# Hive 999 — Validation Checklist

## 1. Matrix Generation

```bash
python data/matrix/generate_matrix.py
```

- [ ] Output: `data/matrix/matrix_729.json`
- [ ] Exactly 729 nodes
- [ ] All digital roots = 9
- [ ] ID range: H9-0009 to H9-6561

```bash
python -c "
import json
nodes = json.load(open('data/matrix/matrix_729.json'))
print(f'Nodes: {len(nodes)}')
print(f'All DR=9: {all(n[\"digital_root\"]==9 for n in nodes)}')
print(f'First: {nodes[0][\"id\"]}  Last: {nodes[-1][\"id\"]}')
"
```

## 2. Embeddings

```bash
python data/embeddings/embed_matrix.py
```

- [ ] Collection `matrix_999` created in `data/vectors/hive_vectors/`
- [ ] All 729 documents embedded
- [ ] No errors

## 3. Tool Tests

### Matrix Search
```bash
python -c "
from tools.blockchain.matrix_search import matrix_search_tool
print(matrix_search_tool.fn(query='Ethereum RegTech compliance for investors', n_results=3))
"
```
- [ ] Returns 3 nodes with relevant blockchain/stakeholder/trend metadata

### Compliance Checker
```bash
python -c "
from tools.regtech.compliance_checker import compliance_check_tool
print(compliance_check_tool.fn(blockchain='Ethereum', stakeholder='Investors'))
"
```
- [ ] KYC/AML score: 92
- [ ] ESG score: 88
- [ ] MiCA readiness: high

### Federation Router
```bash
python -c "
from tools.ibc.federation_router import federation_route_tool
print(federation_route_tool.fn(source_chain='Bitcoin', target_chain='Optimism'))
"
```
- [ ] Route found (Bitcoin → Ethereum → Optimism)
- [ ] Digital root invariant preserved

### Caterpillar Artist
```bash
python -c "
from tools.art.caterpillar_artist import caterpillar_ansi_tool
print(caterpillar_ansi_tool.fn(art_name='queen bee'))
"
```
- [ ] ANSI art displayed
- [ ] Timestamped copy in `art/generated/`

## 4. Queen Bee Agent

```bash
python main.py --query "Compare Ethereum and Solana for institutional investors considering RegTech compliance"
```

- [ ] Response references matrix nodes
- [ ] Uses compliance_check tool
- [ ] Mentions KYC/AML and ESG scores
- [ ] Favors Ethereum for MiCA compliance

## 5. Sample Queries for Each Agent Tier

### Queen Bee
- "What are the top 3 blockchains for government CBDC pilots?"
- "Analyze sustainability-compliant validation across all stakeholders"
- "Route a cross-chain transfer from Bitcoin to Polygon PoS"

### Worker Bee (Ethereum)
- `:worker eth` then "How does Ethereum serve trade unions in asset tokenization?"

### Drone (Government Agencies)
- `:drone gov` then "Which blockchains are most compliant for government use?"

### Forager (RegTech)
- `:forager regtech` then "How mature is RegTech across all 9 blockchains?"

## 6. TUI Verification

```bash
python main.py
```

- [ ] Full-screen layout renders correctly
- [ ] Sidebar shows agents and keybinds
- [ ] Chat panel is scrollable
- [ ] Art panel shows ANSI art with `:art queen bee`
- [ ] Alt+Q switches to Queen
- [ ] Alt+1-9 switch to Workers
- [ ] `:quit` exits cleanly
- [ ] Ctrl-C exits cleanly

## 7. Systemd Service

```bash
sudo systemctl start beeai-hive
journalctl -u beeai-hive --no-pager -n 20
```

- [ ] Service starts without errors
- [ ] Logs show "non-interactive mode"
