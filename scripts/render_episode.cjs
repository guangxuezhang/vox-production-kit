const fs = require('fs');
const path = require('path');
const {spawnSync} = require('child_process');

const [plan, composition, output] = process.argv.slice(2);
if (!plan || !composition || !output) {
  console.error('Usage: node scripts/render_episode.cjs <episode-plan.json> <composition-id> <output.mp4>');
  process.exit(1);
}
if (!/^[A-Za-z0-9_-]+$/.test(composition) || /[&|<>^"%]/.test(output)) {
  console.error('Invalid composition ID or output path');
  process.exit(1);
}
const root = path.resolve(__dirname, '..');
const check = spawnSync(process.execPath, [path.join(__dirname, 'validate_director_plan.cjs'), path.resolve(plan)], {stdio: 'inherit'});
if (check.status !== 0) process.exit(check.status || 1);
const remotion = path.join(root, 'remotion');
const cli = path.join(remotion, 'node_modules', '.bin', process.platform === 'win32' ? 'remotion.cmd' : 'remotion');
if (!fs.existsSync(cli)) {
  console.error('Remotion is not installed. Run the repository setup before rendering.');
  process.exit(1);
}
const result = spawnSync(cli, ['render', 'src/index.tsx', composition, path.resolve(output)], {cwd: remotion, stdio: 'inherit', shell: process.platform === 'win32'});
process.exit(result.status || 0);
