#!/bin/bash
mkdir -p "$HOME/my-gemini-cli"
cd "$HOME/my-gemini-cli" || { echo "Failed to navigate to ~/my-gemini-cli"; exit 1; }
npm install ajv
cat > test_ajv.js << 'INNER_EOF'
const Ajv = require('ajv');
const ajv = new Ajv();
const schema = {
type: 'array',
items: { type: 'array', items: { type: 'integer' }, minItems: 3, maxItems: 3 },
minItems: 6, maxItems: 6
};
const validate = ajv.compile(schema);
const matrix = [[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18]];
const valid = validate(matrix);
console.log('Valid:', valid);
INNER_EOF
node test_ajv.js
