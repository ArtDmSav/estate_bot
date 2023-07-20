import csv


def write_csv(date_msg, city, price, message_id, message_chat_id):
    with open("data_base.csv", "a", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        # writer.writerow(["date_msg", "city", "price", "message_id", "message_chat_id"])
        writer.writerow([date_msg, city, price, message_id, message_chat_id])
