from upload.Uploader import Uploader
import csv


ticket_ids = []
with open('data_package/Ticket_Handler/old_ids.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for value in row:
            ticket_ids.append(int(value))

iter = 0
for id in ticket_ids.ticket_ids:
    Uploader().uploadTicket(id)
    iter += 1
    print("Uploaded Ticket ", iter, " / ", len(ticket_ids.ticket_ids))

print("All Tickets uploaded!")