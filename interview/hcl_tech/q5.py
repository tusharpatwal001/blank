
path = "interview/hcl_tech/csv_file.csv"
out = []
with open(path) as f:
    for  line in f:
        nums = list(map(int, line.strip().split(",")))
        out.append(sum(nums[n] for n in range(len(nums)) if n % 2 == 0))

    print(out)
