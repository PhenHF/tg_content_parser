from pathlib import Path
from typing import List


from moviepy.editor import VideoFileClip, concatenate_videoclips


class VideoSplicer:
    def __init__(self, path_to_videos: Path | str, full_video_name: str) -> None:
        self.__path_to_videos = path_to_videos
        self.__full_video_name = full_video_name

    def __get_video_file_clip_ojbects_list(self) -> List[VideoFileClip]:
        if not isinstance(self.__path_to_videos, Path):
            self.__path_to_videos = Path(self.__path_to_videos)

        return [VideoFileClip(str(video)) for video in sorted(self.__path_to_videos.iterdir())]

    def __get_resize_video_list(self):
        return [video.resize((1080, 1920)) for video in self.__get_video_file_clip_ojbects_list()]

    def get_full_video(self):
        full_video = concatenate_videoclips(
            clips=self.__get_resize_video_list(),
            method='compose'
        )

        full_video.write_videofile(self.__full_video_name)
