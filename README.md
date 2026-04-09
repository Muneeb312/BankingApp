# BankingApp

To run the Banking App, run this command in a terminal:
```
python main.py valid_accounts.txt transactions.out
```

To run the front end test script, run this command in the terminal
```
bash run_tests.sh
```

To run the back end test cases, enter this command in the terminal:
```
pytest test_backend.py -v
```
To run the weekly script, open Git Bash in the root folder of the project, then run:
```
chmod +x daily.sh

chmod +x weekly.sh

./weekly.sh
```
Note: If you recieve a `Python was not found` error, open daily.sh and replace `python` with either `py` or `python3` on lines 11, 12 and 44.