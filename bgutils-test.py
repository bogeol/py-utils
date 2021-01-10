import bgutils as bg

x = list(range(239))

print("bg.split_list_by_number(x, 10)")
print("------------------------------")
for i in bg.split_list_by_number(x, 10):
    print(i)

print("\nbg.split_list_by_chunk(x, 3)")
print("------------------------------")
for i in bg.split_list_by_chunk(x, 3):
    print(i)
