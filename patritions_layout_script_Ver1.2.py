#############
#Ver 1.2: sort the results file by sd...
#############


import os
import pandas as pd
import natsort as ns

def pull_partition_info():
    #create partitions sizes
    os.system('adb shell su -c "cat /proc/partitions > /data/local/tmp/partition_size.txt"')
    #create partitions names
    from subprocess import check_output
    next_folder1 = check_output('adb shell su -c "ls /dev/block/platform/ | xargs -n 1"').strip()
    changed_folder_name1 = next_folder1.decode("utf-8")
    if changed_folder_name1 == "soc":
        next_folder2 = check_output('adb shell su -c "ls /dev/block/platform/soc/ | xargs -n 1"').strip()
        changed_folder_name2 = next_folder2.decode("utf-8")
        command_part1 = "adb shell su -c "
        command_part2 = '"ls -la /dev/block/platform/soc/'
        command_part4 = "/by-name/ > /data/local/tmp/partition_name.txt"
        create_action = command_part1 + command_part2 + changed_folder_name2 + command_part4
        os.system(create_action)
    else:
        command_part1 = "adb shell su -c "
        command_part2 = '"ls -la /dev/block/platform/'
        command_part4 = "/by-name/ > /data/local/tmp/partition_name.txt"
        create_action = command_part1 + command_part2 + changed_folder_name1 + command_part4
        os.system(create_action)

    #pull partitions info files
    os.system("adb pull /data/local/tmp/partition_size.txt C:\Temp")
    os.system("adb pull /data/local/tmp/partition_name.txt C:\Temp")

def convert_text_files_to_csv():
    df1 = pd.read_csv(r'C:\Temp\partition_size.txt', delim_whitespace=True, header=None, skiprows=1)
    df1.to_csv (r'C:\Temp\partition_size.csv', index=True)

    with open('C:\Temp\partition_name.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open('C:\Temp\partition_name.txt', 'w') as fout:
        fout.writelines(data[2:])
    df2 = pd.read_csv(r'C:\Temp\partition_name.txt', sep='/', engine='python', header=None, skiprows=1)
    df2[3] = pd.Categorical(df2[3], ordered=True, categories= ns.natsorted(df2[3].unique()))
    df2 = df2.sort_values(3)
    df2.to_csv(r'C:\Temp\partition_name_for_test.csv', index=True)


    df3 = pd.read_csv(r'C:\Temp\partition_name.txt', delim_whitespace=True, engine='python', header=None, skiprows=1)
    maximum_index_df3 = df3.index[-1]
    index=0
    while index <= maximum_index_df3:
        df3.iloc[index,6] = df3.iloc[index,7] + ' ' + df3.iloc[index,8] + ' ' + df3.iloc[index,9]
        index+=1
    df3[9] = pd.Categorical(df3[9], ordered=True, categories= ns.natsorted(df3[9].unique()))
    df3 = df3.sort_values(9)
    df3.to_csv(r'C:\Temp\partition_name_for_name.csv', index=True)

def compare_function():
    df1 = pd.read_csv(r'C:\Temp\partition_size.csv')
    df2 = pd.read_csv(r'C:\Temp\partition_name_for_test.csv')
    df3 = pd.read_csv(r'C:\Temp\partition_name_for_name.csv')

    data = {'Partition':[], 'Size(KB)':[], 'FS':[], 'ro/rw':[]}

    maximum_index_df2 = df2.index[-1]
    maximum_index_df1 = df1.index[-1]

    loop_index_df2 = 0
    loop_index_df1 = 0

    while loop_index_df2 <= maximum_index_df2:
        while loop_index_df1 <= maximum_index_df1:
            if df2.iloc[loop_index_df2, 4] == df1.iloc[loop_index_df1, 4]:
                data["Partition"].append(df3.iloc[loop_index_df2, 7])
                data["Size(KB)"].append(df1.iloc[loop_index_df1, 3])
                data["FS"].append(" ")
                data["ro/rw"].append(" ")
                break
            else:
                loop_index_df1 += 1

        loop_index_df2 += 1
        loop_index_df1 = 0

    df_results = pd.DataFrame(data)
    df_results.to_csv(r'C:\Temp\Partitions_Layout.csv', index=True)

def clear_data_files():
    os.remove('C:\Temp\partition_name.txt')
    os.remove('C:\Temp\partition_size.csv')
    os.remove('C:\Temp\partition_name_for_test.csv')
    os.remove('C:\Temp\partition_name_for_name.csv')
    os.remove('C:\Temp\partition_size.txt')
    os.remove('C:\Temp\mount.txt')
    os.remove('C:\Temp\mount.csv')

def get_fs_data():
    os.system('adb shell su -c "mount > /data/local/tmp/mount.txt"')
    os.system("adb pull /data/local/tmp/mount.txt C:\Temp")
    df = pd.read_csv(r'C:\Temp\mount.txt', delim_whitespace=True, engine='python', header=None, skiprows=1)
    df.to_csv(r'C:\Temp\mount.csv', index=True)

    df1 = pd.read_csv(r'C:\Temp\mount.csv')
    df2 = pd.read_csv(r'C:\Temp\Partitions_Layout.csv')

    maximum_index_df1 = df1.index[-1]
    maximum_index_df2 = df2.index[-1]

    loop_index_df1 = 0
    loop_index_df2 = 0

    while loop_index_df1 <= maximum_index_df1:
        while loop_index_df2 <= maximum_index_df2:
            if df1.iloc[loop_index_df1, 1] in df2.iloc[loop_index_df2, 1]:
                df2.iloc[loop_index_df2, 3] = df1.iloc[loop_index_df1, 5]
                if "rw" in df1.iloc[loop_index_df1, 6]:
                    df2.iloc[loop_index_df2, 4] = "rw"
                else:
                    df2.iloc[loop_index_df2, 4] = "ro"
                break
            else:
                loop_index_df2 += 1

        loop_index_df1 += 1
        loop_index_df2 = 0
    df2.pop("Unnamed: 0")
    df2.to_csv(r'C:\Temp\Partitions_Layout.csv', index=True)


pull_partition_info()
convert_text_files_to_csv()
compare_function()
get_fs_data()
clear_data_files()

