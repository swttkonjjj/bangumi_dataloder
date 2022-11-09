import sqlite3
# from video import Video
from utils import logging
import json
import os

def connetcdb(path: str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    return conn, cur

def initdb():
    if os.path.exists('./video.db'):
        return

    conn, cur = connetcdb('./video.db')
    creat_video_table = '''CREATE TABLE IF NOT EXISTS local_video(
        path text primary key,
        animeId integer,
        episodeId integer,
        animeTitle text,
        episodeTitle text,
        typeDescription text,
        matchRate integer
        );
    '''
    creat_tvshow_table = '''CREATE TABLE IF NOT EXISTS tvshow(
        animeid integer primary key,
        animeTitle text,
        episodes text,
        typeDescription text,
        summary text,
        metadete text,
        bangumiUrl text,
        ratingDetails text,
        imageUrl text,
        imagePath text
    );
    '''
    cur.execute(creat_tvshow_table)
    cur.execute(creat_video_table)
    conn.commit()

    conn.close()

def insert_data(video):
    conn, cur = connetcdb('./video.db')

    insert_video = f'''replace into local_video values(
        '{video.local_video['path']}',{video.local_video['animeId']},{video.local_video['episodeId']},'{video.local_video['animeTitle']}',
        '{video.local_video['episodeTitle']}','{video.local_video['typeDescription']}','{video.local_video['matchRate']}'
    );
    '''
    serch_tvshow = f"SELECT episodes  FROM tvshow WHERE animeid={video.tvshow['animeId']}"

    insert_tvshow = f'''insert into tvshow values(
        {video.tvshow['animeId']},'{video.tvshow['animeTitle']}','{video.tvshow['episodes']}','{video.tvshow['typeDescription']}','{video.tvshow['summary']}',
        '{video.tvshow['metadata']}','{video.tvshow['bangumiUrl']}','{video.tvshow['ratingDetails']}','{video.tvshow['imageUrl']}','{video.tvshow['imagePath']}'
    );
    '''
    
    cur.execute(insert_video)
    cur.execute(serch_tvshow)
    conn.commit()

    # 重复需要更新
    for i in cur:
        episodes = json.loads(i[0])
        for j in episodes:
            if j['episodeId'] == video.local_video['episodeId']:
                if 'path' in j and video.local_video['path'] not in j['path']:
                    j['path'].append(video.local_video['path'])
                else :
                    j['path'] = [video.local_video['path']]
        ep_json = json.dumps(episodes)
        insert_tvshow = f"update tvshow set episodes='{ep_json}' where animeId={video.tvshow['animeId']}"

    cur.execute(insert_tvshow)
    conn.commit()
    conn.close
    
    logging.info('insert success')

def delete_data(video_path):
    serch_video = f"SELECT animeId,episodeId  FROM local_video WHERE path='{video_path}'"
    # print(serch_video)
    conn, cur = connetcdb("./video.db")
    cur.execute(serch_video)
    conn.commit()
    for animeId, episodeId in cur:
        # print(ans)
        serch_tvshow = f"SELECT episodes  FROM tvshow WHERE animeid={animeId}"
        # print(serch_tvshow)
        cur.execute(serch_tvshow)
        conn.commit()
        # print(list(cur)[0])
        # episodes = list(cur)[0][0]
        # print(episodes)
        
        episodes = json.loads(list(cur)[0][0])
        count = 0
        for ep_index, ep in enumerate(episodes):
            # if j['episodeId'] == episodeId:
            if 'path' in ep:
                count += len(ep['path'])
                for index, path in enumerate(ep['path']):
                    if path == video_path:
                        del episodes[ep_index]['path'][index]
                        count -= 1
        episodes = json.dumps(episodes)

    if count == 0:
        del_tv = f'DELETE FROM tvshow WHERE animeid={animeId}'
        cur.execute(del_tv)
    else :
        update_tv = f"UPDATE tvshow SET episodes='{episodes}' WHERE animeid={animeId}"
        cur.execute(update_tv)       
    del_video = f"DELETE FROM local_video WHERE path='{video_path}'"
    cur.execute(del_video)
    conn.commit()
    conn.close()
    ...
if __name__ == '__main__':
    path = r'Z:\video\download\间谍过家家 第二部分\[Nekomoe kissaten][SPYxFAMILY][13][1080p][JPSC].mp4'
    # os.path.split
    delete_data(path)