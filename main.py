from scoreboard import app
from download_files import getFileList
from tsp_recognition import get_score
import time


if __name__ == '__main__':
    # app.run()
    counter: int = 0
    while True:
        result_dict = getFileList('GOOGLE_DRIVE_ID')
        for entry in result_dict:
            instance_name = f"user_input/{entry['filename']}"
            score = get_score(f"user_input/{entry['filename']}", entry['type'], entry['filename'])
            entry['score'] = f'{score:.2f}'
            # print(f'Score trimmed: {entry["score"]}')
            with open('user_input/entries.txt', 'a') as f:
                f.write(f"{entry['type']},{entry['name']},{entry['score']},{entry['filename']}\n")
        print(f'{counter}: {result_dict}')
        time.sleep(5)
        counter += 1
