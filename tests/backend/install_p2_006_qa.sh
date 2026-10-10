#!/usr/bin/env bash
# CI-only: signed immutable Ubuntu indexes, exact revisions, no live-apt fallback.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
definition="$root/tests/backend/p2_006_qa_environment.json"
source /etc/os-release
test "$VERSION_ID" = "24.04"
test "$(dpkg --print-architecture)" = "amd64"
qa_apt="$(mktemp -d "${RUNNER_TEMP:?}/p2-006-apt.XXXXXX")"
snapshot="$(python -c 'import json,sys; print(json.load(open(sys.argv[1]))["snapshot"])' "$definition")"
cat > "$qa_apt/sources.list" <<EOF
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://snapshot.ubuntu.com/ubuntu/$snapshot noble main universe
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://snapshot.ubuntu.com/ubuntu/$snapshot noble-updates main universe
deb [signed-by=/usr/share/keyrings/ubuntu-archive-keyring.gpg] https://snapshot.ubuntu.com/ubuntu/$snapshot noble-security main universe
EOF
# Ignore runner/PPA/live indexes; dependencies resolve only from the same snapshot.
mkdir -p "$qa_apt/lists/partial"
chmod 755 "$qa_apt" "$qa_apt/lists" "$qa_apt/lists/partial"
options=(-o "Dir::Etc::sourcelist=$qa_apt/sources.list" -o 'Dir::Etc::sourceparts=-'
         -o "Dir::State::lists=$qa_apt/lists" -o 'Acquire::Check-Valid-Until=false')
# Expired historical metadata is expected; archive signature/hash checks stay enabled.
sudo apt-get "${options[@]}" update -qq
mapfile -t packages < <(python -c 'import json,sys; d=json.load(open(sys.argv[1])); print("\n".join(k+"="+v for k,v in d["packages"].items()))' "$definition")
sudo apt-get "${options[@]}" install -y --no-install-recommends --allow-downgrades "${packages[@]}"
python "$root/tests/backend/verify_p2_006_qa_environment.py"
mkdir -p "$HOME/.local/share/fonts"
cp "$root/backend/app/services/assets/fonts/"*.ttf "$HOME/.local/share/fonts/"
fc-cache -f
