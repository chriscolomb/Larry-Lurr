import csv

def getPatrons():
    command = []
    live = []
    tip = []
    with open('patrons.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            tier = row['Tier']
            if tier == "Commandin' Larry":
                command.append(name)
            elif tier == "Livin' Like Larry":
                live.append(name)
            elif tier == "Tippin' Larry":
                tip.append(name)
    # return command, live, tip
    return ["Bree"], live, tip

# print(getPatrons())
