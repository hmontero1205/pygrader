import os
from pathlib import Path
from pushit_trace import pushd, pushit, popd

def add_init():
    with open('__init__.py', 'w'): pass 

def remove_init():
    inpath = Path(os.getcwd()) / '__init__.py'

    os.remove(inpath)

os.makedirs('pushtest/pushtest1/pushtest2')



print('Running "pushit/pushd" demo..\n')
# dirs can be traced from home or by cwd only
print('Echo:\n',pushd)
print('-' * 50)
print('Empty call:\n',pushd())
print('-' * 50)

print('Single dir addition:') 
pushd('pushtest', chdir=False) 
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
    pushd('pushtest/pushtest1', chdir=False) # Correct path specifed from current location of pushd
except FileNotFoundError as e:
    print(e)
else:
    print('Exception did not raise!')
print('Echo:\n',pushd)
print('-'*50)

print('Append right w/ dir change:')
pushd('pushtest/pushtest1', right=True)
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
pushd('pushtest')
print('Echo: ', pushd)
print('Another one...')
pushd('pushtest1')
print('But wait..Now using relative paths')
pushd('../..')
print('Echo: ',pushd)
print('-'* 50)
pushd.clear()
print('\n--Context mgr 3 levels--')
pushd('pushtest', chdir=False)
pushd('pushtest/pushtest1', chdir=False)
pushd('pushtest/pushtest1/pushtest2', chdir=False)

with pushit() as foo:
    add_init()
    with pushit() as bar:
        add_init()
        with pushit() as f:
                add_init()
                print(f)
print('-'*50)
print('Echo: ', pushd)


print('--ContextMgr with args--')
with pushit('../..') as f:
    print('Do stuff here')
    print('CWD: ',os.getcwd())

popd()
pushd('pushtest', chdir=False)
pushd('pushtest/pushtest1', chdir=False)
pushd('pushtest/pushtest1/pushtest2', chdir=False)
print('Echo: ', pushd)
input('Press any key to remove newly created files/dir')
with pushit() as f:
    with pushit() as b:
        with pushit() as foo:
            remove_init()
        remove_init()
    remove_init()

os.removedirs('pushtest/pushtest1/pushtest2')