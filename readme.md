**Activate the virtual environment**
'''
. .\blockchain-env\Scripts\activate.ps1
'''

**Install all packages**
'''
pip3 install -r requirements.txt
'''

**Run the tests**
Make sure to activate the vitual environment
'''
python -m pytest backend\tests
'''

**Run the application and API**
Make sure to activate the virtual environment
'''
python -m backend.app
Stop-Process -Name 'python' -Force
'''

**Run a peer instance**
Make sure to activate the virtual environment
'''
$env:PEER='True'; python -m backend.app
'''
