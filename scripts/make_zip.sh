#!/bin/sh
# Packages the submission: python3 scripts/build_normalization.py first if CSVs changed.
set -e
cd "$(dirname "$0")/.."
NAME=Group5_Normalization_Submission
STAGE=$(mktemp -d)
mkdir "$STAGE/$NAME"
cp -R 1NF 2NF 3NF BCNF 4NF normalization_explanation.docx normalization_explanation.pdf "$STAGE/$NAME/"
rm -f "$NAME.zip"
(cd "$STAGE" && zip -qrX "$OLDPWD/$NAME.zip" "$NAME" -x '*/.*')
echo "Built $NAME.zip"
