

from moviepy.editor import VideoFileClip, concatenate_videoclips


video1 = VideoFileClip('videos/2024_07_21_08_30_12.mp4')
video2 = VideoFileClip('videos/2024_07_21_15_57_31.mp4')
video3 = VideoFileClip('videos/2024_07_21_08_30_12.mp4')

video4 = VideoFileClip('videos/2024_07_21_08_30_12.mp4')

video5 = VideoFileClip('videos/2024_07_21_08_30_12.mp4')


video1.resize((1920, 1920))
video2.resize((1920, 1920))
video3.resize((1920, 1920))
video4.resize((1920, 1920))
video5.resize((1920, 1920))


# video1.write_videofile('test1.mp4')
# video2.write_videofile('test2.mp4')


f = concatenate_videoclips(
    clips=[video1, video2, video3, video4, video5],
    method='compose'
)


f.write_videofile('test1.mp4')
