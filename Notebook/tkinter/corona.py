import tkinter as tk
import pandas as pd

url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
df = pd.read_csv(url)

root = tk.Tk()
col = list(df.columns)

for i in col:
    tk.Label(root,text=i.pack()

root.mainloop()
