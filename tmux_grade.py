#!/usr/bin/python3
"""
wrapper script to run grade.py in tmux session.
this is not a perfect solution. Use with your own risk
"""
import sys
import libtmux

def main(hw, student, table):

    serever = libtmux.Server()
    session = serever.new_session(session_name="Grade HW", kill_session=True, attach=False)
    window = session.new_window(attach=True, window_name="Grade HW")
    main_pane = window.attached_pane
    other_pane = window.split_window(vertical=False)
    window.select_layout('even-horizontal')
    other_pane.send_keys('sudo dmesg -w')
    main_pane.send_keys('./grade.py {} {} {}'.format(hw, student, table))
    serever.attach_session(target_session="Grade HW")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
