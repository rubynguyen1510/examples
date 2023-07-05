# Result -> Needs API_KEY
printf "1. One KB file -> Tinypng\n"
curl http://localhost:3000/ -H "X-Internal-Challenge: secret-key" -H "Content-Type: application/json" -d '{"payload": {"provider": "tinypng", "image":"iVBORw0KGgoAAAANSUhEUgAAABEAAAAOCAMAAAD+MweGAAADAFBMVEUAAAAAAFUAAKoAAP8AJAAAJFUAJKoAJP8ASQAASVUASaoASf8AbQAAbVUAbaoAbf8AkgAAklUAkqoAkv8AtgAAtlUAtqoAtv8A2wAA21UA26oA2/8A/wAA/1UA/6oA//8kAAAkAFUkAKokAP8kJAAkJFUkJKokJP8kSQAkSVUkSaokSf8kbQAkbVUkbaokbf8kkgAkklUkkqokkv8ktgAktlUktqoktv8k2wAk21Uk26ok2/8k/wAk/1Uk/6ok//9JAABJAFVJAKpJAP9JJABJJFVJJKpJJP9JSQBJSVVJSapJSf9JbQBJbVVJbapJbf9JkgBJklVJkqpJkv9JtgBJtlVJtqpJtv9J2wBJ21VJ26pJ2/9J/wBJ/1VJ/6pJ//9tAABtAFVtAKptAP9tJABtJFVtJKptJP9tSQBtSVVtSaptSf9tbQBtbVVtbaptbf9tkgBtklVtkqptkv9ttgBttlVttqpttv9t2wBt21Vt26pt2/9t/wBt/1Vt/6pt//+SAACSAFWSAKqSAP+SJACSJFWSJKqSJP+SSQCSSVWSSaqSSf+SbQCSbVWSbaqSbf+SkgCSklWSkqqSkv+StgCStlWStqqStv+S2wCS21WS26qS2/+S/wCS/1WS/6qS//+2AAC2AFW2AKq2AP+2JAC2JFW2JKq2JP+2SQC2SVW2Saq2Sf+2bQC2bVW2baq2bf+2kgC2klW2kqq2kv+2tgC2tlW2tqq2tv+22wC221W226q22/+2/wC2/1W2/6q2///bAADbAFXbAKrbAP/bJADbJFXbJKrbJP/bSQDbSVXbSarbSf/bbQDbbVXbbarbbf/bkgDbklXbkqrbkv/btgDbtlXbtqrbtv/b2wDb21Xb26rb2//b/wDb/1Xb/6rb////AAD/AFX/AKr/AP//JAD/JFX/JKr/JP//SQD/SVX/Sar/Sf//bQD/bVX/bar/bf//kgD/klX/kqr/kv//tgD/tlX/tqr/tv//2wD/21X/26r/2////wD//1X//6r////qm24uAAAA1ElEQVR42h1PMW4CQQwc73mlFJGCQChFIp0Rh0RBGV5AFUXKC/KPfCFdqryEgoJ8IX0KEF64q0PPnow3jT2WxzNj+gAgAGfvvDdCQIHoSnGYcGDE2nH92DoRqTYJ2bTcsKgqhIi47VdgAWNmwFSFA1UAAT2sSFcnq8a3x/zkkJrhaHT3N+hD3aH7ZuabGHX7bsSMhxwTJLr3evf1e0nBVcwmqcTZuatKoJaB7dSHjTZdM0G1HBTWefly//q2EB7/BEvk5vmzeQaJ7/xKPImpzv8/s4grhAxHl0DsqGUAAAAASUVORK5CYII="}, "variables": {"API_KEY": "R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ"}}' -o image_test/image_test_output/1KB_Tinypng.txt
printf '\n'

printf "2. One KB file -> krakenio\n"
curl http://localhost:3000/ -H "X-Internal-Challenge: secret-key" -H "Content-Type: application/json" -d '{"payload": {"provider": "krakenio", "image":"iVBORw0KGgoAAAANSUhEUgAAABEAAAAOCAMAAAD+MweGAAADAFBMVEUAAAAAAFUAAKoAAP8AJAAAJFUAJKoAJP8ASQAASVUASaoASf8AbQAAbVUAbaoAbf8AkgAAklUAkqoAkv8AtgAAtlUAtqoAtv8A2wAA21UA26oA2/8A/wAA/1UA/6oA//8kAAAkAFUkAKokAP8kJAAkJFUkJKokJP8kSQAkSVUkSaokSf8kbQAkbVUkbaokbf8kkgAkklUkkqokkv8ktgAktlUktqoktv8k2wAk21Uk26ok2/8k/wAk/1Uk/6ok//9JAABJAFVJAKpJAP9JJABJJFVJJKpJJP9JSQBJSVVJSapJSf9JbQBJbVVJbapJbf9JkgBJklVJkqpJkv9JtgBJtlVJtqpJtv9J2wBJ21VJ26pJ2/9J/wBJ/1VJ/6pJ//9tAABtAFVtAKptAP9tJABtJFVtJKptJP9tSQBtSVVtSaptSf9tbQBtbVVtbaptbf9tkgBtklVtkqptkv9ttgBttlVttqpttv9t2wBt21Vt26pt2/9t/wBt/1Vt/6pt//+SAACSAFWSAKqSAP+SJACSJFWSJKqSJP+SSQCSSVWSSaqSSf+SbQCSbVWSbaqSbf+SkgCSklWSkqqSkv+StgCStlWStqqStv+S2wCS21WS26qS2/+S/wCS/1WS/6qS//+2AAC2AFW2AKq2AP+2JAC2JFW2JKq2JP+2SQC2SVW2Saq2Sf+2bQC2bVW2baq2bf+2kgC2klW2kqq2kv+2tgC2tlW2tqq2tv+22wC221W226q22/+2/wC2/1W2/6q2///bAADbAFXbAKrbAP/bJADbJFXbJKrbJP/bSQDbSVXbSarbSf/bbQDbbVXbbarbbf/bkgDbklXbkqrbkv/btgDbtlXbtqrbtv/b2wDb21Xb26rb2//b/wDb/1Xb/6rb////AAD/AFX/AKr/AP//JAD/JFX/JKr/JP//SQD/SVX/Sar/Sf//bQD/bVX/bar/bf//kgD/klX/kqr/kv//tgD/tlX/tqr/tv//2wD/21X/26r/2////wD//1X//6r////qm24uAAAA1ElEQVR42h1PMW4CQQwc73mlFJGCQChFIp0Rh0RBGV5AFUXKC/KPfCFdqryEgoJ8IX0KEF64q0PPnow3jT2WxzNj+gAgAGfvvDdCQIHoSnGYcGDE2nH92DoRqTYJ2bTcsKgqhIi47VdgAWNmwFSFA1UAAT2sSFcnq8a3x/zkkJrhaHT3N+hD3aH7ZuabGHX7bsSMhxwTJLr3evf1e0nBVcwmqcTZuatKoJaB7dSHjTZdM0G1HBTWefly//q2EB7/BEvk5vmzeQaJ7/xKPImpzv8/s4grhAxHl0DsqGUAAAAASUVORK5CYII="}, "variables": {"API_KEY": "f66cec6f44df73d3ba48d8dbce302738", "SECRET_API_KEY":"7bbd29dd53c00a068b7ebe20b074540a0d7cea9d"}}' -o image_test/image_test_output/1KB_Kraken.txt
printf '\n'

printf "3.  200 KB file -> tinypng\n"
file_content=$(cat image_test/200_kb.txt)
data="{\"payload\": {\"provider\": \"tinypng\", \"image\": \"$file_content\" }, \"variables\": { \"API_KEY\": \"R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ\" } }"
curl http://localhost:3000/ -H "X-Internal-Challenge: secret-key" -H "Content-Type: application/json" -d "$data" -o image_test/image_test_output/200KB_Tinypng.txt
printf '\n'

printf "4.  200 KB file -> krakenio\n"
file_content=$(cat image_test/200_kb.txt)
data="{\"payload\": {\"provider\": \"tinypng\", \"image\": \"$file_content\" }, \"variables\": { \"API_KEY\": \"R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ\", \"SECRET_API_KEY\": \"7bbd29dd53c00a068b7ebe20b074540a0d7cea9d\"} }"
curl http://localhost:3000/ -H "X-Internal-Challenge: secret-key" -H "Content-Type: application/json" -d "$data" -o image_test/image_test_output/200KB_Kraken.txt
printf '\n'


# printf "5.  3.7 MB file -> tinypng\n"
# file_content=$(cat image_test/3.7_mb.txt)
# data="{\"payload\": {\"provider\": \"tinypng\", \"image\": \"$file_content\" }, \"variables\": { \"API_KEY\": \"R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ\" } }"
# curl http://localhost:3000/ -H "X-Internal-Challenge: secret-key" -H "Content-Type: application/json" -d "$data" -o image_test/image_test_output/3.7MB_Tinypng.txt
# printf '\n'

# printf "6.  3.7 MB file -> krakenio\n"
# file_content=$(cat image_test/3.7_mb.txt)
# data="{\"payload\": {\"provider\": \"tinypng\", \"image\": \"$file_content\" }, \"variables\": { \"API_KEY\": \"R4nM3B54NbHNcHblC0XXl0LZyV82PBgZ\", \"SECRET_API_KEY\": \"7bbd29dd53c00a068b7ebe20b074540a0d7cea9d\"} }"
# curl http://localhost:3000/ -H "X-Internal-Challenge: secret-key" -H "Content-Type: application/json" -d "$data" -o image_test/image_test_output/3.7MB_Kraken.txt
# printf '\n'