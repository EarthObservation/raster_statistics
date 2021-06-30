import pandas as pd

cls_path = r"C:\Users\Uporabnik\Desktop\tst2.class"
out_cls_path = r"C:\Users\Uporabnik\Desktop\tst_cls2.csv"
land_path = r"C:\Users\Uporabnik\Desktop\tst2.land"
out_land_path = r"C:\Users\Uporabnik\Desktop\tst_land2.csv"

cls_df = pd.read_csv(cls_path, delimiter=",", skipinitialspace=True)
cls_df.rename(columns=lambda x: x.strip(), inplace=True)
cls_df.sort_values(by="TYPE", inplace=True)
cls_df2 = cls_df.copy()
del cls_df2["LID"]
cls_df2.to_csv(out_cls_path, sep=";", decimal=",")

print(cls_df2)


land_df = pd.read_csv(land_path, delimiter=",", skipinitialspace=True)
land_df.rename(columns=lambda x: x.strip(), inplace=True)
land_df2 = land_df.copy()
del land_df2["LID"]
land_df2.to_csv(out_land_path, sep=";", decimal=",")
