require('dotenv').config();
const createTestCafe = require('testcafe');
let testcafe         = null;

createTestCafe('localhost', 1337, 1338)
    .then(tc => {
        testcafe     = tc;
        const runner = testcafe.createRunner();

        return runner
            .src('tests/sample.test.js')
            .browsers([ 'browserstack:Edge@15.0:Windows 10', 'browserstack:IE@10:Windows 8' ])
            .run();
    })
    .then(failedCount => {
        console.log('Tests failed: ' + failedCount);
        testcafe.close();
    })
    .catch(err => {
        console.log("err", err);
        testcafe.close();
    });
