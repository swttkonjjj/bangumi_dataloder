from video import Video
from data import insert_data

# %%
# path = r"Z:\video\ bgm\86 -不存在的战区-\[Sakurato][20210410] 86—Eitishikkusu— [01-23 Fin v2][TVRip][1080p@60FPS][CHS]\[Sakurato] 86—Eitishikkusu— [01v2][AVC-8bit 1080p@60FPS AAC][CHS].mp4"
path = r"Z:\video\bangumi\黄金神威\[HYSUB]Golden Kamuy[01v2][GB_MP4][1280X720].mp4"
a = Video(path)
# a.get_data()
a.match()
insert_data(a)
# a.
