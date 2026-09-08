
    const fs = require('fs');
    const content = fs.readFileSync('js/data.js', 'utf-8');
    // Mock window to avoid ReferenceError
    global.window = {};
    eval(content + "\nfs.writeFileSync('temp_parks.json', JSON.stringify(parks));");
    