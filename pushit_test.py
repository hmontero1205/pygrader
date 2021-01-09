import os

from pushit import pushd, pushit

print('Running "pushit/psuhd" demo..\n')
# dirs can be traced from home or by cwd only
print('Echo:\n',pushd)
print('-' * 50)
print('Empty call:\n',pushd())
print('-' * 50)

print('Single dir addition:') 
pushd('test', chdir=False) 
print('Empty Call:\n',pushd())
print('-' * 50)

print('Single dir addition w/o dir change: *Incorrect way*')
try:
    pushd('test1', chdir=False) # This will raise an Error
except FileNotFoundError as e:
    print(e)
print('Echo:\n',pushd)
print('-'*50)

print('Single dir addition w/o dir change: *correct way*')
try:
    pushd('test/test1', chdir=False) # Correct path specifed from current location of pushd
except FileNotFoundError as e:
    print(e)
else:
    print('Exception did not raise!')
print('Echo:\n',pushd)
print('-'*50)

print('Append right w/ dir change:')
pushd('test/test1', right=True)
print('Echo:\n',pushd)
print('-'*50)

print('From home dir')
pushd('~')
print('Echo:\n',pushd)

print('-'*50)
print('--Start--')
print(pushd)

print('\n--Context mgr--')
print('CM--withoutargs')
with pushit() as f:
    print('Begin for loop')
    for obj in f:
        print('No arg: ',obj)

print('Echo: ', pushd)
print('Now clearing...')
pushd.clear()
print('Echo: ', pushd)
print('...All Clear!')
print('-' * 50)
print('Single dir addition w/ dir change and queue instantion')
pushd('test')
print('Echo: ', pushd)
print('Another one...')
pushd('test1')
print('But wait..Now using relative paths')
pushd('../..')
print('Echo: ',pushd)
print('-'* 50)
print('\n--Context mgr 3 levels--') 
with pushit() as foo:
    print('Level 1. Doing stuff in: ', os.getcwd())
    with pushit() as bar:
        print('LEvel 2. Doing stuff in: ', os.getcwd())
        with pushit() as f:
            print('Level 3. Doing stuff in: ', os.getcwd())  
            print(f)
        print('Returned to Level 2: ', os.getcwd())
    print('Return to level 1: ', os.getcwd())
print('-'*50)
print('Echo: ', pushd)


print('--ContextMgr with args--')
with pushit('../..') as f:
    print('Do stuff here')
    print('CWD: ',os.getcwd())

print('Echo: ', pushd)