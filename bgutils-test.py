import bgutils as bg

x = list(range(239))

print("------------------------------")
print("bg.split_list_by_number")

for i in bg.split_list_by_number(x, 10):
    print(i)

print("------------------------------")
print("bg.split_list_by_chunk")
for i in bg.split_list_by_chunk(x, 3):
    print(i)

print("------------------------------")
print("bg.peek_file")
bg.peek_file("./README.md", 10)

print("------------------------------")
print("bg.listdir")
for i in bg.listdir("./")["name"]:
    print(i)
for i in bg.listdir("./")["path"]:
    print(i)
for i in bg.listdir("./")["abs"]:
    print(i)

print("------------------------------")
print("bg.print_list")
bg.print_list(list(range(5)))

print("------------------------------")
print("bg.current_time")
print(bg.current_time())

print("------------------------------")
print("bg.print_var")  # TODO BUG
aaa = 10
bg.print_var(aaa)
bbb = 10
bg.print_var(bbb)
ccc = 11
bg.print_var(ccc)
