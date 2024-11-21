import xlsxwriter


def create_workbook(filename):
    return xlsxwriter.Workbook(filename)


def create_worksheet(workbook):
    return workbook.add_worksheet()

def write_data(worksheet, data):
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])
            
    worksheet.write(len(data), 0, "Avg. Age")
    avg_formula = "=AVERAGE(B{}:B{})".format(1, len(data))
    worksheet.write(len(data), 1, avg_formula)


def close_workbook(workbook):
    workbook.close()
    

if __name__ == '__main__':
    data = [
        ['John Doe', 38],
        ['Stacy Cuvver', 22],
        ['Adam Martin', 28],
        ['Tom Harries', 42],
    ]
    
    workbook = create_workbook('sample_workbook.xlsx')
    worksheet = create_worksheet(workbook)
    write_data(worksheet, data)
    close_workbook(workbook)