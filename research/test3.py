# part-1 (Quine) self printing program
s = 's = %r\nprint(s %% s)'
print(s % s)

# part-2 (Quine) self replicating file 
# s = 's = %r\ncode = s %% s\nwith open("clone.py", "w") as f:\n f.write(code)\n\n'
# code = s % s

# with open("clone.py", "w") as f:
#     f.write(code)

# part-3 (Quine) Infectious Program
# s = 's = %r\ncode = s %% s\nwith open("clone.py", "w") as f:\n  f.write(code)\n\n'
# code = s % s
# with open("clone.py", "w") as f:
#     f.write(code)

# target = find_a_python_file_in(some_directory)

# if target is not already infected:
# insert_self_into(target, code)
