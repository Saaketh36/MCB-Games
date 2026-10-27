// Opens the portal in the default browser once the Flask server (python app.py) is answering.
const http = require('http');
const { exec } = require('child_process');
const url = 'http://localhost:5000/';

function check(tries) {
  http.get(url, res => {
    res.resume();
    const cmd = process.platform === 'win32' ? 'start ""' : process.platform === 'darwin' ? 'open' : 'xdg-open';
    exec(cmd + ' ' + url);
  }).on('error', () => {
    if (tries > 0) setTimeout(() => check(tries - 1), 500);
    else console.log('Server did not start on ' + url);
  });
}
check(60);
