from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def button(request):
    return render(request, "home.html")


@login_required(login_url='/accounts/login/')
def output(request):
    import random
    import xlsxwriter
    import gspread
    import pandas as pd
    from oauth2client.service_account import ServiceAccountCredentials

    # Availability
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'autogen3-23b61156b4f9.json', scope)
    # authorize the clientsheet
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('Kennys Availability')
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    # create pandas file
    sheet_data = sheet_instance.get_all_records()
    sheet_pandas = pd.DataFrame.from_dict(sheet_data)

    # Request off
    # define the scope
    scope2 = ['https://spreadsheets.google.com/feeds',
              'https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds2 = ServiceAccountCredentials.from_json_keyfile_name(
        'autogen3-23b61156b4f9.json', scope2)
    # authorize the clientsheet
    client2 = gspread.authorize(creds2)
    # get the instance of the Spreadsheet
    sheet2 = client.open('Request off')
    # get the first sheet of the Spreadsheet
    sheet_instance2 = sheet2.get_worksheet(0)
    # create pandas file
    request_data = sheet_instance2.get_all_records()
    request_pandas = pd.DataFrame.from_dict(request_data)

    everyone = []
    sheet_names = sheet_pandas["Name"].to_list()
    total_servers = len(sheet_names) - 1

    # Creates required staff data
    sheet3 = client.open('Required Staff')
    instance = sheet3.get_worksheet(0)
    needed_data = instance.get_all_records()
    needed_pandas = pd.DataFrame.from_dict(needed_data)

    def generate(day, shift):
        it = 0
        if shift == 3:
            it = 0
        elif shift == 5:
            it = 2
        elif shift == 7:
            it = 1
        elif shift == 11:
            it = 4
        elif shift == 13:
            it = 3
        needed_list = needed_pandas[day].to_list()
        length = needed_list[it]
        people = []
        # Availability of each day
        sheet_collumn = sheet_pandas[day].to_list()
        # Request offs
        request_names = request_pandas["Name"].to_list()
        sheet_days = request_pandas["What day would you like to request off?"].to_list(
        )
        counter = 0
        while len(people) < length:
            random_number = random.randint(0, total_servers)
            # Availability of selected person
            random_shift = int(sheet_collumn[random_number])
            # Name of person selected
            random_person = sheet_names[random_number]

            has_not_requested_off = True
            # Determines if person requested off on that shift
            if random_person in request_names:
                for x in range(len(request_names)):
                    if random_person == request_names[x] and day == sheet_days[x]:
                        has_not_requested_off = False
            # Over rides request off if not enough shifts
            if counter > 100:
                has_not_requested_off = True
            # Stops generating if less people availible than shifts
            if counter > 200:
                break
            # Determnes if person can work that shift
            mod = int(random_shift) % int(shift)
            if int(mod) == 0:
                if random_person not in everyone:
                    if random_person not in people:
                        if has_not_requested_off:
                            people.append(random_person)
                            everyone.append(random_person)
            counter += 1
        return people

    workbook = xlsxwriter.Workbook('shift.xlsx')
    worksheet = workbook.add_worksheet()
    global row
    row = 0
    col = 0

    # Generates all of the people for one day
    # def day(shift):
    #     global row
    #     global col
    #     sundayAM_servers = generate(shift, 3)
    #     sundayAM_host = generate(shift, 5)
    #     sundayAM_bar = generate(shift, 7)
    #     sundayAM_runner = generate(shift, 11)
    #     sundayAM_expo = generate(shift, 13)
    #     day = (
    #         sundayAM_servers,
    #         sundayAM_host,
    #         sundayAM_bar,
    #         sundayAM_runner,
    #     )
    #     for item in sundayAM_servers:
    #         worksheet.write(row, col,     item)
    #         col += 1
    #     row += 1
    #     col = 0
    #     for item in sundayAM_host:
    #         worksheet.write(row, col,     item)
    #         col += 1
    #     row += 1
    #     col = 0
    #     for item in sundayAM_bar:
    #         worksheet.write(row, col,     item)
    #         col += 1
    #     row += 1
    #     col = 0
    #     for item in sundayAM_runner:
    #         worksheet.write(row, col,     item)
    #         col += 1
    #     row += 1
    #     col = 0
    #     for item in sundayAM_expo:
    #         worksheet.write(row, col,     item)
    #         col += 1
    #     row += 2
    #     col = 0
    all_shifts = [
        "SundayAM",
        "SundayPM",
        "MondayAM",
        "MondayPM",
        "TuesdayAM",
        "TuesdayPM",
        "WednesdayAM",
        "WednesdayPM",
        "ThursdayAM",
        "ThursdayPM",
        "FridayAM",
        "FridayPM",
        "SaturdayAM",
        "SaturdayPM", ]

    r = 1
    worksheet.write(0, 0,     " ")
    for x in sheet_names:
        worksheet.write(r, 0,     x)
        r += 1
    for x in all_shifts:
        worksheet.write(0, col + 1,     x)
        col += 1

    def complex(shift):
        global row
        server = generate(shift, 3)
        hostess = generate(shift, 5)
        bartender = generate(shift, 7)
        runner = generate(shift, 11)
        expo = generate(shift, 13)

        col = 1

        def quick_write(position, text):
            for x in position:
                val = sheet_names.index(x) + 1
                worksheet.write(val, all_shifts.index(shift) + 1,     text)

        quick_write(server, "Server")
        quick_write(hostess, "H/G")
        quick_write(bartender, "Bar")
        quick_write(runner, "Runner")
        quick_write(expo, "Expo")

        row += 1

    for y in range(len(all_shifts)):
        for x in range(total_servers + 1):
            worksheet.write(x + 1, y + 1,     "     ")
    complex("SundayAM")
    everyone = []
    complex("SundayPM")
    everyone = []

    complex("MondayAM")
    everyone = []
    complex("MondayPM")
    everyone = []

    complex("TuesdayAM")
    everyone = []
    complex("TuesdayPM")
    everyone = []

    complex("WednesdayAM")
    everyone = []
    complex("WednesdayPM")
    everyone = []

    complex("ThursdayAM")
    everyone = []
    complex("ThursdayPM")
    everyone = []

    complex("FridayAM")
    everyone = []
    complex("FridayPM")
    everyone = []

    complex("SaturdayAM")
    everyone = []
    complex("SaturdayPM")
    everyone = []

    workbook.close()

    # This reads in your excel doc as a pandas DataFrame
    wb = pd.read_excel("shift.xlsx")
    new_version = wb.to_html()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(wb.to_html(), "html.parser")
    soup.find('table')['id'] = 'tblStocks'
    print("Generated a new Schedule")
    # print(soup)
    # print(type(new_version))
    # print(wb)  # Export the DataFrame (Excel doc) to an html file
    return render(request, "home.html", {"data": str(soup)})


def form(request):
    return render(request, "form.html")


def log(request):
    return render(request, "registration/logged_out.html")
