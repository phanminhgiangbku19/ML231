# importing the module
import pytube
import time

# where to save
SAVE_PATH = "/Users/macbook/documentOfKhanh/Mask_Detect/video/"  # to_do


# def downloadYoutubeVideo():

#     try:
#         # object creation using YouTube
#         # which was imported in the beginning
#         link = "https://www.youtube.com/watch?v=KEUUKA3fuaQ"
#         yt = pytube.YouTube(link)
#         stream = yt.streams.first()
#         # to set the name of the file
#         # yt.set_filename('GeeksforGeeksVideo')
#         stream.download(SAVE_PATH)
#     except:
#         print("Connection Error")  # to handle exception

#     print('Task Completed!')

def downloadYoutubeVideo(path):
    link = path
    yt = pytube.YouTube(link)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    file_name = 'downloaded_video_' + timestr + '.mp4'
    try:
        yt.streams.filter(progressive=True,
                          file_extension="mp4").first().download(output_path=SAVE_PATH,
                                                                 filename=file_name)

        return file_name
    except Exception as err:
        print(f"Unexpected {err}, {type(err)}")
        return err
    print('Task Completed!')
