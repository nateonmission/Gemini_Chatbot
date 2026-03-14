
from functions.write_file import write_file


print(f'write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")')
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(f"\n")


print(f'write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")')
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(f"\n")


print(f'write_file("calculator", "/tmp/temp.txt", "this should not be allowed")')
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
print(f"\n")

