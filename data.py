import sqlite3
from video import Video

def connetcdb(path: str):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    return conn, cur

def initdb():
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

    insert_video = f'''insert into local_video values(
        '{video.local_video['path']}',{video.local_video['animeId']},{video.local_video['episodeId']},'{video.local_video['animeTitle']}',
        '{video.local_video['episodeTitle']}','{video.local_video['typeDescription']}','{video.local_video['matchRate']}'
    );
    '''
    insert_tvshow = f'''insert into tvshow values(
        {video.tvshow['animeId']},'{video.tvshow['animeTitle']}','{video.tvshow['episodes']}','{video.tvshow['typeDescription']}','{video.tvshow['summary']}',
        '{video.tvshow['metadata']}','{video.tvshow['bangumiUrl']}','{video.tvshow['ratingDetails']}','{video.tvshow['imageUrl']}','{video.tvshow['imagePath']}'
    );
    '''
    
    cur.execute(insert_video)
    

    cur.execute(insert_tvshow)
    conn.commit()
    conn.close
    
    print('insert success')

if __name__ == '__main__':
    conn, cur = connetcdb('./video.db')
    sql = 'SELECT animeTitle  FROM tvshow WHERE animeid=13337'
    cur.execute(sql)
    conn.commit()
    print(len(list(cur)))

    for i in cur:
        print(i)
        
        

        
    else:
        print('进入else')
    conn.close()