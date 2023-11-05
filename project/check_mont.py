import datetime

def check_month():
    with open('test.txt', 'r', encoding='UTF-8') as file:
        lines = file.readlines()


    current_date = datetime.datetime.now()

    new_lines = []
    for line in lines:
        data = line.strip().split()
        date_str = data[-2]  # ดึงวันที่จากข้อมูล
        date = datetime.datetime.strptime(date_str, '%d/%m/%y')
        print(date)
        print(line)
        delta = current_date - date
        print(delta.days)
        if delta.days <= 30:
            print('pass')
            new_lines.append(line)



    with open('test.txt', 'w', encoding='UTF-8') as file:
        file.writelines(new_lines)