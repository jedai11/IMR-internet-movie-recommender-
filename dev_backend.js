const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const winPy = path.join(root, 'backend', '.venv', 'Scripts', 'python.exe');
const unixPy = path.join(root, 'backend', '.venv', 'bin', 'python');

let py = 'python';
if (fs.existsSync(winPy)) {
  py = winPy;
} else if (fs.existsSync(unixPy)) {
  py = unixPy;
}

const child = spawn(py, ['run_backend.py'], {
  cwd: path.join(root, 'backend'),
  stdio: 'inherit',
  shell: false
});

child.on('error', (err) => {
  console.error('Failed to start backend process:', err);
  process.exit(1);
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
