from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def getDate(input):
    import datetime
    todayInt = datetime.datetime.today().weekday()
    sunday = 6 - todayInt
    num = 0
    if "Sunday" in input:
        num = 0
    if "Monday" in input:
        num = 1
    if "Tuesday" in input:
        num = 2
    if "Wednesday" in input:
        num = 3
    if "Thursday" in input:
        num = 4
    if "Friday" in input:
        num = 5
    if "Saturday" in input:
        num = 6
    dt = datetime.date.today() + datetime.timedelta(sunday + num)
    month = int(str(dt.strftime("%m")))
    day = int(str(dt.strftime("%d")))
    year = int(str(dt.strftime("%y")))
    comb = f"{month}/{day}/20{year}"
    return comb


def help(request):
    return render(request, "help.html")


def why(request):
    return render(request, "why.html")


@login_required(login_url='/accounts/login/')
def button(request):
    return render(request, "home.html")


def home(request):
    return render(request, "hub.html")


@login_required(login_url='/accounts/login/')
def kbjplano(request):
    return output(request, 'Kennys Availability', 'Request off', 'Required Staff', 'home.html')


@login_required(login_url='/accounts/login/')
def kbjfrisco(request):
    return render(request, "frisco.html")


@login_required(login_url='/accounts/login/')
def kbjfrisco_schedule(request):
    return output(request, 'KBJFrisco Availability', 'KBJFrisco Request off', 'Required Staff - KBJFrisco', 'frisco.html')


@login_required(login_url='/accounts/login/')
def pizza(request):
    return render(request, "pizza.html")


@login_required(login_url='/accounts/login/')
def pizza_schedule(request):
    return output(request, 'Pizza Availability', 'Pizza Request off', 'Required Staff - KBJFrisco', 'pizza.html')


@login_required(login_url='/accounts/login/')
def wood(request):
    return render(request, "wood.html")


@login_required(login_url='/accounts/login/')
def wood_schedule(request):
    return output(request, 'WFG Availability', 'WFG Request off', 'Required Staff - WFG', 'wood.html')


@login_required(login_url='/accounts/login/')
def italian(request):
    return render(request, "italian.html")


@login_required(login_url='/accounts/login/')
def italian_schedule(request):
    return output(request, 'Italian Availability', 'Italian Request off', 'Required Staff - Italian', 'italian.html')


@login_required(login_url='/accounts/login/')
def output(request, availability_name, requests_name, staff_name, page):
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
    sheet = client.open(availability_name)
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
    sheet2 = client.open(requests_name)
    # get the first sheet of the Spreadsheet
    sheet_instance2 = sheet2.get_worksheet(0)
    # create pandas file
    request_data = sheet_instance2.get_all_records()
    request_pandas = pd.DataFrame.from_dict(request_data)

    everyone = []
    sheet_names = sheet_pandas["Name"].to_list()
    request_dates = request_pandas["Select a date to request off."].to_list()
    request_shift = request_pandas["Select the shift"].to_list()
    total_servers = len(sheet_names) - 1
    capacity_list = sheet_pandas["Highest Section"].to_list()
    # Creates required staff data
    sheet3 = client.open(staff_name)
    instance = sheet3.get_worksheet(0)
    needed_data = instance.get_all_records()
    needed_pandas = pd.DataFrame.from_dict(needed_data)
    workbook = xlsxwriter.Workbook('shift.xlsx')
    worksheet = workbook.add_worksheet()
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

    def generate(day, shift):
        it = 0
        if shift == "s":
            it = 0
        elif shift == "b":
            it = 1
        elif shift == "h":
            it = 2
        elif shift == "e":
            it = 3
        elif shift == "f":
            it = 4
        needed_list = needed_pandas[day].to_list()
        length = needed_list[it]
        people = []
        # Availability of each day
        sheet_collumn = sheet_pandas[day].to_list()
        # Request offs
        request_names = request_pandas["Name"].to_list()
        counter = 0
        server_section = 1
        while len(people) < length:
            # Selects random person
            random_number = random.randint(0, total_servers)
            # Availability of selected person
            random_shift = sheet_collumn[random_number]
            # Name of person selected
            random_person = sheet_names[random_number]

            has_not_requested_off = True
            # Determines if person requested off on that shift
            if random_person in request_names:
                for x in range(len(request_names)):
                    date_in_question = getDate(day)
                    if random_person == request_names[x] and request_dates[x] in date_in_question:
                        if request_shift[x] in day or request_shift[x] == "Both":
                            has_not_requested_off = False
            # Over rides request off if not enough shifts
            if counter > 100:
                has_not_requested_off = True
            # Stops generating if less people availible than shifts
            if counter > 200:
                tab = all_shifts.index(day) + 1
                worksheet.write(0, tab,     "Not Full")
                break
            # Determnes if person can work that shift
            if shift in random_shift:
                if random_person not in everyone:
                    if random_person not in people:
                        if has_not_requested_off:
                            if shift == "s":
                                max_capacity = capacity_list[random_number]
                                if server_section >= max_capacity:
                                    people.append(random_person)
                                    everyone.append(random_person)
                                    server_section += 1
                            else:
                                people.append(random_person)
                                everyone.append(random_person)
            counter += 1
        return people

    global row
    row = 0
    col = 0

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
        bartender = generate(shift, "b")
        expo = generate(shift, "e")
        server = generate(shift, "s")
        hostess = generate(shift, "h")
        runner = generate(shift, "f")

        col = 1

        def quick_write(position, text):
            sec = 1
            for x in position:
                val = sheet_names.index(x) + 1
                msg = "error"
                if "AM" in shift:
                    if text == "Bar":
                        msg = "10:00: Bar"
                    if text == "H/G":
                        msg = "11:00: H/G"
                    if text == "Server":
                        msg = f"10:00: {sec}"
                    if text == "Expo":
                        msg = "10:00: Expo"
                    if text == "Runner":
                        msg = "12:00 Runner"
                else:
                    if text == "Runner":
                        msg = "4:00 Runner"
                    if text == "Bar":
                        msg = "4:00: Bar"
                    if text == "H/G":
                        if sec == 1:
                            msg = "4:00: H/G"
                        else:
                            msg = "5:00: H/G"
                    if text == "Server":
                        if "Fri" in shift or "Sat" in shift or "Sun" in shift:
                            msg = f"4:00: {sec}"
                        else:
                            if sec <= 2:
                                msg = f"5:00: {sec}"
                            else:
                                msg = f"4:00: {sec}"
                    if text == "Expo":
                        msg = "4:00: Expo"
                worksheet.write(val, all_shifts.index(shift) + 1,     msg)
                sec += 1

        quick_write(server, "Server")
        quick_write(hostess, "H/G")
        quick_write(bartender, "Bar")
        quick_write(runner, "Runner")
        quick_write(expo, "Expo")

        row += 1

    for y in range(len(all_shifts)):
        for x in range(total_servers + 1):
            worksheet.write(x + 1, y + 1,     "-")
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
    worksheet.write(0, 0,     "Name")
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
    return render(request, page, {"data": str(soup)})


def form(request):
    return render(request, "form.html")


def log(request):
    return render(request, "registration/logged_out.html")


@login_required(login_url='/accounts/login/')
def upload(request, file_type):
    import pandas as pd
    if request.method == 'POST' and request.FILES['document']:
        myfile = request.FILES['document']
        fs = FileSystemStorage()
        tp = type(myfile)
        print(f"The file is of type{tp}")
        try:
            fs.delete(file_type)
        except(baseError):
            print("Could not locate CSV")
        filename = fs.save(file_type, myfile)
        tp = type(filename)
        print(f"The file is of type{tp}")
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'upload.html')


def show_upload(request, file_name):
    import pandas as pd
    import csv
    a = pd.read_excel("shift.xlsx")
    try:
        a = pd.read_csv(file_name)
        a = a.drop(a.columns[[0]], axis=1)
    except BaseException:
        print("not csv")
    try:
        a = pd.read_excel(file_name)
    except BaseException:
        print("not excel")
    html_file = a.to_html()
    return render(request, 'schedule.html', {
        'data': html_file
    })


def upload_plano(request):
    return upload(request, "KBJP-Schedule.csv")


def show_plano(request):
    return show_upload(request, "KBJP-Schedule.csv")


def upload_frisco(request):
    return upload(request, "KBJF-Schedule.csv")


def show_frisco(request):
    return show_upload(request, "KBJF-Schedule.csv")


def upload_pizza(request):
    return upload(request, "Pizza-Schedule.csv")


def show_pizza(request):
    return show_upload(request, "Pizza-Schedule.csv")


def upload_italian(request):
    return upload(request, "Italian-Schedule.csv")


def show_italian(request):
    return show_upload(request, "Italian-Schedule.csv")


def upload_wood(request):
    return upload(request, "WFG-Schedule.csv")


def show_wood(request):
    return show_upload(request, "WFG-Schedule.csv")


def get_emails(availability_name):
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
    sheet = client.open(availability_name)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    # create pandas file
    sheet_data = sheet_instance.get_all_records()
    sheet_pandas = pd.DataFrame.from_dict(sheet_data)
    emails_list = sheet_pandas["Email"]
    return emails_list


def get_message(availability_name):
    import gspread
    import pandas as pd
    import random
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
    sheet = client.open(availability_name)
    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)
    # create pandas file
    sheet_data = sheet_instance.get_all_records()
    sheet_pandas = pd.DataFrame.from_dict(sheet_data)
    emails_list = sheet_pandas["Message"]
    with open('mysite/quotes.txt') as file:
        all_quotes = file.readlines()
        quote = random.choice(all_quotes)
    return f"{emails_list[0]}\n\nHere's your quote for the week:\n{quote}"


def get_next_week():
    import datetime
    num = 6 - (datetime.datetime.today().weekday())
    today = str(datetime.datetime.now() + datetime.timedelta(days=num))
    today = today[0:10]
    return f'Schedule for {today}'


def send_mail(body, emails, file, subject):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.application import MIMEApplication
    sender_email = "quickshiftschedule@gmail.com"
    receiver_email = emails

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.attach(MIMEText(body))
    msg.attach(MIMEText("\n\n\n"))
    pdf = MIMEApplication(open(file, 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename=file)
    msg.attach(pdf)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("quickshiftschedule@gmail.com", "IloveBurgers!")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(e)


def send_plano(request):
    all_emails = get_emails("Kennys Availability")
    message = get_message("Kennys Availability")
    subject = get_next_week()
    for person in all_emails:
        send_mail(message, person, "KBJP-Schedule.csv", subject)
    print("Hello")
    return render(request, "home.html")


def send_frisco(request):
    all_emails = get_emails("KBJFrisco Availability")
    message = get_message("KBJFrisco Availability")
    subject = get_next_week()
    for person in all_emails:
        send_mail(message, person, "KBJF-Schedule.csv", subject)
    print("Hello")
    return render(request, "frisco.html")


def send_pizza(request):
    subject = get_next_week()
    all_emails = get_emails("Pizza Availability")
    message = get_message("Pizza Availability")
    for person in all_emails:
        send_mail(message, person, "Pizza-Schedule.csv", subject)
    print("Hello")
    return render(request, "pizza.html")


def send_italian(request):
    all_emails = get_emails("Italian Availability")
    message = get_message("Italian Availability")
    subject = get_next_week()
    for person in all_emails:
        send_mail(message, person, "Italian-Schedule.csv", subject)
    print("Hello")
    return render(request, "italian.html")


def send_woodfire(request):
    all_emails = get_emails("WFG Availability")
    message = get_message("WFG Availability")
    subject = get_next_week()
    for person in all_emails:
        send_mail(message, person, "WFG-Schedule.csv", subject)
    print("Hello")
    return render(request, "wood.html")


def check_for_cap(request):
    # from Google import Create_Service
    import random
    import xlsxwriter
    import gspread
    import pandas as pd
    from oauth2client.service_account import ServiceAccountCredentials

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'autogen3-23b61156b4f9.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Request off")
    sheet_instance = sheet.get_worksheet(0)
    sheet_data = sheet_instance.get_all_records()
    sheet_pandas = pd.DataFrame.from_dict(sheet_data)
    date_list = sheet_pandas["Select a date to request off."].to_list()
    length = len(date_list)
    last_request = date_list[length - 1]
    print(last_request)
    count = 0
    for x in date_list:
        if x == last_request:
            count += 1
    if count > 4:
        email_list = sheet_pandas["Email Address"].to_list()
        last_person = email_list[length - 1]
        send_mail("Unfortunately, there have been too many requests for that date; your request has been denied. Sorry for the inconvenience. \n-Kenny's Management",
                  last_person, "logo.png", "YOUR REQUEST HAS BEEN DENIED")
        # sheet_instance.delete
        # Delete Request
        # CLIENT_SECRET_FILE = 'client_secret.json'
        # API_NAME = 'sheets'
        # API_VERSION = 'v4'
        # SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        # service = Create_Service(
        #     CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        # request_body = {
        #     'requests': [
        #         {
        #             'deleteDimension': {
        #                 'range': {
        #                     'sheetID': '373398604',
        #                     'dimension': 'ROWS',
        #                     'startIndex': length,
        #                     'endIndex': length + 1
        #                 }
        #             }
        #         },
        #         {
        #             'deleteDimension': {
        #                 'range': {
        #                     'sheetID': '373398604',
        #                     'dimension': 'COLUMNS',
        #                     'startIndex': 0,
        #                     'endIndex': 4
        #                 }
        #             }
        #         }
        #     ]
        # }
        # service.spreadsheets().bashUpdate(
        #     spreadsheetId='373398604',
        #     body=request_body
        # ).execute()
        print("max")
    print(count)
    return render(request, "home.html")
