PWD=$(dirname $0)

python3 merge.py --dst "${PWD}/dut" --logging debug "${PWD}/data/A.zip" "${PWD}/data/B.zip"


if [ -n "$(git status --porcelain)" ]; then
    exit 1
else
    exit 0
fi