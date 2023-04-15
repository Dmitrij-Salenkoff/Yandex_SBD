class DataCenter:
    def __init__(self, m):
        self.__servers = [1 for i in range(m)]
        self.__reboot_count = 0

    def disable_server(self, i):
        self.__servers[i - 1] = 0

    def reboot_all_servers(self):
        self.__servers = [1 for i in range(m)]
        self.__reboot_count += 1

    def get_reboot_count(self):
        return self.__reboot_count

    def get_working_servers_count(self):
        return sum(self.__servers)


##### PRODUCTION AREA
# n, m, q = list(map(int, input().split(' ')))

# rows = []
# for row in range(q):
#     row_info = input()
#     rows.append(row_info)
#####


##### TEST AREA
with open('test2.txt', 'r') as f:
    rows = f.read().splitlines()

n, m, q = list(map(int, rows[0].split()))
rows = rows[1:]
#####

dc_arr = [''] + [DataCenter(m) for i in range(n)]

for row in rows:
    if row.startswith('DISABLE'):
        _, dc_num, server_num = row.split(' ')
        dc_arr[int(dc_num)].disable_server(int(server_num))
    elif row.startswith('RESET'):
        _, dc_num = row.split(' ')
        dc_arr[int(dc_num)].reboot_all_servers()
    elif row.startswith('GETMAX'):
        R_DOT_A_values = [i.get_reboot_count() * i.get_working_servers_count() for i in dc_arr[1:]]
        max_R_DOT_A_value = max(R_DOT_A_values)
        print(R_DOT_A_values.index(max_R_DOT_A_value) + 1)
    elif row.startswith('GETMIN'):
        R_DOT_A_values = [i.get_reboot_count() * i.get_working_servers_count() for i in dc_arr[1:]]
        min_R_DOT_A_value = min(R_DOT_A_values)
        print(R_DOT_A_values.index(min_R_DOT_A_value) + 1)
