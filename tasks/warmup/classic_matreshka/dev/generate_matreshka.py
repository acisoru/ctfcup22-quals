#!/usr/bin/env python3
import logging, argparse, os, random, string, time

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def generate_password(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def generate_zip_file(password, zipfile, flagfile):
    try:
        os.system(f"zip -q -e --password {password} {zipfile} {flagfile}")
    except Exception as err:
        log.error(err)
        return False
    return True

def save_password_entry(password, filename):
    try:
        os.system(f"zipnote -q {filename} > tmp.txt")
    except Exception as err:
        log.error(err)
        return False
    time.sleep(0.1)
    lines = ""
    with open("tmp.txt", "r") as f:
        lines = f.readlines()
    lines.append(f"Password for this zip archive is: {password}\n")
    log.info(f"{filename} has password: {password}")
    with open("tmp.txt", "w") as f:
        for line in lines:
            f.write(line)
    try:
        os.system(f"zipnote -q -w {filename} < tmp.txt")
        os.remove("tmp.txt")
    except Exception as err:
        log.error(err)
        return False
    return True

def matreshkify(filename, times):
    zip_filename = "matreshka"
    for i in range(1, times+1):
        password = generate_password(8)
        generate_zip_file(password, f"{zip_filename}_{i}.zip", filename)
        save_password_entry(password, f"{zip_filename}_{i}.zip")
        filename = f"{zip_filename}_{i}.zip"


if __name__ == "__main__":
    log.info("Starting matreshka generator.")
    parser = argparse.ArgumentParser(
        prog = "./generate_matreshka.py", 
        description = "This is script for generating matreshka task.",
        epilog = "GazPromBank task"
    )
    parser.add_argument("filename", help="What file should we matreshkify? :)", default="flag.txt")
    parser.add_argument("-t", "--times", help="How many times should we matreshkify file?", type=int, default=1000)
    args = parser.parse_args()
    log.info(f"Parsed parameters: {args}")
    log.info("Check if file exists...")
    if os.path.exists(args.filename):
        log.info("EXIST")
    else:
        log.error("ERROR: Cannot find file. Exit!")
        quit()
    log.info("Starting processing.")
    matreshkify(args.filename, args.times)
