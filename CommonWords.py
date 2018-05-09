class Message(object):
    def __init__(self, date, time, sender, text):
        self.date = date
        self.sender = sender
        self.text = text
        if "PM" in time:
            self.time = str(int(time[:2]) + 12) + time[2:8]
        else:
            self.time = time


class MessageList(object):
    def __init__(self, messages = [], amounts = {}):
        self.messages = messages
        self.amounts = amounts

    def scrape(self, csvfile, invalids = [",", ".", "*", "(", ")", "?", "[", "]", "'", "\""]):
        f = open(csvfile, "r", encoding="utf8")
        empties = 0
        while True:
            line = f.readline()
            if line == "":
                empties += 1
                if empties >= 20:
                    break
            else:
                empties = 0
                line = line.replace(",", "‼", 4)
                for i in invalids:   line = line.replace(i, "")
                line = line.lower()
                line = line[:-1]
                line = line.split("‼")
                if len(line) == 5:
                    self.messages.append(Message(line[0], line[1], line[2], line[4]))

    def word_amounts(self):
        for i in self.messages:
            words = i.text.split(" ")
            for i in words:
                if i in self.amounts.keys():
                    self.amounts[i] += 1
                else:
                    self.amounts[i] = 1


def reverse_dict(dic):
    ret = {}
    for i in dic.keys():
        if not dic[i] in ret.keys():
            ret[dic[i]] = [i]
        else:
            ret[dic[i]].append(i)
    return ret


def file_length(fname):
    f = open(fname, "r", encoding="utf8")
    empties = 0
    length = 0
    while True:
        line = f.readline()
        length += 1
        if line == "":
            empties += 1
            if empties >= 20:
                return length - 30
        else:
            empties = 0


main = MessageList()
main.scrape("Viki.csv")
main.word_amounts()
out = open("WordAmount.txt", "w+", encoding="utf8")
reverse_amounts = reverse_dict(main.amounts)
sorted_keys = sorted(reverse_amounts.keys(), reverse = True)
n = 0
for i in sorted_keys:
    n += 1
    out.write(str(n) + ". " + str(i) + ":" + str(reverse_amounts[i]) + "\n")
