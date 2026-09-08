
    const fs = require('fs');
    const content = fs.readFileSync('js/data.js', 'utf-8');
    // We execute the JS code in a limited context to extract parks
    eval(content);
    fs.writeFileSync('temp_parks.json', JSON.stringify(parks));
    