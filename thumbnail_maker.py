# thumbnail_maker.py
import time
import os
import logging
from urllib.parse import urlparse
from urllib.request import urlretrieve
from threading import Thread
from queue import Queue

import PIL
from PIL import Image

from source import IMG_URLS


logging.basicConfig(filename='logfile.log',level=logging.DEBUG)



# Consumer/Producer pattern


class ThumbnailMakerService(object):
    def __init__(self, home_dir='.'):
        self.home_dir = home_dir
        self.input_dir = self.home_dir + os.path.sep + 'incoming'
        self.output_dir = self.home_dir + os.path.sep + 'outgoing'
        self.img_queue = Queue()
        self.dl_queue = Queue()


    def download_image(self):
        while not self.dl_queue.empty():
            try:
                url = self.dl_queue.get(block=False) #block=False, will raise exception if Q happented to be empty (Somehow).
                # download each image and save to the input dir 
                img_filename = urlparse(url).path.split('/')[-1]
                urlretrieve(url, self.input_dir + os.path.sep + img_filename)
                self.img_queue.put(img_filename)
                self.dl_queue.task_done() #mark Q as done for every url, when completed
            # Thread Gurding
            except Queue.Empty:
                """This is a safety mechanisam.
                
                There is a possibility of while get true and queue
                get empty since we have multiple threads running at the same time.
                """
                print("Queue is empty")
                logging.info("Queue is empty")

    def perform_resizing(self):

        os.makedirs(self.output_dir, exist_ok=True)

        logging.info("beginning image resizing")
        target_sizes = [32, 64, 200]
        num_images = len(os.listdir(self.input_dir))

        start = time.perf_counter()
        while True:
            filename = self.img_queue.get()
            if filename:
                orig_img = Image.open(self.input_dir + os.path.sep + filename)
                for basewidth in target_sizes:
                    img = orig_img
                    # calculate target height of the resized image to maintain the aspect ratio
                    wpercent = (basewidth / float(img.size[0]))
                    hsize = int((float(img.size[1]) * float(wpercent)))
                    # perform resizing
                    img = img.resize((basewidth, hsize), PIL.Image.LANCZOS)
                    
                    # save the resized image to the output dir with a modified file name 
                    new_filename = os.path.splitext(filename)[0] + \
                        '_' + str(basewidth) + os.path.splitext(filename)[1]
                    img.save(self.output_dir + os.path.sep + new_filename)
            else:
                self.img_queue.task_done()
                break

            os.remove(self.input_dir + os.path.sep + filename)
            self.img_queue.task_done()
        end = time.perf_counter()

        logging.info("created {} thumbnails in {} seconds".format(num_images, end - start))

    def make_thumbnails(self, img_url_list):
        logging.info("START make_thumbnails")
        start = time.perf_counter()

        for image_url in IMG_URLS:
            self.dl_queue.put(image_url)
        
        num_dl_threads = 20
        for _ in range(num_dl_threads):
            t = Thread(target=self.download_image)
            t.start()


        t2 = Thread(target=self.perform_resizing)
        t2.start()

        self.dl_queue.join()
        self.img_queue.put(None) #Poison pill

        end = time.perf_counter()
        logging.info("END make_thumbnails in {} seconds".format(end - start))
    


if __name__ == "__main__":
    tn_maker = ThumbnailMakerService()
    tn_maker.make_thumbnails(IMG_URLS)