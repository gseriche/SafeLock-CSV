import os
import csv
import pandas as pd

csv_done = "./approve-list-done"
csv_path = "./approve-list-csv"
csv_files = os.listdir(csv_path)


header = ['Full File Path']
for file in csv_files:
    with open(csv_path+"/"+file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        TempOnlyFilePath = list()
        for row in csv_reader:
            filePath = row[0].split('\\')
            TempOnlyFilePath.append(filePath[0]+'\\'+filePath[1])
        onlyFilePath = list(dict.fromkeys(TempOnlyFilePath))
    

    data = pd.DataFrame(onlyFilePath, columns=header)
    data.to_csv(csv_done+"/"+'done-'+file, index=False)

