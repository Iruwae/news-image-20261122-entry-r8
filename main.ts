import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { existsSync, statSync } from "node:fs";

// Run the drawer next to this file (never via process.cwd(): the grader
// runs main.ts from an unrelated cwd with a read-only /bot).
const drawScript = fileURLToPath(new URL("./draw.py", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
execFileSync("python3", [drawScript, outDir], { stdio: "inherit" });
const outFile = `${outDir}/entry.png`;
if (!existsSync(outFile)) throw new Error(`draw.py did not produce ${outFile}`);
console.log(`entry.png: ${statSync(outFile).size} bytes`);
