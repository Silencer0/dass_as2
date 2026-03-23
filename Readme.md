# Whtiebox

running the code
```
cd moneypoly/moneypoly
python main.py
```
running the tests
```
python -m venv venv
source venv/bin/activate
pip install pytest

cd tests/

pytest test_integration.py
```

# Integration
running code
```
cd integration/code
python main.py
```

running tests
```
cd integration/tests

python -m venv venv
source venv/bin/activate
pip install pytest

pytest test_integration.py
```

# Blackbox

running tests
```
cd blackbox/tests

python -m venv venv
source venv/bin/activate
pip install pytest

pytest test_blackbox.py
```