#!/usr/bin/env bash
# Runs each eval in a fresh, empty directory via `claude -p` so neither config sees this
# session's memory or conversation. Baseline has the Skill tool disabled; with_skill invokes
# the skill explicitly via its slash command. Usage: bash run_isolated.sh <iteration-dir>
IT="$(cd "$1" && pwd)"
# Run dirs must live OUTSIDE any git repo whose root has Claude auto-memory (memory resolves to the
# repo root), e.g. not under a home dir that is itself a repo. Each run dir also gets its own git init.
ISO="${PSW_ISO_DIR:-${TMPDIR:-/tmp}}/psw-iso-$(basename "$IT")"
export MSYS_NO_PATHCONV=1 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1   # keep "/premium-saas-web" from being rewritten to a Windows path
SUFFIX=$'\n\nAz egészet egy index.html fájlba tedd ebbe a mappába.'
declare -A P
P[1-flowpilot]="Csinálj egy weboldalt a Flowpilot nevű szoftvernek. AI ügynökökkel automatizálja a csapatok munkáját Slackben, Notionben és Gmailben."
P[2-northlane]="Kéne egy weboldal a Northlane nevű cégnek, AI tanácsadással foglalkoznak cégeknek."
P[3-bence]="Csinálj nekem egy portfólió oldalt, Kovács Bence vagyok, UX/UI designer."
P[4-szamlakor]="Csinálj landing page-et a Számlakör nevű online számlázó programhoz kisvállalkozásoknak."

run() { # $1=eval key  $2=config
  local key="$1" cfg="$2" dir="$ISO/$1-$2" out="$IT/eval-$1/$2/run-1"
  rm -rf "$dir" "$out"; mkdir -p "$dir" "$out/outputs"; (cd "$dir" && git init -q)
  local prompt="${P[$key]}$SUFFIX" extra=()
  if [ "$cfg" = with_skill ]; then prompt="/premium-saas-web ${P[$key]}$SUFFIX"; else extra=(--disallowedTools Skill); fi
  ( cd "$dir" && claude -p "$prompt" --model claude-opus-5-5 --permission-mode acceptEdits \
      --allowedTools "Bash Read Write Edit Glob Grep" "${extra[@]}" --output-format json > "$out/result.json" 2> "$out/stderr.txt" )
  cp "$dir/index.html" "$out/outputs/" 2>/dev/null || echo "NO index.html: $key $cfg"
  python - "$out/result.json" "$out/timing.json" <<'EOF'
import json, sys
try:
    r = json.load(open(sys.argv[1], encoding="utf-8"))
    u = r.get("usage", {})
    tok = sum(u.get(k, 0) for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    json.dump({"total_tokens": tok, "duration_ms": r.get("duration_ms"), "total_duration_seconds": round(r.get("duration_ms", 0) / 1000, 1)}, open(sys.argv[2], "w"))
except Exception as e:
    print("timing parse failed", sys.argv[1], e)
EOF
  echo "done: $key $cfg"
}

for key in "${!P[@]}"; do
  for cfg in with_skill without_skill; do run "$key" "$cfg" & done
done
wait
echo ALL DONE
