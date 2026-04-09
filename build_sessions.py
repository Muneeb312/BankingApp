# this file is used for creating the 7-day session files
import os

weekly_data = {
    "day1": {
        "session1.txt": "login admin\ncreate 99999 Alice\ncreate 88888 Bob\nlogout\n",
        "session2.txt": "login standard\ndeposit 99999 500.00\nwithdrawal 99999 50.00\nlogout\n",
        "session3.txt": "login standard\ndeposit 88888 200.00\nlogout\n"
    },
    "day2": {
        "session1.txt": "login standard\ntransfer 99999 88888 100.00\nlogout\n",
        "session2.txt": "login standard\npaybill 88888 CQ 40.00\nlogout\n"
    },
    "day3": {
        "session1.txt": "login standard\nwithdrawal 99999 99999.00\ndeposit 99999 10.00\nlogout\n",
        "session2.txt": "login standard\npaybill 99999 XX 100.00\nlogout\n"
    },
    "day4": {
        "session1.txt": "login standard\ntransfer 88888 12345 25.00\nlogout\n",
        "session2.txt": "login standard\nwithdrawal 99999 20.00\nlogout\n"
    },
    "day5": {
        "session1.txt": "login admin\ndisable 12345 John\nlogout\n",
        "session2.txt": "login standard\ndeposit 88888 150.00\nlogout\n",
        "session3.txt": "login standard\npaybill 99999 EC 80.00\nlogout\n"
    },
    "day6": {
        "session1.txt": "login standard\nwithdrawal 88888 40.00\nlogout\n",
        "session2.txt": "login standard\ndeposit 99999 15.00\nlogout\n"
    },
    "day7": {
        "session1.txt": "login admin\ndelete 12345 John\nlogout\n",
        "session2.txt": "login standard\ntransfer 99999 88888 200.00\nlogout\n"
    }
}


def generate_files():
    base_dir = "sessions"

    # Create the main sessions folder
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    files_created = 0

    # Loop through the dictionary and build the folders and files
    for day, sessions in weekly_data.items():
        day_dir = os.path.join(base_dir, day)

        if not os.path.exists(day_dir):
            os.makedirs(day_dir)

        for filename, content in sessions.items():
            filepath = os.path.join(day_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)
            files_created += 1

    print(f"[+] Success! Generated {files_created} session files across 7 daily folders.")


if __name__ == "__main__":
    generate_files()