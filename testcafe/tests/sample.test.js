const nodeStatic = require('node-static');
const fileServer = new nodeStatic.Server('./public');

// サンプル用にサーバを立てる
const __server = require('http').createServer( (req,res)=>{
    req.addListener('end', ()=>{ fileServer.serve(req, res); }).resume();
} ).listen(3000);

fixture('Sample Test')
    .page('http://localhost:3000/')
    .after( async (ctx) => {
        __server.close();
    });

test('Assert page title', async (t) => {
    const title = await t.eval( () => window.document.querySelector('title').text );
    await t.expect( 'samplepage' ).eql( title );
});
