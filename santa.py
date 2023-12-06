import smtplib, random, time
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
port = 465

# There should be a sibling file called 'credentials' with the
# the sending email address on the first line and
# the app password for it on the second line
credentials = open('./creds', 'r')
sender_email = credentials.readline()
password = credentials.readline()

# There should be a sibling file called 'participants' with the
# name, email, and interests separated by a pipe "|" character
parsed_participants = [];

with open('./participants', 'r') as participants:
    for line in participants:
        if (line.startswith("#")):
            continue
        parsed_participants.append(list(map(lambda x: x.strip(), line.strip().split("|"))))


secret_santas = parsed_participants.copy()
random.shuffle(secret_santas)
names_in_the_hat = parsed_participants.copy()
random.shuffle(names_in_the_hat)

pairings = []

while len(secret_santas) > 0:
    drawing_santa = secret_santas.pop()
    name_from_hat = names_in_the_hat.pop()

    if (drawing_santa[0] == name_from_hat[0]):
        if len(names_in_the_hat) == 0:
            secret_santas = parsed_participants.copy()
            random.shuffle(secret_santas)
            names_in_the_hat = parsed_participants.copy()
            random.shuffle(names_in_the_hat)
            pairings = []
            continue


        secret_santas.append(drawing_santa)
        names_in_the_hat.append(name_from_hat)
        random.shuffle(names_in_the_hat)
        continue

    pairings.append([drawing_santa, name_from_hat])

server = smtplib.SMTP_SSL(smtp_server,port)
server.login(sender_email, password)
assignments = open("./top_secret_assignments", "w")

for pair in pairings:
    message_body = f"""
    Hello {pair[0][0]},

    You are {pair[1][0]}'s Secret Santa this year!
    Some of their interests are: {pair[1][2]}
    """
    message = MIMEText(message_body)
    message['Subject'] = "Your Secret Santa 2023 Assignment"
    message['From'] = sender_email
    message['To'] = pair[0][1]

    
    
    try:
        server.sendmail(sender_email, pair[0][1], message.as_string())
        assignments.write(f'{pair[0][0]} drew {pair[1][0]}\n')
    except Exception as e:
        print("Secret Santa did not complete successfully, some people may have received emails")
        print(e)
        quit()
    
    time.sleep(10)
    

server.quit()
print("Secret Santa executed successfully. Results written to 'top_secret_assignments' if verification is needed")