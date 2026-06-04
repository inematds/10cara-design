#!/usr/bin/env bash
# Espera as 11 imagens serem geradas e faz commit+push automatico.
set -u
cd /home/nmaldaner/projetos/10cara-design
EXPECTED=11
DEADLINE=$(( $(date +%s) + 7200 ))   # 2h de teto
while :; do
  n=$(ls assets/img/*.png 2>/dev/null | wc -l)
  if [ "$n" -ge "$EXPECTED" ]; then break; fi
  if [ "$(date +%s)" -ge "$DEADLINE" ]; then echo "[watch] timeout com $n/$EXPECTED imgs" >> assets/watch.log; break; fi
  sleep 20
done
n=$(ls assets/img/*.png 2>/dev/null | wc -l)
echo "[watch] $n imagens — commitando" >> assets/watch.log
git add assets/img/*.png 2>/dev/null
git -c user.name="inematds" -c user.email="nei.maldaner2014@gmail.com" \
  commit -q -m "imagens: galeria de exemplos gerada com inemaimg (ERNIE)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>" >> assets/watch.log 2>&1
git push -q origin master >> assets/watch.log 2>&1
echo "[watch] push done (exit $?)" >> assets/watch.log
