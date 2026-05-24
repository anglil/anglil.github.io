import os
import time

def wait_and_push():
    while True:
        # Check if mac_pipeline.py is running
        ret = os.system("pgrep -f mac_pipeline.py > /dev/null")
        if ret != 0: # Process not found, it finished!
            print("Pipeline finished! Committing and pushing...")
            os.system("git add -A college-electrical-engineering/images college-electrical-engineering/*.html")
            os.system("git commit -m 'Replace text with high-fidelity native macOS Vision OCR translations'")
            os.system("git push")
            break
        time.sleep(60)

if __name__ == '__main__':
    wait_and_push()
