const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = `
<!DOCTYPE html>
<html>
<body>
    <div id="infra-region-selector"></div>
    <div id="infra-grid"></div>
</body>
</html>
`;

const dom = new JSDOM(html, { runScripts: "dangerously" });

// Load data.js
const dataScript = fs.readFileSync('js/data.js', 'utf8');
const infraScript = fs.readFileSync('js/infrastructure.js', 'utf8');

try {
    dom.window.eval(dataScript);
    console.log("Loaded data.js");
} catch(e) {
    console.error("Error in data.js:", e.message);
}

try {
    dom.window.eval(infraScript);
    console.log("Loaded infrastructure.js");
} catch(e) {
    console.error("Error in infrastructure.js:", e.message);
}

setTimeout(() => {
    console.log("Grid HTML length:", dom.window.document.getElementById('infra-grid').innerHTML.length);
    console.log("Selector HTML length:", dom.window.document.getElementById('infra-region-selector').innerHTML.length);
}, 1000);
